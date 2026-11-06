import asyncio
import unittest
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from CashSave.ai_services import parse_payable_bill
from CashSave.state import AppState, XanoAPIError


class PayableBillParserTests(unittest.TestCase):
    def test_recognizes_colloquial_electricity_bill_and_missing_due_date(self):
        bill = parse_payable_bill(
            "tenho uma conta apagar conta de luz 200 reais",
            [],
            [],
        )

        self.assertIsNotNone(bill)
        self.assertEqual(bill.description, "Conta de luz")
        self.assertEqual(bill.value_centavos, 20000)
        self.assertIsNone(bill.data_vencimento)

    def test_recognizes_standard_bill_wording_and_explicit_due_date(self):
        bill = parse_payable_bill(
            "Tenho uma conta a pagar de luz R$ 200,50 vencimento 10/11/2026",
            [],
            [],
        )

        self.assertIsNotNone(bill)
        self.assertEqual(bill.description, "Conta de luz")
        self.assertEqual(bill.value_centavos, 20050)
        self.assertEqual(bill.data_vencimento, "2026-11-10")

    def test_resolves_only_loaded_category_and_account(self):
        bill = parse_payable_bill(
            "Tenho uma conta a pagar de luz 200 reais vence dia 10",
            [{"id": 4, "nome": "Conta de luz", "tipo": "despesa"}],
            [{"id": 7, "nome": "Casa"}],
        )

        self.assertEqual(bill.categoria_id, 4)
        self.assertIsNone(bill.conta_id)

    def test_does_not_classify_payment_or_deletion_as_bill_creation(self):
        for request in (
            "Apague a conta de luz",
            "Pague a conta de luz",
            "Quitei a conta de luz",
        ):
            with self.subTest(request=request):
                self.assertIsNone(parse_payable_bill(request, [], []))

    def test_rejects_invalid_explicit_due_date(self):
        with self.assertRaisesRegex(Exception, "data de vencimento"):
            parse_payable_bill(
                "Tenho uma conta a pagar de luz 200 reais vence 31/02/2026",
                [],
                [],
            )

    def test_rejects_non_positive_bill_amount(self):
        with self.assertRaisesRegex(Exception, "maior que zero"):
            parse_payable_bill(
                "Tenho uma conta a pagar de luz R$ 0 vence dia 10",
                [],
                [],
            )


