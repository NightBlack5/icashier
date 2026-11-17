from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass, replace
from datetime import datetime
from decimal import Decimal
import os
from threading import RLock
from time import monotonic
from typing import Callable, Literal, Protocol, TypeVar, cast


AssetCategory = Literal["acao", "fii", "etf"]
Freshness = Literal["real_time", "delayed", "historical", "unknown"]


class MarketDataError(Exception):
    """Base error for market-data requests."""


class MarketDataNotConfigured(MarketDataError):
    """Raised when no approved market-data provider is configured."""


class MarketDataProviderError(MarketDataError):
    """Raised when a configured provider cannot return verified data."""


class MarketDataRateLimitError(MarketDataProviderError):
    """Raised when a provider rejects a request due to its rate limit."""


@dataclass(frozen=True)
class MarketAsset:
    symbol: str
    name: str
    category: AssetCategory
    source: str
    stale: bool = False

    def __post_init__(self) -> None:
        if not self.symbol.strip() or not self.name.strip() or not self.source.strip():
            raise ValueError("Ativo exige código, nome e fonte.")
        if self.category not in {"acao", "fii", "etf"}:
            raise ValueError("Categoria de ativo não suportada.")


@dataclass(frozen=True)
class MarketQuote:
    symbol: str
    category: AssetCategory
    price: Decimal
    currency: str
    source: str
    reference_at: datetime
    freshness: Freshness
    daily_change_percent: Decimal | None = None
    stale: bool = False

    def __post_init__(self) -> None:
        if not self.symbol.strip() or not self.source.strip():
            raise ValueError("Cotação exige código e fonte.")
        if not isinstance(self.price, Decimal):
            raise ValueError("Cotação deve usar Decimal.")
        if not self.price.is_finite() or self.price <= 0:
            raise ValueError("Cotação deve ser um valor positivo e finito.")
        if self.currency != "BRL":
            raise ValueError("A cotação deve estar expressa em BRL.")
        if self.category not in {"acao", "fii", "etf"}:
            raise ValueError("Categoria de ativo não suportada.")
        if self.freshness not in {
            "real_time",
            "delayed",
            "historical",
            "unknown",
        }:
            raise ValueError("Classificação de atualização não suportada.")
        if self.daily_change_percent is not None:
            if not isinstance(self.daily_change_percent, Decimal):
                raise ValueError("Variação diária deve usar Decimal.")
            if not self.daily_change_percent.is_finite():
                raise ValueError("Variação diária deve ser finita.")
        if self.reference_at.tzinfo is None:
            raise ValueError("Horário de referência deve incluir fuso horário.")


@dataclass(frozen=True)
class MarketHistoryPoint:
    observed_at: datetime
    price: Decimal

    def __post_init__(self) -> None:
        if self.observed_at.tzinfo is None:
            raise ValueError("Observação histórica deve incluir fuso horário.")
        if not isinstance(self.price, Decimal):
            raise ValueError("Preço histórico deve usar Decimal.")
        if not self.price.is_finite() or self.price <= 0:
            raise ValueError("Preço histórico deve ser positivo e finito.")


@dataclass(frozen=True)
class MarketHistory:
    symbol: str
    points: tuple[MarketHistoryPoint, ...]
    source: str
    reference_at: datetime
    freshness: Freshness
    stale: bool = False

    def __post_init__(self) -> None:
        if not self.symbol.strip() or not self.source.strip():
            raise ValueError("Histórico exige código e fonte.")
        if self.reference_at.tzinfo is None:
            raise ValueError("Referência do histórico deve incluir fuso horário.")
        if not isinstance(self.points, tuple) or not all(
            isinstance(point, MarketHistoryPoint) for point in self.points
        ):
            raise ValueError("Histórico contém observações inválidas.")
        if self.freshness not in {
            "real_time",
            "delayed",
            "historical",
            "unknown",
        }:
            raise ValueError("Classificação de atualização não suportada.")
        if tuple(sorted(self.points, key=lambda point: point.observed_at)) != self.points:
            raise ValueError("Observações históricas devem estar em ordem temporal.")


