import json
import os
import re
from dataclasses import dataclass
from datetime import date, timedelta
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


def parse_expense_command(
    text: str,
    categories: list[dict],
    accounts: list[dict],
) -> ParsedExpense | None:
    normalized = " ".join(text.casefold().split())
    if normalized.startswith(("quanto ", "qual ", "como ", "onde ")):
        return None
    tipo = _transaction_type(normalized)
    if tipo is None:
        return None

    amount_match = re.search(
        r"(?:r\$\s*)?(\d+(?:[.,]\d{3})*(?:[.,]\d{1,2})?)"
        r"\s*(milh(?:ão|oes)|mil|reais?|rs?)?\b",
        normalized,
    )
    if not amount_match:
        raise ExpenseCommandError(
            "Informe o valor da despesa, por exemplo: 'gastei R$ 25,90 em transporte'."
        )
    try:
        amount = _parse_brazilian_amount(
            amount_match.group(1),
            amount_match.group(2),
        )
        value_centavos = int((amount * 100).quantize(Decimal("1")))
    except (InvalidOperation, ValueError) as error:
        raise ExpenseCommandError("O valor informado não é válido.") from error
    if value_centavos <= 0:
        raise ExpenseCommandError(        "O valor da transação deve ser maior que zero.")

    description = normalized[amount_match.end() :].strip(" .,:;-")
    description = re.sub(
        r"^(?:(?:reais?|rs?)\b\s*)?(?:em|de|com)\s*",
        "",
        description,
    ).strip(" .,:;-")
    description = re.sub(r"\b(?:hoje|ontem)\b", "", description).strip(" .,:;-")
    if not description:
        raise ExpenseCommandError("Informe uma descrição para a transação.")

    data = date.today()
    if "ontem" in normalized:
        data -= timedelta(days=1)

    categoria_id = _resolve_named_record(description, categories, "categoria")
    conta_id = _resolve_named_record(description, accounts, "conta")
    return ParsedExpense(
        description=description[:160],
        value_centavos=value_centavos,
        data=data.isoformat(),
        categoria_id=categoria_id,
        conta_id=conta_id,
        tipo=tipo,
    )


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
    matches = [
        item
        for item in records
        if str(item.get("nome", "")).strip()
        and str(item.get("nome", "")).casefold() in description
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
        if "categoria" in question or "gasto" in question or "despes" in question:
            categories = context["gastos_por_categoria"]
            if categories:
                top = categories[0]
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
            calculations.append(
                "Priorize revisar as maiores categorias de despesas antes de "
                "definir um valor fixo para poupar."
            )
            calculations.append(
                "Separe uma quantia compatível com o saldo calculado e revise "
                "o resultado no próximo mês."
            )
        projection = context["previsao"]
        if projection.get("status") == "insuficiente":
            estimates.append(str(projection["motivo"]))
        else:
            estimates.append(
                "A projeção é uma estimativa baseada em média simples de "
                f"{projection['meses_analisados']} meses; não é uma certeza."
            )
        return {
            "answer": (
                (
                    "Para economizar, comece pelas maiores categorias de "
                    "despesas e defina uma quantia sustentável para poupar. "
                    "Não executei nenhuma alteração."
                )
                if savings_question
                else (
                    "Aqui está o resumo calculado com os dados disponíveis. "
                    "Não executei nenhuma alteração."
                )
            ),
            "classification": "analise_financeira",
            "facts": facts,
            "calculations": calculations,
            "estimates": estimates,
        }
