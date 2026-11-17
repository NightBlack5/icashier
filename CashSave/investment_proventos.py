from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Mapping


_CATEGORIES = {"acao", "fii", "etf"}
_TYPES = {"dividendo", "jcp", "rendimento_fii", "outro"}
_STATUSES = {"anunciado", "pago"}
_CATEGORY_LABELS = {"acao": "Ação", "fii": "FII", "etf": "ETF"}
_TYPE_LABELS = {
    "dividendo": "Dividendo",
    "jcp": "JCP",
    "rendimento_fii": "Rendimento de FII",
    "outro": "Outro",
}


def _optional_iso_date(value: object, field: str) -> str:
    if value is None or value == "":
        return ""
    if not isinstance(value, str):
        raise ValueError(f"A data de {field} do provento é inválida.")
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as error:
        raise ValueError(f"A data de {field} do provento é inválida.") from error


def format_provento_record(record: Mapping[str, object]) -> dict[str, object]:
    symbol = record.get("ativo_codigo")
    category = record.get("ativo_categoria")
    provento_type = record.get("tipo")
    status = record.get("status")
    amount = record.get("valor_centavos")
    if not isinstance(symbol, str) or not symbol.strip():
        raise ValueError("O provento retornado não tem código de ativo válido.")
    if not isinstance(category, str) or category not in _CATEGORIES:
        raise ValueError("O provento retornado tem categoria inválida.")
    if not isinstance(provento_type, str) or provento_type not in _TYPES:
        raise ValueError("O provento retornado tem tipo inválido.")
    if not isinstance(status, str) or status not in _STATUSES:
        raise ValueError("O provento retornado tem status inválido.")
    if (
        not isinstance(amount, int)
        or isinstance(amount, bool)
        or amount <= 0
    ):
        raise ValueError("O provento retornado tem valor inválido.")

    announcement_date = _optional_iso_date(
        record.get("data_anuncio"),
        "anúncio",
    )
    payment_date = _optional_iso_date(
        record.get("data_pagamento"),
        "pagamento",
    )
    if status == "pago" and not payment_date:
        raise ValueError("Provento pago sem data de pagamento.")

    eligible_quantity = record.get("quantidade_elegivel")
    quantity_display = ""
    if eligible_quantity is not None:
        try:
            quantity = Decimal(str(eligible_quantity))
        except InvalidOperation as error:
            raise ValueError("A quantidade elegível do provento é inválida.") from error
        if not quantity.is_finite() or quantity < 0:
            raise ValueError("A quantidade elegível do provento é inválida.")
        quantity_display = format(quantity, "f")
        if "." in quantity_display:
            quantity_display = quantity_display.rstrip("0").rstrip(".")

    reference_date = payment_date or announcement_date or "Não informada"
    amount_value = Decimal(amount) / 100
    amount_display = (
        f"R$ {amount_value:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )
    return {
        "id": record.get("id"),
        "ativo_codigo": symbol.strip().upper(),
        "ativo_categoria": category,
        "tipo": provento_type,
        "status": status,
        "valor_centavos": amount,
        "quantidade_elegivel": eligible_quantity,
        "data_anuncio": announcement_date,
        "data_pagamento": payment_date,
        "observacoes": record.get("observacoes"),
        "categoria_formatada": _CATEGORY_LABELS[str(category)],
        "data_referencia": reference_date,
        "quantidade_elegivel_formatada": quantity_display,
        "status_formatado": "Pago" if status == "pago" else "Anunciado",
        "tipo_formatado": _TYPE_LABELS[str(provento_type)],
        "valor_formatado": amount_display,
    }


def total_received_proventos_centavos(
    records: list[Mapping[str, object]],
    start_date: date | None = None,
    end_date: date | None = None,
) -> int:
    if start_date is not None and end_date is not None and end_date < start_date:
        raise ValueError("O período de proventos está invertido.")

    total = 0
    for record in records:
        formatted = format_provento_record(record)
        if formatted["status"] != "pago":
            continue
        payment_date = date.fromisoformat(str(formatted["data_pagamento"]))
        if start_date is not None and payment_date < start_date:
            continue
        if end_date is not None and payment_date > end_date:
            continue
        total += int(formatted["valor_centavos"])
    return total
