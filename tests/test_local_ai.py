import json
import unittest
from datetime import date
from unittest.mock import Mock

from CashSave.ai_services import (
    ExpenseCommandError,
    FinancialCalculator,
    FinancialContextService,
    FinancialOrchestrator,
    OllamaClient,
    OllamaError,
    OllamaResponseError,
    OllamaSettings,
    OllamaUnavailableError,
    parse_expense_command,
    validate_ai_response,
)


VALID_RESPONSE = json.dumps(
    {
        "answer": "As despesas superam as receitas no período observado.",
        "classification": "analise",
        "facts": ["Despesas observadas: R$ 100,00."],
        "calculations": ["Saldo calculado: -R$ 20,00."],
        "estimates": ["A projeção depende da manutenção do histórico."],
    }
)


class FakeResponse:
    def __init__(self, body: bytes):
        self.body = body

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self.body


class FinancialCalculatorTests(unittest.TestCase):
    def test_calculates_totals_in_cents(self):
        result = FinancialCalculator.totals(
            [
                {"tipo": "receita", "valor_centavos": 10000},
                {"tipo": "despesa", "valor_centavos": 2500},
            ]
        )
        self.assertEqual(result, {"receita": 10000, "despesa": 2500, "saldo": 7500})

    def test_projection_requires_two_months(self):
        result = FinancialCalculator.projection(
            [{"tipo": "despesa", "valor_centavos": 100, "data": "2026-10-01"}]
        )
        self.assertEqual(result["status"], "insuficiente")

    def test_projection_is_explicitly_an_estimate(self):
        result = FinancialCalculator.projection(
            [
                {"tipo": "receita", "valor_centavos": 1000, "data": "2026-09-01"},
                {"tipo": "despesa", "valor_centavos": 400, "data": "2026-09-02"},
                {"tipo": "receita", "valor_centavos": 1200, "data": "2026-10-01"},
                {"tipo": "despesa", "valor_centavos": 600, "data": "2026-10-02"},
            ],
            months=3,
        )
        self.assertEqual(result["status"], "estimativa")
        self.assertEqual(result["saldo_horizonte_estimado_centavos"], 1800)
        self.assertIn("premissa", result)

    def test_goal_progress_is_capped_at_target(self):
        result = FinancialCalculator.goals(
            [
                {
                    "nome": "Reserva",
                    "valor_objetivo_centavos": 1000,
                    "valor_atual_centavos": 1200,
                }
            ]
        )
        self.assertEqual(result[0]["faltante_centavos"], 0)
        self.assertEqual(result[0]["percentual"], 120)

    def test_uncategorized_budget_uses_all_expenses(self):
        result = FinancialCalculator.budgets(
            [{"nome": "Geral", "limite_centavos": 1000}],
            [{"tipo": "despesa", "valor_centavos": 250}],
            [],
        )
        self.assertEqual(result[0]["gasto_centavos"], 250)


class OllamaClientTests(unittest.TestCase):
    def test_sends_chat_request_to_local_service(self):
        opener = Mock(
            return_value=FakeResponse(
                json.dumps({"message": {"content": VALID_RESPONSE}}).encode()
            )
        )
        client = OllamaClient(
            OllamaSettings(model="test-model"),
            opener=opener,
        )
        result = client.chat([{"role": "user", "content": "Como estou?"}])
        self.assertEqual(result, VALID_RESPONSE)
        request = opener.call_args.args[0]
        body = json.loads(request.data.decode())
        self.assertEqual(body["model"], "test-model")
        self.assertFalse(body["stream"])

    def test_reports_unavailable_ollama(self):
        def fail(*args, **kwargs):
            raise TimeoutError("timeout")

        client = OllamaClient(OllamaSettings(), opener=fail)
        with self.assertRaises(OllamaUnavailableError):
            client.chat([{"role": "user", "content": "Olá"}])

    def test_rejects_non_local_ollama_url(self):
        with self.assertRaises(OllamaError):
            OllamaClient(OllamaSettings(base_url="https://ollama.example.com"))


