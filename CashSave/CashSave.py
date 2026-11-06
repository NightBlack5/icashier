import reflex as rx

from .components.layout import app_layout
from .pages.assistente import assistente
from .pages.apoiar import conteudo_apoiar
from .pages.calendario import calendario_page
from .pages.financas import financas
from .pages.landing import landing_page
from .pages.sobre import conteudo_sobre
from .pages.suporte import conteudo_suporte
from .pages.auth import auth_page, cadastro_page, login_page
from .state import AppState


# ============================================================
# MENU
# ============================================================

MENU = [
    ("Visão Geral", "layout-dashboard", "/app"),
    ("Jarvis", "bot", "/assistente"),
    ("Finanças", "trending-up", "/financas"),
    ("Calendário", "calendar", "/calendario"),
    ("Preferências", "settings", "/perfil"),
    ("Sobre", "info", "/sobre"),
    ("Suporte", "life-buoy", "/suporte"),
    ("Apoiar o CashSave", "heart", "/apoiar"),
]


# ============================================================
# ITEM DO MENU
# ============================================================

def item_menu(
    texto: str,
    icone: str,
    rota: str,
    ativa: bool,
) -> rx.Component:

    return rx.link(
        rx.hstack(
            rx.icon(
                tag=icone,
                size=18,
            ),

            rx.text(
                texto,
                size="3",
                weight="medium",
            ),

            spacing="3",
            align="center",
            padding="0.6em 0.8em",
            width="100%",
            border_radius="8px",

            background=(
                "var(--green-3)"
                if ativa
                else "transparent"
            ),

            _hover={
                "background": (
                    "var(--green-4)"
                    if ativa
                    else "var(--gray-4)"
                )
            },
        ),

        href=rota,
        width="100%",

        color=(
            "var(--green-11)"
            if ativa
            else "var(--gray-12)"
        ),

        text_decoration="none",
    )


# ============================================================
# BARRA LATERAL
# ============================================================

def sidebar(rota_atual: str) -> rx.Component:

    return rx.vstack(

        # Logo
        rx.hstack(
            rx.icon(
                tag="piggy-bank",
                size=26,
                color="var(--green-9)",
            ),

            rx.heading(
                "CashSave",
                size="6",
            ),

            align="center",
            spacing="2",
            padding="0.7em 0.9em",
        ),

        rx.divider(),

        # Menu
        *[
            item_menu(
                texto,
                icone,
                rota,
                rota == rota_atual,
            )
            for texto, icone, rota in MENU
        ],

        rx.spacer(),

        rx.divider(),

        # Usuário
        rx.box(
            rx.hstack(
                rx.avatar(
                    src=AppState.avatar_url,
                    fallback="U",
                    size="2",
                    radius="full",
                ),

                rx.text(
                    AppState.nome_usuario,
                    size="2",
                    weight="medium",
                    title=AppState.nome_usuario,
                    flex="1",
                    min_width="0",
                    overflow="hidden",
                    text_overflow="ellipsis",
                    white_space="nowrap",
                ),

                align="center",
                spacing="3",
                width="100%",
                min_width="0",
            ),

            width="100%",
            padding="0.65em 0.8em",
            border_radius="10px",
            background="var(--gray-3)",
        ),

        rx.button(
            "Sair",
            on_click=AppState.sair,
            variant="soft",
            color_scheme="gray",
            width="100%",
            justify_content="center",
        ),

        spacing="2",
        align="start",

        width="250px",
        height="100vh",

        flex_shrink="0",

        padding="1em",

        border_right="1px solid rgba(148, 163, 184, 0.18)",
        background="linear-gradient(180deg, #0f1318 0%, #111923 100%)",

        position="sticky",
        top="0",
    )


# ============================================================
# LAYOUT PRINCIPAL
# ============================================================

def page_layout(
    rota_atual: str,
    *conteudo: rx.Component,
) -> rx.Component:
    return app_layout(rota_atual, *conteudo)


# ============================================================
# CABEÇALHO
# ============================================================

def cabecalho(
    titulo: str,
    subtitulo: str = "",
) -> rx.Component:

    return rx.vstack(

        rx.heading(
            titulo,
            size="8",
        ),

        rx.text(
            subtitulo,
            color_scheme="gray",
        ),

        spacing="1",
        align="start",
    )


# ============================================================
# ÍCONE COLORIDO
# ============================================================

def icone_colorido(
    icone: str,
    cor: str,
) -> rx.Component:

    return rx.center(

        rx.icon(
            tag=icone,
            size=18,
            color=f"var(--{cor}-9)",
        ),

        width="40px",
        height="40px",

        border_radius="10px",

        background=f"var(--{cor}-3)",
    )


