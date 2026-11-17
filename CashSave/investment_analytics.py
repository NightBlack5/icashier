from dataclasses import dataclass
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from typing import Mapping

from .investment_portfolio import InvestmentOperation, InvestmentPosition, calculate_position
from .investment_proventos import format_provento_record


def assert_investment_record_owner(
    records: list[Mapping[str, object]],
    authenticated_user_id: object,
) -> None:
    if authenticated_user_id is None or not str(authenticated_user_id).strip():
        raise ValueError("A carteira exige uma identidade autenticada.")
    owner_id = str(authenticated_user_id)
    if any(
        record.get("usuario_id") is not None
        and str(record["usuario_id"]) != owner_id
        for record in records
    ):
        raise ValueError("A carteira retornou dados de outro usuário.")


@dataclass(frozen=True)
class PortfolioHolding:
    symbol: str
    category: str
    position: InvestmentPosition


@dataclass(frozen=True)
class PortfolioSnapshot:
    holdings: tuple[PortfolioHolding, ...]
    total_cost_basis_centavos: int
    total_purchase_outlay_centavos: int
    total_realized_result_centavos: int
    total_market_value_centavos: int | None
    total_unrealized_result_centavos: int | None
    simple_return_percent: Decimal | None
    allocation_by_category: tuple[tuple[str, int, Decimal], ...]


def _round_centavos(value: Decimal) -> int:
    return int(value.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def calculate_portfolio_snapshot(
    operations: list[InvestmentOperation] | tuple[InvestmentOperation, ...],
    categories: Mapping[str, str],
    market_prices_centavos: Mapping[str, int],
) -> PortfolioSnapshot:
    grouped: dict[str, list[InvestmentOperation]] = {}
    for operation in operations:
        grouped.setdefault(operation.symbol, []).append(operation)
    if any(
        category not in {"acao", "fii", "etf"}
        for category in categories.values()
    ):
        raise ValueError("A carteira contém uma categoria de ativo inválida.")
    if any(symbol not in categories for symbol in grouped):
        raise ValueError("A carteira não contém a categoria de todos os ativos.")

    holdings: list[PortfolioHolding] = []
    total_purchase_outlay = Decimal("0")
    total_realized = 0
    total_cost_basis = 0
    missing_quote = False
    total_market_value = 0
    total_unrealized = 0
    allocation_values: dict[str, int] = {}

    for operation in operations:
        if operation.operation_type == "compra":
            total_purchase_outlay += (
                operation.quantity * operation.unit_price_centavos
                + operation.costs_centavos
            )

    for symbol, history in sorted(grouped.items()):
        position = calculate_position(
            symbol,
            history,
            market_price_centavos=market_prices_centavos.get(symbol),
        )
        category = categories[symbol]
        holdings.append(PortfolioHolding(symbol, category, position))
        total_cost_basis += position.cost_basis_centavos
        total_realized += position.realized_result_centavos
        if position.quantity == 0:
            continue
        if (
            position.market_value_centavos is None
            or position.unrealized_result_centavos is None
        ):
            missing_quote = True
            continue
        total_market_value += position.market_value_centavos
        total_unrealized += position.unrealized_result_centavos
        allocation_values[category] = (
            allocation_values.get(category, 0) + position.market_value_centavos
        )

    market_value = None if missing_quote else total_market_value
    unrealized_result = None if missing_quote else total_unrealized
    purchase_outlay_centavos = _round_centavos(total_purchase_outlay)
    simple_return = None
    allocations: tuple[tuple[str, int, Decimal], ...] = ()
    if market_value is not None and purchase_outlay_centavos > 0:
        simple_return = (
            Decimal(total_realized + (unrealized_result or 0))
            / Decimal(purchase_outlay_centavos)
            * 100
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if market_value:
        allocations = tuple(
            (
                category,
                value,
                (Decimal(value) / Decimal(market_value) * 100).quantize(
                    Decimal("0.01"),
                    rounding=ROUND_HALF_UP,
                ),
            )
            for category, value in sorted(allocation_values.items())
        )

    return PortfolioSnapshot(
        holdings=tuple(holdings),
        total_cost_basis_centavos=total_cost_basis,
        total_purchase_outlay_centavos=purchase_outlay_centavos,
        total_realized_result_centavos=total_realized,
        total_market_value_centavos=market_value,
        total_unrealized_result_centavos=unrealized_result,
        simple_return_percent=simple_return,
        allocation_by_category=allocations,
    )


def monthly_investment_flows(
    operations: list[InvestmentOperation] | tuple[InvestmentOperation, ...],
    proventos: list[Mapping[str, object]],
) -> list[dict[str, int | str]]:
    periods: dict[str, dict[str, int | str]] = {}

    def period_for(flow_date: date) -> dict[str, int | str]:
        period = flow_date.strftime("%Y-%m")
        return periods.setdefault(
            period,
            {
                "periodo": period,
                "contribuicoes_centavos": 0,
                "retiradas_centavos": 0,
                "proventos_centavos": 0,
            },
        )

    for operation in operations:
        flow = period_for(operation.operation_date)
        amount = operation.quantity * operation.unit_price_centavos
        if operation.operation_type == "compra":
            flow["contribuicoes_centavos"] = int(
                flow["contribuicoes_centavos"]
            ) + _round_centavos(amount + operation.costs_centavos)
        else:
            flow["retiradas_centavos"] = int(
                flow["retiradas_centavos"]
            ) + _round_centavos(amount - operation.costs_centavos)

    for record in proventos:
        formatted = format_provento_record(record)
        if formatted["status"] != "pago":
            continue
        payment_date = date.fromisoformat(str(formatted["data_pagamento"]))
        flow = period_for(payment_date)
        flow["proventos_centavos"] = int(flow["proventos_centavos"]) + int(
            formatted["valor_centavos"]
        )

    return [periods[key] for key in sorted(periods)]
