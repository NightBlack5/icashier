from __future__ import annotations

import json
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .market_data import (
    AssetCategory,
    MarketAsset,
    MarketDataProviderError,
    MarketDataRateLimitError,
    MarketHistory,
    MarketHistoryPoint,
    MarketMover,
    MarketMovers,
    MarketQuote,
)


class BrapiMarketDataProvider:
    name = "brapi.dev"
    base_url = "https://brapi.dev/api"

    def __init__(self, token: str, timeout_seconds: int = 10) -> None:
        normalized_token = token.strip()
        if not normalized_token:
            raise ValueError("A chave da brapi.dev não pode estar vazia.")
        if timeout_seconds < 1:
            raise ValueError("O tempo limite da brapi.dev deve ser positivo.")
        self._token = normalized_token
        self._timeout_seconds = timeout_seconds

    def search(
        self,
        query: str,
        category: AssetCategory | None,
    ) -> tuple[MarketAsset, ...]:
        params: dict[str, str] = {"search": query, "limit": "100"}
        if category == "acao":
            params["type"] = "stock"
        elif category == "fii":
            params["subType"] = "fii"
        elif category == "etf":
            params["subType"] = "etf"

        payload = self._request("/v2/tickers", params)
        assets: list[MarketAsset] = []
        for result in self._results(payload):
            symbol = result.get("symbol")
            name = result.get("name")
            mapped_category = self._category(result.get("subType"))
            if (
                not isinstance(symbol, str)
                or not isinstance(name, str)
                or mapped_category is None
                or result.get("isActive") is not True
                or (category is not None and mapped_category != category)
            ):
                continue
            assets.append(
                MarketAsset(
                    symbol=symbol,
                    name=name,
                    category=mapped_category,
                    source=self.name,
                )
            )
        return tuple(assets)

    def quote(self, symbol: str) -> MarketQuote:
        category = self._lookup_category(symbol)
        payload = self._request(
            "/v2/stocks/quote",
            {"symbols": symbol},
        )
        result = self._find_result(payload, symbol)
        data = result.get("data")
        if not isinstance(data, dict):
            raise MarketDataProviderError(
                "A brapi.dev retornou uma cotação sem dados."
            )
        price = self._decimal(data.get("regularMarketPrice"), "cotação")
        daily_change = self._decimal(
            data.get("regularMarketChangePercent"),
            "variação diária",
            optional=True,
        )
        return MarketQuote(
            symbol=symbol,
            category=category,
            price=price,
            currency=str(data.get("currency", "")),
            source=self.name,
            reference_at=self._timestamp(data.get("regularMarketTime")),
            freshness="delayed",
            daily_change_percent=daily_change,
        )

    def history(self, symbol: str, period: str) -> MarketHistory:
        ranges = {
            "intraday": ("1d", "5m"),
            "1d": ("1d", "5m"),
            "1w": ("7d", "15m"),
            "1m": ("1mo", "1d"),
            "6m": ("6mo", "1d"),
            "1y": ("1y", "1d"),
            "5y": ("5y", "1wk"),
        }
        selected_range = ranges.get(period)
        if selected_range is None:
            raise ValueError("Período histórico não suportado pela brapi.dev.")

        payload = self._request(
            "/v2/stocks/historical",
            {
                "symbols": symbol,
                "range": selected_range[0],
                "interval": selected_range[1],
                "sortOrder": "asc",
            },
        )
        result = self._find_result(payload, symbol)
        data = result.get("data")
        if not isinstance(data, dict):
            raise MarketDataProviderError(
                "A brapi.dev retornou um histórico sem dados."
            )
        raw_points = data.get("historicalDataPrice")
        if not isinstance(raw_points, list):
            raise MarketDataProviderError(
                "A brapi.dev retornou uma série histórica inválida."
            )

        points = tuple(
            sorted(
                (
                    MarketHistoryPoint(
                        observed_at=self._epoch_timestamp(item.get("date")),
                        price=self._decimal(
                            item.get("close")
                            if item.get("close") is not None
                            else item.get("adjustedClose"),
                            "preço histórico",
                        ),
                    )
                    for item in raw_points
                    if isinstance(item, dict)
                ),
                key=lambda point: point.observed_at,
            )
        )
        if len(points) != len(raw_points):
            raise MarketDataProviderError(
                "A brapi.dev retornou pontos históricos inválidos."
            )

        freshness = "delayed" if period in {"intraday", "1d", "1w"} else "historical"
        return MarketHistory(
            symbol=symbol,
            points=points,
            source=self.name,
            reference_at=self._timestamp(payload.get("requestedAt")),
            freshness=freshness,
        )

    def market_movers(self, limit: int) -> MarketMovers:
        candidates: dict[str, str] = {}
        list_timestamps: list[datetime] = []
        fetch_limit = str(max(20, limit * 4))

        for order in ("desc", "asc"):
            payload = self._request(
                "/v2/tickers",
                {
                    "type": "stock",
                    "sortBy": "change",
                    "sortOrder": order,
                    "limit": fetch_limit,
                },
            )
            list_timestamps.append(self._timestamp(payload.get("requestedAt")))
            for result in self._results(payload):
                symbol = result.get("symbol")
                name = result.get("name")
                quote = result.get("quote")
                volume = (
                    self._decimal(
                        quote.get("volume"),
                        "volume negociado",
                        optional=True,
                    )
                    if isinstance(quote, dict)
                    else None
                )
                if (
                    not isinstance(symbol, str)
                    or not isinstance(name, str)
                    or not isinstance(quote, dict)
                    or result.get("isActive") is not True
                    or symbol.upper().endswith("F")
                    or volume is None
                    or volume <= 0
                ):
                    continue
                candidates.setdefault(symbol.upper(), name)

        symbols = tuple(candidates)
        quotes: list[MarketMover] = []
        for offset in range(0, len(symbols), 20):
            batch = symbols[offset : offset + 20]
            payload = self._request(
                "/v2/stocks/quote",
                {"symbols": ",".join(batch)},
            )
            for result in self._results(payload):
                symbol = result.get("symbol")
                data = result.get("data")
                if (
                    not isinstance(symbol, str)
                    or symbol.upper() not in candidates
                    or not isinstance(data, dict)
                ):
                    continue
                price = self._decimal(
                    data.get("regularMarketPrice"),
                    "cotação",
                    optional=True,
                )
                change = self._decimal(
                    data.get("regularMarketChangePercent"),
                    "variação diária",
                    optional=True,
                )
                volume = self._integer(data.get("regularMarketVolume"))
                if (
                    price is None
                    or change is None
                    or volume is None
                    or price <= 0
                    or volume <= 0
                    or symbol.upper().endswith("F")
                ):
                    continue
                quotes.append(
                    MarketMover(
                        symbol=symbol.upper(),
                        name=candidates[symbol.upper()],
                        price=price,
                        daily_change_percent=change,
                        volume=volume,
                        source=self.name,
                        reference_at=self._timestamp(
                            data.get("regularMarketTime")
                        ),
                    )
                )

        gainers = tuple(
            sorted(
                (
                    mover
                    for mover in quotes
                    if mover.daily_change_percent > 0
                ),
                key=lambda mover: mover.daily_change_percent,
                reverse=True,
            )[:limit]
        )
        losers = tuple(
            sorted(
                (
                    mover
                    for mover in quotes
                    if mover.daily_change_percent < 0
                ),
                key=lambda mover: mover.daily_change_percent,
            )[:limit]
        )
        reference_at = max(
            (
                mover.reference_at
                for mover in gainers + losers
            ),
            default=max(list_timestamps),
        )
        return MarketMovers(
            gainers=gainers,
            losers=losers,
            source=self.name,
            reference_at=reference_at,
        )

    def _lookup_category(self, symbol: str) -> AssetCategory:
        payload = self._request(
            "/v2/tickers",
            {"search": symbol, "limit": "100"},
        )
        for result in self._results(payload):
            result_symbol = result.get("symbol")
            if (
                isinstance(result_symbol, str)
                and result_symbol.upper() == symbol.upper()
            ):
                category = self._category(result.get("subType"))
                if category is not None:
                    return category
        raise MarketDataProviderError(
            "A brapi.dev não encontrou a categoria do ativo solicitado."
        )

    def _request(self, path: str, params: dict[str, str]) -> dict[str, object]:
        url = f"{self.base_url}{path}?{urlencode(params)}"
        request = Request(
            url,
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {self._token}",
            },
        )
        try:
            with urlopen(request, timeout=self._timeout_seconds) as response:
                body = response.read()
        except HTTPError as error:
            if error.code == 429:
                error.close()
                raise MarketDataRateLimitError(
                    "A brapi.dev atingiu o limite da conta. Tente novamente mais tarde."
                ) from error
            try:
                error_payload = json.loads(error.read().decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                error_payload = {}
            finally:
                error.close()
            if error.code == 401:
                raise MarketDataProviderError(
                    "A chave da brapi.dev é inválida ou expirou."
                ) from error
            if error.code == 403:
                raise MarketDataProviderError(
                    "O plano atual da brapi.dev não inclui este dado."
                ) from error
            if (
                error.code == 400
                and isinstance(error_payload, dict)
                and error_payload.get("code") == "QUOTES_PER_REQUEST_EXCEEDED"
            ):
                raise MarketDataProviderError(
                    "O plano atual da brapi.dev permite apenas um ativo por "
                    "requisição; o ranking da bolsa exige o plano Pro."
                ) from error
            raise MarketDataProviderError(
                f"A brapi.dev respondeu com HTTP {error.code}."
            ) from error
        except (TimeoutError, URLError) as error:
            raise MarketDataProviderError(
                "Não foi possível conectar à brapi.dev."
            ) from error

        try:
            payload = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise MarketDataProviderError(
                "A brapi.dev retornou uma resposta JSON inválida."
            ) from error
        if not isinstance(payload, dict):
            raise MarketDataProviderError(
                "A brapi.dev retornou uma resposta incompatível."
            )
        return payload

    @staticmethod
    def _results(payload: dict[str, object]) -> list[dict[str, object]]:
        results = payload.get("results")
        if not isinstance(results, list) or not all(
            isinstance(result, dict) for result in results
        ):
            raise MarketDataProviderError(
                "A brapi.dev retornou uma lista de resultados inválida."
            )
        return results

    @staticmethod
    def _find_result(
        payload: dict[str, object],
        symbol: str,
    ) -> dict[str, object]:
        for result in BrapiMarketDataProvider._results(payload):
            returned_symbol = result.get("symbol")
            requested_symbol = result.get("requestedSymbol")
            if (
                isinstance(returned_symbol, str)
                and returned_symbol.upper() == symbol.upper()
            ) or (
                isinstance(requested_symbol, str)
                and requested_symbol.upper() == symbol.upper()
            ):
                return result
        raise MarketDataProviderError(
            "A brapi.dev não retornou o ativo solicitado."
        )

    @staticmethod
    def _category(value: object) -> AssetCategory | None:
        if value in ("stock", "unit"):
            return "acao"
        if value == "fii":
            return "fii"
        if value == "etf":
            return "etf"
        return None

    @staticmethod
    def _decimal(
        value: object,
        field: str,
        optional: bool = False,
    ) -> Decimal | None:
        if value is None and optional:
            return None
        if isinstance(value, bool):
            raise MarketDataProviderError(
                f"A brapi.dev retornou {field} inválido."
            )
        try:
            parsed = Decimal(str(value))
        except (InvalidOperation, ValueError) as error:
            if optional:
                return None
            raise MarketDataProviderError(
                f"A brapi.dev retornou {field} inválido."
            ) from error
        if not parsed.is_finite():
            if optional:
                return None
            raise MarketDataProviderError(
                f"A brapi.dev retornou {field} não finito."
            )
        return parsed

    @staticmethod
    def _integer(value: object) -> int | None:
        parsed = BrapiMarketDataProvider._decimal(
            value,
            "volume negociado",
            optional=True,
        )
        if parsed is None or parsed != parsed.to_integral_value():
            return None
        return int(parsed)

    @staticmethod
    def _timestamp(value: object) -> datetime:
        if not isinstance(value, str):
            raise MarketDataProviderError(
                "A brapi.dev não retornou um horário de referência válido."
            )
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as error:
            raise MarketDataProviderError(
                "A brapi.dev retornou um horário de referência inválido."
            ) from error
        if parsed.tzinfo is None:
            raise MarketDataProviderError(
                "A brapi.dev retornou um horário sem fuso."
            )
        return parsed

    @staticmethod
    def _epoch_timestamp(value: object) -> datetime:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise MarketDataProviderError(
                "A brapi.dev retornou uma data histórica inválida."
            )
        try:
            return datetime.fromtimestamp(value, tz=timezone.utc)
        except (OverflowError, OSError, ValueError) as error:
            raise MarketDataProviderError(
                "A brapi.dev retornou uma data histórica fora do intervalo."
            ) from error