# ============================================================
# CARTÃO DE RESUMO
# ============================================================

def cartao_resumo(
    titulo: str,
    valor: str | rx.Var[str],
    legenda: str,
    icone: str,
    cor: str,
) -> rx.Component:

    return rx.card(

        rx.hstack(

            rx.vstack(

                rx.text(
                    titulo,
                    size="2",
                    color="rgba(226,232,240,0.7)",
                ),

                rx.heading(
                    valor,
                    size="6",
                    color="white",
                ),

                rx.text(
                    legenda,
                    size="1",
                    color="rgba(148,163,184,0.9)",
                ),

                spacing="1",
                align="start",
            ),

            rx.spacer(),

            icone_colorido(
                icone,
                cor,
            ),

            align="start",
            width="100%",
        ),

        width="100%",
        background="linear-gradient(180deg, rgba(17,24,39,0.96), rgba(15,23,42,0.96))",
        border="1px solid rgba(148, 163, 184, 0.15)",
        border_radius="16px",
        padding="1.1em",
    )


# ============================================================
# GRÁFICO
# ============================================================

def grafico_visao_geral() -> rx.Component:

    return rx.card(

        rx.vstack(

            rx.hstack(

                rx.vstack(

                    rx.heading(
                        "Visão Geral",
                        size="4",
                    ),

                    rx.text(
                        "Últimos 6 meses",
                        size="2",
                        color="rgba(148,163,184,0.9)",
                    ),

                    spacing="0",
                    align="start",
                ),

                rx.spacer(),

                rx.hstack(

                    rx.badge(
                        "Receitas",
                        color_scheme="green",
                        variant="soft",
                    ),

                    rx.badge(
                        "Despesas",
                        color_scheme="red",
                        variant="soft",
                    ),

                    spacing="2",
                ),

                width="100%",
                align="start",
            ),

            rx.recharts.area_chart(

                rx.recharts.cartesian_grid(
                    stroke_dasharray="3 3",
                ),

                rx.recharts.area(
                    data_key="receitas",
                    type_="monotone",
                    stroke="#10b981",
                    fill="#10b981",
                    fill_opacity=0.15,
                ),

                rx.recharts.area(
                    data_key="despesas",
                    type_="monotone",
                    stroke="#ef4444",
                    fill="#ef4444",
                    fill_opacity=0.10,
                ),

                rx.recharts.x_axis(
                    data_key="mes",
                ),

                rx.recharts.y_axis(),

                rx.recharts.tooltip(),

                data=AppState.grafico_financeiro,

                width="100%",
                height=300,
            ),

            spacing="4",
            width="100%",
        ),

        width="100%",
        background="linear-gradient(180deg, rgba(13,17,23,0.96), rgba(17,24,39,0.96))",
        border="1px solid rgba(148,163,184,0.15)",
        border_radius="18px",
        padding="1.2em",
    )


# ============================================================
# PRÓXIMOS VENCIMENTOS
# ============================================================

def proximos_vencimentos() -> rx.Component:

    return rx.card(

        rx.vstack(

            rx.hstack(

                rx.vstack(

                    rx.heading(
                        "Próximos Vencimentos",
                        size="4",
                    ),

                    rx.text(
                        "Contas a pagar",
                        size="2",
                        color="rgba(148,163,184,0.9)",
                    ),

                    spacing="0",
                    align="start",
                ),

                rx.spacer(),

                rx.link(
                    "Ver todas",
                    href="/calendario",
                    size="2",
                ),

                width="100%",
                align="start",
            ),

            rx.cond(
                AppState.contas_proximas.length() > 0,
                rx.vstack(
                    rx.foreach(
                        AppState.contas_proximas,
                        lambda item: rx.hstack(
                            rx.vstack(
                                rx.text(item["descricao"], weight="medium"),
                                rx.text(
                                    item["data_vencimento"],
                                    size="1",
                                    color_scheme="gray",
                                ),
                                spacing="0",
                                align="start",
                            ),
                            rx.spacer(),
                            rx.text(item["valor_formatado"], size="2", weight="bold"),
                            width="100%",
                            padding_y="0.5em",
                            border_bottom="1px solid var(--gray-5)",
                        ),
                    ),
                    rx.text(
                        "Total pendente: " + AppState.proximo_vencimento_total,
                        weight="bold",
                        color="var(--red-9)",
                        margin_top="0.5em",
                    ),
                    width="100%",
                    spacing="2",
                ),
                rx.center(
                    rx.vstack(
                        rx.icon(tag="circle-check", size=28),
                        rx.text("Nenhuma conta próxima", weight="medium"),
                        rx.text("Você está em dia!", size="2", color_scheme="gray"),
                        align="center",
                        spacing="2",
                    ),
                    width="100%",
                    padding_y="2em",
                ),
            ),

            spacing="4",
            width="100%",
        ),

        width="100%",
        background="linear-gradient(180deg, rgba(13,17,23,0.96), rgba(17,24,39,0.96))",
        border="1px solid rgba(148,163,184,0.15)",
        border_radius="18px",
        padding="1.2em",
    )