class ExpenseCommandTests(unittest.TestCase):
    def test_parses_expense_with_category(self):
        result = parse_expense_command(
            "Hoje gastei R$ 25,90 em transporte",
            [{"id": 4, "nome": "Transporte"}],
            [],
        )
        self.assertEqual(result.value_centavos, 2590)
        self.assertEqual(result.categoria_id, 4)
        self.assertEqual(result.data, date.today().isoformat())

    def test_rejects_expense_without_amount(self):
        with self.assertRaises(ExpenseCommandError):
            parse_expense_command("cadastre uma despesa em transporte", [], [])

    def test_parses_income_with_thousands_and_day(self):
        result = parse_expense_command(
            "eu recebo 10 mil de salário dia 5",
            [],
            [],
        )
        self.assertEqual(result.tipo, "receita")
        self.assertEqual(result.value_centavos, 1_000_000)
        self.assertEqual(result.description, "salário dia 5")

    def test_parses_brazilian_thousands_amount(self):
        result = parse_expense_command(
            "recebi R$ 10.000,00 de salário",
            [],
            [],
        )
        self.assertEqual(result.tipo, "receita")
        self.assertEqual(result.value_centavos, 1_000_000)

    def test_ignores_non_write_question(self):
        self.assertIsNone(parse_expense_command("Quanto gastei?", [], []))


class ValidationAndOrchestrationTests(unittest.TestCase):
    def setUp(self):
        self.context = FinancialContextService(
            transactions=[
                {
                    "tipo": "despesa",
                    "valor_centavos": 800,
                    "data": "2026-10-19",
                    "categoria_id": 1,
                }
            ],
            accounts=[],
            categories=[{"id": 1, "nome": "Transporte"}],
            bills=[],
            budgets=[],
            goals=[],
            recurring=[],
        )

    def test_refuses_financial_writes_without_calling_model(self):
        client = Mock()
        result = FinancialOrchestrator(client=client).answer(
            "cadastre como despesa 8 reais em transporte",
            [],
            self.context,
        )
        self.assertEqual(result["classification"], "somente_leitura")
        self.assertIn("somente leitura", result["answer"])
        client.chat.assert_not_called()

    def test_answers_observed_finances_without_calling_model(self):
        client = Mock()
        result = FinancialOrchestrator(client=client).answer(
            "Quanto gastei e qual categoria gastou mais?",
            [],
            self.context,
        )
        self.assertEqual(result["classification"], "analise_financeira")
        self.assertTrue(any("R$ 8,00" in item for item in result["facts"]))
        self.assertTrue(any("Transporte" in item for item in result["facts"]))
        client.chat.assert_not_called()

    def test_answers_savings_questions_without_model_hallucinations(self):
        client = Mock()
        result = FinancialOrchestrator(client=client).answer(
            "Como posso economizar dinheiro?",
            [],
            self.context,
        )
        self.assertEqual(result["classification"], "analise_financeira")
        self.assertIn("economizar", result["answer"])
        self.assertTrue(any("R$ 8,00" in item for item in result["facts"]))
        self.assertFalse(any("R$ 850.000,00" in item for item in result["facts"]))
        client.chat.assert_not_called()

    def test_generic_prompt_forbids_invented_identity(self):
        client = Mock()
        client.chat.return_value = VALID_RESPONSE
        FinancialOrchestrator(client=client).answer(
            "Explique o que é uma reserva de emergência.",
            [],
            self.context,
        )
        prompt = client.chat.call_args.args[0][0]["content"]
        self.assertIn("CashSave", prompt)
        self.assertIn("empresa", prompt)
        self.assertIn("alterar dados", prompt)

    def test_rejects_invalid_model_response(self):
        with self.assertRaises(OllamaResponseError):
            validate_ai_response('{"answer":"sem contrato"}')

    def test_orchestrator_limits_question_and_uses_context(self):
        client = Mock()
        client.chat.return_value = VALID_RESPONSE
        settings = OllamaSettings(max_question_chars=10)
        orchestrator = FinancialOrchestrator(client=client, settings=settings)
        context = FinancialContextService(
            transactions=[],
            accounts=[],
            categories=[],
            bills=[],
            budgets=[],
            goals=[],
            recurring=[],
        )
        with self.assertRaises(OllamaError):
            orchestrator.answer("pergunta muito longa", [], context)
        client.chat.assert_not_called()

    def test_context_does_not_include_authentication_token(self):
        context = FinancialContextService(
            transactions=[{"tipo": "despesa", "valor_centavos": 100}],
            accounts=[],
            categories=[],
            bills=[],
            budgets=[],
            goals=[],
            recurring=[],
        ).build("quanto gastei?")
        self.assertNotIn("auth_token", json.dumps(context))
        self.assertNotIn("password", json.dumps(context))
        self.assertNotIn("email", json.dumps(context))


if __name__ == "__main__":
    unittest.main()