@dataclass(frozen=True)
class MarketMover:
    symbol: str
    name: str
    price: Decimal
    daily_change_percent: Decimal
    volume: int
    source: str
    reference_at: datetime
    stale: bool = False

    def __post_init__(self) -> None:
        if not self.symbol.strip() or not self.name.strip() or not self.source.strip():
            raise ValueError("Movimentação exige código, nome e fonte.")
        if (
            not isinstance(self.price, Decimal)
            or not self.price.is_finite()
            or self.price <= 0
        ):
            raise ValueError("Preço do ativo deve ser positivo e finito.")
        if (
            not isinstance(self.daily_change_percent, Decimal)
            or not self.daily_change_percent.is_finite()
        ):
            raise ValueError("Variação diária deve ser finita.")
        if (
            isinstance(self.volume, bool)
            or not isinstance(self.volume, int)
            or self.volume <= 0
        ):
            raise ValueError("Volume negociado deve ser positivo.")
        if self.reference_at.tzinfo is None:
            raise ValueError("Horário de referência deve incluir fuso horário.")


@dataclass(frozen=True)
class MarketMovers:
    gainers: tuple[MarketMover, ...]
    losers: tuple[MarketMover, ...]
    source: str
    reference_at: datetime
    stale: bool = False

    def __post_init__(self) -> None:
        if not self.source.strip():
            raise ValueError("Ranking de mercado exige uma fonte.")
        if self.reference_at.tzinfo is None:
            raise ValueError("Horário de referência deve incluir fuso horário.")
        if not isinstance(self.gainers, tuple) or not isinstance(self.losers, tuple):
            raise ValueError("Ranking de mercado deve usar sequências imutáveis.")
        if not all(
            isinstance(mover, MarketMover)
            for mover in self.gainers + self.losers
        ):
            raise ValueError("Ranking contém movimentações inválidas.")
        if tuple(
            sorted(
                self.gainers,
                key=lambda mover: mover.daily_change_percent,
                reverse=True,
            )
        ) != self.gainers:
            raise ValueError("Maiores altas devem estar em ordem decrescente.")
        if tuple(
            sorted(
                self.losers,
                key=lambda mover: mover.daily_change_percent,
            )
        ) != self.losers:
            raise ValueError("Maiores baixas devem estar em ordem crescente.")
        if any(mover.daily_change_percent <= 0 for mover in self.gainers):
            raise ValueError("Maiores altas devem ter variação positiva.")
        if any(mover.daily_change_percent >= 0 for mover in self.losers):
            raise ValueError("Maiores baixas devem ter variação negativa.")


class MarketDataProvider(Protocol):
    name: str

    def search(
        self,
        query: str,
        category: AssetCategory | None,
    ) -> tuple[MarketAsset, ...]: ...

    def quote(self, symbol: str) -> MarketQuote: ...

    def history(self, symbol: str, period: str) -> MarketHistory: ...

    def market_movers(self, limit: int) -> MarketMovers: ...


T = TypeVar("T")


@dataclass(frozen=True)
class _CacheEntry:
    value: object
    expires_at: float


