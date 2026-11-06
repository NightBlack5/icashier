import asyncio
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from CashSave.state import AppState, XanoAPIError


EXAMPLE_MESSAGE = (
    "Recebi R$ 2.500 de salário este mês. Gastei R$ 850 de aluguel, "
    "R$ 420 de mercado, R$ 180 de transporte, R$ 120 de internet e "
    "celular e R$ 250 com lazer. Quanto sobrou do meu salário e "
    "qual foi meu gasto total?"
)


class AssistantTransactionTests(unittest.TestCase):
    def create_state(self, message=EXAMPLE_MESSAGE, api=None):
        return SimpleNamespace(
            auth_token="test-session",
            assistente_mensagem=message,
            assistente_mensagens=[],
            assistente_conversas=[],
            assistente_conversa_id=0,
            assistente_conversas_storage="{}",
            assistente_carregando=False,
            categorias=[{"id": 3, "nome": "transporte"}],
            contas=[{"id": 8, "nome": "conta corrente"}],
            contas_a_pagar=[],
            orcamentos=[],
            metas=[],
            recorrencias=[],
            transacoes=[],
            erro="",
            usuario={"id": 10, "email": "teste@example.com"},
            auth_email="teste@example.com",
            _api=api or AsyncMock(),
            _persistir_conversas_assistente=Mock(),
        )

    def test_saves_each_item_and_reports_totals_after_confirmations(self):
        responses = [
            {"id": index, "valor_centavos": value}
            for index, value in enumerate(
                (250000, 85000, 42000, 18000, 12000, 25000),
                start=1,
            )
        ]
        assistant_state = self.create_state(
            api=AsyncMock(side_effect=responses)
        )

        asyncio.run(AppState.enviar_mensagem_assistente.fn(assistant_state))

        self.assertEqual(assistant_state._api.await_count, 6)
        payloads = [
            call.args[2] for call in assistant_state._api.await_args_list
        ]
        self.assertEqual(
            [(item["tipo"], item["descricao"], item["valor_centavos"]) for item in payloads],
            [
                ("receita", "salário", 250000),
                ("despesa", "aluguel", 85000),
                ("despesa", "mercado", 42000),
                ("despesa", "transporte", 18000),
                ("despesa", "internet e celular", 12000),
                ("despesa", "lazer", 25000),
            ],
        )
        self.assertEqual(payloads[3]["categoria_id"], 3)
        self.assertIsNone(payloads[3]["conta_id"])
        self.assertEqual(len(assistant_state.transacoes), 6)
        answer = assistant_state.assistente_mensagens[-1]["texto"]
        self.assertIn("Todos os 6 lançamentos foram confirmados", answer)
        self.assertIn("despesas informadas: R$ 1.820,00", answer)
        self.assertIn("Saldo deste conjunto de lançamentos: R$ 680,00", answer)
        self.assertFalse(assistant_state.assistente_carregando)

    def test_failed_later_item_reports_partial_success_and_keeps_only_saved_items(self):
        assistant_state = self.create_state(
            api=AsyncMock(
                side_effect=[
                    {"id": 1, "valor_centavos": 250000},
                    XanoAPIError("Falha ao salvar no Xano.", status_code=500),
                ]
            )
        )

        asyncio.run(AppState.enviar_mensagem_assistente.fn(assistant_state))

        self.assertEqual(assistant_state._api.await_count, 2)
        self.assertEqual([item["id"] for item in assistant_state.transacoes], [1])
        answer = assistant_state.assistente_mensagens[-1]["texto"]
        self.assertIn("apenas 1 de 6 lançamentos", answer)
        self.assertIn("despesa 'aluguel'", answer)
        self.assertIn("Não calculei o saldo", answer)
        self.assertFalse(assistant_state.assistente_carregando)

    def test_missing_confirmation_id_is_reported_as_partial_failure(self):
        assistant_state = self.create_state(
            api=AsyncMock(
                side_effect=[
                    {"id": 1, "valor_centavos": 250000},
                    {"valor_centavos": 85000},
                ]
            )
        )

        asyncio.run(AppState.enviar_mensagem_assistente.fn(assistant_state))

        self.assertEqual([item["id"] for item in assistant_state.transacoes], [1])
        self.assertIn(
            "O Xano não confirmou o lançamento.",
            assistant_state.assistente_mensagens[-1]["texto"],
        )

    def test_rejects_incomplete_batch_before_sending_any_transaction(self):
        assistant_state = self.create_state(
            message="Recebi R$ 2.500 de salário e gastei R$ 50"
        )

        asyncio.run(AppState.enviar_mensagem_assistente.fn(assistant_state))

        assistant_state._api.assert_not_awaited()
        self.assertEqual(assistant_state.transacoes, [])
        self.assertIn("descrição", assistant_state.erro)

    def test_requires_an_authenticated_session_before_writing(self):
        assistant_state = self.create_state()
        assistant_state.auth_token = ""

        asyncio.run(AppState.enviar_mensagem_assistente.fn(assistant_state))

        assistant_state._api.assert_not_awaited()
        self.assertIn("Entre na sua conta", assistant_state.erro)

    def test_read_only_question_does_not_send_transaction_requests(self):
        assistant_state = self.create_state(message="Quanto gastei?")
        answer = {
            "answer": "Despesas observadas: R$ 0,00.",
            "facts": [],
            "calculations": [],
            "estimates": [],
        }

        with patch(
            "CashSave.state.FinancialOrchestrator.answer",
            return_value=answer,
        ) as orchestrator:
            asyncio.run(
                AppState.enviar_mensagem_assistente.fn(assistant_state)
            )

        assistant_state._api.assert_not_awaited()
        orchestrator.assert_called_once()


if __name__ == "__main__":
    unittest.main()
