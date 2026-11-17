import io
import json
import unittest
from datetime import datetime, timezone
from decimal import Decimal
from urllib.error import HTTPError
from unittest.mock import patch

from CashSave.brapi_market_data import BrapiMarketDataProvider
from CashSave.market_data import (
    MarketDataProviderError,
    MarketDataRateLimitError,
)


class BrapiMarketDataProviderTests(unittest.TestCase):
    def setUp(self):
        self.provider = BrapiMarketDataProvider("server-test-token")

    def test_search_maps_only_active_supported_assets(self):
        payload = {
            "results": [
                {
                    "symbol": "PETR4",
                    "name": "Petrobras",
                    "subType": "stock",
                    "isActive": True,
                },
                {
                    "symbol": "HGLG11",
                    "name": "FII",
                    "subType": "fii",
                    "isActive": True,
                },
                {
                    "symbol": "VALE3",
                    "name": "Vale",
                    "subType": "stock",
                    "isActive": False,
                },
            ]
        }
        with patch.object(self.provider, "_request", return_value=payload):
            assets = self.provider.search("petr", category="acao")

        self.assertEqual(len(assets), 1)
        self.assertEqual(assets[0].symbol, "PETR4")
        self.assertEqual(assets[0].category, "acao")
        self.assertEqual(assets[0].source, "brapi.dev")

    def test_quote_normalizes_category_price_and_observation_time(self):
        quote_payload = {
            "results": [
                {
                    "symbol": "PETR4",
                    "data": {
                        "regularMarketPrice": 37.12,
                        "regularMarketChangePercent": 1.25,
                        "currency": "BRL",
                        "regularMarketTime": "2026-11-16T12:00:00.000Z",
                    },
                }
            ]
        }
        category_payload = {
            "results": [
                {
                    "symbol": "PETR4",
                    "subType": "stock",
                }
            ]
        }
        with patch.object(
            self.provider,
            "_request",
            side_effect=[category_payload, quote_payload],
        ):
            quote = self.provider.quote("PETR4")

        self.assertEqual(quote.price, Decimal("37.12"))
        self.assertEqual(quote.daily_change_percent, Decimal("1.25"))
        self.assertEqual(quote.category, "acao")
        self.assertEqual(quote.freshness, "delayed")
        self.assertEqual(
            quote.reference_at,
            datetime(2026, 11, 16, 12, 0, tzinfo=timezone.utc),
        )

    def test_history_converts_epoch_prices_and_orders_points(self):
        payload = {
            "requestedAt": "2026-11-16T12:05:00.000Z",
            "results": [
                {
                    "symbol": "PETR4",
                    "data": {
                        "historicalDataPrice": [
                            {"date": 1794830400, "close": 37.12},
                            {"date": 1794744000, "close": 36.9},
                        ]
                    },
                }
            ],
        }
        with patch.object(self.provider, "_request", return_value=payload):
            history = self.provider.history("PETR4", "1m")

        self.assertEqual([point.price for point in history.points], [
            Decimal("36.9"),
            Decimal("37.12"),
        ])
        self.assertEqual(history.freshness, "historical")
        self.assertEqual(
            history.points[0].observed_at,
            datetime.fromtimestamp(1794744000, tz=timezone.utc),
        )

    def test_market_movers_filter_inactive_empty_and_fractional_stocks(self):
        requested_at = "2026-11-16T12:05:00.000Z"
        ticker_results = {
            "desc": {
                "requestedAt": requested_at,
                "results": [
                    {
                        "symbol": "PETR4",
                        "name": "Petrobras",
                        "isActive": True,
                        "quote": {"volume": 1000},
                    },
                    {
                        "symbol": "GARB3",
                        "name": "Sem volume",
                        "isActive": True,
                        "quote": {"volume": 500},
                    },
                    {
                        "symbol": "PETR4F",
                        "name": "Fracionário",
                        "isActive": True,
                        "quote": {"volume": 100},
                    },
                ],
            },
            "asc": {
                "requestedAt": requested_at,
                "results": [
                    {
                        "symbol": "BBAS3",
                        "name": "Banco do Brasil",
                        "isActive": True,
                        "quote": {"volume": 800},
                    },
                    {
                        "symbol": "VALE3",
                        "name": "Vale",
                        "isActive": False,
                        "quote": {"volume": 900},
                    },
                ],
            },
        }
        quote_payload = {
            "results": [
                {
                    "symbol": "PETR4",
                    "data": {
                        "regularMarketPrice": 37.12,
                        "regularMarketChangePercent": 3.5,
                        "regularMarketVolume": 1000,
                        "regularMarketTime": requested_at,
                    },
                },
                {
                    "symbol": "GARB3",
                    "data": {
                        "regularMarketPrice": 10,
                        "regularMarketChangePercent": 2,
                        "regularMarketVolume": 0,
                        "regularMarketTime": requested_at,
                    },
                },
                {
                    "symbol": "BBAS3",
                    "data": {
                        "regularMarketPrice": 25,
                        "regularMarketChangePercent": -4.1,
                        "regularMarketVolume": 800,
                        "regularMarketTime": requested_at,
                    },
                },
            ]
        }

        def fake_request(path, params):
            if path == "/v2/tickers":
                return ticker_results[params["sortOrder"]]
            return quote_payload

        with patch.object(
            self.provider,
            "_request",
            side_effect=fake_request,
        ):
            movers = self.provider.market_movers(5)

        self.assertEqual([item.symbol for item in movers.gainers], ["PETR4"])
        self.assertEqual([item.symbol for item in movers.losers], ["BBAS3"])
        self.assertEqual(movers.gainers[0].volume, 1000)
        self.assertEqual(movers.gainers[0].daily_change_percent, Decimal("3.5"))
        self.assertEqual(movers.source, "brapi.dev")

    def test_http_errors_are_explicit_and_never_include_token(self):
        error = HTTPError(
            "https://brapi.dev/api/v2/tickers",
            429,
            "rate limit",
            {},
            io.BytesIO(b""),
        )
        with patch(
            "CashSave.brapi_market_data.urlopen",
            side_effect=error,
        ):
            with self.assertRaises(MarketDataRateLimitError) as caught:
                self.provider.search("PETR", category=None)

        self.assertNotIn("server-test-token", str(caught.exception))

    def test_free_plan_limit_explains_that_market_movers_require_pro(self):
        body = json.dumps(
            {"code": "QUOTES_PER_REQUEST_EXCEEDED"}
        ).encode("utf-8")
        error = HTTPError(
            "https://brapi.dev/api/v2/stocks/quote",
            400,
            "bad request",
            {},
            io.BytesIO(body),
        )
        with patch(
            "CashSave.brapi_market_data.urlopen",
            side_effect=error,
        ):
            with self.assertRaises(MarketDataProviderError) as caught:
                self.provider.search("PETR", category=None)

        self.assertIn("plano Pro", str(caught.exception))
        self.assertNotIn("server-test-token", str(caught.exception))

    def test_provider_request_keeps_token_in_server_side_header(self):
        request_details = {}

        def fake_urlopen(request, timeout):
            request_details["authorization"] = request.get_header("Authorization")
            request_details["url"] = request.full_url
            request_details["timeout"] = timeout
            return io.BytesIO(json.dumps({"results": []}).encode("utf-8"))

        with patch(
            "CashSave.brapi_market_data.urlopen",
            side_effect=fake_urlopen,
        ):
            self.provider._request("/v2/tickers", {"search": "PETR"})

        self.assertEqual(
            request_details["authorization"],
            "Bearer server-test-token",
        )
        self.assertNotIn("server-test-token", request_details["url"])
        self.assertEqual(request_details["timeout"], 10)

    def test_invalid_provider_payloads_are_not_treated_as_empty_data(self):
        with patch.object(
            self.provider,
            "_request",
            return_value={"results": "invalid"},
        ):
            with self.assertRaises(MarketDataProviderError):
                self.provider.search("PETR", category=None)


if __name__ == "__main__":
    unittest.main()