class PayableBillAssistantTests(unittest.TestCase):
    def create_state(self, message, api=None):
        return SimpleNamespace(
            auth_token="test-session",
            assistente_mensagem=message,
            assistente_mensagens=[],
            assistente_conversas=[],
            assistente_conversa_id=0,
            assistente_conversas_storage="{}",
            assistente_carregando=False,
            categorias=[],
            contas=[],
            contas_a_pagar=[],
            transacoes=[],
            orcamentos=[],
            metas=[],
            recorrencias=[],
            erro="",
            usuario={"id": 10, "email": "teste@example.com"},
            auth_email="teste@example.com",
            _api=api or AsyncMock(),
            _persistir_conversas_assistente=Mock(),
        )

    def test_asks_due_date_without_calling_xano_then_uses_followup(self):
        today = date.today()
        year, month = today.year, today.month
        if today.day > 10:
            month += 1
            if month > 12:
                month = 1
                year += 1
        due_date = date(year, month, 10)
        assistant_state = self.create_state(
            "tenho uma conta apagar conta de luz 200 reais",
            api=AsyncMock(
                return_value={
                    "id": 31,
                    "descricao": "Conta de luz",
                    "valor_centavos": 20000,
                    "data_vencimento": due_date.isoformat(),
                    "status": "pendente",
                }
            ),
        )

        asyncio.run(AppState.enviar_mensagem_assistente.fn(assistant_state))

        assistant_state._api.assert_not_awaited()
        self.assertIn(
            "Qual é a data de vencimento",
            assistant_state.assistente_mensagens[-1]["texto"],
        )
        self.assertEqual(assistant_state.contas_a_pagar, [])

        assistant_state.assistente_mensagem = "vence dia 10"
        asyncio.run(AppState.enviar_mensagem_assistente.fn(assistant_state))

        assistant_state._api.assert_awaited_once_with(
            "POST",
            "contas_a_pagar",
            {
                "descricao": "Conta de luz",
                "valor_centavos": 20000,
                "data_vencimento": due_date.isoformat(),
                "categoria_id": None,
                "conta_id": None,
            },
        )
        self.assertEqual(assistant_state.contas_a_pagar[0]["id"], 31)
        self.assertIn(
            "Conta a pagar cadastrada",
            assistant_state.assistente_mensagens[-1]["texto"],
        )

    def test_asks_for_missing_amount_or_description_without_writing(self):
        assistant_state = self.create_state("Tenho uma conta a pagar de luz")

        asyncio.run(AppState.enviar_mensagem_assistente.fn(assistant_state))

        assistant_state._api.assert_not_awaited()
        self.assertIn(
            "Qual é o valor",
            assistant_state.assistente_mensagens[-1]["texto"],
        )
        assistant_state._api.return_value = {
            "id": 32,
            "descricao": "Conta de luz",
            "valor_centavos": 20000,
            "data_vencimento": "2026-11-10",
        }
        assistant_state.assistente_mensagem = "200 reais, vence 10/11/2026"

        asyncio.run(AppState.enviar_mensagem_assistente.fn(assistant_state))

        assistant_state._api.assert_awaited_once_with(
            "POST",
            "contas_a_pagar",
            {
                "descricao": "Conta de luz",
                "valor_centavos": 20000,
                "data_vencimento": "2026-11-10",
                "categoria_id": None,
                "conta_id": None,
            },
        )

        assistant_state = self.create_state("Tenho uma conta a pagar 200 reais")

        asyncio.run(AppState.enviar_mensagem_assistente.fn(assistant_state))

        assistant_state._api.assert_not_awaited()
        self.assertIn(
            "Qual é a descrição",
            assistant_state.assistente_mensagens[-1]["texto"],
        )
        assistant_state._api.return_value = {
            "id": 33,
            "descricao": "Conta de luz",
            "valor_centavos": 20000,
            "data_vencimento": "2026-11-10",
        }
        assistant_state.assistente_mensagem = "Conta de luz, vence 10/11/2026"

        asyncio.run(AppState.enviar_mensagem_assistente.fn(assistant_state))

        assistant_state._api.assert_awaited_once()
        self.assertEqual(
            assistant_state._api.await_args.args[2]["descricao"],
            "Conta de luz",
        )

    def test_date_reply_without_bill_clarification_does_not_create_bill(self):
        assistant_state = self.create_state("10/11/2026")

        asyncio.run(AppState.enviar_mensagem_assistente.fn(assistant_state))

        assistant_state._api.assert_not_awaited()

    def test_does_not_create_or_change_bill_for_delete_or_payment_request(self):
        assistant_state = self.create_state("Apague a conta de luz")
        assistant_state.contas_a_pagar = [
            {"id": 5, "descricao": "Conta de luz", "status": "pendente"}
        ]
        refusal = {
            "answer": "Não posso excluir registros.",
            "facts": [],
            "calculations": [],
            "estimates": [],
        }

        with patch(
            "CashSave.state.FinancialOrchestrator.answer",
            return_value=refusal,
        ):
            asyncio.run(AppState.enviar_mensagem_assistente.fn(assistant_state))

        assistant_state._api.assert_not_awaited()
        self.assertEqual(
            assistant_state.contas_a_pagar,
            [{"id": 5, "descricao": "Conta de luz", "status": "pendente"}],
        )

    def test_reports_xano_error_without_adding_unconfirmed_bill(self):
        assistant_state = self.create_state(
            "Tenho uma conta a pagar de luz 200 reais vence 10/11/2026",
            api=AsyncMock(
                side_effect=XanoAPIError(
                    "Falha ao salvar no Xano.",
                    status_code=500,
                )
            ),
        )

        asyncio.run(AppState.enviar_mensagem_assistente.fn(assistant_state))

        self.assertEqual(assistant_state.contas_a_pagar, [])
        self.assertIn(
            "Não consegui confirmar o cadastro",
            assistant_state.assistente_mensagens[-1]["texto"],
        )

    def test_missing_xano_bill_id_is_not_confirmed_or_added(self):
        assistant_state = self.create_state(
            "Tenho uma conta a pagar de luz 200 reais vence 10/11/2026",
            api=AsyncMock(return_value={"descricao": "Conta de luz"}),
        )

        asyncio.run(AppState.enviar_mensagem_assistente.fn(assistant_state))

        self.assertEqual(assistant_state.contas_a_pagar, [])
        self.assertIn(
            "O Xano não confirmou a conta a pagar.",
            assistant_state.assistente_mensagens[-1]["texto"],
        )

    def test_requires_authentication_before_creating_bill(self):
        assistant_state = self.create_state(
            "Tenho uma conta a pagar de luz 200 reais vence 10/11/2026"
        )
        assistant_state.auth_token = ""

        asyncio.run(AppState.enviar_mensagem_assistente.fn(assistant_state))

        assistant_state._api.assert_not_awaited()
        self.assertIn("Entre na sua conta", assistant_state.erro)


if __name__ == "__main__":
    unittest.main()
