import unittest
from datetime import date
from decimal import Decimal

from CashSave.investment_analytics import (
    assert_investment_record_owner,
    calculate_portfolio_snapshot,
    monthly_investment_flows,
)
from CashSave.investment_portfolio import InvestmentOperation


def operation(
    symbol="PETR4",
    operation_type="compra",
    operation_date=date(2026, 3, 10),
    quantity="2",
    price=1000,
    costs=0,
):
    return InvestmentOperation(
        symbol,
        operation_type,
        operation_date,
        Decimal(quantity),
        price,
        costs,
    )


def provento(status="pago", payment_date="2026-03-20", amount=500):
    return {
        "ativo_codigo": "PETR4",
        "ativo_categoria": "acao",
        "tipo": "dividendo",
        "status": status,
        "valor_centavos": amount,
        "quantidade_elegivel": None,
        "data_anuncio": None,
        "data_pagamento": payment_date,
    }


class InvestmentAnalyticsTests(unittest.TestCase):
    def test_jarvis_context_rejects_a_record_for_another_owner(self):
        with self.assertRaisesRegex(ValueError, "outro usuário"):
            assert_investment_record_owner(
                [{"usuario_id": 45, "ativo_codigo": "PETR4"}],
                authenticated_user_id=44,
            )

        assert_investment_record_owner(
            [{"usuario_id": 44, "ativo_codigo": "PETR4"}],
            authenticated_user_id=44,
        )

    def test_missing_quote_marks_market_metrics_and_roi_unavailable(self):
        snapshot = calculate_portfolio_snapshot(
            [operation(costs=100)],
            {"PETR4": "acao"},
            {},
        )

        self.assertEqual(snapshot.total_cost_basis_centavos, 2100)
        self.assertEqual(snapshot.total_purchase_outlay_centavos, 2100)
        self.assertIsNone(snapshot.total_market_value_centavos)
        self.assertIsNone(snapshot.total_unrealized_result_centavos)
        self.assertIsNone(snapshot.simple_return_percent)
        self.assertEqual(snapshot.allocation_by_category, ())

    def test_return_and_allocation_use_verified_prices_and_exclude_dividends(self):
        snapshot = calculate_portfolio_snapshot(
            [operation(costs=100)],
            {"PETR4": "acao"},
            {"PETR4": 1500},
        )

        self.assertEqual(snapshot.total_market_value_centavos, 3000)
        self.assertEqual(snapshot.total_unrealized_result_centavos, 900)
        self.assertEqual(snapshot.simple_return_percent, Decimal("42.86"))
        self.assertEqual(
            snapshot.allocation_by_category,
            (("acao", 3000, Decimal("100.00")),),
        )

    def test_closed_positions_do_not_require_a_current_quote(self):
        snapshot = calculate_portfolio_snapshot(
            [
                operation(),
                operation(
                    operation_type="venda",
                    operation_date=date(2026, 3, 11),
                    quantity="2",
                    price=1200,
                ),
            ],
            {"PETR4": "acao"},
            {},
        )

        self.assertEqual(snapshot.total_market_value_centavos, 0)
        self.assertEqual(snapshot.total_unrealized_result_centavos, 0)
        self.assertEqual(snapshot.total_realized_result_centavos, 400)
        self.assertEqual(snapshot.simple_return_percent, Decimal("20.00"))

    def test_monthly_evolution_separates_contributions_withdrawals_and_paid_income(self):
        flows = monthly_investment_flows(
            [
                operation(costs=100),
                operation(
                    operation_type="venda",
                    operation_date=date(2026, 4, 2),
                    quantity="1",
                    price=1200,
                    costs=50,
                ),
            ],
            [
                provento(),
                provento(
                    status="anunciado",
                    payment_date=None,
                    amount=9000,
                ),
            ],
        )

        self.assertEqual(
            flows,
            [
                {
                    "periodo": "2026-03",
                    "contribuicoes_centavos": 2100,
                    "retiradas_centavos": 0,
                    "proventos_centavos": 500,
                },
                {
                    "periodo": "2026-04",
                    "contribuicoes_centavos": 0,
                    "retiradas_centavos": 1150,
                    "proventos_centavos": 0,
                },
            ],
        )


if __name__ == "__main__":
    unittest.main()