# ============================================================
# ATALHO
# ============================================================

def atalho(
    titulo: str,
    descricao: str,
    icone: str,
    cor: str,
    rota: str,
) -> rx.Component:

    return rx.link(

        rx.card(

            rx.hstack(

                rx.center(

                    rx.icon(
                        tag=icone,
                        size=20,
                        color="white",
                    ),

                    width="42px",
                    height="42px",

                    border_radius="10px",

                    background=f"var(--{cor}-9)",
                ),

                rx.vstack(

                    rx.text(
                        titulo,
                        size="3",
                        weight="bold",
                    ),

                    rx.text(
                        descricao,
                        size="2",
                        color_scheme="gray",
                    ),

                    spacing="0",
                    align="start",
                ),

                rx.spacer(),

                rx.icon(
                    tag="chevron-right",
                    size=18,
                ),

                align="center",
                width="100%",
            ),

            width="100%",
        ),

        href=rota,
        width="100%",

        color="var(--gray-12)",
        text_decoration="none",
    )


# ============================================================
# BANNER DA IA
# ============================================================

def banner_ia() -> rx.Component:

    return rx.box(

        rx.hstack(

            rx.center(

                rx.icon(
                    tag="bot",
                    size=32,
                    color="white",
                ),

                width="64px",
                height="64px",

                border_radius="14px",

                background="rgba(255,255,255,0.15)",
            ),

            rx.vstack(

                rx.heading(
                    "Converse com nossa IA Financeira",
                    size="6",
                    color="white",
                ),

                rx.text(
                    "Receba dicas personalizadas, simule cenários "
                    "e organize melhor suas finanças com ajuda inteligente.",
                    size="3",
                    color="white",
                ),

                spacing="1",
                align="start",
            ),

            rx.spacer(),

            rx.link(

                rx.button(
                    "Começar agora",
                    variant="solid",
                    color_scheme="gray",
                    width=rx.breakpoints(initial="100%", lg="auto"),
                ),

                href="/assistente",
                width=rx.breakpoints(initial="100%", lg="auto"),
            ),

            align="center",
            spacing="4",
            width="100%",
            flex_direction=rx.breakpoints(initial="column", lg="row"),
        ),

        background="linear-gradient(90deg, #0f9d7a, #0e7490)",

        border_radius="16px",

        padding="1.5em",

        width="100%",
    )


# ============================================================
# DASHBOARD
# ============================================================

