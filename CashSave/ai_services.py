import json
import os
import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen


class OllamaError(Exception):
    """Base error for local Ollama integration."""


class OllamaUnavailableError(OllamaError):
    """Raised when the local Ollama service cannot be reached."""


class OllamaResponseError(OllamaError):
    """Raised when Ollama returns an invalid response."""


class ExpenseCommandError(OllamaError):
    """Raised when a natural-language expense command is incomplete."""


@dataclass(frozen=True)
class ParsedExpense:
    description: str
    value_centavos: int
    data: str
    categoria_id: int | None = None
    conta_id: int | None = None
    tipo: str = "despesa"


@dataclass(frozen=True)
class ParsedPayableBill:
    description: str
    value_centavos: int | None
    data_vencimento: str | None
    categoria_id: int | None = None
    conta_id: int | None = None


_MONEY_PATTERN = re.compile(
    r"(?:r\$\s*)?(\d+(?:[.,]\d{3})*(?:[.,]\d{1,2})?)"
    r"\s*(milh(?:ão|oes)|mil|reais?|rs?)?\b",
    re.IGNORECASE,
)
_PAYABLE_INTENT_PATTERN = re.compile(
    r"\b(?:conta\s+(?:a|para)\s+pagar|contas\s+(?:a|para)\s+pagar|"
    r"boleto\s+(?:a|para)\s+pagar|conta\s+pendente|"
    r"tenho\s+(?:uma\s+)?conta\b|"
    r"(?:cadastre|cadastrar|registre|registrar|crie|criar|"
    r"adicione|adicionar)\s+(?:uma\s+)?(?:conta|boleto|fatura))\b",
    re.IGNORECASE,
)
_EXPLICIT_BILL_ACTION_PATTERN = re.compile(
    r"\b(?:apague|exclua|delete|remova|pague|quitei|quite)\b"
    r"(?:(?!\b(?:conta|boleto|fatura)\b).){0,45}"
    r"\b(?:conta|boleto|fatura)\b",
    re.IGNORECASE,
)
_BILL_NOUN_PATTERN = re.compile(r"\b(?:conta|boleto|fatura)\b", re.IGNORECASE)
_BILL_LEAD_PATTERN = re.compile(
    r"^\s*(?:(?:eu\s+)?(?:tenho|tem|há|existe)\s+)?"
    r"(?:(?:uma|um|a|o)\s+)?",
    re.IGNORECASE,
)
_BILL_PAYMENT_WORDING = re.compile(
    r"\b(?:a\s+pagar|para\s+pagar|pendente|apagar)\b",
    re.IGNORECASE,
)
_BR_DATE_PATTERN = re.compile(
    r"\b(?P<day>\d{1,2})[/-](?P<month>\d{1,2})"
    r"(?:[/-](?P<year>20\d{2}))?\b"
)
_ISO_DATE_PATTERN = re.compile(
    r"\b(?P<year>20\d{2})-(?P<month>\d{1,2})-(?P<day>\d{1,2})\b"
)
_DAY_DATE_PATTERN = re.compile(
    r"\b(?:vence(?:mento)?\s+(?:no\s+)?|dia\s+)(?:dia\s+)?"
    r"(?P<day>\d{1,2})\b"
)
_TRANSACTION_MARKERS = (
    (
        "receita",
        re.compile(
            r"\b(?:recebi|recebo|receber|ganhei|ganho|faturei|"
            r"sal[aá]rio|renda|receita|entrada|entrou|caiu)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "despesa",
        re.compile(
            r"\b(?:gastei|gasto|gastando|paguei|pago|pagar|pagando|"
            r"comprei|compra|despesa|despesas|lancei|lan[çc]ar|"
            r"registre|registrei|cadastre|cadastrei|adicione|adicionei)\b",
            re.IGNORECASE,
        ),
    ),
)
_TRANSACTION_VERB_PATTERN = re.compile(
    r"\b(?:recebi|recebo|receber|ganhei|ganho|faturei|gastei|gasto|"
    r"gastando|paguei|pago|pagar|pagando|comprei|lancei|lan[çc]ar|"
    r"registre|registrei|cadastre|cadastrei|adicione|adicionei)\b",
    re.IGNORECASE,
)
_WRITE_INTENT_PATTERN = re.compile(
    r"\b(?:cadastre|cadastrar|registre|registrar|lance|lançar|lancar|"
    r"adicione|adicionar|crie|criar)\b",
    re.IGNORECASE,
)
_QUESTION_START_PATTERN = re.compile(
    r"^\s*(?:quanto|qual|como|onde|por que|porque|quando)\b",
    re.IGNORECASE,
)
_FOLLOWUP_QUESTION_PATTERN = re.compile(
    r"\b(?:quanto sobrou|quanto restou|qual foi|quanto foi|"
    r"qual categoria|qual foi meu gasto)\b",
    re.IGNORECASE,
)


def parse_payable_bill(
    text: str,
    categories: list[dict],
    accounts: list[dict],
) -> ParsedPayableBill | None:
    normalized = " ".join(text.casefold().split())
    intent_match = _PAYABLE_INTENT_PATTERN.search(normalized)
    if not intent_match:
        return None

    explicit_action = _EXPLICIT_BILL_ACTION_PATTERN.search(normalized)
    colloquial_create = (
        re.search(r"\btenho\s+(?:uma\s+)?conta\b", normalized)
        and re.search(r"\bapagar\s+(?:a\s+)?conta\b", normalized)
    )
    if explicit_action and not colloquial_create:
        return None

    due_date, date_spans = _parse_bill_due_date(normalized)
    amount_text = normalized
    for start, end in reversed(date_spans):
        amount_text = amount_text[:start] + (" " * (end - start)) + amount_text[end:]
    amount_match = _MONEY_PATTERN.search(amount_text)
    value_centavos = None
    if amount_match:
        try:
            amount = _parse_brazilian_amount(
                amount_match.group(1),
                amount_match.group(2).casefold() if amount_match.group(2) else None,
            )
            value_centavos = int((amount * 100).quantize(Decimal("1")))
        except (InvalidOperation, ValueError) as error:
            raise ExpenseCommandError("O valor da conta não é válido.") from error
        if value_centavos <= 0:
            raise ExpenseCommandError(
                "O valor da conta precisa ser maior que zero."
            )

    noun_matches = list(_BILL_NOUN_PATTERN.finditer(normalized))
    description = ""
    if noun_matches:
        last_noun = noun_matches[-1]
        description_end = amount_match.start() if amount_match else len(normalized)
        description_source = normalized[last_noun.end() : description_end]
        for start, end in reversed(date_spans):
            relative_start = max(0, start - last_noun.end())
            relative_end = max(0, end - last_noun.end())
            description_source = (
                description_source[:relative_start]
                + (" " * (relative_end - relative_start))
                + description_source[relative_end:]
            )
        description_source = _BILL_PAYMENT_WORDING.sub(" ", description_source)
        description_source = re.sub(
            r"^\s*(?:de|do|da|dos|das|para|no|na)\s+",
            "",
            description_source,
        )
        description_source = re.sub(
            r"\s+(?:de|do|da|dos|das|para|vence|vencimento)\s*$",
            "",
            description_source,
        )
        description = " ".join(description_source.strip(" .,:;-\n").split())
        if description:
            description = f"Conta de {description}"[:160]

    category_id = (
        _resolve_named_record(description, categories, "categoria")
        if description
        else None
    )
    account_id = (
        _resolve_named_record(description, accounts, "conta")
        if description
        else None
    )
    return ParsedPayableBill(
        description=description,
        value_centavos=value_centavos,
        data_vencimento=due_date,
        categoria_id=category_id,
        conta_id=account_id,
    )


def _parse_bill_due_date(text: str) -> tuple[str | None, list[tuple[int, int]]]:
    date_matches: list[tuple[re.Match, str]] = []
    for pattern, kind in (
        (_ISO_DATE_PATTERN, "iso"),
        (_BR_DATE_PATTERN, "br"),
    ):
        for match in pattern.finditer(text):
            date_matches.append((match, kind))
    if date_matches:
        match, kind = date_matches[0]
        if kind == "iso":
            year, month, day = (
                int(match.group("year")),
                int(match.group("month")),
                int(match.group("day")),
            )
        else:
            day, month = int(match.group("day")), int(match.group("month"))
            year = int(match.group("year")) if match.group("year") else date.today().year
            if not match.group("year") and date(year, month, day) < date.today():
                year += 1
        try:
            parsed_date = date(year, month, day)
        except ValueError as error:
            raise ExpenseCommandError("A data de vencimento não é válida.") from error
        return parsed_date.isoformat(), [(match.start(), match.end())]

    day_match = _DAY_DATE_PATTERN.search(text)
    if day_match:
        day = int(day_match.group("day"))
        today = date.today()
        try:
            year, month = today.year, today.month
            if day < today.day:
                month += 1
                if month > 12:
                    month = 1
                    year += 1
            parsed_date = date(year, month, day)
        except ValueError as error:
            raise ExpenseCommandError("O dia de vencimento não é válido.") from error
        return parsed_date.isoformat(), [(day_match.start(), day_match.end())]

    if re.search(r"\b(?:amanh[ãa]|tomorrow)\b", text):
        return (date.today() + timedelta(days=1)).isoformat(), []
    if re.search(r"\bhoje\b", text):
        return date.today().isoformat(), []
    return None, []


def complete_payable_bill(
    bill: ParsedPayableBill,
    text: str,
    categories: list[dict],
    accounts: list[dict],
) -> ParsedPayableBill:
    normalized = text.casefold()
    due_date, date_spans = _parse_bill_due_date(normalized)
    value_centavos = bill.value_centavos
    description = bill.description

    amount_text = normalized
    for start, end in reversed(date_spans):
        amount_text = amount_text[:start] + (" " * (end - start)) + amount_text[end:]
    amount_match = _MONEY_PATTERN.search(amount_text)
    if value_centavos is None and amount_match:
        amount = _parse_brazilian_amount(
            amount_match.group(1),
            amount_match.group(2).casefold() if amount_match.group(2) else None,
        )
        value_centavos = int((amount * 100).quantize(Decimal("1")))
        if value_centavos <= 0:
            raise ExpenseCommandError(
                "O valor da conta precisa ser maior que zero."
            )

    if not description:
        follow_up = normalized
        for start, end in reversed(date_spans):
            follow_up = (
                follow_up[:start]
                + (" " * (end - start))
                + follow_up[end:]
            )
        follow_up = re.sub(
            r"\b(?:vencimento|vence|para|no dia|dia|hoje|amanh[ãa])\b",
            " ",
            follow_up,
        )
        if amount_match:
            follow_up = (
                follow_up[: amount_match.start()]
                + follow_up[amount_match.end() :]
            )
        follow_up = re.sub(
            r"^\s*conta\s+(?:de|do|da|dos|das)\s+",
            "",
            follow_up,
        )
        follow_up = re.sub(r"^\s*(?:de|do|da|dos|das)\s+", "", follow_up)
        description = " ".join(follow_up.strip(" .,:;-\n").split())
        if description:
            description = f"Conta de {description}"[:160]

    return ParsedPayableBill(
        description=description,
        value_centavos=value_centavos,
        data_vencimento=due_date or bill.data_vencimento,
        categoria_id=(
            _resolve_named_record(description, categories, "categoria")
            if description
            else bill.categoria_id
        ),
        conta_id=(
            _resolve_named_record(description, accounts, "conta")
            if description
            else bill.conta_id
        ),
    )


def parse_transaction_batch(
    text: str,
    categories: list[dict],
    accounts: list[dict],
) -> list[ParsedExpense] | None:
    normalized = " ".join(text.casefold().split()).split("?", maxsplit=1)[0]
    if _QUESTION_START_PATTERN.search(normalized):
        return None
    followup_question = _FOLLOWUP_QUESTION_PATTERN.search(normalized)
    if followup_question:
        normalized = normalized[: followup_question.start()].rstrip(" ,.;:")
    markers = sorted(
        (
            (match.start(), match.end(), transaction_type)
            for transaction_type, pattern in _TRANSACTION_MARKERS
            for match in pattern.finditer(normalized)
        ),
        key=lambda marker: marker[0],
    )
    if not markers:
        return None

    amounts = list(_MONEY_PATTERN.finditer(normalized))
    amounts = [
        amount
        for amount in amounts
        if not re.search(
            r"\bdia\s*$",
            normalized[max(0, amount.start() - 8) : amount.start()],
        )
    ]
    if not amounts:
        if _WRITE_INTENT_PATTERN.search(normalized):
            raise ExpenseCommandError(
                "Informe o valor da transação, por exemplo: "
                "'gastei R$ 25,90 em transporte'."
            )
        return None

    transactions = []
    previous_amount_end = 0
    for amount_index, amount_match in enumerate(amounts):
        applicable_markers = [
            marker for marker in markers if marker[1] <= amount_match.start()
        ]
        if not applicable_markers:
            previous_amount_end = amount_match.end()
            continue
        marker_start, marker_end, transaction_type = applicable_markers[-1]
        next_amount_start = (
            amounts[amount_index + 1].start()
            if amount_index + 1 < len(amounts)
            else len(normalized)
        )
        next_action = _TRANSACTION_VERB_PATTERN.search(
            normalized,
            amount_match.end(),
            next_amount_start,
        )
        description_end = next_action.start() if next_action else next_amount_start
        suffix_description = _clean_transaction_description(
            normalized[amount_match.end() : description_end]
        )
        prefix_start = max(marker_end, previous_amount_end)
        prefix_description = _clean_transaction_description(
            normalized[prefix_start : amount_match.start()]
        )
        description = suffix_description or prefix_description
        previous_amount_end = amount_match.end()
        if not description:
            raise ExpenseCommandError(
                "Informe uma descrição para cada lançamento financeiro."
            )

        try:
            amount = _parse_brazilian_amount(
                amount_match.group(1),
                amount_match.group(2).casefold() if amount_match.group(2) else None,
            )
            value_centavos = int((amount * 100).quantize(Decimal("1")))
        except (InvalidOperation, ValueError) as error:
            raise ExpenseCommandError("O valor informado não é válido.") from error
        if value_centavos <= 0:
            raise ExpenseCommandError(
                "O valor de cada transação deve ser maior que zero."
            )

        transaction_context_start = normalized.rfind(".", 0, marker_start) + 1
        transaction_context = normalized[
            transaction_context_start : description_end
        ]
        transaction_date = date.today()
        if "ontem" in transaction_context:
            transaction_date -= timedelta(days=1)
        transactions.append(
            ParsedExpense(
                description=description[:160],
                value_centavos=value_centavos,
                data=transaction_date.isoformat(),
                categoria_id=_resolve_named_record(
                    description,
                    categories,
                    "categoria",
                ),
                conta_id=_resolve_named_record(description, accounts, "conta"),
                tipo=transaction_type,
            )
        )

    if not transactions:
        if _WRITE_INTENT_PATTERN.search(normalized):
            raise ExpenseCommandError(
                "Não encontrei um valor associado a um lançamento financeiro."
            )
        return None
    return transactions


def parse_expense_command(
    text: str,
    categories: list[dict],
    accounts: list[dict],
) -> ParsedExpense | None:
    transactions = parse_transaction_batch(text, categories, accounts)
    if not transactions:
        return None
    if len(transactions) > 1:
        raise ExpenseCommandError(
            "A mensagem contém vários lançamentos; use o parser de lote."
        )
    return transactions[0]


def _clean_transaction_description(text: str) -> str:
    description = text.strip(" .,:;-\n")
    description = re.sub(
        r"^(?:(?:e|de|do|da|dos|das|com|em|no|na|nos|nas|"
        r"reais?|rs?)\b\s*)+",
        "",
        description,
    )
    description = re.sub(
        r"\b(?:este mês|neste mês|esse mês|hoje|ontem)\b",
        "",
        description,
    )
    description = re.sub(r"^(?:meu|minha|meus|minhas)\s+", "", description)
    description = re.sub(r"\s+(?:e|,)\s*$", "", description)
    return description.strip(" .,:;-\n")


def _transaction_type(normalized: str) -> str | None:
    if any(
        phrase in normalized
        for phrase in (
            "receita",
            "recebi",
            "receber",
            "salário",
            "salario",
            "ganhei",
            "renda",
            "entrada",
        )
    ):
        return "receita"
    if any(
        phrase in normalized
        for phrase in (
            "cadastre",
            "cadastrar",
            "registre",
            "registrar",
            "lance",
            "lançar",
            "lancar",
            "gastei",
            "despesa de",
            "despesa no valor",
        )
    ):
        return "despesa"
    return None


def _parse_brazilian_amount(value: str, scale: str | None) -> Decimal:
    normalized = value
    if "," in normalized and "." in normalized:
        normalized = normalized.replace(".", "").replace(",", ".")
    elif "," in normalized:
        normalized = normalized.replace(",", ".")
    elif normalized.count(".") > 1:
        normalized = normalized.replace(".", "")
    elif "." in normalized and len(normalized.rsplit(".", 1)[1]) == 3:
        normalized = normalized.replace(".", "")
    amount = Decimal(normalized)
    if scale in {"mil", "milhão", "milhoes"}:
        amount *= 1_000 if scale == "mil" else 1_000_000
    return amount


def _resolve_named_record(
    description: str,
    records: list[dict],
    label: str,
) -> int | None:
    normalized_description = description.casefold()
    matches = [
        item
        for item in records
        if str(item.get("nome", "")).strip()
        and str(item.get("nome", "")).casefold() in normalized_description
    ]
    if len(matches) > 1:
        raise ExpenseCommandError(
            f"Informe apenas uma {label}; encontrei mais de uma opção."
        )
    if not matches:
        return None
    try:
        return int(matches[0]["id"])
    except (KeyError, TypeError, ValueError) as error:
        raise ExpenseCommandError(f"A {label} encontrada não possui ID válido.") from error


@dataclass(frozen=True)
class OllamaSettings:
    base_url: str = "http://127.0.0.1:11434"
    model: str = "llama3.2:3b"
    timeout_seconds: float = 20.0
    max_question_chars: int = 1200
    max_context_chars: int = 12000
    max_history_messages: int = 8
    max_response_chars: int = 4000
    max_tokens: int = 700

    @classmethod
    def from_env(cls) -> "OllamaSettings":
        settings = cls(
            base_url=os.getenv("CASHSAVE_OLLAMA_BASE_URL", cls.base_url).rstrip("/"),
            model=os.getenv("CASHSAVE_OLLAMA_MODEL", cls.model).strip(),
            timeout_seconds=_positive_float(
                os.getenv("CASHSAVE_OLLAMA_TIMEOUT", str(cls.timeout_seconds)),
                cls.timeout_seconds,
            ),
            max_question_chars=_positive_int(
                os.getenv("CASHSAVE_OLLAMA_MAX_QUESTION_CHARS", str(cls.max_question_chars)),
                cls.max_question_chars,
            ),
            max_context_chars=_positive_int(
                os.getenv("CASHSAVE_OLLAMA_MAX_CONTEXT_CHARS", str(cls.max_context_chars)),
                cls.max_context_chars,
            ),
            max_history_messages=_positive_int(
                os.getenv("CASHSAVE_OLLAMA_MAX_HISTORY", str(cls.max_history_messages)),
                cls.max_history_messages,
            ),
            max_response_chars=_positive_int(
                os.getenv("CASHSAVE_OLLAMA_MAX_RESPONSE_CHARS", str(cls.max_response_chars)),
                cls.max_response_chars,
            ),
            max_tokens=_positive_int(
                os.getenv("CASHSAVE_OLLAMA_MAX_TOKENS", str(cls.max_tokens)),
                cls.max_tokens,
            ),
        )
        _validate_local_url(settings.base_url)
        if not settings.model:
            raise OllamaError("Configure CASHSAVE_OLLAMA_MODEL com um modelo local.")
        return settings


def _positive_int(value: str, fallback: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return fallback
    return parsed if parsed > 0 else fallback


def _positive_float(value: str, fallback: float) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return fallback
    return parsed if parsed > 0 else fallback


def _validate_local_url(base_url: str) -> None:
    parsed = urlsplit(base_url)
    if parsed.scheme not in {"http", "https"} or parsed.hostname not in {
        "localhost",
        "127.0.0.1",
        "::1",
    }:
        raise OllamaError(
            "Ollama deve estar acessível somente por localhost ou 127.0.0.1."
        )


class OllamaClient:
    def __init__(
        self,
        settings: OllamaSettings | None = None,
        opener=urlopen,
    ):
        self.settings = settings or OllamaSettings.from_env()
        _validate_local_url(self.settings.base_url)
        self._opener = opener

    def chat(self, messages: list[dict[str, str]]) -> str:
        if not messages:
            raise OllamaResponseError("A conversa local não possui mensagens.")
        payload = {
            "model": self.settings.model,
            "messages": messages[-self.settings.max_history_messages :],
            "stream": False,
            "format": RESPONSE_SCHEMA,
            "options": {"num_predict": self.settings.max_tokens},
        }
        request = Request(
            urljoin(f"{self.settings.base_url}/", "api/chat"),
            data=json.dumps(payload).encode("utf-8"),
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with self._opener(request, timeout=self.settings.timeout_seconds) as response:
                raw = response.read()
        except (HTTPError, TimeoutError, URLError, OSError) as error:
            raise OllamaUnavailableError(
                "Ollama local está indisponível. Inicie o serviço e tente novamente."
            ) from error
        try:
            decoded = json.loads(raw.decode("utf-8"))
            content = decoded["message"]["content"]
        except (UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError) as error:
            raise OllamaResponseError(
                "Ollama retornou uma resposta inválida."
            ) from error
        if not isinstance(content, str) or not content.strip():
            raise OllamaResponseError("Ollama não retornou conteúdo.")
        return content[: self.settings.max_response_chars]


RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["answer", "classification", "facts", "calculations", "estimates"],
    "properties": {
        "answer": {"type": "string"},
        "classification": {"type": "string"},
        "facts": {"type": "array", "items": {"type": "string"}},
        "calculations": {"type": "array", "items": {"type": "string"}},
        "estimates": {"type": "array", "items": {"type": "string"}},
    },
}


def validate_ai_response(content: str, max_chars: int = 4000) -> dict[str, object]:
    try:
        response = json.loads(content)
    except (TypeError, json.JSONDecodeError) as error:
        raise OllamaResponseError("A resposta da IA não está em JSON válido.") from error
    if not isinstance(response, dict):
        raise OllamaResponseError("A resposta da IA deve ser um objeto JSON.")
    required = ("answer", "classification", "facts", "calculations", "estimates")
    if any(key not in response for key in required):
        raise OllamaResponseError("A resposta da IA não segue o formato esperado.")
    if not isinstance(response["answer"], str) or not response["answer"].strip():
        raise OllamaResponseError("A resposta da IA não contém uma explicação.")
    if len(response["answer"]) > max_chars:
        response["answer"] = response["answer"][:max_chars].rstrip()
    for key in ("classification",):
        if not isinstance(response[key], str):
            raise OllamaResponseError("A classificação da resposta é inválida.")
    for key in ("facts", "calculations", "estimates"):
        if not isinstance(response[key], list) or not all(
            isinstance(item, str) for item in response[key]
        ):
            raise OllamaResponseError(f"O campo {key} da resposta é inválido.")
    return response


class FinancialCalculator:
    @staticmethod
    def totals(transactions: list[dict]) -> dict[str, int]:
        totals = {"receita": 0, "despesa": 0}
        for transaction in transactions:
            kind = transaction.get("tipo")
            if kind in totals:
                totals[kind] += _cents(transaction.get("valor_centavos"))
        totals["saldo"] = totals["receita"] - totals["despesa"]
        return totals

    @staticmethod
    def monthly_totals(transactions: list[dict]) -> dict[str, dict[str, int]]:
        result: dict[str, dict[str, int]] = {}
        for transaction in transactions:
            month = str(transaction.get("data", ""))[:7]
            kind = transaction.get("tipo")
            if len(month) != 7 or kind not in {"receita", "despesa"}:
                continue
            bucket = result.setdefault(month, {"receita": 0, "despesa": 0})
            bucket[kind] += _cents(transaction.get("valor_centavos"))
        return result

    @staticmethod
    def category_expenses(
        transactions: list[dict],
        categories: list[dict],
    ) -> list[dict[str, object]]:
        names = {str(item.get("id")): item.get("nome", "Sem categoria") for item in categories}
        totals: dict[str, int] = {}
        for transaction in transactions:
            if transaction.get("tipo") != "despesa":
                continue
            category = str(transaction.get("categoria_id", ""))
            name = str(names.get(category) or "Sem categoria")
            totals[name] = totals.get(name, 0) + _cents(transaction.get("valor_centavos"))
        return [
            {"categoria": name, "valor_centavos": value}
            for name, value in sorted(totals.items(), key=lambda item: item[1], reverse=True)
        ]

    @staticmethod
    def budgets(
        budgets: list[dict],
        transactions: list[dict],
        categories: list[dict],
    ) -> list[dict[str, object]]:
        category_expenses = FinancialCalculator.category_expenses(transactions, categories)
        expenses_by_category = {
            item["categoria"]: int(item["valor_centavos"]) for item in category_expenses
        }
        total_expenses = sum(
            _cents(item.get("valor_centavos"))
            for item in transactions
            if item.get("tipo") == "despesa"
        )
        result = []
        for budget in budgets:
            limit = _cents(budget.get("limite_centavos"))
            category_id = budget.get("categoria_id")
            category = next(
                (item for item in categories if str(item.get("id")) == str(category_id)),
                None,
            )
            spent = expenses_by_category.get(
                str(category.get("nome")) if category else "Sem categoria",
                total_expenses if category is None else 0,
            )
            result.append(
                {
                    "nome": str(budget.get("nome") or "Orçamento"),
                    "limite_centavos": limit,
                    "gasto_centavos": spent,
                    "desvio_centavos": spent - limit,
                }
            )
        return result

    @staticmethod
    def goals(goals: list[dict]) -> list[dict[str, object]]:
        result = []
        for goal in goals:
            target = _cents(goal.get("valor_objetivo_centavos"))
            current = _cents(goal.get("valor_atual_centavos"))
            result.append(
                {
                    "nome": str(goal.get("nome") or "Meta"),
                    "objetivo_centavos": target,
                    "atual_centavos": current,
                    "faltante_centavos": max(target - current, 0),
                    "percentual": round(current * 100 / target, 2) if target else 0,
                }
            )
        return result

    @staticmethod
    def projection(transactions: list[dict], months: int = 3) -> dict[str, object]:
        monthly = FinancialCalculator.monthly_totals(transactions)
        valid_months = sorted(monthly)[-6:]
        if len(valid_months) < 2:
            return {
                "status": "insuficiente",
                "meses_analisados": len(valid_months),
                "motivo": "São necessários pelo menos dois meses com dados.",
            }
        expenses = [monthly[month]["despesa"] for month in valid_months]
        incomes = [monthly[month]["receita"] for month in valid_months]
        average_expense = sum(expenses) // len(expenses)
        average_income = sum(incomes) // len(incomes)
        return {
            "status": "estimativa",
            "meses_analisados": len(valid_months),
            "mes_inicial": valid_months[0],
            "mes_final": valid_months[-1],
            "media_receita_centavos": average_income,
            "media_despesa_centavos": average_expense,
            "saldo_mensal_estimado_centavos": average_income - average_expense,
            "horizonte_meses": months,
            "saldo_horizonte_estimado_centavos": (average_income - average_expense) * months,
            "premissa": "média simples dos últimos meses disponíveis",
        }


def _cents(value: object) -> int:
    try:
        return int(Decimal(str(value or 0)))
    except (InvalidOperation, ValueError, TypeError):
        return 0


def _money(cents: int) -> str:
    value = Decimal(cents) / 100
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


class FinancialContextService:
    def __init__(
        self,
        transactions: list[dict],
        accounts: list[dict],
        categories: list[dict],
        bills: list[dict],
        budgets: list[dict],
        goals: list[dict],
        recurring: list[dict],
    ):
        self.transactions = transactions
        self.accounts = accounts
        self.categories = categories
        self.bills = bills
        self.budgets = budgets
        self.goals = goals
        self.recurring = recurring

    def build(self, question: str) -> dict[str, object]:
        context = {
            "data_atual": date.today().isoformat(),
            "pergunta": question,
            "totais": FinancialCalculator.totals(self.transactions),
            "gastos_por_categoria": FinancialCalculator.category_expenses(
                self.transactions, self.categories
            )[:8],
            "orcamentos": FinancialCalculator.budgets(
                self.budgets, self.transactions, self.categories
            )[:8],
            "metas": FinancialCalculator.goals(self.goals)[:8],
            "previsao": FinancialCalculator.projection(self.transactions),
            "contas": [
                {
                    "nome": str(item.get("nome") or "Conta"),
                    "saldo_inicial_centavos": _cents(item.get("saldo_inicial_centavos")),
                    "ativa": bool(item.get("ativa", True)),
                }
                for item in self.accounts[:8]
            ],
            "contas_a_pagar_pendentes": sum(
                1 for item in self.bills if item.get("status") == "pendente"
            ),
            "recorrencias": len(self.recurring),
        }
        return context


class FinancialOrchestrator:
    def __init__(
        self,
        client: OllamaClient | None = None,
        settings: OllamaSettings | None = None,
    ):
        self.settings = settings or OllamaSettings.from_env()
        self.client = client or OllamaClient(self.settings)

    def answer(
        self,
        question: str,
        history: list[dict[str, str]],
        context_service: FinancialContextService,
    ) -> dict[str, object]:
        question = question.strip()
        if not question:
            raise OllamaError("Digite uma pergunta financeira.")
        if len(question) > self.settings.max_question_chars:
            raise OllamaError(
                f"A pergunta deve ter no máximo {self.settings.max_question_chars} caracteres."
            )
        normalized_question = question.casefold()
        if any(
            phrase in normalized_question
            for phrase in (
                "cadastre",
                "cadastra",
                "registre",
                "registrar",
                "crie uma despesa",
                "criar uma despesa",
                "adicione uma despesa",
                "adicionar uma despesa",
                "lance uma despesa",
                "lançar uma despesa",
                "edite",
                "editar",
                "altere",
                "alterar",
                "apague",
                "apagar",
                "exclua",
                "excluir",
                "delete",
                "pague a conta",
            )
        ):
            return {
                "answer": (
                    "Não posso cadastrar, editar, excluir ou pagar registros. "
                    "A assistente está em modo somente leitura. Use a tela "
                    "Finanças para realizar essa operação manualmente."
                ),
                "classification": "somente_leitura",
                "facts": [],
                "calculations": [],
                "estimates": [],
            }
        context = json.dumps(
            context_service.build(question),
            ensure_ascii=False,
            separators=(",", ":"),
        )[: self.settings.max_context_chars]
        if any(
            phrase in normalized_question
            for phrase in (
                "saldo",
                "quanto gastei",
                "quanto gastei",
                "despesas",
                "gastos",
                "receitas",
                "categoria",
                "orçamento",
                "orcamento",
                "meta",
                "economizar",
                "economize",
                "poupar",
                "poupar",
                "reduzir gastos",
                "guardar dinheiro",
            )
        ):
            return self._deterministic_financial_answer(
                normalized_question,
                context_service,
            )
        messages = [
            {
                "role": "system",
                "content": (
                    "Você é um assistente financeiro educativo local. "
                    "Responda em português e use somente o CONTEXTO fornecido. "
                    "O CONTEXTO é a única fonte sobre o usuário e seus dados. "
                    "Não invente que CashSave é uma empresa, não descreva "
                    "produtos ou fatos que não estejam no contexto, não invente "
                    "valores, não diga que cadastrou, editou, apagou ou pagou "
                    "algo. Você não possui ferramentas e não pode alterar dados. "
                    "Se a pergunta exigir dados ausentes, diga que eles não "
                    "estão disponíveis. Diferencie fatos observados, cálculos "
                    "e estimativas. Retorne apenas JSON no formato solicitado."
                ),
            },
            *history[-self.settings.max_history_messages :],
            {
                "role": "user",
                "content": f"CONTEXTO={context}\nPERGUNTA={question}",
            },
        ]
        raw_response = self.client.chat(messages)
        return validate_ai_response(raw_response, self.settings.max_response_chars)

    @staticmethod
    def _deterministic_financial_answer(
        question: str,
        context_service: FinancialContextService,
    ) -> dict[str, object]:
        context = context_service.build(question)
        totals = context["totais"]
        facts = [
            f"Receitas observadas: {_money(int(totals['receita']))}.",
            f"Despesas observadas: {_money(int(totals['despesa']))}.",
        ]
        calculations = [f"Saldo calculado: {_money(int(totals['saldo']))}."]
        estimates: list[str] = []
        top_category = None
        if "categoria" in question or "gasto" in question or "despes" in question:
            categories = context["gastos_por_categoria"]
            if categories:
                top = categories[0]
                top_category = top
                facts.append(
                    "Maior categoria de despesas observada: "
                    f"{top['categoria']} ({_money(int(top['valor_centavos']))})."
                )
            else:
                facts.append("Não há despesas categorizadas disponíveis.")
        if "meta" in question:
            goals = context["metas"]
            if goals:
                for goal in goals[:3]:
                    calculations.append(
                        f"Na meta {goal['nome']}, faltam "
                        f"{_money(int(goal['faltante_centavos']))} "
                        f"({goal['percentual']}% alcançado)."
                    )
            else:
                facts.append("Não há metas financeiras disponíveis.")
        if "orçamento" in question or "orcamento" in question:
            budgets = context["orcamentos"]
            if budgets:
                for budget in budgets[:3]:
                    calculations.append(
                        f"O orçamento {budget['nome']} tem limite de "
                        f"{_money(int(budget['limite_centavos']))} e gasto "
                        f"calculado de {_money(int(budget['gasto_centavos']))}."
                    )
            else:
                facts.append("Não há orçamentos disponíveis.")
        savings_question = any(
            phrase in question
            for phrase in (
                "economizar",
                "economize",
                "poupar",
                "reduzir gasto",
                "guardar dinheiro",
            )
        )
        if savings_question:
            categories = context["gastos_por_categoria"]
            if categories:
                top = categories[0]
                top_category = top
                category_name = str(top["categoria"]).strip()
                if category_name and category_name.lower() != "sem categoria":
                    answer_bits = [
                        f"Seu maior gasto atual é {category_name} ({_money(int(top['valor_centavos']))}).",
                        "Para economizar, reduza primeiro esse item e mantenha uma reserva mensal compatível com o seu saldo atual.",
                    ]
                else:
                    answer_bits = [
                        f"Seu maior gasto atual foi de {_money(int(top['valor_centavos']))}.",
                        "Para economizar, reduza primeiro esse valor e mantenha uma reserva mensal compatível com o seu saldo atual.",
                    ]
            else:
                answer_bits = [
                    "Para economizar, comece revisando suas maiores despesas e definindo uma quantia sustentável para poupar.",
                ]
            saldo = int(totals["saldo"])
            if saldo < 0:
                answer_bits.append(
                    f"O saldo atual está negativo em {_money(abs(saldo))}, então a prioridade é cortar gastos variáveis antes de aumentar a poupança."
                )
            else:
                answer_bits.append(
                    f"Seu saldo atual é {_money(saldo)}, então você pode separar uma parte dessa margem para poupança sem comprometer o mês."
                )
            answer_bits.append("Não realizei nenhuma alteração.")
            answer = " ".join(answer_bits)
            calculations.append(
                "Priorize revisar as maiores categorias de despesas antes de definir um valor fixo para poupar."
            )
            calculations.append(
                "Separe uma quantia compatível com o saldo calculado e revise o resultado no próximo mês."
            )
        else:
            answer = "Aqui está o resumo calculado com os dados disponíveis. Não realizei nenhuma alteração."
        projection = context["previsao"]
        if projection.get("status") == "insuficiente":
            estimates.append(str(projection["motivo"]))
        else:
            estimates.append(
                "A projeção é uma estimativa baseada em média simples de "
                f"{projection['meses_analisados']} meses; não é uma certeza."
            )
        return {
            "answer": answer,
            "classification": "analise_financeira",
            "facts": facts,
            "calculations": calculations,
            "estimates": estimates,
        }
