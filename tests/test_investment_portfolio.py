import unittest
from datetime import date
from decimal import Decimal

from CashSave.investment_portfolio import (
    InsufficientInvestmentQuantityError,
    InvestmentOperation,
    calculate_position,
    validate_operation_mutation,
)


class InvestmentPortfolioCalculationTests(unittest.TestCase):
    def test_weighted_average_includes_purchase_fees(self):
        position = calculate_position(
            "petr4",
            [
                InvestmentOperation(
                    "PETR4",
                    "compra",
                    date(2026, 1, 2),
                    Decimal("10"),
                    1000,
                    100,
                ),
                InvestmentOperation(
                    "PETR4",
                    "compra",
                    date(2026, 1, 3),
                    Decimal("5"),
                    1200,
                    500,
                ),
            ],
        )

        self.assertEqual(position.quantity, Decimal("15"))
        self.assertEqual(position.cost_basis_centavos, 16600)
        self.assertEqual(
            position.average_unit_cost_centavos,
            Decimal(16600) / Decimal(15),
        )

    def test_partial_sale_accounts_for_average_cost_and_sale_fees(self):
        position = calculate_position(
            "PETR4",
            [
                InvestmentOperation(
                    "PETR4",
                    "compra",
                    date(2026, 1, 2),
                    Decimal("10"),
                    1000,
                    100,
                ),
                InvestmentOperation(
                    "PETR4",
                    "venda",
                    date(2026, 1, 3),
                    Decimal("4"),
                    1200,
                    100,
                ),
            ],
        )

        self.assertEqual(position.quantity, Decimal("6"))
        self.assertEqual(position.cost_basis_centavos, 6060)
        self.assertEqual(position.realized_result_centavos, 660)
        self.assertEqual(
            position.average_unit_cost_centavos,
            Decimal("1010"),
        )

    def test_market_results_are_unavailable_without_a_verified_quote(self):
        position = calculate_position(
            "PETR4",
            [
                InvestmentOperation(
                    "PETR4",
                    "compra",
                    date(2026, 1, 2),
                    Decimal("2"),
                    1000,
                )
            ],
        )

        self.assertEqual(position.cost_basis_centavos, 2000)
        self.assertIsNone(position.market_value_centavos)
        self.assertIsNone(position.unrealized_result_centavos)

    def test_market_value_and_unrealized_result_use_quote_centavos(self):
        position = calculate_position(
            "PETR4",
            [
                InvestmentOperation(
                    "PETR4",
                    "compra",
                    date(2026, 1, 2),
                    Decimal("2"),
                    1000,
                )
            ],
            market_price_centavos=1250,
        )

        self.assertEqual(position.market_value_centavos, 2500)
        self.assertEqual(position.unrealized_result_centavos, 500)

    def test_sale_above_available_quantity_is_rejected(self):
        with self.assertRaises(InsufficientInvestmentQuantityError):
            calculate_position(
                "PETR4",
                [
                    InvestmentOperation(
                        "PETR4",
                        "venda",
                        date(2026, 1, 2),
                        Decimal("1"),
                        1000,
                    )
                ],
            )

    def test_history_is_replayed_chronologically_and_rejects_invalid_sale(self):
        operations = [
            InvestmentOperation(
                "PETR4",
                "venda",
                date(2026, 1, 3),
                Decimal("2"),
                1200,
                operation_id=2,
            ),
            InvestmentOperation(
                "PETR4",
                "compra",
                date(2026, 1, 2),
                Decimal("2"),
                1000,
                operation_id=1,
            ),
        ]

        position = calculate_position("PETR4", operations)

        self.assertEqual(position.quantity, Decimal("0"))
        self.assertEqual(position.cost_basis_centavos, 0)
        self.assertEqual(position.realized_result_centavos, 400)

    def test_fractional_centavo_rounding_is_half_up(self):
        position = calculate_position(
            "PETR4",
            [
                InvestmentOperation(
                    "PETR4",
                    "compra",
                    date(2026, 1, 2),
                    Decimal("0.0005"),
                    1000,
                )
            ],
        )

        self.assertEqual(position.cost_basis_centavos, 1)

    def test_invalid_operation_values_are_rejected(self):
        with self.assertRaises(ValueError):
            InvestmentOperation(
                "PETR4",
                "compra",
                date(2026, 1, 2),
                Decimal("NaN"),
                1000,
            )
        with self.assertRaises(ValueError):
            InvestmentOperation(
                "PETR4",
                "compra",
                date(2026, 1, 2),
                Decimal("1"),
                0,
            )

    def test_edit_that_invalidates_a_later_sale_is_rejected(self):
        operations = [
            InvestmentOperation(
                "PETR4",
                "compra",
                date(2026, 1, 2),
                Decimal("5"),
                1000,
                operation_id=1,
            ),
            InvestmentOperation(
                "PETR4",
                "venda",
                date(2026, 1, 3),
                Decimal("4"),
                1200,
                operation_id=2,
            ),
        ]
        edited_purchase = InvestmentOperation(
            "PETR4",
            "compra",
            date(2026, 1, 2),
            Decimal("3"),
            1000,
            operation_id=1,
        )

        with self.assertRaises(InsufficientInvestmentQuantityError):
            validate_operation_mutation(
                operations,
                candidate=edited_purchase,
                excluded_operation_id=1,
            )

    def test_deletion_that_invalidates_a_later_sale_is_rejected(self):
        operations = [
            InvestmentOperation(
                "PETR4",
                "compra",
                date(2026, 1, 2),
                Decimal("5"),
                1000,
                operation_id=1,
            ),
            InvestmentOperation(
                "PETR4",
                "venda",
                date(2026, 1, 3),
                Decimal("4"),
                1200,
                operation_id=2,
            ),
        ]

        with self.assertRaises(InsufficientInvestmentQuantityError):
            validate_operation_mutation(
                operations,
                excluded_operation_id=1,
            )


if __name__ == "__main__":
    unittest.main()
