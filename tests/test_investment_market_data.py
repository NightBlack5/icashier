import unittest
from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import patch

from CashSave.market_data import (
    MarketAsset,
    MarketDataNotConfigured,
    MarketDataProviderError,
    MarketDataRateLimitError,
    MarketDataService,
    MarketHistory,
    MarketHistoryPoint,
    MarketMover,
    MarketMovers,
    MarketQuote,
    create_market_data_service_from_environment,
)


class FakeProvider:
    name = "test-provider"

    def __init__(self):
        self.quote_result = MarketQuote(
            symbol="PETR4",
            category="acao",
            price=Decimal("37.12"),
            currency="BRL",
            source="test-provider",
            reference_at=datetime(2026, 11, 16, 12, 0, tzinfo=timezone.utc),
            freshness="delayed",
            daily_change_percent=Decimal("1.25"),
        )
        self.quote_error = None
        self.search_result = (
            MarketAsset(
                symbol="PETR4",
                name="Petrobras",
                category="acao",
                source="test-provider",
            ),
        )
        self.history_result = MarketHistory(
            symbol="PETR4",
            points=(
                MarketHistoryPoint(
                    datetime(2026, 11, 15, 12, 0, tzinfo=timezone.utc),
                    Decimal("36.90"),
                ),
                MarketHistoryPoint(
                    datetime(2026, 11, 16, 12, 0, tzinfo=timezone.utc),
                    Decimal("37.12"),
                ),
            ),
            source="test-provider",
            reference_at=datetime(2026, 11, 16, 12, 0, tzinfo=timezone.utc),
            freshness="historical",
        )
        self.movers_result = MarketMovers(
            gainers=(
                MarketMover(
                    symbol="PETR4",
                    name="Petrobras",
                    price=Decimal("37.12"),
                    daily_change_percent=Decimal("1.25"),
                    volume=1000,
                    source="test-provider",
                    reference_at=datetime(
                        2026,
                        11,
                        16,
                        12,
                        0,
                        tzinfo=timezone.utc,
                    ),
                ),
            ),
            losers=(),
            source="test-provider",
            reference_at=datetime(2026, 11, 16, 12, 0, tzinfo=timezone.utc),
        )

    def search(self, query, category):
        _ = (query, category)
        if self.quote_error:
            raise self.quote_error
        return self.search_result

    def quote(self, symbol):
        _ = symbol
        if self.quote_error:
            raise self.quote_error
        return self.quote_result

    def history(self, symbol, period):
        _ = (symbol, period)
        if self.quote_error:
            raise self.quote_error
        return self.history_result

    def market_movers(self, limit):
        _ = limit
        if self.quote_error:
            raise self.quote_error
        return self.movers_result


