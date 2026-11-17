import unittest
from datetime import datetime, timezone
from decimal import Decimal

from CashSave.investment_comparison import compare_price_histories
from CashSave.market_data import MarketHistory, MarketHistoryPoint


def history(symbol, points):
    return MarketHistory(
        symbol=symbol,
        points=tuple(
            MarketHistoryPoint(
                datetime.fromisoformat(f"{observed}T12:00:00+00:00"),
                Decimal(price),
            )
            for observed, price in points
        ),
        source=f"{symbol}-provider",
        reference_at=datetime(2026, 3, 3, 12, 0, tzinfo=timezone.utc),
        freshness="historical",
    )


class InvestmentComparisonTests(unittest.TestCase):
    def test_normalizes_assets_to_the_same_base_and_reports_price_performance(self):
        result = compare_price_histories(
            {
                "PETR4": history(
                    "PETR4",
                    [("2026-03-01", "10"), ("2026-03-02", "12")],
                ),
                "HGLG11": history(
                    "HGLG11",
                    [("2026-03-01", "50"), ("2026-03-02", "45")],
                ),
            }
        )

        self.assertTrue(result.complete)
        self.assertEqual(result.series[0]["PETR4"], Decimal("100.00"))
        self.assertEqual(result.series[1]["PETR4"], Decimal("120.00"))
        self.assertEqual(
            result.performance_percent,
            (("HGLG11", Decimal("-10.00")), ("PETR4", Decimal("20.00"))),
        )

    def test_incomplete_series_has_missing_dates_but_no_inferred_performance(self):
        result = compare_price_histories(
            {
                "PETR4": history(
                    "PETR4",
                    [("2026-03-01", "10"), ("2026-03-02", "11")],
                ),
                "HGLG11": history(
                    "HGLG11",
                    [("2026-03-02", "50"), ("2026-03-03", "51")],
                ),
            }
        )

        self.assertFalse(result.complete)
        self.assertEqual(result.series, ())
        self.assertEqual(result.performance_percent, ())
        self.assertEqual(
            result.missing_dates,
            (("HGLG11", "2026-03-01"), ("PETR4", "2026-03-03")),
        )

    def test_requires_two_assets_and_verified_history(self):
        with self.assertRaisesRegex(ValueError, "dois ativos"):
            compare_price_histories(
                {"PETR4": history("PETR4", [("2026-03-01", "10")])}
            )
        with self.assertRaisesRegex(ValueError, "duas datas"):
            compare_price_histories(
                {
                    "PETR4": history("PETR4", [("2026-03-01", "10")]),
                    "HGLG11": history("HGLG11", [("2026-03-01", "50")]),
                }
            )


if __name__ == "__main__":
    unittest.main()