def dashboard_conteudo() -> rx.Component:
    return page_layout(

        "/app",

        cabecalho(
            rx.cond(
                AppState.nome_usuario != "Minha conta",
                "Olá, " + AppState.nome_usuario + "!",
                "Olá!",
            ),
            "Resumo das suas finanças",
        ),

        rx.cond(
            AppState.erro != "",
            rx.callout(
                AppState.erro,
                icon="triangle-alert",
                color_scheme="red",
                width="100%",
            ),
            rx.fragment(),
        ),

        rx.vstack(
            rx.heading("Notificações", size="4"),
            rx.cond(
                AppState.notificacoes_ativas.length() > 0,
                rx.vstack(
                    rx.foreach(
                        AppState.notificacoes_ativas,
                        lambda item: rx.hstack(
                            rx.icon("bell-ring", color="var(--amber-9)"),
                            rx.vstack(
                                rx.text(item["titulo"], weight="bold"),
                                rx.text(item["mensagem"], size="2"),
                                align="start",
                                spacing="1",
                            ),
                            rx.spacer(),
                            rx.icon_button(
                                rx.icon("x", size=16),
                                on_click=AppState.dispensar_notificacao(
                                    item["id"]
                                ),
                                variant="ghost",
                                aria_label="Dispensar notificação",
                            ),
                            align="center",
                            width="100%",
                        ),
                    ),
                    width="100%",
                    spacing="3",
                ),
                rx.text("Você não tem alertas financeiros no momento."),
            ),
            width="100%",
            align="start",
            spacing="3",
            padding="1em",
            border="1px solid var(--gray-5)",
            border_radius="12px",
        ),

        rx.cond(
            AppState.sugestoes_financeiras.length() > 0,
            rx.vstack(
                rx.heading("Sugestões para você", size="4"),
                rx.grid(
                    rx.foreach(
                        AppState.sugestoes_financeiras,
                        lambda item: rx.card(
                            rx.vstack(
                                rx.heading(item["titulo"], size="3"),
                                rx.text(item["mensagem"], size="2"),
                                align="start",
                                spacing="2",
                                width="100%",
                            ),
                            width="100%",
                        ),
                    ),
                    columns=rx.breakpoints(initial="1", md="2"),
                    spacing="3",
                    width="100%",
                ),
                width="100%",
                align="start",
                spacing="3",
            ),
            rx.fragment(),
        ),

        # Cards
        rx.grid(

            cartao_resumo(
                "Saldo do Mês",
                AppState.saldo_total,
                "Mês atual",
                "wallet",
                "green",
            ),

            cartao_resumo(
                "Receitas",
                AppState.total_receitas,
                "Este mês",
                "trending-up",
                "green",
            ),

            cartao_resumo(
                "Despesas",
                AppState.total_despesas,
                "Este mês",
                "trending-down",
                "red",
            ),

            cartao_resumo(
                "Contas a Pagar",
                AppState.proximo_vencimento_total,
                "Próximos 7 dias",
                "calendar",
                "red",
            ),

            columns=rx.breakpoints(initial="1", sm="2", xl="4"),
            spacing="4",
            width="100%",
        ),

        # Gráfico + vencimentos
        rx.hstack(

            rx.vstack(

                grafico_visao_geral(),

                rx.heading(
                    "Acesso Rápido",
                    size="5",
                ),

                rx.grid(

                    atalho(
                        "Jarvis",
                        "Tire suas dúvidas financeiras",
                        "bot",
                        "purple",
                        "/assistente",
                    ),

                    atalho(
                        "Planilhas",
                        "Controle suas finanças",
                        "file-spreadsheet",
                        "blue",
                        "/financas",
                    ),

                    atalho(
                        "Calendário",
                        "Gerencie seus vencimentos",
                        "calendar",
                        "green",
                        "/calendario",
                    ),

                    atalho(
                        "Nova Transação",
                        "Registre receitas e despesas",
                        "plus",
                        "green",
                        "/financas",
                    ),

                    columns=rx.breakpoints(initial="1", md="2"),
                    spacing="4",
                    width="100%",
                ),

                spacing="5",
                align="start",

                flex="3",
                min_width="0",
                width="100%",
            ),

            rx.box(
                proximos_vencimentos(),
                flex="1",
                min_width="0",
                width="100%",
            ),

            spacing="5",
            align="start",
            width="100%",
            flex_direction=rx.breakpoints(initial="column", xl="row"),
        ),

        # Banner IA
        banner_ia(),
    )


def dashboard() -> rx.Component:
    return rx.cond(
        AppState.autenticado,
        dashboard_conteudo(),
        auth_page(),
    )


# ============================================================
# PÁGINAS DO MENU AINDA EM DESENVOLVIMENTO
# ============================================================

def pagina_em_desenvolvimento(
    titulo: str,
    rota: str,
) -> rx.Component:

    return page_layout(
        rota,
        cabecalho(
            titulo,
            "Esta página está em desenvolvimento.",
        ),
    )


def calendario() -> rx.Component:
    return calendario_page()


