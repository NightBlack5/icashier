import asyncio
import json
import os
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from urllib.parse import urlsplit
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import reflex as rx


API_BASE_URL = os.getenv("CASH_SAVE_API_URL", "").rstrip("/")


class XanoAPIError(Exception):
    pass


def _send_request(
    method: str,
    path: str,
    payload: dict | None,
    token: str = "",
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

    body = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Accept": "application/json"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = f"Bearer {token}"

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
        message = (
            detail.get("message")
            or detail.get("error")
            or f"Xano respondeu com HTTP {error.code}."
        )
        raise XanoAPIError(str(message)) from error
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
    try:
        amount = Decimal(value.replace(",", ".").strip())
    except InvalidOperation as error:
        raise XanoAPIError("Informe um valor monetário válido.") from error
    if not amount.is_finite() or amount <= 0:
        raise XanoAPIError("O valor deve ser maior que zero.")
    return int(
        (amount * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    )


class AppState(rx.State):
    auth_token: str = rx.Cookie(
        "",
        name="cashsave_auth",
        max_age=86400,
        same_site="strict",
        secure=os.getenv("CASH_SAVE_COOKIE_SECURE", "true").lower() == "true",
    )
    usuario: dict[str, str] = {}
    auth_email: str = ""
    auth_email_salvo: str = rx.LocalStorage(
        "",
        name="cashsave_remembered_email",
    )
    lembrar_email: str = rx.LocalStorage(
        "true",
        name="cashsave_remember_email",
    )
    auth_password: str = ""
    auth_name: str = ""
    senha_visivel: bool = False
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
    moeda: str = "BRL"
    localidade: str = "pt-BR"
    fuso_horario: str = "America/Sao_Paulo"
    notificacoes_vencimento: bool = True
    notificacoes_orcamento: bool = True
    assistente_conversas: list[dict] = []
    assistente_conversa_id: int = 0
    assistente_mensagens: list[dict[str, str]] = [
        {
            "tipo": "ia",
            "texto": (
                "Olá! Sou o assistente do CashSave. "
                "Como posso ajudar você a organizar suas finanças?"
            ),
        }
    ]
    assistente_mensagem: str = ""
    assistente_carregando: bool = False

    @rx.var
    def autenticado(self) -> bool:
        return bool(self.auth_token)

    @rx.var
    def nome_usuario(self) -> str:
        return self.usuario.get("name", "Minha conta")

    @rx.var
    def email_usuario(self) -> str:
        return self.usuario.get("email", "")

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

    async def _api(
        self,
        method: str,
        path: str,
        payload: dict | None = None,
    ) -> object:
        return await asyncio.to_thread(
            _send_request,
            method,
            path,
            payload,
            self.auth_token,
        )

    @rx.event
    def set_auth_email(self, value: str):
        self.auth_email = value
        if self.lembrar_email == "true":
            self.auth_email_salvo = value
        self.erro = ""

    @rx.event
    def set_lembrar_email(self, value: bool):
        if not value and not self.auth_email and self.auth_email_salvo:
            self.auth_email = self.auth_email_salvo
        self.lembrar_email = "true" if value else "false"
        self.auth_email_salvo = self.auth_email if value else ""

    @rx.event
    def set_auth_password(self, value: str):
        self.auth_password = value
        self.erro = ""

    @rx.event
    def alternar_visibilidade_senha(self):
        self.senha_visivel = not self.senha_visivel

    @rx.event
    def set_auth_name(self, value: str):
        self.auth_name = value
        self.erro = ""

    @rx.event
    def alternar_cadastro(self):
        self.cadastro = not self.cadastro
        self.erro = ""

    @rx.event
    def login_google(self):
        self.erro = "O login com Google ainda não está configurado."

    @rx.event
    async def autenticar(self):
        self.carregando = True
        self.erro = ""
        try:
            if self.cadastro:
                response = _as_record(
                    await self._api(
                        "POST",
                        "auth/signup",
                        {
                            "name": self.auth_name.strip(),
                            "email": self.auth_email.strip(),
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
                            "email": self.auth_email.strip(),
                            "password": self.auth_password,
                        },
                    )
                )
            token = response.get("authToken")
            if not token:
                raise XanoAPIError("O Xano não retornou um token de sessão.")
            self.auth_token = str(token)
            self.usuario = _as_record(response.get("user"))
            self.auth_password = ""
            await self.carregar_dados()
        except XanoAPIError as error:
            self.erro = str(error)
        finally:
            self.carregando = False

    @rx.event
    async def carregar_dados(self):
        if not self.auth_token:
            return
        self.carregando = True
        self.erro = ""
        try:
            respostas = await asyncio.gather(
                self._api("GET", "auth/me"),
                self._api("GET", "transacoes"),
                self._api("GET", "contas"),
                self._api("GET", "categorias"),
                self._api("GET", "contas_a_pagar"),
                self._api("GET", "orcamentos"),
                self._api("GET", "metas_financeiras"),
                self._api("GET", "preferencias_usuario/me"),
            )
            self.usuario = _as_record(respostas[0])
            self.transacoes = _records_with_money(
                respostas[1],
                "valor_centavos",
            )
            self.contas = _records_with_money(
                respostas[2],
                "saldo_inicial_centavos",
                "saldo_inicial_formatado",
            )
            self.categorias = _records(respostas[3])
            self.contas_a_pagar = _records_with_money(
                respostas[4],
                "valor_centavos",
            )
            self.orcamentos = _records_with_money(
                respostas[5],
                "limite_centavos",
            )
            self.metas = _records_with_money(
                respostas[6],
                "valor_objetivo_centavos",
            )
            self.preferencias = _as_record(respostas[7])
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
        except XanoAPIError as error:
            self.erro = str(error)
            if "401" in str(error) or "autentica" in str(error).lower():
                self.auth_token = ""
                self.usuario = {}
                self.assistente_conversas = []
                self.assistente_conversa_id = 0
                self.assistente_mensagens = []
        finally:
            self.carregando = False

    @rx.event
    def sair(self):
        self.auth_token = ""
        self.usuario = {}
        self.transacoes = []
        self.contas = []
        self.categorias = []
        self.contas_a_pagar = []
        self.orcamentos = []
        self.metas = []
        self.assistente_conversas = []
        self.assistente_conversa_id = 0
        self.assistente_mensagens = []
        self.assistente_mensagem = ""
        self.auth_password = ""
        self.aviso = "Você saiu da sua conta."

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
    def set_transacao_data(self, value: str):
        self.transacao_data = value

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
            await self._api("POST", "transacoes", payload)
            self.transacao_descricao = ""
            self.transacao_valor = ""
            await self.carregar_dados()
        except (XanoAPIError, ValueError) as error:
            self.erro = str(error) or "Confira os dados da transação."

    @rx.event
    async def excluir_transacao(self, transacao_id: int):
        try:
            await self._api("DELETE", f"transacoes/{transacao_id}")
            await self.carregar_dados()
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
            await self._api(
                "POST",
                "categorias",
                {"nome": nome, "tipo": self.nova_categoria_tipo},
            )
            self.nova_categoria_nome = ""
            await self.carregar_dados()
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
            self.nova_conta_nome = ""
            self.nova_conta_saldo = "0"
            self.nova_conta_instituicao = ""
            await self.carregar_dados()
        except (XanoAPIError, InvalidOperation) as error:
            self.erro = str(error)

    @rx.event
    def set_conta_descricao(self, value: str):
        self.conta_descricao = value

    @rx.event
    def set_conta_valor(self, value: str):
        self.conta_valor = value

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
            self.conta_descricao = ""
            self.conta_valor = ""
            self.conta_vencimento = ""
            await self.carregar_dados()
        except (XanoAPIError, ValueError) as error:
            self.erro = str(error)

    @rx.event
    async def pagar_conta(self, conta_id: int):
        try:
            await self._api(
                "POST",
                f"contas_a_pagar/{conta_id}/pagar",
                {"data_pagamento": date.today().isoformat()},
            )
            await self.carregar_dados()
        except XanoAPIError as error:
            self.erro = str(error)

    @rx.event
    async def excluir_conta_a_pagar(self, conta_id: int):
        try:
            await self._api("DELETE", f"contas_a_pagar/{conta_id}")
            await self.carregar_dados()
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
            self.orcamento_nome = ""
            self.orcamento_limite = ""
            await self.carregar_dados()
        except (XanoAPIError, ValueError) as error:
            self.erro = str(error)

    @rx.event
    async def excluir_orcamento(self, orcamento_id: int):
        try:
            await self._api("DELETE", f"orcamentos/{orcamento_id}")
            await self.carregar_dados()
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
    async def criar_meta(self):
        if not self.meta_nome.strip():
            self.erro = "Informe o nome da meta."
            return
        try:
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
            self.meta_nome = ""
            self.meta_objetivo = ""
            self.meta_data_alvo = ""
            await self.carregar_dados()
        except (XanoAPIError, ValueError) as error:
            self.erro = str(error)

    @rx.event
    async def excluir_meta(self, meta_id: int):
        try:
            await self._api("DELETE", f"metas_financeiras/{meta_id}")
            await self.carregar_dados()
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
                },
            )
            self.aviso = "Preferências salvas."
            await self.carregar_dados()
        except XanoAPIError as error:
            self.erro = str(error)

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
                    "Olá! Sou o assistente do CashSave. "
                    "Como posso ajudar você a organizar suas finanças?"
                ),
            }
        ]
        self.assistente_mensagem = ""
        self.erro = ""

    @rx.event
    async def carregar_conversas_assistente(self):
        if not self.auth_token:
            return
        try:
            response = await self._api("GET", "assistente/conversas")
            self.assistente_conversas = _records(response)
        except XanoAPIError as error:
            self.erro = str(error)

    @rx.event
    async def abrir_conversa_assistente(self, conversation_id: int):
        try:
            response = _as_record(
                await self._api(
                    "GET",
                    f"assistente/conversas/{conversation_id}",
                )
            )
            messages = response.get("messages", [])
            self.assistente_conversa_id = conversation_id
            self.assistente_mensagens = [
                {
                    "tipo": "usuario" if item.get("role") == "user" else "ia",
                    "texto": _message_text(item.get("content")),
                }
                for item in messages
                if isinstance(item, dict)
                and item.get("role") in {"user", "assistant"}
            ]
            if not self.assistente_mensagens:
                self.assistente_mensagens = [
                    {
                        "tipo": "ia",
                        "texto": "Esta conversa ainda não tem mensagens.",
                    }
                ]
            self.erro = ""
        except XanoAPIError as error:
            self.erro = str(error)

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
        try:
            response = _as_record(
                await self._api(
                    "POST",
                    "assistente/conversation",
                    {
                        "conversation_id": self.assistente_conversa_id or None,
                        "message": texto,
                    },
                )
            )
            conversation_id = response.get("conversation_id")
            answer = _message_text(response.get("result"))
            if not conversation_id or not answer:
                raise XanoAPIError(
                    "O assistente não retornou uma resposta válida."
                )
            self.assistente_conversa_id = int(conversation_id)
            self.assistente_mensagens.extend(
                [
                    {"tipo": "usuario", "texto": texto},
                    {"tipo": "ia", "texto": answer},
                ]
            )
            self.assistente_mensagem = ""
            await self.carregar_conversas_assistente()
        except XanoAPIError as error:
            self.erro = str(error)
        finally:
            self.assistente_carregando = False