class MarketDataService:
    """Normalizes provider access and caches only for an explicitly allowed TTL."""

    def __init__(
        self,
        provider: MarketDataProvider | None = None,
        cache_ttl_seconds: int = 0,
        max_cache_entries: int = 256,
    ) -> None:
        if cache_ttl_seconds < 0:
            raise ValueError("O tempo de cache não pode ser negativo.")
        if max_cache_entries < 1:
            raise ValueError("O limite do cache deve ser positivo.")
        self._provider = provider
        self._cache_ttl_seconds = cache_ttl_seconds
        self._max_cache_entries = max_cache_entries
        self._cache: dict[tuple[str, ...], _CacheEntry] = {}
        self._cache_lock = RLock()

    @property
    def configured(self) -> bool:
        return self._provider is not None

    def search(
        self,
        query: str,
        category: AssetCategory | None = None,
        sort_by: Literal["symbol", "name"] = "symbol",
    ) -> tuple[MarketAsset, ...]:
        normalized_query = query.strip()
        if not normalized_query:
            raise ValueError("Informe um código ou nome para pesquisar.")
        if len(normalized_query) > 80:
            raise ValueError("A pesquisa deve ter no máximo 80 caracteres.")
        if category is not None and category not in {"acao", "fii", "etf"}:
            raise ValueError("Categoria de ativo não suportada.")
        if sort_by not in {"symbol", "name"}:
            raise ValueError("Ordenação de ativos não suportada.")
        assets = self._fetch(
            ("search", normalized_query.casefold(), category or ""),
            lambda provider: provider.search(normalized_query, category),
        )
        if not isinstance(assets, tuple) or not all(
            isinstance(asset, MarketAsset) for asset in assets
        ):
            raise MarketDataProviderError(
                "O provedor retornou uma lista de ativos inválida."
            )
        if category is not None:
            assets = tuple(asset for asset in assets if asset.category == category)
        return tuple(
            sorted(assets, key=lambda asset: getattr(asset, sort_by).casefold())
        )

    def quote(self, symbol: str) -> MarketQuote:
        normalized_symbol = self._validate_symbol(symbol)
        quote = self._fetch(
            ("quote", normalized_symbol),
            lambda provider: provider.quote(normalized_symbol),
        )
        if not isinstance(quote, MarketQuote) or quote.symbol != normalized_symbol:
            raise MarketDataProviderError(
                "O provedor retornou uma cotação incompatível com o ativo solicitado."
            )
        return quote

    def history(self, symbol: str, period: str) -> MarketHistory:
        normalized_symbol = self._validate_symbol(symbol)
        normalized_period = period.strip().lower()
        if normalized_period not in {
            "intraday",
            "1d",
            "1w",
            "1m",
            "6m",
            "1y",
            "5y",
        }:
            raise ValueError("Período histórico não suportado.")
        history = self._fetch(
            ("history", normalized_symbol, normalized_period),
            lambda provider: provider.history(
                normalized_symbol,
                normalized_period,
            ),
        )
        if (
            not isinstance(history, MarketHistory)
            or history.symbol != normalized_symbol
        ):
            raise MarketDataProviderError(
                "O provedor retornou um histórico incompatível com o ativo solicitado."
            )
        return history

    def market_movers(self, limit: int = 5) -> MarketMovers:
        if (
            isinstance(limit, bool)
            or not isinstance(limit, int)
            or limit < 1
            or limit > 10
        ):
            raise ValueError("O ranking deve conter entre 1 e 10 ativos.")
        movers = self._fetch(
            ("market-movers", str(limit)),
            lambda provider: provider.market_movers(limit),
        )
        if (
            not isinstance(movers, MarketMovers)
            or len(movers.gainers) > limit
            or len(movers.losers) > limit
        ):
            raise MarketDataProviderError(
                "O provedor retornou um ranking de mercado inválido."
            )
        return movers

    @staticmethod
    def _validate_symbol(symbol: str) -> str:
        normalized_symbol = symbol.strip().upper()
        if not normalized_symbol or len(normalized_symbol) > 24:
            raise ValueError("Informe um código de ativo válido.")
        return normalized_symbol

    def _fetch(
        self,
        key: tuple[str, ...],
        fetcher: Callable[[MarketDataProvider], T],
    ) -> T:
        provider = self._provider
        if provider is None:
            raise MarketDataNotConfigured(
                "Dados de mercado indisponíveis: nenhum provedor aprovado está configurado."
            )

        now = monotonic()
        with self._cache_lock:
            entry = self._cache.get(key)
            if entry is not None and now < entry.expires_at:
                return cast(T, entry.value)

        try:
            value = fetcher(provider)
        except MarketDataProviderError:
            if entry is not None and self._cache_ttl_seconds > 0:
                stale_value = self._mark_stale(entry.value)
                return cast(T, stale_value)
            raise

        if self._cache_ttl_seconds > 0:
            with self._cache_lock:
                if len(self._cache) >= self._max_cache_entries:
                    oldest_key = min(
                        self._cache,
                        key=lambda cache_key: self._cache[cache_key].expires_at,
                    )
                    del self._cache[oldest_key]
                self._cache[key] = _CacheEntry(
                    value=value,
                    expires_at=monotonic() + self._cache_ttl_seconds,
                )
        return value

    @staticmethod
    def _mark_stale(value: object) -> object:
        if isinstance(value, tuple):
            return tuple(MarketDataService._mark_stale(item) for item in value)
        if is_dataclass(value) and any(
            item.name == "stale" for item in fields(value)
        ):
            return replace(value, stale=True)
        return value


def create_market_data_service_from_environment() -> MarketDataService:
    token = os.getenv("CASHSAVE_BRAPI_TOKEN", "").strip()
    if not token:
        return MarketDataService()

    from .brapi_market_data import BrapiMarketDataProvider

    return MarketDataService(
        provider=BrapiMarketDataProvider(token),
        cache_ttl_seconds=300,
    )


market_data_service = create_market_data_service_from_environment()