class MarketDataServiceTests(unittest.TestCase):
    def test_service_reports_whether_a_provider_is_configured(self):
        self.assertFalse(MarketDataService().configured)
        self.assertTrue(MarketDataService(FakeProvider()).configured)

    def test_unconfigured_provider_fails_explicitly(self):
        with self.assertRaises(MarketDataNotConfigured):
            MarketDataService().quote("PETR4")

    def test_environment_factory_only_configures_with_a_server_token(self):
        with patch.dict("os.environ", {"CASHSAVE_BRAPI_TOKEN": ""}):
            self.assertFalse(
                create_market_data_service_from_environment().configured
            )
        with patch.dict(
            "os.environ",
            {"CASHSAVE_BRAPI_TOKEN": "server-test-token"},
        ):
            self.assertTrue(
                create_market_data_service_from_environment().configured
            )

    def test_quote_retains_source_timestamp_and_freshness(self):
        provider = FakeProvider()
        quote = MarketDataService(provider).quote(" petr4 ")

        self.assertEqual(quote.symbol, "PETR4")
        self.assertEqual(quote.source, "test-provider")
        self.assertEqual(quote.freshness, "delayed")
        self.assertEqual(
            quote.reference_at,
            datetime(2026, 11, 16, 12, 0, tzinfo=timezone.utc),
        )

    def test_quote_rejects_a_provider_result_for_another_symbol(self):
        provider = FakeProvider()
        provider.quote_result = MarketQuote(
            symbol="VALE3",
            category="acao",
            price=Decimal("65.00"),
            currency="BRL",
            source="test-provider",
            reference_at=datetime(2026, 11, 16, 12, 0, tzinfo=timezone.utc),
            freshness="delayed",
        )

        with self.assertRaises(MarketDataProviderError):
            MarketDataService(provider).quote("PETR4")

    def test_search_and_history_use_normalized_inputs(self):
        provider = FakeProvider()
        service = MarketDataService(provider)

        assets = service.search(" petr ", category="acao")
        history = service.history("petr4", "1M")

        self.assertEqual(assets[0].symbol, "PETR4")
        self.assertEqual(history.symbol, "PETR4")
        self.assertEqual(len(history.points), 2)

    def test_search_enforces_the_requested_category(self):
        provider = FakeProvider()
        provider.search_result = (
            MarketAsset(
                symbol="PETR4",
                name="Petrobras",
                category="acao",
                source="test-provider",
            ),
            MarketAsset(
                symbol="HGLG11",
                name="FII",
                category="fii",
                source="test-provider",
            ),
        )

        assets = MarketDataService(provider).search("ativos", category="fii")

        self.assertEqual([asset.symbol for asset in assets], ["HGLG11"])

    def test_search_sorts_by_symbol_or_name(self):
        provider = FakeProvider()
        provider.search_result = (
            MarketAsset("ZZZ3", "Beta", "acao", "test-provider"),
            MarketAsset("AAA3", "Alpha", "acao", "test-provider"),
        )
        service = MarketDataService(provider)

        by_symbol = service.search("ativos")
        by_name = service.search("ativos", sort_by="name")

        self.assertEqual([asset.symbol for asset in by_symbol], ["AAA3", "ZZZ3"])
        self.assertEqual([asset.name for asset in by_name], ["Alpha", "Beta"])

    def test_search_returns_empty_results_without_fabricating_assets(self):
        provider = FakeProvider()
        provider.search_result = ()

        self.assertEqual(MarketDataService(provider).search("inexistente"), ())

    def test_search_surfaces_provider_failures(self):
        provider = FakeProvider()
        provider.quote_error = MarketDataRateLimitError("Limite atingido.")

        with self.assertRaises(MarketDataRateLimitError):
            MarketDataService(provider).search("PETR")

    def test_search_rejects_empty_query_and_unsupported_sort(self):
        service = MarketDataService(FakeProvider())

        with self.assertRaises(ValueError):
            service.search(" ")
        with self.assertRaises(ValueError):
            service.search("PETR", sort_by="unknown")

    def test_search_rejects_malformed_provider_results(self):
        provider = FakeProvider()
        provider.search_result = ("PETR4",)

        with self.assertRaises(MarketDataProviderError):
            MarketDataService(provider).search("PETR")

    def test_history_returns_only_timestamped_source_observations(self):
        provider = FakeProvider()
        history = MarketDataService(provider).history("petr4", "1M")

        self.assertEqual(history.source, "test-provider")
        self.assertEqual(len(history.points), 2)
        self.assertEqual(
            [point.observed_at for point in history.points],
            sorted(point.observed_at for point in history.points),
        )

    def test_history_allows_empty_periods_without_inventing_points(self):
        provider = FakeProvider()
        provider.history_result = MarketHistory(
            symbol="PETR4",
            points=(),
            source="test-provider",
            reference_at=datetime(2026, 11, 16, 12, 0, tzinfo=timezone.utc),
            freshness="historical",
        )

        self.assertEqual(
            MarketDataService(provider).history("PETR4", "1m").points,
            (),
        )

    def test_history_rejects_other_symbols_and_unsupported_periods(self):
        provider = FakeProvider()
        provider.history_result = MarketHistory(
            symbol="VALE3",
            points=(),
            source="test-provider",
            reference_at=datetime(2026, 11, 16, 12, 0, tzinfo=timezone.utc),
            freshness="historical",
        )
        service = MarketDataService(provider)

        with self.assertRaises(MarketDataProviderError):
            service.history("PETR4", "1m")
        with self.assertRaises(ValueError):
            service.history("PETR4", "10y")

    def test_market_movers_are_ranked_and_limit_is_validated(self):
        service = MarketDataService(FakeProvider())

        movers = service.market_movers()

        self.assertEqual([mover.symbol for mover in movers.gainers], ["PETR4"])
        self.assertEqual(movers.source, "test-provider")
        with self.assertRaises(ValueError):
            service.market_movers(0)
        with self.assertRaises(ValueError):
            service.market_movers(11)

    def test_rate_limit_returns_expired_quote_marked_stale(self):
        provider = FakeProvider()
        service = MarketDataService(provider, cache_ttl_seconds=10)
        clock = [0.0]

        with patch("CashSave.market_data.monotonic", side_effect=lambda: clock[0]):
            initial_quote = service.quote("PETR4")
            clock[0] = 11.0
            provider.quote_error = MarketDataRateLimitError("Limite atingido.")
            cached_quote = service.quote("PETR4")

        self.assertFalse(initial_quote.stale)
        self.assertTrue(cached_quote.stale)
        self.assertEqual(cached_quote.price, Decimal("37.12"))

    def test_expired_search_results_are_marked_stale(self):
        provider = FakeProvider()
        service = MarketDataService(provider, cache_ttl_seconds=10)
        clock = [0.0]

        with patch("CashSave.market_data.monotonic", side_effect=lambda: clock[0]):
            service.search("PETR")
            clock[0] = 11.0
            provider.quote_error = MarketDataRateLimitError("Limite atingido.")
            assets = service.search("PETR")

        self.assertTrue(assets[0].stale)

    def test_rate_limit_without_cached_value_is_not_hidden(self):
        provider = FakeProvider()
        provider.quote_error = MarketDataRateLimitError("Limite atingido.")

        with self.assertRaises(MarketDataRateLimitError):
            MarketDataService(provider).quote("PETR4")

    def test_invalid_market_values_are_rejected(self):
        with self.assertRaises(ValueError):
            MarketQuote(
                symbol="PETR4",
                category="acao",
                price=Decimal("0"),
                currency="BRL",
                source="provider",
                reference_at=datetime(2026, 11, 16, 12, 0, tzinfo=timezone.utc),
                freshness="unknown",
            )

    def test_history_requires_ordered_timestamped_values(self):
        with self.assertRaises(ValueError):
            MarketHistory(
                symbol="PETR4",
                points=(
                    MarketHistoryPoint(
                        datetime(2026, 11, 16, 12, 0, tzinfo=timezone.utc),
                        Decimal("37.12"),
                    ),
                    MarketHistoryPoint(
                        datetime(2026, 11, 15, 12, 0, tzinfo=timezone.utc),
                        Decimal("36.90"),
                    ),
                ),
                source="provider",
                reference_at=datetime(2026, 11, 16, 12, 0, tzinfo=timezone.utc),
                freshness="historical",
            )


if __name__ == "__main__":
    unittest.main()
