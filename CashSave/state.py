import asyncio
import calendar
import csv
import io
import json
import mimetypes
import os
import re
import secrets
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from urllib.parse import quote, urlsplit
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import reflex as rx
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from .ai_services import (
    ExpenseCommandError,
    FinancialContextService,
    FinancialOrchestrator,
    OllamaError,
    complete_payable_bill,
    parse_payable_bill,
    parse_transaction_batch,
)
from .expense_reports import (
    expense_report_data,
    generate_expense_pdf,
    is_expense_pdf_request,
)
from .market_data import (
    MarketAsset,
    MarketDataError,
    MarketDataNotConfigured,
    MarketMover,
    market_data_service,
)
from .investment_portfolio import (
    InvestmentOperation,
    calculate_position,
    validate_operation_mutation,
)
from .investment_analytics import (
    assert_investment_record_owner,
    calculate_portfolio_snapshot,
    monthly_investment_flows,
)
from .investment_comparison import compare_price_histories
from .investment_proventos import (
    format_provento_record,
    total_received_proventos_centavos,
)

API_BASE_URL = os.getenv("CASH_SAVE_API_URL", "").rstrip("/")


class XanoAPIError(Exception):
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


def _send_request(
    method: str,
    path: str,
    payload: dict | None,
    token: str = "",
    upload: tuple[str, str, bytes] | None = None,
) -> object:
    if not API_BASE_URL:
        raise XanoAPIError(
            "Configure CASH_SAVE_API_URL no arquivo .env para conectar ao Xano."
        )
    parsed_url = urlsplit(API_BASE_URL)
    if not parsed_url.hostname or (
        parsed_url.scheme != "https"
        and parsed_url.hostname not in {"localhost", "127.0.0.1"}
    ):
        raise XanoAPIError(
            "CASH_SAVE_API_URL deve usar HTTPS e apontar para o grupo de APIs do Xano."
        )

    content_type = "application/json"
    if upload is not None:
        field_name, filename, file_data = upload
        boundary = secrets.token_hex(16)
        safe_filename = os.path.basename(filename).replace('"', "")
        media_type = mimetypes.guess_type(safe_filename)[0] or "application/octet-stream"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="{field_name}"; '
            f'filename="{safe_filename}"\r\n'
            f"Content-Type: {media_type}\r\n\r\n"
        ).encode("utf-8") + file_data + f"\r\n--{boundary}--\r\n".encode("utf-8")
        content_type = f"multipart/form-data; boundary={boundary}"
    else:
        body = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Accept": "application/json"}
    if body is not None:
        headers["Content-Type"] = content_type
    if token:
        headers["Authorization"] = "Bearer " + token

    request = Request(
        f"{API_BASE_URL}/{path.lstrip('/')}",
        data=body,
        headers=headers,
        method=method,
    )

    try:
        with urlopen(request, timeout=20) as response:
            raw = response.read()
    except HTTPError as error:
        try:
            detail = json.loads(error.read().decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            detail = {}
        message = _api_error_message(
            detail,
            f"Xano respondeu com HTTP {error.code}.",
        )
        raise XanoAPIError(message, status_code=error.code) from error
    except (TimeoutError, URLError) as error:
        raise XanoAPIError(
            "Não foi possível conectar ao Xano. Verifique a URL e sua conexão."
        ) from error

    if not raw:
        return None
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise XanoAPIError("O Xano retornou uma resposta inválida.") from error


def _records(response: object) -> list[dict]:
    if isinstance(response, list):
        return [item for item in response if isinstance(item, dict)]
    if isinstance(response, dict):
        items = response.get("items", response.get("records", []))
        if isinstance(items, list):
            return [item for item in items if isinstance(item, dict)]
    return []


def _as_record(response: object) -> dict:
    return response if isinstance(response, dict) else {}


def _api_error_message(detail: object, fallback: str) -> str:
    if isinstance(detail, str) and detail.strip():
        return detail.strip()
    if isinstance(detail, dict):
        message = detail.get("message")
        if isinstance(message, str) and message.strip():
            return message.strip()
        for key in ("error", "response", "data"):
            message = _api_error_message(detail.get(key), "")
            if message:
                return message
    return fallback


def _message_text(content: object) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, dict):
        text = content.get("text", content.get("content"))
        return _message_text(text) if text is not None else ""
    if isinstance(content, list):
        return "".join(_message_text(item) for item in content)
    return ""


def _formatar_centavos(centavos: int) -> str:
    valor = Decimal(centavos) / 100
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _formatar_horario_mercado(reference_at: datetime) -> str:
    horario_brasilia = reference_at.astimezone(
        timezone(timedelta(hours=-3), "BRT")
    )
    return horario_brasilia.strftime("%d/%m/%Y %H:%M BRT")


def _formatar_movimentacao_mercado(
    mover: MarketMover,
) -> dict[str, str | float]:
    price_centavos = int(
        (mover.price * 100).quantize(
            Decimal("1"),
            rounding=ROUND_HALF_UP,
        )
    )
    variation = float(mover.daily_change_percent)
    return {
        "symbol": mover.symbol,
        "name": mover.name,
        "price": _formatar_centavos(price_centavos),
        "variation": variation,
        "variation_display": f"{variation:+.2f}%".replace(".", ","),
    }


def _records_with_money(
    response: object,
    amount_key: str,
    display_key: str = "valor_formatado",
) -> list[dict]:
    return [
        {
            **item,
            display_key: _formatar_centavos(
                int(item.get(amount_key, 0) or 0)
            ),
        }
        for item in _records(response)
    ]