def perfil() -> rx.Component:
    return rx.cond(
        AppState.autenticado,
        page_layout(
            "/perfil",
            cabecalho("Preferências", "Personalize sua conta CashSave."),
            rx.card(
                rx.vstack(
                    rx.text("Moeda"),
                    rx.select(
                        ["BRL", "USD", "EUR"],
                        value=AppState.moeda,
                        on_change=AppState.set_moeda,
                    ),
                    rx.text("Localidade"),
                    rx.select(
                        ["pt-BR", "en-US", "es-ES"],
                        value=AppState.localidade,
                        on_change=AppState.set_localidade,
                    ),
                    rx.text("Fuso horário"),
                    rx.input(
                        value=AppState.fuso_horario,
                        on_change=AppState.set_fuso_horario,
                    ),
                    rx.checkbox(
                        "Lembretes de vencimento",
                        checked=AppState.notificacoes_vencimento,
                        on_change=AppState.set_notificacoes_vencimento,
                    ),
                    rx.checkbox(
                        "Alertas de orçamento",
                        checked=AppState.notificacoes_orcamento,
                        on_change=AppState.set_notificacoes_orcamento,
                    ),
                    rx.checkbox(
                        "Alertas de metas financeiras",
                        checked=AppState.notificacoes_metas,
                        on_change=AppState.set_notificacoes_metas,
                        disabled=AppState.notificacoes_metas_disponivel == False,
                    ),
                    rx.cond(
                        AppState.notificacoes_metas_disponivel,
                        rx.fragment(),
                        rx.text(
                            "Os alertas de metas precisam da atualização do Xano.",
                            size="2",
                            color_scheme="amber",
                        ),
                    ),
                    rx.heading("Foto de perfil", size="4"),
                    rx.text(
                        "Escolha uma imagem e clique em Enviar foto para atualizar "
                        "seu avatar.",
                        size="2",
                        color_scheme="gray",
                    ),
                    rx.avatar(
                        src=AppState.avatar_url,
                        fallback="U",
                        size="6",
                        radius="full",
                    ),
                    rx.upload(
                        rx.vstack(
                            rx.text("Escolher uma imagem (PNG, JPG ou WebP)"),
                            rx.text(
                                rx.selected_files("profile-photo"),
                                size="1",
                                color_scheme="gray",
                            ),
                            spacing="1",
                        ),
                        id="profile-photo",
                        accept={
                            "image/png": [".png"],
                            "image/jpeg": [".jpg", ".jpeg"],
                            "image/webp": [".webp"],
                        },
                        max_files=1,
                        border="1px dashed var(--gray-7)",
                        padding="1em",
                        width="100%",
                        on_drop=AppState.enviar_foto_perfil(
                            rx.upload_files(upload_id="profile-photo")
                        ),
                    ),
                    rx.button(
                        "Enviar foto",
                        on_click=AppState.enviar_foto_perfil(
                            rx.upload_files(upload_id="profile-photo")
                        ),
                        variant="outline",
                        disabled=AppState.autenticado == False,
                    ),
                    rx.button(
                        "Remover foto",
                        on_click=AppState.remover_foto_perfil,
                        variant="ghost",
                        disabled=AppState.autenticado == False,
                    ),
                    rx.button(
                        "Salvar preferências",
                        on_click=AppState.salvar_preferencias,
                        color_scheme="green",
                    ),
                    rx.text(AppState.aviso, color_scheme="green"),
                    rx.text(AppState.erro, color_scheme="red"),
                    spacing="3",
                    width="100%",
                    align="start",
                ),
                width="100%",
                max_width="640px",
            ),
        ),
        auth_page(),
    )


def sobre() -> rx.Component:
    return page_layout(
        "/sobre",
        conteudo_sobre(),
    )


def suporte() -> rx.Component:
    return page_layout(
        "/suporte",
        conteudo_suporte(),
    )


def apoiar() -> rx.Component:
    return page_layout(
        "/apoiar",
        conteudo_apoiar(),
    )


# ============================================================
# APLICAÇÃO
# ============================================================

app = rx.App(stylesheets=["/password-visibility.css"])

app.add_page(
    landing_page,
    route="/",
    title="CashSave | Organize seu dinheiro",
)

app.add_page(
    login_page,
    route="/login",
    title="CashSave | Entrar",
    on_load=AppState.preparar_login,
)

app.add_page(
    cadastro_page,
    route="/cadastro",
    title="CashSave | Criar conta",
    on_load=AppState.preparar_cadastro,
)

app.add_page(
    dashboard,
    route="/app",
    title="CashSave | Visão Geral",
    on_load=AppState.carregar_dados,
)

app.add_page(
    assistente,
    route="/assistente",
    title="CashSave | Jarvis",
    on_load=AppState.carregar_conversas_assistente,
)

app.add_page(
    financas,
    route="/financas",
    title="CashSave | Finanças",
    on_load=AppState.carregar_dados,
)

app.add_page(
    calendario,
    route="/calendario",
    title="CashSave | Calendário",
    on_load=AppState.carregar_dados,
)

app.add_page(
    perfil,
    route="/perfil",
    title="CashSave | Preferências",
    on_load=AppState.carregar_dados,
)

app.add_page(
    sobre,
    route="/sobre",
    title="CashSave | Sobre",
)

app.add_page(
    suporte,
    route="/suporte",
    title="CashSave | Suporte",
)

app.add_page(
    apoiar,
    route="/apoiar",
    title="CashSave | Apoiar o CashSave",
)   