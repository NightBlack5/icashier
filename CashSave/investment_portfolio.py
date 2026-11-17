from dataclasses import dataclass
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from typing import Literal


OperationType = Literal["compra", "venda"]


class InsufficientInvestmentQuantityError(ValueError):
    """Raised when a sale exceeds the position available at that date."""


@dataclass(frozen=True)
class InvestmentOperation:
    symbol: str
    operation_type: OperationType
    operation_date: date
    quantity: Decimal
    unit_price_centavos: int
    costs_centavos: int = 0
    operation_id: int = 0

    def __post_init__(self) -> None:
        normalized_symbol = self.symbol.strip().upper()
        if not normalized_symbol:
            raise ValueError("Informe o código do ativo.")
        object.__setattr__(self, "symbol", normalized_symbol)
        if self.operation_type not in {"compra", "venda"}:
            raise ValueError("Tipo de operação não suportado.")
        if not isinstance(self.quantity, Decimal):
            raise ValueError("A quantidade deve usar Decimal.")
        if not self.quantity.is_finite() or self.quantity <= 0:
            raise ValueError("A quantidade deve ser positiva e finita.")
        if (
            not isinstance(self.unit_price_centavos, int)
            or isinstance(self.unit_price_centavos, bool)
            or self.unit_price_centavos <= 0
        ):
            raise ValueError("O preço unitário deve ser positivo em centavos.")
        if (
            not isinstance(self.costs_centavos, int)
            or isinstance(self.costs_centavos, bool)
            or self.costs_centavos < 0
        ):
            raise ValueError("Os custos devem ser zero ou positivos em centavos.")
        if not isinstance(self.operation_date, date):
            raise ValueError("Informe uma data válida para a operação.")


@dataclass(frozen=True)
class InvestmentPosition:
    symbol: str
    quantity: Decimal
    average_unit_cost_centavos: Decimal | None
    cost_basis_centavos: int
    realized_result_centavos: int
    market_value_centavos: int | None
    unrealized_result_centavos: int | None


def _round_centavos(value: Decimal) -> int:
    return int(value.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def calculate_position(
    symbol: str,
    operations: list[InvestmentOperation] | tuple[InvestmentOperation, ...],
    market_price_centavos: int | None = None,
) -> InvestmentPosition:
    normalized_symbol = symbol.strip().upper()
    if not normalized_symbol:
        raise ValueError("Informe o código do ativo.")
    if market_price_centavos is not None and (
        not isinstance(market_price_centavos, int)
        or isinstance(market_price_centavos, bool)
        or market_price_centavos <= 0
    ):
        raise ValueError("A cotação deve ser positiva em centavos.")
    if any(operation.symbol != normalized_symbol for operation in operations):
        raise ValueError("Todas as operações devem pertencer ao mesmo ativo.")

    ordered_operations = sorted(
        operations,
        key=lambda operation: (operation.operation_date, operation.operation_id),
    )
    quantity = Decimal("0")
    cost_basis = Decimal("0")
    realized_result = Decimal("0")

    for operation in ordered_operations:
        if operation.operation_type == "compra":
            quantity += operation.quantity
            cost_basis += (
                operation.quantity * operation.unit_price_centavos
                + operation.costs_centavos
            )
            continue

        if operation.quantity > quantity:
            raise InsufficientInvestmentQuantityError(
                f"A venda de {operation.symbol} excede a quantidade disponível."
            )
        average_cost = cost_basis / quantity
        sale_proceeds = (
            operation.quantity * operation.unit_price_centavos
            - operation.costs_centavos
        )
        consumed_basis = average_cost * operation.quantity
        realized_result += sale_proceeds - consumed_basis
        quantity -= operation.quantity
        cost_basis -= consumed_basis
        if quantity == 0:
            cost_basis = Decimal("0")

    average_unit_cost = cost_basis / quantity if quantity else None
    cost_basis_centavos = _round_centavos(cost_basis)
    realized_result_centavos = _round_centavos(realized_result)
    market_value_centavos = (
        _round_centavos(quantity * market_price_centavos)
        if market_price_centavos is not None
        else None
    )
    unrealized_result_centavos = (
        market_value_centavos - cost_basis_centavos
        if market_value_centavos is not None
        else None
    )
    return InvestmentPosition(
        symbol=normalized_symbol,
        quantity=quantity,
        average_unit_cost_centavos=average_unit_cost,
        cost_basis_centavos=cost_basis_centavos,
        realized_result_centavos=realized_result_centavos,
        market_value_centavos=market_value_centavos,
        unrealized_result_centavos=unrealized_result_centavos,
    )


def validate_operation_mutation(
    operations: list[InvestmentOperation] | tuple[InvestmentOperation, ...],
    candidate: InvestmentOperation | None = None,
    excluded_operation_id: int | None = None,
) -> None:
    if excluded_operation_id is not None and not any(
        operation.operation_id == excluded_operation_id
        for operation in operations
    ):
        raise ValueError("A operação a alterar não foi encontrada.")

    grouped: dict[str, list[InvestmentOperation]] = {}
    for operation in operations:
        if operation.operation_id == excluded_operation_id:
            continue
        grouped.setdefault(operation.symbol, []).append(operation)
    if candidate is not None:
        grouped.setdefault(candidate.symbol, []).append(candidate)

    for symbol, history in grouped.items():
        calculate_position(symbol, history)
