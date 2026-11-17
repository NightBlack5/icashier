from dataclasses import dataclass
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from typing import Mapping

from .market_data import MarketHistory


@dataclass(frozen=True)
class PriceComparison:
    complete: bool
    series: tuple[dict[str, str | Decimal], ...]
    performance_percent: tuple[tuple[str, Decimal], ...]
    missing_dates: tuple[tuple[str, str], ...]
    start_date: str
    end_date: str


def compare_price_histories(
    histories: Mapping[str, MarketHistory],
) -> PriceComparison:
    if len(histories) < 2:
        raise ValueError("Selecione pelo menos dois ativos para comparar.")

    points_by_symbol: dict[str, dict[date, Decimal]] = {}
    for selected_symbol, history in histories.items():
        symbol = selected_symbol.strip().upper()
        if not symbol or history.symbol.strip().upper() != symbol:
            raise ValueError("A série retornada não corresponde ao ativo selecionado.")
        if symbol in points_by_symbol:
            raise ValueError("Cada ativo deve aparecer uma única vez.")
        daily_points: dict[date, Decimal] = {}
        for point in sorted(history.points, key=lambda item: item.observed_at):
            daily_points[point.observed_at.date()] = point.price
        if not daily_points:
            raise ValueError(f"Não há histórico verificado para {symbol}.")
        points_by_symbol[symbol] = daily_points

    all_dates = set().union(
        *(set(points) for points in points_by_symbol.values())
    )
    reference_dates = set(next(iter(points_by_symbol.values())))
    complete = all(
        set(points) == reference_dates
        for points in points_by_symbol.values()
    )
    if not complete:
        missing_dates = tuple(
            (symbol, missing.isoformat())
            for symbol, points in sorted(points_by_symbol.items())
            for missing in sorted(all_dates - set(points))
        )
        return PriceComparison(
            complete=False,
            series=(),
            performance_percent=(),
            missing_dates=missing_dates,
            start_date=min(all_dates).isoformat(),
            end_date=max(all_dates).isoformat(),
        )

    ordered_dates = sorted(reference_dates)
    if len(ordered_dates) < 2:
        raise ValueError("O período precisa conter ao menos duas datas verificadas.")
    first_date = ordered_dates[0]
    series: list[dict[str, str | Decimal]] = []
    for observed_date in ordered_dates:
        row: dict[str, str | Decimal] = {"data": observed_date.isoformat()}
        for symbol, points in sorted(points_by_symbol.items()):
            baseline = points[first_date]
            row[symbol] = (
                points[observed_date] / baseline * 100
            ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        series.append(row)

    final_date = ordered_dates[-1]
    performance = tuple(
        (
            symbol,
            (
                (points[final_date] / points[first_date] - 1) * 100
            ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        )
        for symbol, points in sorted(points_by_symbol.items())
    )
    return PriceComparison(
        complete=True,
        series=tuple(series),
        performance_percent=performance,
        missing_dates=(),
        start_date=first_date.isoformat(),
        end_date=final_date.isoformat(),
    )
