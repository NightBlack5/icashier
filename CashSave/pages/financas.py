import reflex as rx


MENU = [
    ("Visão Geral", "layout-dashboard", "/"),
    ("Assistente IA", "bot", "/assistente"),
    ("Finanças", "trending-up", "/financas"),
    ("Calendário", "calendar", "/calendario"),
    ("Sobre", "info", "/sobre"),
    ("Suporte", "life-buoy", "/suporte"),
    ("Apoiar o CashSave", "heart", "/apoiar"),
]


def item_menu(
    texto: str,
    icone: str,
    rota: str,
    ativa: bool,
) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icone, size=18),
            rx.text(texto, size="3", weight="medium"),
            spacing="3",
            align="center",
            width="100%",
            padding="0.65em 0.8em",
            border_radius="9px",
            background=(
                "rgba(16, 185, 129, 0.14)"
                if ativa
                else "transparent"
            ),
            color="#10b981" if ativa else "#d1d5db",
            _hover={
                "background": (
                    "rgba(16, 185, 129, 0.18)"
                    if ativa
                    else "rgba(255,255,255,0.05)"
                )
            },
        ),
        href=rota,
        width="100%",
        text_decoration="none",
    )


def sidebar() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.center(
                rx.icon(
                    "piggy-bank",
                    size=26,
                    color="#10b981",
                ),
                width="42px",
                height="42px",
            ),
            rx.heading("CashSave", size="5"),
            spacing="2",
            align="center",
            padding="0.2em 0.4em",
            margin_bottom="0.8em",
        ),
        rx.divider(),
        rx.vstack(
            *[
                item_menu(
                    texto,
                    icone,
                    rota,
                    rota == "/financas",
                )
                for texto, icone, rota in MENU
            ],
            spacing="2",
            width="100%",
        ),
        rx.spacer(),
        rx.divider(),
        rx.hstack(
            rx.avatar(fallback="E", size="2", radius="full"),
            rx.vstack(
                rx.text("ed tuber", size="2", weight="bold"),
                rx.text(
                    "edudiasof@gmail.com",
                    size="1",
                    color="#9ca3af",
                ),
                spacing="0",
                align="start",
            ),
            spacing="3",
            align="center",
            padding="0.5em",
        ),
        width="238px",
        height="100vh",
        padding="1em",
        spacing="3",
        align="start",
        flex_shrink="0",
        position="sticky",
        top="0",
        background="#111111",
        border_right="1px solid #292929",
    )


def resumo_card(
    titulo: str,
    valor: str,
    icone: str,
    tipo: str,
) -> rx.Component:
    if tipo == "despesa":
        cor = "#ff5c5c"
        fundo = "rgba(255, 92, 92, 0.15)"
    else:
        cor = "#10b981"
        fundo = "rgba(16, 185, 129, 0.15)"

    return rx.box(
        rx.hstack(
            rx.center(
                rx.icon(icone, size=22, color=cor),
                width="48px",
                height="48px",
                border_radius="10px",
                background=fundo,
                flex_shrink="0",
            ),
            rx.vstack(
                rx.text(titulo, size="2", color="#9ca3af"),
                rx.text(valor, size="6", weight="bold", color=cor),
                spacing="0",
                align="start",
            ),
            spacing="3",
            align="center",
        ),
        width="100%",
        padding="1.4em",
        border="1px solid #353535",
        border_radius="14px",
        background="#121212",
    )


def filtros() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.box(
                rx.hstack(
                    rx.icon("search", size=18, color="#777777"),
                    rx.input(
                        placeholder="Buscar transações...",
                        variant="soft",
                        border="none",
                        background="transparent",
                        width="100%",
                        color="#ffffff",
                        _placeholder={"color": "#777777"},
                    ),
                    spacing="2",
                    width="100%",
                ),
                flex="1",
                border="1px solid #353535",
                border_radius="8px",
                padding_x="0.8em",
                height="42px",
                display="flex",
                align_items="center",
            ),
            rx.select(
                ["outubro 2026", "setembro 2026", "agosto 2026"],
                default_value="outubro 2026",
                width="180px",
            ),
            rx.select(
                ["Todos", "Receitas", "Despesas"],
                default_value="Todos",
                width="150px",
            ),
            rx.select(
                ["Todas", "Alimentação", "Transporte", "Moradia"],
                default_value="Todas",
                width="150px",
            ),
            spacing="3",
            width="100%",
            align="center",
        ),
        width="100%",
        padding="1em",
        border="1px solid #353535",
        border_radius="14px",
        background="#121212",
    )


def tabela_transacoes() -> rx.Component:
    return rx.box(
        rx.grid(
            rx.text("Data", size="2", color="#9ca3af"),
            rx.text("Descrição", size="2", color="#9ca3af"),
            rx.text("Categoria", size="2", color="#9ca3af"),
            rx.text("Valor", size="2", color="#9ca3af"),
            rx.text("Ações", size="2", color="#9ca3af"),
            columns="5",
            width="100%",
            padding="0.8em",
            border_bottom="1px solid #292929",
        ),
        rx.center(
            rx.vstack(
                rx.center(
                    rx.icon("file-text", size=38, color="#d1d5db"),
                    width="70px",
                    height="70px",
                    border_radius="12px",
                    background="#202020",
                ),
                rx.text(
                    "Nenhuma transação encontrada",
                    size="3",
                    color="#9ca3af",
                ),
                rx.text(
                    "Adicione uma transação para começar a acompanhar suas finanças.",
                    size="2",
                    color="#777777",
                    text_align="center",
                ),
                spacing="3",
                align="center",
            ),
            width="100%",
            min_height="210px",
        ),
        width="100%",
        border="1px solid #353535",
        border_radius="14px",
        overflow="hidden",
        background="#121212",
    )


def botao_chat() -> rx.Component:
    return rx.center(
        rx.icon("message-circle", size=24, color="white"),
        position="fixed",
        bottom="22px",
        right="28px",
        width="54px",
        height="54px",
        border_radius="50%",
        background="#10b981",
        box_shadow="0 8px 25px rgba(0,0,0,0.35)",
        cursor="pointer",
        _hover={
            "transform": "scale(1.05)",
            "background": "#059669",
        },
    )


def financas() -> rx.Component:
    return rx.hstack(
        sidebar(),
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.heading("Planilhas Financeiras", size="8"),
                    rx.text(
                        "Controle suas receitas e despesas",
                        color="#9ca3af",
                        size="3",
                    ),
                    spacing="1",
                    align="start",
                ),
                rx.spacer(),
                rx.hstack(
                    rx.button(
                        rx.icon("download", size=17),
                        "Exportar CSV",
                        variant="outline",
                        color_scheme="gray",
                        height="42px",
                    ),
                    rx.button(
                        rx.icon("plus", size=18),
                        "Nova Transação",
                        color_scheme="green",
                        height="42px",
                    ),
                    spacing="3",
                ),
                width="100%",
                align="center",
            ),
            rx.grid(
                resumo_card("Receitas", "R$ 0,00", "trending-up", "receita"),
                resumo_card("Despesas", "R$ 0,00", "trending-down", "despesa"),
                resumo_card("Saldo", "R$ 0,00", "file-spreadsheet", "saldo"),
                columns="3",
                spacing="4",
                width="100%",
            ),
            filtros(),
            tabela_transacoes(),
            spacing="5",
            padding="2em",
            width="100%",
            min_width="0",
            align="start",
        ),
        botao_chat(),
        spacing="0",
        width="100%",
        min_height="100vh",
        background="#0f0f0f",
        align="start",
    )