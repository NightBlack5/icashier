import asyncio
import unittest
from unittest.mock import Mock, patch

from CashSave.expense_reports import (
    expense_report_data,
    generate_expense_pdf,
    is_expense_pdf_request,
)
from CashSave.state import AppState


class ExpenseReportTests(unittest.TestCase):
    def test_detects_expense_pdf_request(self):
        self.assertTrue(is_expense_pdf_request("consegue fazer um pdf dos meus gastos?"))
        self.assertTrue(is_expense_pdf_request("relatório PDF de despesas"))

    def test_does_not_intercept_regular_financial_questions(self):
        self.assertFalse(is_expense_pdf_request("como posso reduzir meus gastos?"))
        self.assertFalse(is_expense_pdf_request("gere um pdf do orçamento"))

    def test_report_uses_expenses_only_and_sums_cents(self):
        expenses, total = expense_report_data(
            [
                {"tipo": "despesa", "valor_centavos": 1299, "data": "2026-10-20"},
                {"tipo": "receita", "valor_centavos": 50000, "data": "2026-10-19"},
                {"tipo": "despesa", "valor_centavos": 2500, "data": "2026-10-21"},
            ],
            [],
        )

        self.assertEqual(total, 3799)
        self.assertEqual(len(expenses), 2)
        self.assertEqual(expenses[0]["data"], "2026-10-21")

    def test_generates_valid_pdf_for_empty_report(self):
        pdf = generate_expense_pdf([], [])

        self.assertTrue(pdf.startswith(b"%PDF-"))
        self.assertTrue(pdf.rstrip().endswith(b"%%EOF"))

    def test_generates_valid_pdf_for_expenses(self):
        pdf = generate_expense_pdf(
            [
                {
                    "tipo": "despesa",
                    "descricao": "Aluguel",
                    "valor_centavos": 125000,
                    "data": "2026-10-20",
                }
            ],
            [],
        )

        self.assertTrue(pdf.startswith(b"%PDF-"))

    def test_chat_request_returns_download_without_calling_model(self):
        assistant_state = Mock()
        assistant_state.auth_token = "test-session"
        assistant_state.assistente_mensagem = "consegue fazer um pdf mostrando meus gastos?"
        assistant_state.assistente_mensagens = []
        assistant_state.assistente_conversas = []
        assistant_state.assistente_conversa_id = 0
        assistant_state.transacoes = [
            {
                "tipo": "despesa",
                "descricao": "Mercado",
                "valor_centavos": 1250,
                "data": "2026-10-20",
            }
        ]
        assistant_state.categorias = []
        assistant_state._persistir_conversas_assistente = Mock()

        with patch("CashSave.state.FinancialOrchestrator.answer") as answer:
            download = asyncio.run(
                AppState.enviar_mensagem_assistente.fn(assistant_state)
            )

        answer.assert_not_called()
        self.assertIsNotNone(download)
        self.assertIn(
            "Gerei o relatório em PDF",
            assistant_state.assistente_mensagens[-1]["texto"],
        )


if __name__ == "__main__":
    unittest.main()