def _money_to_cents(value: str) -> int:
    normalized_value = value.replace("R$", "").replace(" ", "").strip()
    if "," in normalized_value:
        normalized_value = normalized_value.replace(".", "").replace(",", ".")
    try:
        amount = Decimal(normalized_value)
    except InvalidOperation as error:
        raise XanoAPIError("Informe um valor monetário válido.") from error
    if not amount.is_finite() or amount <= 0:
        raise XanoAPIError("O valor deve ser maior que zero.")
    return int(
        (amount * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    )


def _nonnegative_money_to_cents(value: str) -> int:
    normalized_value = value.replace("R$", "").replace(" ", "").strip()
    if not normalized_value:
        return 0
    if "," in normalized_value:
        normalized_value = normalized_value.replace(".", "").replace(",", ".")
    try:
        amount = Decimal(normalized_value)
    except InvalidOperation as error:
        raise XanoAPIError("Informe um custo monetário válido.") from error
    if not amount.is_finite() or amount < 0:
        raise XanoAPIError("Os custos não podem ser negativos.")
    return int(
        (amount * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    )


def _formatar_entrada_reais(value: str) -> str:
    centavos = _money_to_cents(value)
    valor = Decimal(centavos) / 100
    return (
        f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )


def _formatar_telefone(value: str) -> str:
    digits = "".join(char for char in value if char.isdigit())
    if digits.startswith("55") and len(digits) in {12, 13}:
        digits = digits[2:]
    digits = digits[:11]
    if len(digits) < 2:
        return f"({digits}" if digits else ""
    if len(digits) == 2:
        return f"({digits})"

    ddd = digits[:2]
    local = digits[2:]
    if len(digits) <= 10:
        if len(local) <= 4:
            return f"({ddd}) {local}"
        return f"({ddd}) {local[:4]}-{local[4:]}"

    if len(local) <= 5:
        return f"({ddd}) {local}"
    return f"({ddd}) {local[:5]}-{local[5:]}"


def _notificacao_ids_from_storage(value: str) -> list[str]:
    try:
        stored_ids = json.loads(value)
    except json.JSONDecodeError:
        return []
    if not isinstance(stored_ids, list):
        return []
    return [item for item in stored_ids if isinstance(item, str)]


def _proxima_data_recorrente(
    data: str,
    frequencia: str,
    dia_referencia: int | None = None,
    mes_referencia: int | None = None,
) -> str:
    try:
        data_atual = date.fromisoformat(data[:10])
    except ValueError as error:
        raise XanoAPIError("A recorrência contém uma data inválida.") from error
    if frequencia == "diaria":
        proxima = data_atual + timedelta(days=1)
    elif frequencia == "semanal":
        proxima = data_atual + timedelta(weeks=1)
    elif frequencia == "mensal":
        indice = data_atual.year * 12 + data_atual.month
        ano, mes_zero = divmod(indice, 12)
        mes = mes_zero + 1
        proxima = data_atual.replace(
            year=ano,
            month=mes,
            day=min(
                dia_referencia or data_atual.day,
                calendar.monthrange(ano, mes)[1],
            ),
        )
    elif frequencia == "anual":
        ano = data_atual.year + 1
        mes = mes_referencia or data_atual.month
        dia = dia_referencia or data_atual.day
        proxima = date(
            ano,
            mes,
            min(dia, calendar.monthrange(ano, mes)[1]),
        )
    else:
        raise XanoAPIError("A frequência da recorrência é inválida.")
    return proxima.isoformat()


def _imagem_corresponde_ao_tipo(data: bytes, media_type: str) -> bool:
    if media_type == "image/png":
        return data.startswith(b"\x89PNG\r\n\x1a\n")
    if media_type == "image/jpeg":
        return data.startswith(b"\xff\xd8\xff")
    if media_type == "image/webp":
        return (
            len(data) >= 12
            and data[:4] == b"RIFF"
            and data[8:12] == b"WEBP"
        )
    return False


def _csv_safe_text(value: object) -> str:
    text = str(value or "")
    if text.lstrip(" \t\r\n").startswith(("=", "+", "-", "@")):
        return "'" + text
    return text


def _normalizar_conversas_assistente(value: object) -> list[dict]:
    if not isinstance(value, list):
        return []
    conversas = []
    for item in value:
        if not isinstance(item, dict):
            continue
        try:
            conversation_id = int(item.get("id", 0))
        except (TypeError, ValueError):
            continue
        if conversation_id <= 0 or not isinstance(item.get("messages"), list):
            continue
        mensagens = []
        for mensagem in item["messages"]:
            if not isinstance(mensagem, dict):
                continue
            tipo = mensagem.get("tipo")
            texto = mensagem.get("texto")
            if tipo in {"usuario", "ia"} and isinstance(texto, str):
                mensagens.append({"tipo": tipo, "texto": texto})
        if mensagens:
            conversas.append(
                {
                    "id": conversation_id,
                    "title": str(item.get("title", ""))[:60],
                    "messages": mensagens[-20:],
                }
            )
    return conversas[:8]


def _conversas_assistente_do_storage(
    storage_value: str,
    owner_key: str,
) -> tuple[list[dict], int]:
    try:
        stored = json.loads(storage_value or "{}")
    except (TypeError, json.JSONDecodeError):
        return [], 0
    if not isinstance(stored, dict):
        return [], 0
    owner_data = stored.get(owner_key, {})
    if not isinstance(owner_data, dict):
        return [], 0
    conversas = _normalizar_conversas_assistente(
        owner_data.get("conversations", [])
    )
    try:
        active_id = int(owner_data.get("active_id", 0))
    except (TypeError, ValueError):
        active_id = 0
    if active_id not in {int(item["id"]) for item in conversas}:
        active_id = 0
    return conversas, active_id


class AppState(rx.State):
    auth_token: str = rx.Cookie(
        "",
        name="cashsave_auth",
        max_age=86400,
        same_site="strict",
        secure=os.getenv("CASH_SAVE_COOKIE_SECURE", "true").lower() == "true",
    )
    usuario: dict[str, object] = {}
    avatar_url: str = ""
    avatar_perfil_disponivel: bool = False
    auth_email: str = ""
    auth_email_salvo: str = rx.LocalStorage(
        "",
        name="cashsave_remembered_email",
    )
    auth_phone: str = ""
    lembrar_email: str = rx.LocalStorage(
        "true",
        name="cashsave_remember_email",
    )
    auth_password: str = ""
    auth_password_confirmation: str = ""
    auth_name: str = ""
    senha_visivel: bool = False
    senha_confirmacao_visivel: bool = False
    aceitou_termos: bool = False
    cadastro: bool = False
    erro: str = ""
    aviso: str = ""
    carregando: bool = False
    transacoes: list[dict] = []
    contas: list[dict] = []
    categorias: list[dict] = []
    contas_a_pagar: list[dict] = []
    orcamentos: list[dict] = []
    metas: list[dict] = []
    preferencias: dict = {}
    tipo_transacao: str = "despesa"
    transacao_descricao: str = ""
    transacao_valor: str = ""
    transacao_data: str = date.today().isoformat()
    transacao_categoria: str = ""
    transacao_conta: str = ""
    nova_categoria_nome: str = ""
    nova_categoria_tipo: str = "despesa"
    nova_conta_nome: str = ""
    nova_conta_tipo: str = "conta_corrente"
    nova_conta_saldo: str = "0"
    nova_conta_instituicao: str = ""
    conta_descricao: str = ""
    conta_valor: str = ""
    conta_vencimento: str = ""
    conta_categoria: str = ""
    orcamento_nome: str = ""
    orcamento_limite: str = ""
    orcamento_inicio: str = ""
    orcamento_fim: str = ""
    orcamento_categoria: str = ""
    meta_nome: str = ""
    meta_objetivo: str = ""
    meta_data_alvo: str = ""
    meta_contribuicao: str = ""
    recorrencias: list[dict] = []
    recorrencia_descricao: str = ""
    recorrencia_valor: str = ""
    recorrencia_tipo: str = "despesa"
    recorrencia_frequencia: str = "mensal"
    recorrencia_proxima_data: str = date.today().isoformat()
    recorrencias_disponiveis: bool = False
    moeda: str = "BRL"
    localidade: str = "pt-BR"
    fuso_horario: str = "America/Sao_Paulo"
    notificacoes_vencimento: bool = True
    notificacoes_orcamento: bool = True
    notificacoes_metas: bool = True
    notificacoes_metas_disponivel: bool = False
    onboarding_storage: str = rx.LocalStorage(
        "{}",
        name="cashsave_onboarding_state",
    )
    onboarding_respostas: dict[str, object] = {}
    onboarding_etapa: int = 0
    onboarding_concluido: bool = False
    investidor_perfil: str = "Ainda não avaliado"
    investidor_descricao: str = (
        "Complete o onboarding para entender melhor o seu perfil de investidor."
    )
    investidor_pontos_atencao: str = (
        "Use a avaliação como referência de contexto para o Jarvis e as metas financeiras."
    )
    dados_carregados: bool = False
    transacao_busca: str = ""
    transacao_filtro_tipo: str = "todas"
    transacao_filtro_periodo: str = "todas"
    transacao_filtro_categoria: str = "todas"
    transacao_filtro_conta: str = "todas"
    notificacoes_descartadas: str = rx.LocalStorage(
        "[]",
        name="cashsave_dismissed_notifications",
    )
    assistente_conversas_storage: str = rx.LocalStorage(
        "{}",
        name="cashsave_jarvis_conversations",
    )
    assistente_conversas: list[dict] = []
    assistente_conversa_id: int = 0
    assistente_mensagens: list[dict[str, str]] = [
        {
            "tipo": "ia",
            "texto": (
                "Olá! Sou o Jarvis do CashSave. "
                "Como posso ajudar você a organizar suas finanças?"
            ),
        }
    ]
    assistente_mensagem: str = ""
    assistente_carregando: bool = False
    bolsa_carregando: bool = False
    bolsa_erro: str = ""
    bolsa_carteira_erro: str = ""
    bolsa_indisponivel: str = (
        "Nenhum provedor de dados de mercado aprovado está configurado."
    )
    bolsa_indicadores: list[dict[str, str]] = []
    bolsa_altas: list[dict] = []
    bolsa_baixas: list[dict] = []
    bolsa_grafico_altas: list[dict] = []
    bolsa_movers_origem: str = ""
    bolsa_movers_referencia: str = ""
    bolsa_movers_atrasado: bool = False
    bolsa_busca: str = ""
    bolsa_categoria: str = "todas"
    bolsa_ordenacao: str = "codigo"
    bolsa_ativos: list[dict[str, str]] = []
    bolsa_ativo_selecionado: str = ""
    bolsa_detalhe: dict[str, str] = {}
    bolsa_periodo: str = "1 mês"
    bolsa_historico: list[dict] = []
    bolsa_historico_mensagem: str = (
        "Selecione um período para consultar o histórico disponível."
    )
    bolsa_historico_origem: str = ""
    bolsa_operacoes: list[dict] = []
    bolsa_proventos: list[dict] = []
    bolsa_proventos_total_geral: str = "R$ 0,00"
    bolsa_proventos_total_ano: str = "R$ 0,00"
    bolsa_proventos_total_mes: str = "R$ 0,00"
    bolsa_favoritos: list[dict] = []
    bolsa_carteira: dict[str, str] = {
        "custo_investido": "R$ 0,00",
        "total_aplicado": "R$ 0,00",
        "resultado_realizado": "R$ 0,00",
        "valor_mercado": "Indisponível",
        "resultado_nao_realizado": "Indisponível",
        "rentabilidade": "Indisponível",
    }
    bolsa_carteira_posicoes: list[dict] = []
    bolsa_carteira_alocacao: list[dict] = []
    bolsa_carteira_evolucao: list[dict] = []
    bolsa_carteira_aviso: str = ""
    bolsa_comparacao_ativos: str = ""
    bolsa_comparacao_periodo: str = "1 mês"
    bolsa_comparacao_series: list[dict] = []
    bolsa_comparacao_linhas: list[dict] = []
    bolsa_comparacao_desempenho: list[dict] = []
    bolsa_comparacao_fontes: list[dict] = []
    bolsa_comparacao_aviso: str = ""
    bolsa_alertas: list[dict] = []
    bolsa_alerta_codigo: str = ""
    bolsa_alerta_categoria: str = "acao"
    bolsa_alerta_condicao: str = "preco_acima"
    bolsa_alerta_preco: str = ""
    bolsa_alerta_percentual: str = ""
    bolsa_provento_codigo: str = ""
    bolsa_provento_categoria: str = "acao"
    bolsa_provento_tipo: str = "dividendo"
    bolsa_provento_status: str = "pago"
    bolsa_provento_valor: str = ""
    bolsa_provento_quantidade: str = ""
    bolsa_provento_data_anuncio: str = ""
    bolsa_provento_data_pagamento: str = ""
    bolsa_provento_observacoes: str = ""
    bolsa_operacao_codigo: str = ""
    bolsa_operacao_categoria: str = "acao"
    bolsa_operacao_tipo: str = "compra"
    bolsa_operacao_data: str = date.today().isoformat()
    bolsa_operacao_quantidade: str = ""
    bolsa_operacao_preco: str = ""
    bolsa_operacao_custos: str = ""
    bolsa_operacao_observacoes: str = ""
    bolsa_operacao_edicao_id: int = 0

    @rx.var
    def autenticado(self) -> bool:
        return bool(self.auth_token)

    @rx.var
    def nome_usuario(self) -> str:
        nome = self.usuario.get("name")
        return nome if isinstance(nome, str) and nome else "Minha conta"

    @rx.var
    def email_usuario(self) -> str:
        email = self.usuario.get("email")
        return email if isinstance(email, str) else ""

    def _assistente_owner_key(self) -> str:
        user_id = self.usuario.get("id")
        if user_id is not None:
            return f"user:{user_id}"
        email = self.usuario.get("email") or self.auth_email
        return f"email:{str(email).strip().lower()}" if email else "default"

    def _persistir_conversas_assistente(self):
        try:
            stored = json.loads(self.assistente_conversas_storage or "{}")
        except (TypeError, json.JSONDecodeError):
            stored = {}
        if not isinstance(stored, dict):
            stored = {}
        owner_key = self._assistente_owner_key()
        stored[owner_key] = {
            "active_id": self.assistente_conversa_id,
            "conversations": _normalizar_conversas_assistente(
                self.assistente_conversas
            ),
        }
        self.assistente_conversas_storage = json.dumps(
            stored,
            ensure_ascii=False,
            separators=(",", ":"),
        )

    def _carregar_onboarding_local(self):
        try:
            payload = json.loads(self.onboarding_storage or "{}")
        except (TypeError, json.JSONDecodeError):
            payload = {}
        if not isinstance(payload, dict):
            payload = {}
        respostas = payload.get("respostas")
        if isinstance(respostas, dict):
            self.onboarding_respostas = respostas
        else:
            self.onboarding_respostas = {}
        etapa = payload.get("etapa", 0)
        try:
            self.onboarding_etapa = int(etapa)
        except (TypeError, ValueError):
            self.onboarding_etapa = 0
        if self.onboarding_etapa < 0:
            self.onboarding_etapa = 0
        if self.onboarding_etapa > 5:
            self.onboarding_etapa = 5
        self.onboarding_concluido = bool(payload.get("concluido", False))
        if self.onboarding_respostas:
            self._atualizar_perfil_investidor()

    def _salvar_onboarding_local(self):
        payload = {
            "etapa": self.onboarding_etapa,
            "concluido": self.onboarding_concluido,
            "respostas": self.onboarding_respostas,
        }
        self.onboarding_storage = json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
        )

    def _atualizar_perfil_investidor(self):
        respostas = self.onboarding_respostas or {}
        score = 0
        conhecimento = str(respostas.get("conhecimento_risco", "")).lower()
        prazo = str(respostas.get("prazo_investimento", "")).lower()
        estabilidade = str(respostas.get("estabilidade", "")).lower()
        renda_variavel = str(respostas.get("renda_variavel", "")).lower()

        if conhecimento == "baixo":
            score += 10
        elif conhecimento == "medio":
            score += 25
        elif conhecimento == "alto":
            score += 40

        if respostas.get("investiu_antes"):
            score += 12
        if respostas.get("acessa_rendimentos_periodicos"):
            score += 8
        if respostas.get("prefere_diversificacao"):
            score += 8
        if renda_variavel == "variavel":
            score += 12
        if renda_variavel == "fixo":
            score -= 6

        if prazo == "curto":
            score += 8
        elif prazo == "medio":
            score += 18
        elif prazo == "longo":
            score += 24

        if estabilidade == "estabilidade":
            score += 8
        elif estabilidade == "equilibrado":
            score += 18
        elif estabilidade == "oscilacoes":
            score += 28

        if respostas.get("tem_reserva_urgencia"):
            score += 6
        if respostas.get("objetivos"):
            score += min(len(respostas.get("objetivos", [])) * 4, 16)

        score = max(0, min(score, 100))

        if score <= 38:
            perfil = "Conservador"
            descricao = (
                "Você tende a valorizar segurança, previsibilidade e menor volatilidade. "
                "O perfil indica prioridade a preservação e objetivos de curto a médio prazo."
            )
            atencao = (
                "Mantenha reservas de emergência e prefira investimentos com baixas oscilações. "
                "Avalie sempre a liquidez antes de comprometer o patrimônio."
            )
        elif score <= 72:
            perfil = "Moderado"
            descricao = (
                "Seu contexto mostra equilíbrio entre segurança e crescimento, com alguma tolerância a oscilações. "
                "Esse perfil costuma funcionar bem com diversificação e objetivos bem definidos."
            )
            atencao = (
                "Continue diversificando e revisando o seu horizonte de investimento. "
                "Evite assumir riscos incompatíveis com a sua capacidade de absorver perdas."
            )
        else:
            perfil = "Arrojado"
            descricao = (
                "Você demonstra disposição para aceitar maior volatilidade em busca de crescimento e ganhos de longo prazo. "
                "Esse perfil pode suportar mais oscilações, mas continua exigindo atenção à disciplina."
            )
            atencao = (
                "Mesmo com maior tolerância ao risco, mantenha uma reserva de emergência e entenda muito bem os cenários de perda antes de ampliar posições."
            )

        self.investidor_perfil = perfil
        self.investidor_descricao = descricao
        self.investidor_pontos_atencao = atencao

    @rx.var
    def total_receitas(self) -> str:
        mes_atual = date.today().strftime("%Y-%m")
        total = sum(
            int(item.get("valor_centavos", 0) or 0)
            for item in self.transacoes
            if item.get("tipo") == "receita"
            and str(item.get("data", ""))[:7] == mes_atual
        )
        return self._formatar_dinheiro(total)

    @rx.var
    def total_despesas(self) -> str:
        mes_atual = date.today().strftime("%Y-%m")
        total = sum(
            int(item.get("valor_centavos", 0) or 0)
            for item in self.transacoes
            if item.get("tipo") == "despesa"
            and str(item.get("data", ""))[:7] == mes_atual
        )
        return self._formatar_dinheiro(total)

    @rx.var
    def saldo_total(self) -> str:
        mes_atual = date.today().strftime("%Y-%m")
        saldo = sum(
            int(item.get("valor_centavos", 0) or 0)
            * (1 if item.get("tipo") == "receita" else -1)
            for item in self.transacoes
            if str(item.get("data", ""))[:7] == mes_atual
        )
        return self._formatar_dinheiro(saldo)

    @rx.var
    def proximo_vencimento_total(self) -> str:
        hoje = date.today()
        limite = hoje + timedelta(days=7)
        total = sum(
            int(item.get("valor_centavos", 0) or 0)
            for item in self.contas_a_pagar
            if item.get("status") == "pendente"
            and hoje.isoformat()
            <= str(item.get("data_vencimento", ""))[:10]
            <= limite.isoformat()
        )
        return self._formatar_dinheiro(total)

    @rx.var
    def contas_proximas(self) -> list[dict]:
        hoje = date.today()
        limite = hoje + timedelta(days=7)
        return [
            item
            for item in self.contas_a_pagar
            if item.get("status") == "pendente"
            and hoje.isoformat()
            <= str(item.get("data_vencimento", ""))[:10]
            <= limite.isoformat()
        ][:5]

    @rx.var
    def transacoes_filtradas(self) -> list[dict]:
        hoje = date.today()
        limite = hoje - timedelta(days=90)
        busca = self.transacao_busca.strip().casefold()
        resultado = []
        for transacao in self.transacoes:
            if (
                self.transacao_filtro_tipo != "todas"
                and transacao.get("tipo") != self.transacao_filtro_tipo
            ):
                continue
            if self.transacao_filtro_categoria != "todas":
                categoria = next(
                    (
                        item
                        for item in self.categorias
                        if str(item.get("id"))
                        == str(transacao.get("categoria_id"))
                    ),
                    {},
                )
                if categoria.get("nome") != self.transacao_filtro_categoria:
                    continue
            if self.transacao_filtro_conta != "todas":
                conta = next(
                    (
                        item
                        for item in self.contas
                        if str(item.get("id")) == str(transacao.get("conta_id"))
                    ),
                    {},
                )
                if conta.get("nome") != self.transacao_filtro_conta:
                    continue
            data_transacao = str(transacao.get("data", ""))[:10]
            if self.transacao_filtro_periodo == "este mes":
                if data_transacao[:7] != hoje.strftime("%Y-%m"):
                    continue
            elif self.transacao_filtro_periodo == "ultimos 3 meses":
                if data_transacao < limite.isoformat():
                    continue
            if busca and busca not in str(transacao.get("descricao", "")).casefold():
                continue
            resultado.append(transacao)
        return resultado

    @rx.var
    def opcoes_filtro_categoria(self) -> list[str]:
        return [
            "todas",
            *sorted({
                str(item.get("nome", ""))
                for item in self.categorias
                if item.get("nome")
            }),
        ]

    @rx.var
    def opcoes_filtro_conta(self) -> list[str]:
        return [
            "todas",
            *sorted({
                str(item.get("nome", ""))
                for item in self.contas
                if item.get("nome")
            }),
        ]

    @rx.var
    def notificacoes_ativas(self) -> list[dict[str, str]]:
        hoje = date.today()
        limite = hoje + timedelta(days=7)
        notificacoes: list[dict[str, str]] = []
        for conta in self.contas_a_pagar:
            if not self.notificacoes_vencimento or conta.get("status") != "pendente":
                continue
            vencimento = str(conta.get("data_vencimento", ""))[:10]
            if hoje.isoformat() <= vencimento <= limite.isoformat():
                chave = (
                    f"user-{self.usuario.get('id', '')}-"
                    f"vencimento-{conta.get('id')}"
                )
                if chave not in _notificacao_ids_from_storage(
                    self.notificacoes_descartadas
                ):
                    notificacoes.append({
                        "id": chave,
                        "titulo": "Conta próxima do vencimento",
                        "mensagem": (
                            f"{conta.get('descricao', 'Conta')} vence em "
                            f"{vencimento} ({conta.get('valor_formatado', '')})."
                        ),
                    })

        if self.notificacoes_orcamento:
            hoje_iso = hoje.isoformat()
            for orcamento in self.orcamentos:
                if not orcamento.get("ativo", True):
                    continue
                inicio = str(orcamento.get("data_inicio", ""))[:10]
                fim = str(orcamento.get("data_fim", ""))[:10]
                if inicio and fim and not inicio <= hoje_iso <= fim:
                    continue
                categoria_id = orcamento.get("categoria_id")
                gastos = sum(
                    int(item.get("valor_centavos", 0) or 0)
                    for item in self.transacoes
                    if item.get("tipo") == "despesa"
                    and inicio <= str(item.get("data", ""))[:10] <= fim
                    and (
                        categoria_id is None
                        or str(item.get("categoria_id")) == str(categoria_id)
                    )
                )
                limite_centavos = int(orcamento.get("limite_centavos", 0) or 0)
                if limite_centavos <= 0 or gastos < limite_centavos * 0.8:
                    continue
                chave = (
                    f"user-{self.usuario.get('id', '')}-"
                    f"orcamento-{orcamento.get('id')}-{hoje:%Y-%m}"
                )
                if chave in _notificacao_ids_from_storage(
                    self.notificacoes_descartadas
                ):
                    continue
                percentual = int(gastos * 100 / limite_centavos)
                notificacoes.append({
                    "id": chave,
                    "titulo": "Atenção ao orçamento",
                    "mensagem": (
                        f"{orcamento.get('nome', 'Seu orçamento')} já usou "
                        f"{percentual}% do limite."
                    ),
                })

        if self.notificacoes_metas:
            for meta in self.metas:
                if meta.get("status", "ativa") != "ativa":
                    continue
                data_alvo = str(meta.get("data_alvo", ""))[:10]
                if not data_alvo or not hoje.isoformat() <= data_alvo <= (
                    hoje + timedelta(days=30)
                ).isoformat():
                    continue
                atual = int(meta.get("valor_atual_centavos", 0) or 0)
                objetivo = int(meta.get("valor_objetivo_centavos", 0) or 0)
                if objetivo <= 0 or atual >= objetivo:
                    continue
                chave = (
                    f"user-{self.usuario.get('id', '')}-meta-{meta.get('id')}"
                )
                if chave in _notificacao_ids_from_storage(
                    self.notificacoes_descartadas
                ):
                    continue
                notificacoes.append({
                    "id": chave,
                    "titulo": "Prazo da meta se aproximando",
                    "mensagem": (
                        f"{meta.get('nome', 'Sua meta')} tem prazo em {data_alvo}."
                    ),
                })
        return notificacoes

    @rx.var
    def sugestoes_financeiras(self) -> list[dict[str, str]]:
        sugestoes: list[dict[str, str]] = []
        hoje = date.today()
        este_mes = hoje.strftime("%Y-%m")
        inicio_mes_anterior = (
            date(hoje.year - 1, 12, 1)
            if hoje.month == 1
            else date(hoje.year, hoje.month - 1, 1)
        )
        ultimo_dia_mes_anterior = calendar.monthrange(
            inicio_mes_anterior.year,
            inicio_mes_anterior.month,
        )[1]
        limite_mes_anterior = inicio_mes_anterior.replace(
            day=min(hoje.day, ultimo_dia_mes_anterior)
        )
        gasto_atual = sum(
            int(item.get("valor_centavos", 0) or 0)
            for item in self.transacoes
            if item.get("tipo") == "despesa"
            and str(item.get("data", ""))[:7] == este_mes
            and str(item.get("data", ""))[:10] <= hoje.isoformat()
        )
        gasto_anterior = sum(
            int(item.get("valor_centavos", 0) or 0)
            for item in self.transacoes
            if item.get("tipo") == "despesa"
            and str(item.get("data", ""))[:7]
            == inicio_mes_anterior.strftime("%Y-%m")
            and str(item.get("data", ""))[:10]
            <= limite_mes_anterior.isoformat()
        )
        if gasto_anterior and gasto_atual > gasto_anterior * 1.2:
            sugestoes.append({
                "titulo": "Seus gastos aumentaram",
                "mensagem": (
                    f"Neste mês você já gastou "
                    f"{_formatar_centavos(gasto_atual - gasto_anterior)} a mais "
                    "que no mesmo período do mês passado. Confira suas "
                    "despesas recentes."
                ),
            })
        elif not self.transacoes:
            sugestoes.append({
                "titulo": "Comece pelo registro das despesas",
                "mensagem": (
                    "Registre algumas receitas e despesas para receber sugestões "
                    "personalizadas e acompanhar seu orçamento."
                ),
            })
        for meta in self.metas:
            if meta.get("status", "ativa") != "ativa":
                continue
            atual = int(meta.get("valor_atual_centavos", 0) or 0)
            objetivo = int(meta.get("valor_objetivo_centavos", 0) or 0)
            if objetivo > 0 and atual < objetivo * 0.25:
                sugestoes.append({
                    "titulo": f"Avance na meta {meta.get('nome', '')}",
                    "mensagem": (
                        f"Faltam {_formatar_centavos(objetivo - atual)} para "
                        "alcançar essa meta. Considere definir um valor mensal."
                    ),
                })
        return sugestoes[:4]

    @rx.var
    def metas_com_progresso(self) -> list[dict]:
        metas = []
        hoje = date.today()
        for meta in self.metas:
            objetivo = int(meta.get("valor_objetivo_centavos", 0) or 0)
            atual = int(meta.get("valor_atual_centavos", 0) or 0)
            restante = max(objetivo - atual, 0)
            data_alvo = str(meta.get("data_alvo", ""))[:10]
            mensal_necessario = ""
            if data_alvo:
                try:
                    prazo = date.fromisoformat(data_alvo)
                except ValueError:
                    prazo = hoje
                if prazo >= hoje and restante:
                    meses = (
                        (prazo.year - hoje.year) * 12
                        + prazo.month
                        - hoje.month
                        + (1 if prazo.day > hoje.day else 0)
                    )
                    meses = max(meses, 1)
                    mensal_necessario = _formatar_centavos(
                        (restante + meses - 1) // meses
                    )
            metas.append({
                **meta,
                "progresso_percentual": min(
                    100,
                    int(atual * 100 / objetivo) if objetivo else 0,
                ),
                "atual_formatado": _formatar_centavos(atual),
                "objetivo_formatado": _formatar_centavos(objetivo),
                "restante_formatado": _formatar_centavos(restante),
                "mensal_necessario_formatado": mensal_necessario,
            })
        return metas

    @rx.var
    def grafico_financeiro(self) -> list[dict[str, float | str]]:
        hoje = date.today()
        meses = []
        for deslocamento in range(5, -1, -1):
            indice = hoje.year * 12 + hoje.month - 1 - deslocamento
            ano, mes_zero = divmod(indice, 12)
            meses.append((ano, mes_zero + 1))

        dados = []
        nomes = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
                 "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
        for ano, mes in meses:
            receitas = 0
            despesas = 0
            for transacao in self.transacoes:
                data_transacao = str(transacao.get("data", ""))
                if data_transacao[:7] != f"{ano:04d}-{mes:02d}":
                    continue
                valor = int(transacao.get("valor_centavos", 0) or 0)
                if transacao.get("tipo") == "receita":
                    receitas += valor
                else:
                    despesas += valor
            dados.append({
                "mes": nomes[mes - 1],
                "receitas": receitas / 100,
                "despesas": despesas / 100,
            })
        return dados

    @staticmethod
    def _formatar_dinheiro(centavos: int) -> str:
        return _formatar_centavos(centavos)

    @staticmethod
    def _avatar_from_user(user: dict[str, object]) -> str:
        avatar = user.get("avatar_url", "")
        if isinstance(avatar, str):
            return avatar
        if isinstance(avatar, dict):
            for key in ("url", "public_url", "signed_url", "download_url", "link"):
                value = avatar.get(key)
                if isinstance(value, str) and value.strip():
                    return value
            nested = avatar.get("file")
            if isinstance(nested, dict):
                return AppState._avatar_from_user({"avatar_url": nested})
        return ""

    async def _api(
        self,
        method: str,
        path: str,
        payload: dict | None = None,
        upload: tuple[str, str, bytes] | None = None,
    ) -> object:
        return await asyncio.to_thread(
            _send_request,
            method,
            path,
            payload,
            self.auth_token,
            upload,
        )

    def _limpar_sessao(self):
        self.auth_token = ""
        self.usuario = {}
        self.avatar_url = ""
        self.avatar_perfil_disponivel = False
        self.dados_carregados = False
        self.transacoes = []
        self.contas = []
        self.categorias = []
        self.contas_a_pagar = []
        self.orcamentos = []
        self.metas = []
        self.recorrencias = []
        self.recorrencias_disponiveis = False
        self.transacao_busca = ""
        self.transacao_filtro_tipo = "todas"
        self.transacao_filtro_periodo = "todas"
        self.transacao_filtro_categoria = "todas"
        self.transacao_filtro_conta = "todas"
        self.recorrencia_descricao = ""
        self.recorrencia_valor = ""
        self.meta_contribuicao = ""
        self.preferencias = {}
        self.moeda = "BRL"
        self.localidade = "pt-BR"
        self.fuso_horario = "America/Sao_Paulo"
        self.notificacoes_vencimento = True
        self.notificacoes_orcamento = True
        self.notificacoes_metas = True
        self.notificacoes_metas_disponivel = False
        self.assistente_conversas = []
        self.assistente_conversa_id = 0
        self.assistente_mensagens = []
        self.assistente_mensagem = ""
        self.bolsa_carregando = False
        self.bolsa_erro = ""
        self.bolsa_carteira_erro = ""
        self.bolsa_indicadores = []
        self.bolsa_altas = []
        self.bolsa_baixas = []
        self.bolsa_grafico_altas = []
        self.bolsa_movers_origem = ""
        self.bolsa_movers_referencia = ""
        self.bolsa_movers_atrasado = False
        self.bolsa_ativos = []
        self.bolsa_ativo_selecionado = ""
        self.bolsa_detalhe = {}
        self.bolsa_historico = []
        self.bolsa_historico_origem = ""
        self.bolsa_operacoes = []
        self.bolsa_proventos = []
        self.bolsa_proventos_total_geral = "R$ 0,00"
        self.bolsa_proventos_total_ano = "R$ 0,00"
        self.bolsa_proventos_total_mes = "R$ 0,00"
        self.bolsa_favoritos = []
        self.bolsa_carteira = {
            "custo_investido": "R$ 0,00",
            "total_aplicado": "R$ 0,00",
            "resultado_realizado": "R$ 0,00",
            "valor_mercado": "Indisponível",
            "resultado_nao_realizado": "Indisponível",
            "rentabilidade": "Indisponível",
        }
        self.bolsa_carteira_posicoes = []
        self.bolsa_carteira_alocacao = []
        self.bolsa_carteira_evolucao = []
        self.bolsa_carteira_aviso = ""
        self.bolsa_comparacao_series = []
        self.bolsa_comparacao_linhas = []
        self.bolsa_comparacao_desempenho = []
        self.bolsa_comparacao_fontes = []
        self.bolsa_comparacao_aviso = ""
        self.bolsa_comparacao_ativos = ""
        self.bolsa_comparacao_periodo = "1 mês"
        self.bolsa_alertas = []
        self.bolsa_alerta_codigo = ""
        self.bolsa_alerta_preco = ""
        self.bolsa_alerta_percentual = ""
        self.bolsa_alerta_condicao = "preco_acima"
        self.bolsa_provento_codigo = ""
        self.bolsa_provento_valor = ""
        self.bolsa_provento_quantidade = ""
        self.bolsa_provento_data_anuncio = ""
        self.bolsa_provento_data_pagamento = ""
        self.bolsa_provento_observacoes = ""
        self.bolsa_operacao_edicao_id = 0
        self.auth_password = ""
        self.auth_password_confirmation = ""
        self.auth_name = ""
        self.auth_phone = ""
        self.aceitou_termos = False

    @rx.event
    def set_auth_email(self, value: str):
        self.auth_email = value
        if self.lembrar_email == "true":
            self.auth_email_salvo = value
        self.erro = ""

    @rx.event
    def set_auth_phone(self, value: str):
        self.auth_phone = _formatar_telefone(value)
        self.erro = ""

    @rx.event
    def set_lembrar_email(self, value: bool | str):
        normalized = value if isinstance(value, bool) else str(value).lower() in {"true", "1", "yes", "on"}
        if not normalized and not self.auth_email and self.auth_email_salvo:
            self.auth_email = self.auth_email_salvo
        self.lembrar_email = "true" if normalized else "false"
        self.auth_email_salvo = self.auth_email if normalized else ""

    @rx.event
    def set_auth_password(self, value: str):
        self.auth_password = value
        self.erro = ""

    @rx.event
    def set_auth_password_confirmation(self, value: str):
        self.auth_password_confirmation = value
        self.erro = ""

    @rx.event
    def set_aceitou_termos(self, value: bool | str):
        self.aceitou_termos = value if isinstance(value, bool) else str(value).lower() in {"true", "1", "yes", "on"}
        self.erro = ""

    @rx.event
    def alternar_visibilidade_senha(self):
        self.senha_visivel = not self.senha_visivel

    @rx.event
    def alternar_visibilidade_confirmacao_senha(self):
        self.senha_confirmacao_visivel = not self.senha_confirmacao_visivel

    @rx.event
    def set_auth_name(self, value: str):
        self.auth_name = value
        self.erro = ""

    @rx.event
    def preparar_cadastro(self):
        self.cadastro = True
        self.auth_password = ""
        self.auth_password_confirmation = ""
        self.aceitou_termos = False
        self.auth_phone = ""
        self.erro = ""
        if self.auth_token:
            return rx.redirect("/app")

    @rx.event
    def preparar_login(self):
        self.cadastro = False
        self.auth_password = ""
        self.auth_password_confirmation = ""
        self.aceitou_termos = False
        self.auth_phone = ""
        self.erro = ""
        if self.auth_token:
            return rx.redirect("/app")

    @rx.event
    def redirecionar_usuario_autenticado(self):
        if self.auth_token:
            return rx.redirect("/app")

    @staticmethod
    def _mensagem_erro_login(error: XanoAPIError) -> str:
        if error.status_code == 429:
            return (
                "Muitas tentativas de login em pouco tempo. "
                "Aguarde cerca de 20 segundos e tente novamente."
            )
        return str(error)

    @rx.event
    async def autenticar(self):
        self.erro = ""
        email = self.auth_email.strip().lower()
        if not email and self.lembrar_email == "true":
            email = self.auth_email_salvo.strip().lower()
        if not email:
            self.erro = "Informe seu e-mail."
            return
        password = self.auth_password.strip()
        if not password:
            self.erro = "Informe sua senha."
            return
        if self.cadastro:
            if not self.auth_name.strip():
                self.erro = "Informe seu nome."
                return
            if len("".join(char for char in self.auth_phone if char.isdigit())) < 10:
                self.erro = "Informe um telefone válido com DDD."
                return
            if self.auth_password != self.auth_password_confirmation:
                self.erro = "As senhas não conferem."
                return
            if not self.aceitou_termos:
                self.erro = "Aceite os Termos de Uso e a Política de Privacidade."
                return
            if (
                len(self.auth_password) < 8
                or not any(char.isalpha() for char in self.auth_password)
                or not any(char.isdigit() for char in self.auth_password)
            ):
                self.erro = "A senha deve ter ao menos 8 caracteres, uma letra e um número."
                return

        self.auth_email = email
        if self.lembrar_email == "true":
            self.auth_email_salvo = email
        self.carregando = True
        try:
            if self.cadastro:
                response = _as_record(
                    await self._api(
                        "POST",
                        "auth/signup",
                        {
                            "name": self.auth_name.strip(),
                            "email": email,
                            "phone": self.auth_phone.strip(),
                            "password": self.auth_password,
                        },
                    )
                )
            else:
                response = _as_record(
                    await self._api(
                        "POST",
                        "auth/login",
                        {
                            "email": email,
                            "password": password,
                        },
                    )
                )
            token = response.get("authToken")
            if not token:
                raise XanoAPIError("O Xano não retornou um token de sessão.")
            self.auth_token = str(token)
            self.usuario = _as_record(response.get("user"))
            self.avatar_url = self._avatar_from_user(self.usuario)
            self.avatar_perfil_disponivel = True
            self.auth_password = ""
            self.auth_password_confirmation = ""
            return rx.redirect("/app")
        except XanoAPIError as error:
            self.erro = self._mensagem_erro_login(error)
        finally:
            self.carregando = False

    async def _carregar_dados(self, force: bool = False):
        if not self.auth_token:
            return rx.redirect("/login")
        if self.dados_carregados and not force:
            return
        self.carregando = True
        self.erro = ""
        try:
            resumo = _as_record(await self._api("GET", "resumo"))
            chaves_resumo = {
                "usuario",
                "transacoes",
                "contas",
                "categorias",
                "contas_a_pagar",
                "orcamentos",
                "metas",
                "recorrencias",
                "preferencias",
            }
            if chaves_resumo.issubset(resumo):
                dados = resumo
            else:
                respostas = await asyncio.gather(
                    self._api("GET", "auth/me"),
                    self._api("GET", "contas"),
                    self._api("GET", "categorias"),
                    self._api("GET", "contas_a_pagar"),
                    self._api("GET", "orcamentos"),
                    self._api("GET", "metas_financeiras"),
                    self._api("GET", "preferencias_usuario/me"),
                )
                dados = {
                    "usuario": respostas[0],
                    "transacoes": resumo.get("transacoes", []),
                    "contas": respostas[1],
                    "categorias": respostas[2],
                    "contas_a_pagar": respostas[3],
                    "orcamentos": respostas[4],
                    "metas": respostas[5],
                    "recorrencias": [],
                    "preferencias": respostas[6],
                }

            self.usuario = _as_record(dados.get("usuario"))
            self.avatar_url = self._avatar_from_user(self.usuario)
            self.avatar_perfil_disponivel = bool(self.auth_token)
            self.transacoes = _records_with_money(
                dados.get("transacoes"),
                "valor_centavos",
            )
            self.contas = _records_with_money(
                dados.get("contas"),
                "saldo_inicial_centavos",
                "saldo_inicial_formatado",
            )
            self.categorias = _records(dados.get("categorias"))
            self.contas_a_pagar = _records_with_money(
                dados.get("contas_a_pagar"),
                "valor_centavos",
            )
            self.orcamentos = _records_with_money(
                dados.get("orcamentos"),
                "limite_centavos",
            )
            self.metas = _records_with_money(
                dados.get("metas"),
                "valor_objetivo_centavos",
            )
            self.recorrencias = _records_with_money(
                dados.get("recorrencias"),
                "valor_centavos",
            )
            self.recorrencias_disponiveis = (
                "recorrencias" in resumo
            )
            self.preferencias = _as_record(dados.get("preferencias"))
            self.notificacoes_metas_disponivel = (
                "notificacoes_metas" in self.preferencias
            )
            self.moeda = self.preferencias.get("moeda", "BRL")
            self.localidade = self.preferencias.get("localidade", "pt-BR")
            self.fuso_horario = self.preferencias.get(
                "fuso_horario",
                "America/Sao_Paulo",
            )
            self.notificacoes_vencimento = self.preferencias.get(
                "notificacoes_vencimento",
                True,
            )
            self.notificacoes_orcamento = self.preferencias.get(
                "notificacoes_orcamento",
                True,
            )
            self.notificacoes_metas = self.preferencias.get(
                "notificacoes_metas",
                True,
            )
            self._carregar_onboarding_local()
            self.dados_carregados = True
            if self.recorrencias_disponiveis:
                try:
                    await self._processar_recorrencias()
                except XanoAPIError as error:
                    self.erro = (
                        f"Não foi possível atualizar recorrências: {error}"
                    )
        except XanoAPIError as error:
            self.erro = str(error)
            if error.status_code == 401:
                self._limpar_sessao()
                self.erro = "Sua sessão expirou. Entre novamente."
                return rx.redirect("/login")
        finally:
            self.carregando = False

    @rx.event
    async def carregar_dados(self):
        return await self._carregar_dados()

    @rx.event
    async def atualizar_dados(self):
        return await self._carregar_dados(force=True)

    @rx.event
    async def carregar_bolsa(self):
        if not self.auth_token:
            return rx.redirect("/login")

        self.bolsa_carregando = True
        self.bolsa_erro = ""
        self.bolsa_carteira_erro = ""
        self.bolsa_indicadores = []
        self.bolsa_altas = []
        self.bolsa_baixas = []
        self.bolsa_grafico_altas = []
        self.bolsa_movers_origem = ""
        self.bolsa_movers_referencia = ""
        self.bolsa_movers_atrasado = False
        try:
            if market_data_service.configured:
                try:
                    movers = await asyncio.to_thread(
                        market_data_service.market_movers,
                        5,
                    )
                    self.bolsa_altas = [
                        _formatar_movimentacao_mercado(mover)
                        for mover in movers.gainers
                    ]
                    self.bolsa_baixas = [
                        _formatar_movimentacao_mercado(mover)
                        for mover in movers.losers
                    ]
                    self.bolsa_grafico_altas = [
                        {
                            "symbol": mover["symbol"],
                            "variation": mover["variation"],
                        }
                        for mover in self.bolsa_altas
                    ]
                    self.bolsa_movers_origem = movers.source
                    self.bolsa_movers_referencia = (
                        _formatar_horario_mercado(movers.reference_at)
                        if movers.gainers or movers.losers
                        else ""
                    )
                    self.bolsa_movers_atrasado = movers.stale
                    self.bolsa_indisponivel = (
                        ""
                        if self.bolsa_altas or self.bolsa_baixas
                        else "A fonte não encontrou ações ativas com volume e "
                        "variação diária verificáveis."
                    )
                except (MarketDataError, ValueError) as error:
                    self.bolsa_erro = str(error)
                    self.bolsa_indisponivel = (
                        "Não foi possível carregar os destaques da bolsa."
                    )
            else:
                self.bolsa_indisponivel = (
                    "Configure CASHSAVE_BRAPI_TOKEN no arquivo .env para "
                    "consultar dados de mercado."
                )

            self.erro = ""
            await self._carregar_dados()
            if not self.auth_token:
                return rx.redirect("/login")
            if self.erro:
                self.bolsa_carteira_erro = self.erro
            try:
                await self._carregar_favoritos_bolsa()
                await self._carregar_alertas_bolsa()
                await self._carregar_operacoes_bolsa()
                await self._carregar_proventos_bolsa()
                await self._carregar_analise_carteira_bolsa()
            except (XanoAPIError, ValueError) as error:
                self.bolsa_carteira_erro = str(error)
        finally:
            self.bolsa_carregando = False

    @rx.event
    def set_bolsa_busca(self, value: str):
        self.bolsa_busca = value

    @rx.event
    def set_bolsa_categoria(self, value: str):
        self.bolsa_categoria = value

    @rx.event
    def set_bolsa_ordenacao(self, value: str):
        self.bolsa_ordenacao = value

    @rx.event
    def set_bolsa_periodo(self, value: str):
        self.bolsa_periodo = value

    @rx.event
    def set_bolsa_comparacao_ativos(self, value: str):
        self.bolsa_comparacao_ativos = value

    @rx.event
    def set_bolsa_comparacao_periodo(self, value: str):
        self.bolsa_comparacao_periodo = value

    @rx.event
    async def comparar_ativos_bolsa(self):
        if not self.auth_token:
            return rx.redirect("/login")
        symbols = list(
            dict.fromkeys(
                symbol.strip().upper()
                for symbol in self.bolsa_comparacao_ativos.split(",")
                if symbol.strip()
            )
        )
        self.bolsa_comparacao_series = []
        self.bolsa_comparacao_linhas = []
        self.bolsa_comparacao_desempenho = []
        self.bolsa_comparacao_fontes = []
        self.bolsa_comparacao_aviso = ""
        if len(symbols) < 2:
            self.bolsa_comparacao_aviso = (
                "Informe pelo menos dois códigos de ativos separados por vírgula."
            )
            return
        periods = {
            "1 mês": "1m",
            "6 meses": "6m",
            "1 ano": "1y",
            "5 anos": "5y",
        }
        period = periods.get(self.bolsa_comparacao_periodo)
        if period is None:
            self.bolsa_comparacao_aviso = (
                "Selecione um período de comparação válido."
            )
            return

        histories = {}
        try:
            for symbol in symbols:
                histories[symbol] = await asyncio.to_thread(
                    market_data_service.history,
                    symbol,
                    period,
                )
            comparison = compare_price_histories(histories)
        except (MarketDataError, ValueError) as error:
            self.bolsa_comparacao_aviso = (
                f"Não foi possível comparar as séries verificadas: {error}"
            )
            return

        if not comparison.complete:
            missing = "; ".join(
                f"{symbol}: {missing_date}"
                for symbol, missing_date in comparison.missing_dates
            )
            self.bolsa_comparacao_aviso = (
                "As séries não cobrem as mesmas datas entre "
                f"{comparison.start_date} e {comparison.end_date}. "
                f"Datas sem observação: {missing}. Rentabilidade não calculada."
            )
            return

        colors = ["#10b981", "#6366f1", "#f59e0b", "#ec4899", "#06b6d4"]
        self.bolsa_comparacao_linhas = [
            {"symbol": symbol, "color": colors[index % len(colors)]}
            for index, symbol in enumerate(symbols)
        ]
        self.bolsa_comparacao_series = [
            {
                key: (
                    float(value)
                    if isinstance(value, Decimal)
                    else value
                )
                for key, value in row.items()
            }
            for row in comparison.series
        ]
        self.bolsa_comparacao_desempenho = [
            {
                "symbol": symbol,
                "percentual": f"{performance:.2f}%".replace(".", ","),
            }
            for symbol, performance in comparison.performance_percent
        ]
        self.bolsa_comparacao_fontes = [
            {
                "symbol": symbol,
                "source": history.source,
                "reference_at": history.reference_at.isoformat(),
                "freshness": history.freshness,
            }
            for symbol, history in sorted(histories.items())
        ]

    @rx.event
    async def pesquisar_ativos(self):
        if not self.auth_token:
            return rx.redirect("/login")

        self.bolsa_carregando = True
        self.bolsa_erro = ""
        self.bolsa_indisponivel = ""
        self.bolsa_ativo_selecionado = ""
        self.bolsa_detalhe = {}
        self.bolsa_historico = []
        self.bolsa_historico_origem = ""
        try:
            category = (
                None
                if self.bolsa_categoria == "todas"
                else self.bolsa_categoria
            )
            sort_by = (
                "name"
                if self.bolsa_ordenacao == "nome"
                else "symbol"
            )
            assets = await asyncio.to_thread(
                market_data_service.search,
                self.bolsa_busca,
                category,
                sort_by,
            )
            self.bolsa_ativos = [
                self._market_asset_record(asset)
                for asset in assets
            ]
            self._atualizar_status_favoritos()
            if not self.bolsa_ativos:
                self.bolsa_indisponivel = (
                    "Nenhum ativo compatível foi encontrado para esta pesquisa."
                )
        except MarketDataNotConfigured as error:
            self.bolsa_ativos = []
            self.bolsa_indisponivel = str(error)
        except (MarketDataError, ValueError) as error:
            self.bolsa_ativos = []
            self.bolsa_erro = str(error)
        finally:
            self.bolsa_carregando = False

    @staticmethod
    def _market_asset_record(asset: MarketAsset) -> dict[str, str]:
        category_labels = {
            "acao": "Ação",
            "fii": "FII",
            "etf": "ETF",
        }
        return {
            "symbol": asset.symbol,
            "name": asset.name,
            "category": category_labels[asset.category],
            "category_code": asset.category,
            "source": asset.source,
            "stale": "true" if asset.stale else "false",
            "favorito": "false",
        }

    def _atualizar_status_favoritos(self):
        favorite_symbols = {
            str(favorite.get("ativo_codigo", "")).upper()
            for favorite in self.bolsa_favoritos
        }
        self.bolsa_ativos = [
            {
                **asset,
                "favorito": (
                    "true"
                    if asset.get("symbol", "").upper() in favorite_symbols
                    else "false"
                ),
            }
            for asset in self.bolsa_ativos
        ]

    async def _carregar_favoritos_bolsa(self):
        response = await self._api("GET", "investimentos/favoritos")
        category_labels = {
            "acao": "Ação",
            "fii": "FII",
            "etf": "ETF",
        }
        favorites: list[dict[str, str]] = []
        for record in _records(response):
            symbol = record.get("ativo_codigo")
            category = record.get("ativo_categoria")
            if (
                not isinstance(symbol, str)
                or not symbol.strip()
                or category not in category_labels
            ):
                raise XanoAPIError("O Xano retornou um favorito inválido.")
            favorites.append(
                {
                    "ativo_codigo": symbol.strip().upper(),
                    "ativo_categoria": str(category),
                    "categoria_formatada": category_labels[str(category)],
                }
            )
        self.bolsa_favoritos = favorites
        self._atualizar_status_favoritos()

    async def _carregar_alertas_bolsa(self):
        response = await self._api("GET", "investimentos/alertas")
        labels = {
            "preco_acima": "Preço acima de",
            "preco_abaixo": "Preço abaixo de",
            "variacao_diaria_acima": "Variação diária acima de",
            "variacao_diaria_abaixo": "Variação diária abaixo de",
        }
        alerts: list[dict[str, str]] = []
        for record in _records(response):
            condition = record.get("condicao")
            symbol = record.get("ativo_codigo")
            monitoring_status = record.get("monitoramento_status")
            if (
                not isinstance(condition, str)
                or condition not in labels
                or not isinstance(symbol, str)
                or not symbol.strip()
            ):
                raise XanoAPIError("O Xano retornou um alerta inválido.")
            if monitoring_status != "nao_monitorado":
                raise XanoAPIError(
                    "O Xano retornou um estado de alerta não suportado."
                )
            price_limit = record.get("preco_limite_centavos")
            percentage_limit = record.get("variacao_limite_percentual")
            if condition.startswith("preco_"):
                if not isinstance(price_limit, int) or price_limit <= 0:
                    raise XanoAPIError("O alerta retornado não tem limite válido.")
                limit = _formatar_centavos(price_limit)
            else:
                try:
                    percentage = Decimal(str(percentage_limit))
                except InvalidOperation as error:
                    raise XanoAPIError(
                        "O alerta retornado não tem percentual válido."
                    ) from error
                if not percentage.is_finite() or percentage <= 0:
                    raise XanoAPIError(
                        "O alerta retornado não tem percentual válido."
                    )
                limit = f"{percentage:.2f}%".replace(".", ",")
            alerts.append(
                {
                    "id": int(record.get("id", 0) or 0),
                    "ativo_codigo": symbol.strip().upper(),
                    "ativo_categoria": str(record.get("ativo_categoria", "")),
                    "condicao": condition,
                    "condicao_formatada": labels[condition],
                    "limite_formatado": limit,
                    "monitoramento_status": "Não monitorado",
                }
            )
        self.bolsa_alertas = alerts

    @rx.event
    def set_bolsa_alerta_codigo(self, value: str):
        self.bolsa_alerta_codigo = value

    @rx.event
    def set_bolsa_alerta_categoria(self, value: str):
        self.bolsa_alerta_categoria = value

    @rx.event
    def set_bolsa_alerta_condicao(self, value: str):
        self.bolsa_alerta_condicao = value

    @rx.event
    def set_bolsa_alerta_preco(self, value: str):
        self.bolsa_alerta_preco = value

    @rx.event
    def set_bolsa_alerta_percentual(self, value: str):
        self.bolsa_alerta_percentual = value

    @rx.event
    async def salvar_alerta_bolsa(self):
        if not self.auth_token:
            return rx.redirect("/login")
        symbol = self.bolsa_alerta_codigo.strip().upper()
        if not symbol:
            self.bolsa_erro = "Informe o código do ativo para o alerta."
            return
        if self.bolsa_alerta_categoria not in {"acao", "fii", "etf"}:
            self.bolsa_erro = "Selecione uma categoria de ativo válida."
            return

        payload: dict[str, object] = {
            "ativo_codigo": symbol,
            "ativo_categoria": self.bolsa_alerta_categoria,
            "condicao": self.bolsa_alerta_condicao,
            "preco_limite_centavos": None,
            "variacao_limite_percentual": None,
        }
        try:
            if self.bolsa_alerta_condicao in {"preco_acima", "preco_abaixo"}:
                payload["preco_limite_centavos"] = _money_to_cents(
                    self.bolsa_alerta_preco
                )
            elif self.bolsa_alerta_condicao in {
                "variacao_diaria_acima",
                "variacao_diaria_abaixo",
            }:
                try:
                    percentage = Decimal(
                        self.bolsa_alerta_percentual.strip().replace(",", ".")
                    )
                except InvalidOperation as error:
                    raise XanoAPIError(
                        "Informe um percentual de variação válido."
                    ) from error
                if not percentage.is_finite() or percentage <= 0:
                    raise XanoAPIError(
                        "O percentual de variação deve ser positivo."
                    )
                payload["variacao_limite_percentual"] = format(
                    percentage,
                    "f",
                )
            else:
                raise XanoAPIError("Selecione uma condição de alerta válida.")

            saved = _as_record(
                await self._api(
                    "POST",
                    "investimentos/alertas",
                    payload,
                )
            )
            if not saved.get("id"):
                raise XanoAPIError("O Xano não confirmou o alerta.")
            await self._carregar_alertas_bolsa()
            self.bolsa_alerta_codigo = ""
            self.bolsa_alerta_preco = ""
            self.bolsa_alerta_percentual = ""
        except (XanoAPIError, ValueError) as error:
            self.bolsa_erro = str(error)

    @rx.event
    async def excluir_alerta_bolsa(self, alert_id: int):
        if not self.auth_token:
            return rx.redirect("/login")
        try:
            await self._api("DELETE", f"investimentos/alertas/{alert_id}")
            await self._carregar_alertas_bolsa()
        except (XanoAPIError, ValueError) as error:
            self.bolsa_erro = str(error)

    @rx.event
    async def alternar_favorito_bolsa(self, symbol: str, category: str):
        if not self.auth_token:
            return rx.redirect("/login")
        normalized_symbol = symbol.strip().upper()
        if not normalized_symbol or category not in {"acao", "fii", "etf"}:
            self.bolsa_erro = "Ativo inválido para favoritos."
            return
        self.bolsa_erro = ""
        favorite = next(
            (
                item
                for item in self.bolsa_favoritos
                if item.get("ativo_codigo") == normalized_symbol
            ),
            None,
        )
        try:
            if favorite is not None:
                await self._api(
                    "DELETE",
                    "investimentos/favoritos/"
                    + quote(normalized_symbol, safe=""),
                )
            else:
                saved = _as_record(
                    await self._api(
                        "POST",
                        "investimentos/favoritos",
                        {
                            "ativo_codigo": normalized_symbol,
                            "ativo_categoria": category,
                        },
                    )
                )
                if not saved.get("id"):
                    raise XanoAPIError("O Xano não confirmou o favorito.")
            await self._carregar_favoritos_bolsa()
        except (XanoAPIError, ValueError) as error:
            self.bolsa_erro = str(error)

    @rx.event
    async def selecionar_ativo(self, symbol: str):
        if not self.auth_token:
            return rx.redirect("/login")

        normalized_symbol = symbol.strip().upper()
        asset = next(
            (
                item
                for item in self.bolsa_ativos
                if item["symbol"].upper() == normalized_symbol
            ),
            None,
        )
        if asset is None:
            favorite = next(
                (
                    item
                    for item in self.bolsa_favoritos
                    if item.get("ativo_codigo") == normalized_symbol
                ),
                None,
            )
            if favorite is not None:
                asset = {
                    "symbol": normalized_symbol,
                    "name": normalized_symbol,
                    "category": favorite["categoria_formatada"],
                    "category_code": favorite["ativo_categoria"],
                }
        if asset is None:
            self.bolsa_erro = "Selecione um ativo retornado pela pesquisa."
            return

        self.bolsa_carregando = True
        self.bolsa_erro = ""
        self.bolsa_ativo_selecionado = normalized_symbol
        self.bolsa_detalhe = {}
        self.bolsa_historico = []
        self.bolsa_historico_origem = ""
        self.bolsa_historico_mensagem = (
            "Selecione um período para consultar o histórico disponível."
        )
        try:
            quote = await asyncio.to_thread(
                market_data_service.quote,
                normalized_symbol,
            )
            expected_categories = {
                "Ação": "acao",
                "FII": "fii",
                "ETF": "etf",
            }
            if quote.category != expected_categories.get(asset["category"]):
                raise MarketDataError(
                    "A categoria da cotação não corresponde ao ativo pesquisado."
                )
            freshness_labels = {
                "real_time": "Tempo real",
                "delayed": "Atrasada",
                "historical": "Histórica",
                "unknown": "Desconhecida",
            }
            self.bolsa_detalhe = {
                "symbol": quote.symbol,
                "name": asset["name"],
                "category": asset["category"],
                "category_code": asset["category_code"],
                "price": f"R$ {quote.price:.2f}".replace(".", ","),
                "daily_change": (
                    f"{quote.daily_change_percent:.2f}%".replace(".", ",")
                    if quote.daily_change_percent is not None
                    else "Indisponível"
                ),
                "source": quote.source,
                "reference_at": quote.reference_at.isoformat(timespec="minutes"),
                "freshness": freshness_labels[quote.freshness],
                "stale": "true" if quote.stale else "false",
                "category_metrics": (
                    "Não fornecidas por uma fonte verificada."
                ),
            }
        except MarketDataNotConfigured as error:
            self.bolsa_erro = str(error)
            self.bolsa_ativo_selecionado = ""
        except (MarketDataError, ValueError) as error:
            self.bolsa_erro = str(error)
            self.bolsa_ativo_selecionado = ""
        finally:
            self.bolsa_carregando = False

    @rx.event
    async def carregar_historico_bolsa(self):
        if not self.auth_token:
            return rx.redirect("/login")
        if not self.bolsa_ativo_selecionado:
            self.bolsa_historico_mensagem = "Selecione um ativo primeiro."
            return

        periods = {
            "Intraday": "intraday",
            "1 dia": "1d",
            "1 semana": "1w",
            "1 mês": "1m",
            "6 meses": "6m",
            "1 ano": "1y",
            "5 anos": "5y",
        }
        period = periods.get(self.bolsa_periodo)
        if period is None:
            self.bolsa_historico_mensagem = "Período histórico não suportado."
            return

        self.bolsa_carregando = True
        self.bolsa_erro = ""
        self.bolsa_historico = []
        self.bolsa_historico_origem = ""
        try:
            history = await asyncio.to_thread(
                market_data_service.history,
                self.bolsa_ativo_selecionado,
                period,
            )
            self.bolsa_historico = [
                {
                    "data": point.observed_at.strftime("%d/%m %H:%M %z"),
                    "preco": float(point.price),
                }
                for point in history.points
            ]
            self.bolsa_historico_origem = (
                f"Fonte: {history.source} · Referência: "
                f"{history.reference_at.isoformat(timespec='minutes')}"
            )
            if history.stale:
                self.bolsa_historico_origem += " · Histórico desatualizado"
            if not self.bolsa_historico:
                self.bolsa_historico_mensagem = (
                    "A fonte não retornou observações para este período."
                )
            else:
                self.bolsa_historico_mensagem = ""
        except (MarketDataError, ValueError) as error:
            self.bolsa_historico_mensagem = str(error)
        finally:
            self.bolsa_carregando = False

    @staticmethod
    def _investment_operation_from_record(
        record: dict[str, object],
    ) -> InvestmentOperation:
        return InvestmentOperation(
            symbol=str(record.get("ativo_codigo", "")),
            operation_type=str(record.get("tipo", "")),
            operation_date=date.fromisoformat(str(record.get("data", ""))[:10]),
            quantity=Decimal(str(record.get("quantidade", ""))),
            unit_price_centavos=int(
                record.get("preco_unitario_centavos", 0) or 0
            ),
            costs_centavos=int(record.get("custos_centavos", 0) or 0),
            operation_id=int(record.get("id", 0) or 0),
        )

    @staticmethod
    def _investment_operation_display(
        operation: InvestmentOperation,
        category: str,
        notes: object = "",
    ) -> dict[str, object]:
        quantity = format(operation.quantity, "f")
        if "." in quantity:
            quantity = quantity.rstrip("0").rstrip(".")
        return {
            "id": operation.operation_id,
            "ativo_codigo": operation.symbol,
            "ativo_categoria": category,
            "tipo": operation.operation_type,
            "data": operation.operation_date.isoformat(),
            "quantidade": quantity,
            "preco": _formatar_centavos(operation.unit_price_centavos),
            "custos": _formatar_centavos(operation.costs_centavos),
            "observacoes": str(notes or ""),
        }

    async def _carregar_operacoes_bolsa(self):
        response = await self._api("GET", "investimentos/operacoes")
        records = _records(response)
        formatted_operations: list[dict[str, object]] = []
        for record in records:
            operation = self._investment_operation_from_record(record)
            formatted_operations.append(
                self._investment_operation_display(
                    operation,
                    str(record.get("ativo_categoria", "")),
                    record.get("observacoes", ""),
                )
            )
        self.bolsa_operacoes = formatted_operations

    async def _carregar_proventos_bolsa(self):
        response = await self._api("GET", "investimentos/proventos")
        records = _records(response)
        proventos = [format_provento_record(record) for record in records]
        today = date.today()
        self.bolsa_proventos = proventos
        self.bolsa_proventos_total_geral = _formatar_centavos(
            total_received_proventos_centavos(records)
        )
        self.bolsa_proventos_total_ano = _formatar_centavos(
            total_received_proventos_centavos(
                records,
                start_date=date(today.year, 1, 1),
                end_date=today,
            )
        )
        self.bolsa_proventos_total_mes = _formatar_centavos(
            total_received_proventos_centavos(
                records,
                start_date=date(today.year, today.month, 1),
                end_date=today,
            )
        )

    async def _carregar_analise_carteira_bolsa(self):
        operation_records = _records(
            await self._api("GET", "investimentos/operacoes")
        )
        operations = [
            self._investment_operation_from_record(record)
            for record in operation_records
        ]
        categories: dict[str, str] = {}
        for record in operation_records:
            symbol = str(record.get("ativo_codigo", "")).strip().upper()
            category = str(record.get("ativo_categoria", ""))
            if symbol in categories and categories[symbol] != category:
                raise XanoAPIError(
                    f"O ativo {symbol} tem categorias inconsistentes no histórico."
                )
            categories[symbol] = category

        market_prices: dict[str, int] = {}
        market_metadata: dict[str, dict[str, str]] = {}
        unavailable_symbols: list[str] = []
        stale_symbols: list[str] = []
        grouped_operations: dict[str, list[InvestmentOperation]] = {}
        for operation in operations:
            grouped_operations.setdefault(operation.symbol, []).append(operation)
        active_symbols = {
            symbol
            for symbol, history in grouped_operations.items()
            if calculate_position(symbol, history).quantity > 0
        }
        if market_data_service.configured:
            for symbol in sorted(active_symbols):
                try:
                    quote = await asyncio.to_thread(
                        market_data_service.quote,
                        symbol,
                    )
                    expected_category = categories[symbol]
                    if quote.category != expected_category:
                        raise MarketDataError(
                            "A categoria da cotação não corresponde à carteira."
                        )
                except (MarketDataError, ValueError):
                    unavailable_symbols.append(symbol)
                    continue
                market_prices[symbol] = int(
                    (quote.price * 100).quantize(
                        Decimal("1"),
                        rounding=ROUND_HALF_UP,
                    )
                )
                market_metadata[symbol] = {
                    "source": quote.source,
                    "reference_at": quote.reference_at.isoformat(),
                    "freshness": quote.freshness,
                    "stale": "true" if quote.stale else "false",
                }
                if quote.stale:
                    stale_symbols.append(symbol)

        snapshot = calculate_portfolio_snapshot(
            operations,
            categories,
            market_prices,
        )
        self.bolsa_carteira = {
            "custo_investido": _formatar_centavos(
                snapshot.total_cost_basis_centavos
            ),
            "total_aplicado": _formatar_centavos(
                snapshot.total_purchase_outlay_centavos
            ),
            "resultado_realizado": _formatar_centavos(
                snapshot.total_realized_result_centavos
            ),
            "valor_mercado": (
                _formatar_centavos(snapshot.total_market_value_centavos)
                if snapshot.total_market_value_centavos is not None
                else "Indisponível"
            ),
            "resultado_nao_realizado": (
                _formatar_centavos(snapshot.total_unrealized_result_centavos)
                if snapshot.total_unrealized_result_centavos is not None
                else "Indisponível"
            ),
            "rentabilidade": (
                f"{snapshot.simple_return_percent:.2f}%".replace(".", ",")
                if snapshot.simple_return_percent is not None
                else "Indisponível"
            ),
        }
        self.bolsa_carteira_posicoes = []
        for holding in snapshot.holdings:
            if holding.position.quantity == 0:
                continue
            quantity = format(holding.position.quantity, "f")
            if "." in quantity:
                quantity = quantity.rstrip("0").rstrip(".")
            self.bolsa_carteira_posicoes.append(
                {
                    "symbol": holding.symbol,
                    "category": holding.category.upper(),
                    "quantity": quantity,
                    "cost_basis": _formatar_centavos(
                        holding.position.cost_basis_centavos
                    ),
                    "market_value": (
                        _formatar_centavos(
                            holding.position.market_value_centavos
                        )
                        if holding.position.market_value_centavos is not None
                        else "Indisponível"
                    ),
                    "source": market_metadata.get(holding.symbol, {}).get(
                        "source",
                        "Indisponível",
                    ),
                    "reference_at": market_metadata.get(holding.symbol, {}).get(
                        "reference_at",
                        "",
                    ),
                    "freshness": market_metadata.get(holding.symbol, {}).get(
                        "freshness",
                        "",
                    ),
                    "stale": market_metadata.get(holding.symbol, {}).get(
                        "stale",
                        "false",
                    ),
                }
            )
        self.bolsa_carteira_alocacao = [
            {
                "categoria": category.upper(),
                "valor": _formatar_centavos(value),
                "percentual": f"{percentage:.2f}%".replace(".", ","),
            }
            for category, value, percentage in snapshot.allocation_by_category
        ]
        evolution = monthly_investment_flows(operations, self.bolsa_proventos)
        self.bolsa_carteira_evolucao = [
            {
                "periodo": str(flow["periodo"]),
                "contribuicoes": float(
                    Decimal(int(flow["contribuicoes_centavos"])) / 100
                ),
                "retiradas": float(
                    Decimal(int(flow["retiradas_centavos"])) / 100
                ),
                "proventos": float(
                    Decimal(int(flow["proventos_centavos"])) / 100
                ),
            }
            for flow in evolution
        ]
        if unavailable_symbols:
            self.bolsa_carteira_aviso = (
                "Cotações indisponíveis para: "
                + ", ".join(sorted(unavailable_symbols))
                + ". Valor de mercado, resultado não realizado, rentabilidade "
                "e alocação podem estar incompletos."
            )
        elif active_symbols and not market_data_service.configured:
            self.bolsa_carteira_aviso = (
                "Sem provedor de mercado aprovado; valores de mercado, "
                "resultado não realizado, rentabilidade e alocação estão "
                "indisponíveis."
            )
        elif stale_symbols:
            self.bolsa_carteira_aviso = (
                "Cotações desatualizadas para: "
                + ", ".join(sorted(stale_symbols))
                + ". Consulte a referência antes de usar esses valores."
            )
        else:
            self.bolsa_carteira_aviso = ""

    async def _contexto_investimentos_jarvis(self) -> dict[str, object]:
        owner_id = self.usuario.get("id")
        operation_records = _records(
            await self._api("GET", "investimentos/operacoes")
        )
        provento_records = _records(
            await self._api("GET", "investimentos/proventos")
        )
        try:
            assert_investment_record_owner(operation_records, owner_id)
            assert_investment_record_owner(provento_records, owner_id)
            operations = [
                self._investment_operation_from_record(record)
                for record in operation_records
            ]
            categories: dict[str, str] = {}
            for record in operation_records:
                symbol = str(record.get("ativo_codigo", "")).strip().upper()
                category = str(record.get("ativo_categoria", ""))
                if symbol in categories and categories[symbol] != category:
                    raise ValueError(
                        f"O ativo {symbol} tem categorias inconsistentes."
                    )
                categories[symbol] = category
            snapshot = calculate_portfolio_snapshot(
                operations,
                categories,
                {},
            )
            positions = [
                {
                    "ativo_codigo": holding.symbol,
                    "ativo_categoria": holding.category.upper(),
                    "quantidade": format(holding.position.quantity, "f"),
                    "custo_investido_centavos": (
                        holding.position.cost_basis_centavos
                    ),
                    "resultado_realizado_centavos": (
                        holding.position.realized_result_centavos
                    ),
                }
                for holding in snapshot.holdings
                if holding.position.quantity > 0
            ]
            proventos_recebidos = total_received_proventos_centavos(
                provento_records
            )
        except ValueError as error:
            raise XanoAPIError(
                "Os registros de investimento não puderam ser validados."
            ) from error

        selected_asset = None
        if (
            self.bolsa_ativo_selecionado
            and self.bolsa_detalhe.get("symbol")
            == self.bolsa_ativo_selecionado
            and self.bolsa_detalhe.get("source")
            and self.bolsa_detalhe.get("reference_at")
        ):
            selected_asset = {
                "symbol": self.bolsa_detalhe["symbol"],
                "price": self.bolsa_detalhe.get("price", "Indisponível"),
                "source": self.bolsa_detalhe["source"],
                "reference_at": self.bolsa_detalhe["reference_at"],
                "freshness": self.bolsa_detalhe.get(
                    "freshness",
                    "Desconhecida",
                ),
                "stale": self.bolsa_detalhe.get("stale", "true"),
            }

        profile_available = bool(
            self.onboarding_concluido and self.onboarding_respostas
        )
        profile_context = (
            {
                "disponivel": True,
                "perfil": self.investidor_perfil,
                "ponto_atencao": self.investidor_pontos_atencao,
            }
            if profile_available
            else {"disponivel": False}
        )
        return {
            "status": "disponivel",
            "posicoes": positions,
            "custo_investido_centavos": snapshot.total_cost_basis_centavos,
            "total_aplicado_centavos": snapshot.total_purchase_outlay_centavos,
            "resultado_realizado_centavos": (
                snapshot.total_realized_result_centavos
            ),
            "valor_mercado_centavos": snapshot.total_market_value_centavos,
            "resultado_nao_realizado_centavos": (
                snapshot.total_unrealized_result_centavos
            ),
            "rentabilidade_simples_percentual": (
                str(snapshot.simple_return_percent)
                if snapshot.simple_return_percent is not None
                else None
            ),
            "proventos_recebidos_centavos": proventos_recebidos,
            "ativo_aberto": selected_asset,
            "perfil_educativo": profile_context,
        }

    @rx.event
    def set_bolsa_provento_codigo(self, value: str):
        self.bolsa_provento_codigo = value

    @rx.event
    def set_bolsa_provento_categoria(self, value: str):
        self.bolsa_provento_categoria = value

    @rx.event
    def set_bolsa_provento_tipo(self, value: str):
        self.bolsa_provento_tipo = value

    @rx.event
    def set_bolsa_provento_status(self, value: str):
        self.bolsa_provento_status = value

    @rx.event
    def set_bolsa_provento_valor(self, value: str):
        self.bolsa_provento_valor = value

    @rx.event
    def set_bolsa_provento_quantidade(self, value: str):
        self.bolsa_provento_quantidade = value

    @rx.event
    def set_bolsa_provento_data_anuncio(self, value: str):
        self.bolsa_provento_data_anuncio = value

    @rx.event
    def set_bolsa_provento_data_pagamento(self, value: str):
        self.bolsa_provento_data_pagamento = value

    @rx.event
    def set_bolsa_provento_observacoes(self, value: str):
        self.bolsa_provento_observacoes = value

    def _nova_data_provento(self, value: str, field: str) -> str | None:
        if not value.strip():
            return None
        try:
            return date.fromisoformat(value).isoformat()
        except ValueError as error:
            raise XanoAPIError(f"Informe uma data válida para {field}.") from error

    def _limpar_formulario_provento(self):
        self.bolsa_provento_codigo = ""
        self.bolsa_provento_valor = ""
        self.bolsa_provento_quantidade = ""
        self.bolsa_provento_data_anuncio = ""
        self.bolsa_provento_data_pagamento = ""
        self.bolsa_provento_observacoes = ""
        self.bolsa_provento_tipo = "dividendo"
        self.bolsa_provento_status = "pago"

    @rx.event
    async def salvar_provento_bolsa(self):
        if not self.auth_token:
            return rx.redirect("/login")
        self.bolsa_erro = ""
        try:
            symbol = self.bolsa_provento_codigo.strip().upper()
            if not symbol:
                raise XanoAPIError("Informe o código do ativo.")
            if self.bolsa_provento_categoria not in {"acao", "fii", "etf"}:
                raise XanoAPIError("Selecione uma categoria de ativo válida.")
            if self.bolsa_provento_tipo not in {
                "dividendo",
                "jcp",
                "rendimento_fii",
                "outro",
            }:
                raise XanoAPIError("Selecione um tipo de provento válido.")
            if self.bolsa_provento_status not in {"anunciado", "pago"}:
                raise XanoAPIError("Selecione um status válido.")

            payment_date = self._nova_data_provento(
                self.bolsa_provento_data_pagamento,
                "pagamento",
            )
            announcement_date = self._nova_data_provento(
                self.bolsa_provento_data_anuncio,
                "anúncio",
            )
            if self.bolsa_provento_status == "pago" and payment_date is None:
                raise XanoAPIError(
                    "Informe a data de pagamento para um provento recebido."
                )

            eligible_quantity = None
            if self.bolsa_provento_quantidade.strip():
                try:
                    eligible_quantity = Decimal(
                        self.bolsa_provento_quantidade.strip().replace(",", ".")
                    )
                except InvalidOperation as error:
                    raise XanoAPIError(
                        "Informe uma quantidade elegível válida."
                    ) from error
                if not eligible_quantity.is_finite() or eligible_quantity < 0:
                    raise XanoAPIError(
                        "A quantidade elegível não pode ser negativa."
                    )

            saved = _as_record(
                await self._api(
                    "POST",
                    "investimentos/proventos",
                    {
                        "ativo_codigo": symbol,
                        "ativo_categoria": self.bolsa_provento_categoria,
                        "tipo": self.bolsa_provento_tipo,
                        "status": self.bolsa_provento_status,
                        "valor_centavos": _money_to_cents(
                            self.bolsa_provento_valor
                        ),
                        "quantidade_elegivel": (
                            format(eligible_quantity, "f")
                            if eligible_quantity is not None
                            else None
                        ),
                        "data_anuncio": announcement_date,
                        "data_pagamento": payment_date,
                        "observacoes": (
                            self.bolsa_provento_observacoes.strip() or None
                        ),
                    },
                )
            )
            if not saved.get("id"):
                raise XanoAPIError("O Xano não confirmou o provento.")
            await self._carregar_proventos_bolsa()
            await self._carregar_analise_carteira_bolsa()
            self._limpar_formulario_provento()
        except (XanoAPIError, ValueError) as error:
            self.bolsa_erro = str(error)

    @rx.event
    def set_bolsa_operacao_codigo(self, value: str):
        self.bolsa_operacao_codigo = value

    @rx.event
    def set_bolsa_operacao_categoria(self, value: str):
        self.bolsa_operacao_categoria = value

    @rx.event
    def set_bolsa_operacao_tipo(self, value: str):
        self.bolsa_operacao_tipo = value

    @rx.event
    def set_bolsa_operacao_data(self, value: str):
        self.bolsa_operacao_data = value

    @rx.event
    def set_bolsa_operacao_quantidade(self, value: str):
        self.bolsa_operacao_quantidade = value

    @rx.event
    def set_bolsa_operacao_preco(self, value: str):
        self.bolsa_operacao_preco = value

    @rx.event
    def set_bolsa_operacao_custos(self, value: str):
        self.bolsa_operacao_custos = value

    @rx.event
    def set_bolsa_operacao_observacoes(self, value: str):
        self.bolsa_operacao_observacoes = value

    @rx.event
    def editar_operacao_bolsa(self, operation_id: int):
        record = next(
            (
                item
                for item in self.bolsa_operacoes
                if item.get("id") == operation_id
            ),
            None,
        )
        if record is None:
            self.bolsa_erro = "Operação não encontrada."
            return
        self.bolsa_operacao_edicao_id = operation_id
        self.bolsa_operacao_codigo = str(record["ativo_codigo"])
        self.bolsa_operacao_categoria = str(record["ativo_categoria"])
        self.bolsa_operacao_tipo = str(record["tipo"])
        self.bolsa_operacao_data = str(record["data"])
        self.bolsa_operacao_quantidade = str(record["quantidade"])
        self.bolsa_operacao_preco = str(record["preco"]).removeprefix("R$ ").strip()
        self.bolsa_operacao_custos = str(record["custos"]).removeprefix("R$ ").strip()
        self.bolsa_operacao_observacoes = str(record["observacoes"])
        self.bolsa_erro = ""

    @rx.event
    def cancelar_edicao_operacao_bolsa(self):
        self._limpar_edicao_operacao_bolsa()

    def _limpar_edicao_operacao_bolsa(self):
        self.bolsa_operacao_edicao_id = 0
        self.bolsa_operacao_codigo = ""
        self.bolsa_operacao_quantidade = ""
        self.bolsa_operacao_preco = ""
        self.bolsa_operacao_custos = ""
        self.bolsa_operacao_observacoes = ""

    def _nova_operacao_bolsa(self) -> InvestmentOperation:
        symbol = self.bolsa_operacao_codigo.strip().upper()
        if not symbol:
            raise XanoAPIError("Informe o código do ativo.")
        if self.bolsa_operacao_categoria not in {"acao", "fii", "etf"}:
            raise XanoAPIError("Selecione uma categoria de ativo válida.")
        if self.bolsa_operacao_tipo not in {"compra", "venda"}:
            raise XanoAPIError("Selecione compra ou venda.")
        try:
            quantity = Decimal(self.bolsa_operacao_quantidade.strip().replace(",", "."))
            operation_date = date.fromisoformat(self.bolsa_operacao_data)
        except (InvalidOperation, ValueError) as error:
            raise XanoAPIError("Informe quantidade e data válidas.") from error
        return InvestmentOperation(
            symbol=symbol,
            operation_type=self.bolsa_operacao_tipo,
            operation_date=operation_date,
            quantity=quantity,
            unit_price_centavos=_money_to_cents(self.bolsa_operacao_preco),
            costs_centavos=_nonnegative_money_to_cents(
                self.bolsa_operacao_custos
            ),
            operation_id=self.bolsa_operacao_edicao_id,
        )

    @rx.event
    async def salvar_operacao_bolsa(self):
        if not self.auth_token:
            return rx.redirect("/login")
        self.bolsa_erro = ""
        try:
            operations = [
                self._investment_operation_from_record(item)
                for item in _records(await self._api("GET", "investimentos/operacoes"))
            ]
            operation = self._nova_operacao_bolsa()
            validate_operation_mutation(
                operations,
                candidate=operation,
                excluded_operation_id=self.bolsa_operacao_edicao_id or None,
            )
            payload = {
                "ativo_codigo": operation.symbol,
                "ativo_categoria": self.bolsa_operacao_categoria,
                "tipo": operation.operation_type,
                "data": operation.operation_date.isoformat(),
                "quantidade": format(operation.quantity, "f"),
                "preco_unitario_centavos": operation.unit_price_centavos,
                "custos_centavos": operation.costs_centavos,
                "observacoes": self.bolsa_operacao_observacoes.strip() or None,
            }
            if self.bolsa_operacao_edicao_id:
                saved = _as_record(
                    await self._api(
                        "PATCH",
                        "investimentos/operacoes/"
                        f"{self.bolsa_operacao_edicao_id}",
                        payload,
                    )
                )
            else:
                saved = _as_record(
                    await self._api("POST", "investimentos/operacoes", payload)
                )
            if not saved.get("id"):
                raise XanoAPIError("O Xano não confirmou a operação.")
            await self._carregar_operacoes_bolsa()
            await self._carregar_analise_carteira_bolsa()
            self._limpar_edicao_operacao_bolsa()
        except (XanoAPIError, ValueError) as error:
            self.bolsa_erro = str(error)

    @rx.event
    async def excluir_operacao_bolsa(self, operation_id: int):
        if not self.auth_token:
            return rx.redirect("/login")
        self.bolsa_erro = ""
        try:
            operations = [
                self._investment_operation_from_record(item)
                for item in _records(await self._api("GET", "investimentos/operacoes"))
            ]
            validate_operation_mutation(
                operations,
                excluded_operation_id=operation_id,
            )
            await self._api(
                "DELETE",
                f"investimentos/operacoes/{operation_id}",
            )
            await self._carregar_operacoes_bolsa()
            await self._carregar_analise_carteira_bolsa()
            if self.bolsa_operacao_edicao_id == operation_id:
                self._limpar_edicao_operacao_bolsa()
        except (XanoAPIError, ValueError) as error:
            self.bolsa_erro = str(error)

    @rx.event
    def sair(self):
        self._limpar_sessao()
        self.erro = ""
        self.aviso = "Você saiu da sua conta."
        return rx.redirect("/login")

    @rx.event
    def set_tipo_transacao(self, value: str):
        self.tipo_transacao = value

    @rx.event
    def set_transacao_descricao(self, value: str):
        self.transacao_descricao = value

    @rx.event
    def set_transacao_valor(self, value: str):
        self.transacao_valor = value

    @rx.event
    def formatar_transacao_valor(self):
        if not self.transacao_valor.strip():
            return
        try:
            self.transacao_valor = _formatar_entrada_reais(
                self.transacao_valor
            )
        except XanoAPIError:
            return

    @rx.event
    def set_transacao_busca(self, value: str):
        self.transacao_busca = value

    @rx.event
    def set_transacao_filtro_tipo(self, value: str):
        self.transacao_filtro_tipo = value

    @rx.event
    def set_transacao_filtro_periodo(self, value: str):
        self.transacao_filtro_periodo = value

    @rx.event
    def set_transacao_filtro_categoria(self, value: str):
        self.transacao_filtro_categoria = value

    @rx.event
    def set_transacao_filtro_conta(self, value: str):
        self.transacao_filtro_conta = value

    @rx.event
    def dispensar_notificacao(self, notificacao_id: str):
        dismissed_ids = _notificacao_ids_from_storage(
            self.notificacoes_descartadas
        )
        if notificacao_id not in dismissed_ids:
            dismissed_ids.append(notificacao_id)
            self.notificacoes_descartadas = json.dumps(
                dismissed_ids,
                separators=(",", ":"),
            )

    @rx.event
    def exportar_transacoes_csv(self):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Data", "Tipo", "Descrição", "Valor (R$)", "Categoria"])
        categorias = {
            str(categoria.get("id")): categoria.get("nome", "")
            for categoria in self.categorias
        }
        for transacao in self.transacoes_filtradas:
            centavos = int(transacao.get("valor_centavos", 0) or 0)
            valor = f"{Decimal(centavos) / 100:.2f}".replace(".", ",")
            writer.writerow([
                transacao.get("data", ""),
                transacao.get("tipo", ""),
                _csv_safe_text(transacao.get("descricao", "")),
                valor,
                _csv_safe_text(
                    categorias.get(str(transacao.get("categoria_id")), "")
                ),
            ])
        return rx.download(
            data="\ufeff" + output.getvalue(),
            filename="cashsave-transacoes.csv",
            mime_type="text/csv;charset=utf-8",
        )

    @rx.event
    def set_transacao_data(self, value: str):
        self.transacao_data = value

    @rx.event
    def set_recorrencia_descricao(self, value: str):
        self.recorrencia_descricao = value

    @rx.event
    def set_recorrencia_valor(self, value: str):
        self.recorrencia_valor = value

    @rx.event
    def formatar_recorrencia_valor(self):
        if not self.recorrencia_valor.strip():
            return
        try:
            self.recorrencia_valor = _formatar_entrada_reais(
                self.recorrencia_valor
            )
        except XanoAPIError:
            return

    @rx.event
    def set_recorrencia_tipo(self, value: str):
        self.recorrencia_tipo = value

    @rx.event
    def set_recorrencia_frequencia(self, value: str):
        self.recorrencia_frequencia = value

    @rx.event
    def set_recorrencia_proxima_data(self, value: str):
        self.recorrencia_proxima_data = value

    @rx.event
    async def criar_recorrencia(self):
        if not self.recorrencias_disponiveis:
            self.erro = (
                "Atualize as APIs do Xano para habilitar lançamentos recorrentes."
            )
            return
        descricao = self.recorrencia_descricao.strip()
        if not descricao or not self.recorrencia_proxima_data:
            self.erro = "Informe a descrição e a data da recorrência."
            return
        try:
            response = _as_record(
                await self._api(
                    "POST",
                    "recorrencias",
                    {
                        "tipo": self.recorrencia_tipo,
                        "descricao": descricao,
                        "valor_centavos": _money_to_cents(
                            self.recorrencia_valor
                        ),
                        "frequencia": self.recorrencia_frequencia,
                        "proxima_data": self.recorrencia_proxima_data,
                        "dia_referencia": int(
                            self.recorrencia_proxima_data[8:10]
                        ),
                        "mes_referencia": int(
                            self.recorrencia_proxima_data[5:7]
                        ),
                    },
                )
            )
            if "id" not in response:
                raise XanoAPIError(
                    "O Xano não confirmou a criação da recorrência."
                )
            self.recorrencias = _records_with_money(
                [*self.recorrencias, response],
                "valor_centavos",
            )
            self.recorrencia_descricao = ""
            self.recorrencia_valor = ""
            self.erro = ""
            self.aviso = "Lançamento recorrente criado."
        except (XanoAPIError, ValueError) as error:
            self.erro = str(error)

    @rx.event
    async def alternar_recorrencia(self, recorrencia_id: int):
        if not self.recorrencias_disponiveis:
            self.erro = (
                "Atualize as APIs do Xano para gerenciar recorrências."
            )
            return
        try:
            atual = next(
                (
                    item
                    for item in self.recorrencias
                    if item.get("id") == recorrencia_id
                ),
                None,
            )
            if atual is None:
                raise XanoAPIError("Recorrência não encontrada.")
            atualizada = _as_record(
                await self._api(
                    "PATCH",
                    f"recorrencias/{recorrencia_id}",
                    {"ativa": not bool(atual.get("ativa", True))},
                )
            )
            if not atualizada:
                raise XanoAPIError(
                    "O Xano não confirmou a alteração da recorrência."
                )
            self.recorrencias = [
                atualizada if item.get("id") == recorrencia_id else item
                for item in self.recorrencias
            ]
        except XanoAPIError as error:
            self.erro = str(error)

    @rx.event
    async def excluir_recorrencia(self, recorrencia_id: int):
        if not self.recorrencias_disponiveis:
            self.erro = (
                "Atualize as APIs do Xano para gerenciar recorrências."
            )
            return
        try:
            await self._api("DELETE", f"recorrencias/{recorrencia_id}")
            self.recorrencias = [
                item
                for item in self.recorrencias
                if item.get("id") != recorrencia_id
            ]
        except XanoAPIError as error:
            self.erro = str(error)

    async def _processar_recorrencias(self):
        hoje = date.today()
        for recorrencia in list(self.recorrencias):
            if not recorrencia.get("ativa", True):
                continue
            data_ocorrencia = str(recorrencia.get("proxima_data", ""))[:10]
            while data_ocorrencia and data_ocorrencia <= hoje.isoformat():
                payload = {
                    "tipo": recorrencia.get("tipo"),
                    "descricao": recorrencia.get("descricao"),
                    "valor_centavos": int(
                        recorrencia.get("valor_centavos", 0) or 0
                    ),
                    "data": data_ocorrencia,
                    "conta_id": recorrencia.get("conta_id"),
                    "categoria_id": recorrencia.get("categoria_id"),
                    "recorrencia_id": recorrencia.get("id"),
                    "recorrencia_data": data_ocorrencia,
                }
                try:
                    transacao = _as_record(
                        await self._api("POST", "transacoes", payload)
                    )
                    if "id" not in transacao:
                        raise XanoAPIError(
                            "O Xano não confirmou o lançamento recorrente."
                        )
                    self.transacoes = _records_with_money(
                        [transacao, *self.transacoes],
                        "valor_centavos",
                    )
                except XanoAPIError as error:
                    if str(error) != (
                        "Esta ocorrência recorrente já foi registrada."
                    ):
                        raise

                proxima_data = _proxima_data_recorrente(
                    data_ocorrencia,
                    str(recorrencia.get("frequencia", "")),
                    int(recorrencia.get("dia_referencia", 0) or 0),
                    int(recorrencia.get("mes_referencia", 0) or 0),
                )
                atualizada = _as_record(
                    await self._api(
                        "PATCH",
                        f"recorrencias/{recorrencia['id']}",
                        {"proxima_data": proxima_data},
                    )
                )
                if not atualizada:
                    raise XanoAPIError(
                        "O Xano não confirmou a próxima data recorrente."
                    )
                recorrencia = {
                    **recorrencia,
                    **atualizada,
                    "valor_formatado": _formatar_centavos(
                        int(atualizada.get("valor_centavos", 0) or 0)
                    ),
                }
                self.recorrencias = [
                    recorrencia
                    if item.get("id") == recorrencia.get("id")
                    else item
                    for item in self.recorrencias
                ]
                data_ocorrencia = proxima_data

    @rx.event
    def set_transacao_categoria(self, value: str):
        self.transacao_categoria = value

    @rx.event
    def set_transacao_conta(self, value: str):
        self.transacao_conta = value

    @rx.event
    async def criar_transacao(self):
        try:
            payload = {
                "tipo": self.tipo_transacao,
                "descricao": self.transacao_descricao.strip(),
                "valor_centavos": _money_to_cents(self.transacao_valor),
                "data": self.transacao_data,
                "categoria_id": int(self.transacao_categoria)
                if self.transacao_categoria
                else None,
                "conta_id": int(self.transacao_conta)
                if self.transacao_conta
                else None,
            }
            if not payload["descricao"] or not payload["data"]:
                raise XanoAPIError("Preencha descrição e data.")
            transacao = _as_record(
                await self._api("POST", "transacoes", payload)
            )
            if "id" not in transacao:
                raise XanoAPIError("O Xano não confirmou o lançamento.")
            self.transacoes = _records_with_money(
                [transacao, *self.transacoes],
                "valor_centavos",
            )
            self.transacao_descricao = ""
            self.transacao_valor = ""
        except (XanoAPIError, ValueError) as error:
            self.erro = str(error) or "Confira os dados da transação."

    @rx.event
    async def excluir_transacao(self, transacao_id: int):
        try:
            await self._api("DELETE", f"transacoes/{transacao_id}")
            self.transacoes = [
                item for item in self.transacoes if item.get("id") != transacao_id
            ]
        except XanoAPIError as error:
            self.erro = str(error)

    @rx.event
    def set_nova_categoria_nome(self, value: str):
        self.nova_categoria_nome = value

    @rx.event
    def set_nova_categoria_tipo(self, value: str):
        self.nova_categoria_tipo = value

    @rx.event
    async def criar_categoria(self):
        nome = self.nova_categoria_nome.strip()
        if not nome:
            self.erro = "Informe o nome da categoria."
            return
        try:
            categoria = _as_record(
                await self._api(
                    "POST",
                    "categorias",
                    {"nome": nome, "tipo": self.nova_categoria_tipo},
                )
            )
            if "id" not in categoria:
                raise XanoAPIError("O Xano não confirmou a categoria.")
            self.categorias = [*self.categorias, categoria]
            self.nova_categoria_nome = ""
        except XanoAPIError as error:
            self.erro = str(error)

    @rx.event
    def set_nova_conta_nome(self, value: str):
        self.nova_conta_nome = value

    @rx.event
    def set_nova_conta_tipo(self, value: str):
        self.nova_conta_tipo = value

    @rx.event
    def set_nova_conta_saldo(self, value: str):
        self.nova_conta_saldo = value

    @rx.event
    def set_nova_conta_instituicao(self, value: str):
        self.nova_conta_instituicao = value

    @rx.event
    async def criar_conta(self):
        nome = self.nova_conta_nome.strip()
        if not nome:
            self.erro = "Informe o nome da conta."
            return
        try:
            saldo = (
                int(
                    (Decimal(self.nova_conta_saldo.replace(",", ".")) * 100)
                    .quantize(Decimal("1"), rounding=ROUND_HALF_UP)
                )
                if self.nova_conta_saldo.strip()
                else 0
            )
            conta = _as_record(
                await self._api(
                    "POST",
                    "contas",
                    {
                        "nome": nome,
                        "tipo": self.nova_conta_tipo,
                        "instituicao": self.nova_conta_instituicao.strip() or None,
                        "saldo_inicial_centavos": saldo,
                    },
                )
            )
            if "id" not in conta:
                raise XanoAPIError("O Xano não confirmou a conta.")
            self.contas = _records_with_money(
                [*self.contas, conta],
                "saldo_inicial_centavos",
                "saldo_inicial_formatado",
            )
            self.nova_conta_nome = ""
            self.nova_conta_saldo = "0"
            self.nova_conta_instituicao = ""
        except (XanoAPIError, InvalidOperation) as error:
            self.erro = str(error)

    @rx.event
    def set_conta_descricao(self, value: str):
        self.conta_descricao = value

    @rx.event
    def set_conta_valor(self, value: str):
        self.conta_valor = value

    @rx.event
    def formatar_conta_valor(self):
        if not self.conta_valor.strip():
            return
        try:
            self.conta_valor = _formatar_entrada_reais(self.conta_valor)
        except XanoAPIError:
            return

    @rx.event
    def set_conta_vencimento(self, value: str):
        self.conta_vencimento = value

    @rx.event
    def set_conta_categoria(self, value: str):
        self.conta_categoria = value

    @rx.event
    async def criar_conta_a_pagar(self):
        descricao = self.conta_descricao.strip()
        if not descricao or not self.conta_vencimento:
            self.erro = "Preencha a descrição e o vencimento."
            return
        try:
            conta = _as_record(
                await self._api(
                    "POST",
                    "contas_a_pagar",
                    {
                        "descricao": descricao,
                        "valor_centavos": _money_to_cents(self.conta_valor),
                        "data_vencimento": self.conta_vencimento,
                        "categoria_id": int(self.conta_categoria)
                        if self.conta_categoria
                        else None,
                    },
                )
            )
            if "id" not in conta:
                raise XanoAPIError("O Xano não confirmou a conta a pagar.")
            self.contas_a_pagar = _records_with_money(
                [*self.contas_a_pagar, conta],
                "valor_centavos",
            )
            self.conta_descricao = ""
            self.conta_valor = ""
            self.conta_vencimento = ""
        except (XanoAPIError, ValueError) as error:
            self.erro = str(error)

    @rx.event
    async def pagar_conta(self, conta_id: int):
        try:
            conta_paga = _as_record(await self._api(
                "POST",
                f"contas_a_pagar/{conta_id}/pagar",
                {"data_pagamento": date.today().isoformat()},
            ))
            if not conta_paga:
                raise XanoAPIError("O Xano não confirmou o pagamento.")
            conta_paga_formatada = _records_with_money(
                [conta_paga],
                "valor_centavos",
            )[0]
            self.contas_a_pagar = [
                conta_paga_formatada if item.get("id") == conta_id else item
                for item in self.contas_a_pagar
            ]
        except XanoAPIError as error:
            self.erro = str(error)

    @rx.event
    async def excluir_conta_a_pagar(self, conta_id: int):
        try:
            await self._api("DELETE", f"contas_a_pagar/{conta_id}")
            self.contas_a_pagar = [
                item
                for item in self.contas_a_pagar
                if item.get("id") != conta_id
            ]
        except XanoAPIError as error:
            self.erro = str(error)

    @rx.event
    def set_orcamento_nome(self, value: str):
        self.orcamento_nome = value

    @rx.event
    def set_orcamento_limite(self, value: str):
        self.orcamento_limite = value

    @rx.event
    def set_orcamento_inicio(self, value: str):
        self.orcamento_inicio = value

    @rx.event
    def set_orcamento_fim(self, value: str):
        self.orcamento_fim = value

    @rx.event
    def set_orcamento_categoria(self, value: str):
        self.orcamento_categoria = value

    @rx.event
    async def criar_orcamento(self):
        if not self.orcamento_nome.strip() or not self.orcamento_inicio or not self.orcamento_fim:
            self.erro = "Preencha nome e período do orçamento."
            return
        try:
            orcamento = _as_record(
                await self._api(
                    "POST",
                    "orcamentos",
                    {
                        "nome": self.orcamento_nome.strip(),
                        "limite_centavos": _money_to_cents(self.orcamento_limite),
                        "data_inicio": self.orcamento_inicio,
                        "data_fim": self.orcamento_fim,
                        "categoria_id": int(self.orcamento_categoria)
                        if self.orcamento_categoria
                        else None,
                        "periodicidade": "mensal",
                    },
                )
            )
            if "id" not in orcamento:
                raise XanoAPIError("O Xano não confirmou o orçamento.")
            self.orcamentos = _records_with_money(
                [*self.orcamentos, orcamento],
                "limite_centavos",
            )
            self.orcamento_nome = ""
            self.orcamento_limite = ""
        except (XanoAPIError, ValueError) as error:
            self.erro = str(error)

    @rx.event
    async def excluir_orcamento(self, orcamento_id: int):
        try:
            await self._api("DELETE", f"orcamentos/{orcamento_id}")
            self.orcamentos = [
                item for item in self.orcamentos if item.get("id") != orcamento_id
            ]
        except XanoAPIError as error:
            self.erro = str(error)

    @rx.event
    def set_meta_nome(self, value: str):
        self.meta_nome = value

    @rx.event
    def set_meta_objetivo(self, value: str):
        self.meta_objetivo = value

    @rx.event
    def set_meta_data_alvo(self, value: str):
        self.meta_data_alvo = value

    @rx.event
    def set_meta_contribuicao(self, value: str):
        self.meta_contribuicao = value

    @rx.event
    async def contribuir_meta(self, meta_id: int):
        try:
            meta = next(
                (item for item in self.metas if item.get("id") == meta_id),
                None,
            )
            if meta is None:
                raise XanoAPIError("Meta financeira não encontrada.")
            atual = int(meta.get("valor_atual_centavos", 0) or 0)
            adicional = _money_to_cents(self.meta_contribuicao)
            objetivo = int(meta.get("valor_objetivo_centavos", 0) or 0)
            response = _as_record(
                await self._api(
                    "PATCH",
                    f"metas_financeiras/{meta_id}",
                    {
                        "valor_atual_centavos": min(atual + adicional, objetivo),
                    },
                )
            )
            if not response:
                raise XanoAPIError("O Xano não confirmou a atualização da meta.")
            self.metas = [
                response if item.get("id") == meta_id else item
                for item in self.metas
            ]
            self.meta_contribuicao = ""
            self.aviso = "Progresso da meta atualizado."
        except XanoAPIError as error:
            self.erro = str(error)

    @rx.event
    async def criar_meta(self):
        if not self.meta_nome.strip():
            self.erro = "Informe o nome da meta."
            return
        try:
            meta = _as_record(
                await self._api(
                    "POST",
                    "metas_financeiras",
                    {
                        "nome": self.meta_nome.strip(),
                        "valor_objetivo_centavos": _money_to_cents(self.meta_objetivo),
                        "valor_atual_centavos": 0,
                        "data_alvo": self.meta_data_alvo or None,
                    },
                )
            )
            if "id" not in meta:
                raise XanoAPIError("O Xano não confirmou a meta.")
            self.metas = [
                *self.metas,
                _records_with_money([meta], "valor_objetivo_centavos")[0],
            ]
            self.meta_nome = ""
            self.meta_objetivo = ""
            self.meta_data_alvo = ""
        except (XanoAPIError, ValueError) as error:
            self.erro = str(error)

    @rx.event
    async def excluir_meta(self, meta_id: int):
        try:
            await self._api("DELETE", f"metas_financeiras/{meta_id}")
            self.metas = [item for item in self.metas if item.get("id") != meta_id]
        except XanoAPIError as error:
            self.erro = str(error)

    @rx.event
    def set_moeda(self, value: str):
        self.moeda = value

    @rx.event
    def set_localidade(self, value: str):
        self.localidade = value

    @rx.event
    def set_fuso_horario(self, value: str):
        self.fuso_horario = value

    @rx.event
    def set_notificacoes_vencimento(self, value: bool):
        self.notificacoes_vencimento = value

    @rx.event
    def set_notificacoes_orcamento(self, value: bool):
        self.notificacoes_orcamento = value

    @rx.event
    def set_notificacoes_metas(self, value: bool):
        self.notificacoes_metas = value

    @rx.event
    async def enviar_foto_perfil(self, files: list[rx.UploadFile]):
        if not self.auth_token:
            self.erro = "Entre na sua conta para alterar a foto de perfil."
            return
        if not files:
            self.erro = "Selecione uma imagem para enviar."
            return
        arquivo = files[0]
        media_type = mimetypes.guess_type(arquivo.name)[0] or ""
        if media_type not in {"image/png", "image/jpeg", "image/webp"}:
            self.erro = "Use uma imagem PNG, JPG ou WebP."
            return
        try:
            conteudo = await arquivo.read()
        except OSError as error:
            raise XanoAPIError("Não foi possível ler a imagem selecionada.") from error
        if not conteudo:
            self.erro = "A imagem selecionada está vazia."
            return
        if len(conteudo) > 5 * 1024 * 1024:
            self.erro = "A foto deve ter no máximo 5 MB."
            return
        if not _imagem_corresponde_ao_tipo(conteudo, media_type):
            self.erro = "O arquivo selecionado não corresponde a uma imagem válida."
            return
        self.erro = ""
        try:
            response = _as_record(
                await self._api(
                    "POST",
                    "auth/avatar",
                    upload=("avatar", arquivo.name, conteudo),
                )
            )
            usuario = _as_record(response.get("user")) or response
            avatar_url = self._avatar_from_user(usuario)
            if not avatar_url:
                raise XanoAPIError("O Xano não retornou a URL da foto.")
            self.usuario = {**self.usuario, **usuario}
            self.avatar_url = avatar_url
            self.avatar_perfil_disponivel = True
            self.aviso = "Foto de perfil atualizada."
            return rx.clear_selected_files("profile-photo")
        except XanoAPIError as error:
            self.erro = str(error)

    @rx.event
    async def remover_foto_perfil(self):
        if not self.auth_token:
            self.erro = "Entre na sua conta para remover a foto de perfil."
            return
        try:
            response = _as_record(
                await self._api("DELETE", "auth/avatar")
            )
            if not response:
                raise XanoAPIError("O Xano não confirmou a remoção da foto.")
            self.avatar_url = ""
            self.usuario = {**self.usuario, "avatar_url": ""}
            self.aviso = "Foto de perfil removida."
        except XanoAPIError as error:
            self.erro = str(error)

    @rx.event
    async def salvar_preferencias(self):
        try:
            await self._api(
                "PATCH",
                "preferencias_usuario/me",
                {
                    "moeda": self.moeda,
                    "localidade": self.localidade,
                    "fuso_horario": self.fuso_horario,
                    "notificacoes_vencimento": self.notificacoes_vencimento,
                    "notificacoes_orcamento": self.notificacoes_orcamento,
                    "notificacoes_metas": self.notificacoes_metas,
                },
            )
            self.aviso = "Preferências salvas."
        except XanoAPIError as error:
            self.erro = str(error)

    @rx.event
    def carregar_onboarding(self):
        self._carregar_onboarding_local()

    @rx.event
    def atualizar_onboarding(self, chave: str, valor: object):
        if chave == "objetivos":
            if not isinstance(valor, list):
                valor = [valor]
        self.onboarding_respostas[chave] = valor
        self._salvar_onboarding_local()
        if self.onboarding_respostas:
            self._atualizar_perfil_investidor()

    @rx.event
    def avancar_onboarding(self):
        if self.onboarding_etapa < 5:
            self.onboarding_etapa += 1
        else:
            self.onboarding_concluido = True
        self._salvar_onboarding_local()

    @rx.event
    def voltar_onboarding(self):
        if self.onboarding_etapa > 0:
            self.onboarding_etapa -= 1
        self._salvar_onboarding_local()

    @rx.event
    def pular_onboarding(self):
        if self.onboarding_etapa < 5:
            self.onboarding_etapa += 1
        else:
            self.onboarding_concluido = True
        self._salvar_onboarding_local()

    @rx.event
    def finalizar_onboarding(self):
        self.onboarding_concluido = True
        self.onboarding_etapa = 5
        self._atualizar_perfil_investidor()
        self._salvar_onboarding_local()

    @rx.event
    def reiniciar_onboarding(self):
        self.onboarding_respostas = {}
        self.onboarding_etapa = 0
        self.onboarding_concluido = False
        self.investidor_perfil = "Ainda não avaliado"
        self.investidor_descricao = (
            "Complete o onboarding para entender melhor o seu perfil de investidor."
        )
        self.investidor_pontos_atencao = (
            "Use a avaliação como referência de contexto para o Jarvis e as metas financeiras."
        )
        self._salvar_onboarding_local()

    @rx.event
    def set_assistente_mensagem(self, value: str):
        self.assistente_mensagem = value

    @rx.event
    def nova_conversa_assistente(self):
        self.assistente_conversa_id = 0
        self.assistente_mensagens = [
            {
                "tipo": "ia",
                "texto": (
                    "Olá! Sou o Jarvis do CashSave. "
                    "Como posso ajudar você a organizar suas finanças?"
                ),
            }
        ]
        self.assistente_mensagem = ""
        self.erro = ""
        self._persistir_conversas_assistente()

    @rx.event
    async def carregar_conversas_assistente(self):
        if not self.auth_token:
            return rx.redirect("/login")
        resultado = await self._carregar_dados()
        if resultado is not None:
            return resultado
        conversas, active_id = _conversas_assistente_do_storage(
            self.assistente_conversas_storage,
            self._assistente_owner_key(),
        )
        self.assistente_conversas = conversas
        self.assistente_conversa_id = active_id
        if active_id:
            conversa = next(
                item for item in conversas if int(item["id"]) == active_id
            )
            self.assistente_mensagens = list(conversa["messages"])
        else:
            self.assistente_mensagens = [
                {
                    "tipo": "ia",
                    "texto": (
                        "Olá! Sou o Jarvis do CashSave. "
                        "Como posso ajudar você a organizar suas finanças?"
                    ),
                }
            ]
        self.erro = ""

    @rx.event
    def abrir_conversa_assistente(self, conversation_id: int):
        conversa = next(
            (
                item
                for item in self.assistente_conversas
                if int(item.get("id", 0)) == conversation_id
            ),
            None,
        )
        if conversa is None:
            self.erro = "Conversa local não encontrada."
            return
        self.assistente_conversa_id = conversation_id
        self.assistente_mensagens = list(conversa.get("messages", []))
        self.erro = ""

    @rx.event
    async def enviar_mensagem_assistente(self):
        texto = self.assistente_mensagem.strip()
        if not texto:
            return
        if not self.auth_token:
            self.erro = "Entre na sua conta para conversar com o assistente."
            return

        self.assistente_carregando = True
        self.erro = ""
        download_event = None
        try:
            pending_bill = None
            last_message = (
                self.assistente_mensagens[-1]
                if self.assistente_mensagens
                else {}
            )
            last_answer = str(last_message.get("texto", "")).casefold()
            if last_message.get("tipo") == "ia" and any(
                phrase in last_answer
                for phrase in (
                    "qual é a descrição da conta",
                    "qual é o valor da conta",
                    "qual é o valor dessa conta",
                    "qual é a data de vencimento dessa conta",
                )
            ):
                previous_user_message = next(
                    (
                        str(message.get("texto", ""))
                        for message in reversed(self.assistente_mensagens[:-1])
                        if message.get("tipo") == "usuario"
                    ),
                    "",
                )
                if previous_user_message:
                    pending_bill = parse_payable_bill(
                        previous_user_message,
                        self.categorias,
                        self.contas,
                    )

            parsed_bill = parse_payable_bill(
                texto,
                self.categorias,
                self.contas,
            )
            if parsed_bill is None and pending_bill is not None:
                parsed_bill = complete_payable_bill(
                    pending_bill,
                    texto,
                    self.categorias,
                    self.contas,
                )

            if parsed_bill is not None:
                if not parsed_bill.description:
                    response = {
                        "answer": (
                            "Qual é a descrição da conta? Por exemplo: "
                            "luz, água ou internet."
                        ),
                        "facts": [],
                        "calculations": [],
                        "estimates": [],
                    }
                elif parsed_bill.value_centavos is None:
                    response = {
                        "answer": "Qual é o valor dessa conta?",
                        "facts": [],
                        "calculations": [],
                        "estimates": [],
                    }
                elif parsed_bill.data_vencimento is None:
                    response = {
                        "answer": (
                            "Qual é a data de vencimento dessa conta? "
                            "Pode informar, por exemplo, 10/11/2026."
                        ),
                        "facts": [],
                        "calculations": [],
                        "estimates": [],
                    }
                else:
                    try:
                        bill = _as_record(
                            await self._api(
                                "POST",
                                "contas_a_pagar",
                                {
                                    "descricao": parsed_bill.description,
                                    "valor_centavos": parsed_bill.value_centavos,
                                    "data_vencimento": parsed_bill.data_vencimento,
                                    "categoria_id": parsed_bill.categoria_id,
                                    "conta_id": parsed_bill.conta_id,
                                },
                            )
                        )
                        if "id" not in bill:
                            raise XanoAPIError(
                                "O Xano não confirmou a conta a pagar."
                            )
                    except XanoAPIError as error:
                        response = {
                            "answer": (
                                "Não consegui confirmar o cadastro da conta "
                                f"'{parsed_bill.description}' no Xano: {error}"
                            ),
                            "facts": [],
                            "calculations": [],
                            "estimates": [],
                        }
                    else:
                        self.contas_a_pagar = _records_with_money(
                            [*self.contas_a_pagar, bill],
                            "valor_centavos",
                        )
                        response = {
                            "answer": (
                                f"Conta a pagar cadastrada: "
                                f"{parsed_bill.description}, "
                                f"{_formatar_centavos(parsed_bill.value_centavos)}, "
                                f"com vencimento em "
                                f"{parsed_bill.data_vencimento}."
                            ),
                            "facts": [],
                            "calculations": [],
                            "estimates": [],
                        }
            else:
                parsed_transactions = parse_transaction_batch(
                    texto,
                    self.categorias,
                    self.contas,
                )
            if parsed_bill is None and parsed_transactions:
                confirmed = []
                failed_transaction = None
                failure_message = ""
                for parsed_transaction in parsed_transactions:
                    payload = {
                        "tipo": parsed_transaction.tipo,
                        "descricao": parsed_transaction.description,
                        "valor_centavos": parsed_transaction.value_centavos,
                        "data": parsed_transaction.data,
                        "categoria_id": parsed_transaction.categoria_id,
                        "conta_id": parsed_transaction.conta_id,
                    }
                    try:
                        transaction = _as_record(
                            await self._api("POST", "transacoes", payload)
                        )
                        if "id" not in transaction:
                            raise XanoAPIError(
                                "O Xano não confirmou o lançamento."
                            )
                    except XanoAPIError as error:
                        failed_transaction = parsed_transaction
                        failure_message = str(error)
                        break
                    confirmed.append(transaction)
                    self.transacoes = _records_with_money(
                        [transaction, *self.transacoes],
                        "valor_centavos",
                    )

                if failed_transaction is not None:
                    failed_kind = (
                        "receita"
                        if failed_transaction.tipo == "receita"
                        else "despesa"
                    )
                    if confirmed:
                        answer = (
                            f"Cadastrei apenas {len(confirmed)} de "
                            f"{len(parsed_transactions)} lançamentos. Falhou "
                            f"a {failed_kind} '{failed_transaction.description}': "
                            f"{failure_message}. Não calculei o saldo do conjunto "
                            "porque nem todos os lançamentos foram confirmados."
                        )
                    else:
                        answer = (
                            f"Não consegui cadastrar a {failed_kind} "
                            f"'{failed_transaction.description}': {failure_message}"
                        )
                    response = {
                        "answer": answer,
                        "facts": [],
                        "calculations": [],
                        "estimates": [],
                    }
                else:
                    income_total = sum(
                        transaction.value_centavos
                        for transaction in parsed_transactions
                        if transaction.tipo == "receita"
                    )
                    expense_total = sum(
                        transaction.value_centavos
                        for transaction in parsed_transactions
                        if transaction.tipo == "despesa"
                    )
                    balance = income_total - expense_total
                    response = {
                        "answer": (
                            f"Todos os {len(parsed_transactions)} lançamentos "
                            "foram confirmados pelo Xano. "
                            f"Receitas informadas: {_formatar_centavos(income_total)}; "
                            f"despesas informadas: {_formatar_centavos(expense_total)}. "
                            "Saldo deste conjunto de lançamentos: "
                            f"{_formatar_centavos(balance)} "
                            "(receitas menos despesas)."
                        ),
                        "facts": [],
                        "calculations": [],
                        "estimates": [],
                    }
            elif parsed_bill is None and is_expense_pdf_request(texto):
                expenses, total = expense_report_data(
                    self.transacoes,
                    self.categorias,
                )
                pdf_bytes = generate_expense_pdf(
                    self.transacoes,
                    self.categorias,
                )
                response = {
                    "answer": "Gerei o relatório em PDF e iniciei o download.",
                    "facts": [
                        f"Despesas incluídas: {len(expenses)}.",
                    ],
                    "calculations": [
                        f"Total de despesas: {_formatar_centavos(total)}.",
                    ],
                    "estimates": [],
                }
                download_event = rx.download(
                    data=pdf_bytes,
                    filename=f"relatorio-despesas-{date.today().isoformat()}.pdf",
                    mime_type="application/pdf",
                )
            elif parsed_bill is None:
                investment_terms = {
                    "investimento",
                    "investimentos",
                    "carteira",
                    "provento",
                    "ação",
                    "acoes",
                    "ações",
                    "fii",
                    "etf",
                    "cotação",
                    "cotacao",
                    "rentabilidade",
                    "posição",
                    "posicao",
                    "comprar",
                    "vender",
                }
                investment_words = set(re.findall(r"\w+", texto.casefold()))
                investment_context = None
                if (
                    getattr(self, "bolsa_ativo_selecionado", "")
                    or investment_words.intersection(investment_terms)
                    or any(
                        phrase in texto.casefold()
                        for phrase in (
                            "resultado realizado",
                            "resultado não realizado",
                        )
                    )
                    or re.search(r"\b[A-Z]{4,5}\d{1,2}\b", texto.upper())
                ):
                    investment_context = (
                        await self._contexto_investimentos_jarvis()
                    )
                context_service = FinancialContextService(
                    transactions=self.transacoes,
                    accounts=self.contas,
                    categories=self.categorias,
                    bills=self.contas_a_pagar,
                    budgets=self.orcamentos,
                    goals=self.metas,
                    recurring=self.recorrencias,
                    investment_context=investment_context,
                )
                history = [
                    {
                        "role": "user" if item.get("tipo") == "usuario" else "assistant",
                        "content": str(item.get("texto", "")),
                    }
                    for item in self.assistente_mensagens[-8:]
                ]
                response = await asyncio.to_thread(
                    FinancialOrchestrator().answer,
                    texto,
                    history,
                    context_service,
                )
            answer = str(response["answer"])
            details = []
            for label, key in (
                ("Fatos observados", "facts"),
                ("Cálculos", "calculations"),
                ("Estimativas e limites", "estimates"),
            ):
                values = response.get(key, [])
                if values:
                    details.append(f"{label}:\n- " + "\n- ".join(str(value) for value in values))
            if details:
                answer = answer + "\n\n" + "\n\n".join(details)

            if not self.assistente_conversa_id:
                existing_ids = [
                    int(item.get("id", 0))
                    for item in self.assistente_conversas
                    if str(item.get("id", "")).isdigit()
                ]
                self.assistente_conversa_id = max(existing_ids, default=0) + 1
            mensagens = [
                *self.assistente_mensagens,
                {"tipo": "usuario", "texto": texto},
                {"tipo": "ia", "texto": answer},
            ]
            conversa = {
                "id": self.assistente_conversa_id,
                "title": texto[:60],
                "messages": mensagens[-20:],
            }
            self.assistente_conversas = [
                item
                for item in self.assistente_conversas
                if int(item.get("id", 0)) != self.assistente_conversa_id
            ]
            self.assistente_conversas = [
                conversa,
                *self.assistente_conversas,
            ][
                :8
            ]
            self.assistente_mensagens = mensagens[-20:]
            self.assistente_mensagem = ""
            self._persistir_conversas_assistente()
        except (OllamaError, ExpenseCommandError, XanoAPIError) as error:
            self.erro = str(error)
        except (KeyError, TypeError, ValueError) as error:
            self.erro = "A resposta da IA local não pôde ser processada."
            raise RuntimeError("Resposta inválida da IA local.") from error
        finally:
            self.assistente_carregando = False
        if download_event is not None:
            return download_event
