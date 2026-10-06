import reflex as rx

from .pages.assistente import assistente
from .pages.apoiar import conteudo_apoiar
from .pages.calendario import conteudo_calendario
from .pages.financas import financas
from .pages.sobre import conteudo_sobre
from .pages.suporte import conteudo_suporte


# ============================================================
# DADOS DE EXEMPLO
# Depois vamos substituir pelos dados vindos do Xano
# ============================================================

DADOS_GRAFICO = [
    {"mes": "Mai", "receitas": 2000, "despesas": 200},
    {"mes": "Jun", "receitas": 0, "despesas": 0},
    {"mes": "Jul", "receitas": 800, "despesas": 100},
    {"mes": "Ago", "receitas": 0, "despesas": 0},
    {"mes": "Set", "receitas": 0, "despesas": 0},
    {"mes": "Out", "receitas": 0, "despesas": 0},
]


# ============================================================
# MENU
# ============================================================

MENU = [
    ("Visão Geral", "layout-dashboard", "/"),
    ("Assistente IA", "bot", "/assistente"),
    ("Finanças", "trending-up", "/financas"),
    ("Calendário", "calendar", "/calendario"),
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
            padding="0.5em 0.8em",
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
        rx.hstack(

            rx.avatar(
                fallback="U",
                size="2",
                radius="full",
            ),

            rx.vstack(
                rx.text(
                    "Usuário",
                    size="2",
                    weight="medium",
                ),

                rx.text(
                    "usuario@exemplo.com",
                    size="1",
                    color_scheme="gray",
                ),

                spacing="0",
                align="start",
            ),

            align="center",
            spacing="3",
            padding="0.5em 0.8em",
        ),

        spacing="2",
        align="start",

        width="250px",
        height="100vh",

        flex_shrink="0",

        padding="1em",

        border_right="1px solid var(--gray-5)",

        background="var(--gray-2)",

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

    return rx.hstack(

        sidebar(rota_atual),

        rx.box(

            rx.vstack(
                *conteudo,

                spacing="5",
                align="start",
                width="100%",
            ),

            padding="2em",
            width="100%",
            min_width="0",
        ),

        spacing="0",
        align="start",
        width="100%",
    )


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
    valor: str,
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
                    color_scheme="gray",
                ),

                rx.heading(
                    valor,
                    size="6",
                ),

                rx.text(
                    legenda,
                    size="1",
                    color_scheme="gray",
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
                        color_scheme="gray",
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

                data=DADOS_GRAFICO,

                width="100%",
                height=300,
            ),

            spacing="4",
            width="100%",
        ),

        width="100%",
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
                        color_scheme="gray",
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

            rx.center(

                rx.vstack(

                    rx.center(

                        rx.icon(
                            tag="circle-check",
                            size=28,
                        ),

                        width="64px",
                        height="64px",

                        border_radius="50%",

                        background="var(--gray-4)",
                    ),

                    rx.text(
                        "Nenhuma conta próxima",
                        weight="medium",
                    ),

                    rx.text(
                        "Você está em dia!",
                        size="2",
                        color_scheme="gray",
                    ),

                    align="center",
                    spacing="2",
                ),

                width="100%",
                padding_y="2em",
            ),

            spacing="4",
            width="100%",
        ),

        width="100%",
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
                ),

                href="/assistente",
            ),

            align="center",
            spacing="4",
            width="100%",
        ),

        background="linear-gradient(90deg, #0f9d7a, #0e7490)",

        border_radius="16px",

        padding="1.5em",

        width="100%",
    )


# ============================================================
# DASHBOARD
# ============================================================

def dashboard() -> rx.Component:

    return page_layout(

        "/",

        cabecalho(
            "Olá, Usuário! 👋",
            "Resumo das suas finanças",
        ),

        # Cards
        rx.grid(

            cartao_resumo(
                "Saldo do Mês",
                "R$ 0,00",
                "Mês atual",
                "wallet",
                "green",
            ),

            cartao_resumo(
                "Receitas",
                "R$ 0,00",
                "Este mês",
                "trending-up",
                "green",
            ),

            cartao_resumo(
                "Despesas",
                "R$ 0,00",
                "Este mês",
                "trending-down",
                "red",
            ),

            cartao_resumo(
                "Contas a Pagar",
                "0",
                "Próximos 7 dias",
                "calendar",
                "orange",
            ),

            columns="4",
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
                        "Assistente IA",
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
                        "amber",
                        "/calendario",
                    ),

                    atalho(
                        "Nova Transação",
                        "Registre receitas e despesas",
                        "plus",
                        "green",
                        "/financas",
                    ),

                    columns="2",
                    spacing="4",
                    width="100%",
                ),

                spacing="5",
                align="start",

                flex="3",
                min_width="0",
            ),

            rx.box(
                proximos_vencimentos(),
                flex="1",
                min_width="0",
            ),

            spacing="5",
            align="start",
            width="100%",
        ),

        # Banner IA
        banner_ia(),
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
    return page_layout(
        "/calendario",
        conteudo_calendario(),
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

app = rx.App()

app.add_page(
    dashboard,
    route="/",
    title="CashSave | Visão Geral",
)

app.add_page(
    assistente,
    route="/assistente",
    title="CashSave | Assistente IA",
)

app.add_page(
    financas,
    route="/financas",
    title="CashSave | Finanças",
)

app.add_page(
    calendario,
    route="/calendario",
    title="CashSave | Calendário",
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