import reflex as rx

from ..state import AppState
from .auth import auth_page


# ============================================================
# SIDEBAR
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


def item_menu(
    texto: str,
    icone: str,
    rota: str,
    ativa: bool = False,
) -> rx.Component:

    return rx.link(
        rx.hstack(
            rx.icon(icone, size=18),

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


def sidebar() -> rx.Component:

    return rx.vstack(

        # Logo
        rx.hstack(
            rx.icon(
                "piggy-bank",
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
                rota == "/assistente",
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

        border_right="1px solid var(--gray-5)",
        background="var(--gray-2)",

        position="sticky",
        top="0",
    )


# ============================================================
# BOLHA DE MENSAGEM
# ============================================================

def mensagem_balao(
    mensagem: dict[str, str],
) -> rx.Component:

    eh_usuario = mensagem["tipo"] == "usuario"

    return rx.hstack(

        # Ícone da IA
        rx.cond(
            eh_usuario,
            rx.fragment(),
            rx.center(
                rx.icon(
                    "bot",
                    size=18,
                    color="var(--green-9)",
                ),

                width="36px",
                height="36px",
                border_radius="10px",
                background="var(--green-3)",
                flex_shrink="0",
            ),
        ),

        # Mensagem
        rx.box(

            rx.text(
                mensagem["texto"],
                size="3",
                line_height="1.6",
            ),

            padding="0.8em 1em",

            border_radius=rx.cond(
                eh_usuario,
                "14px 14px 4px 14px",
                "4px 14px 14px 14px",
            ),

            background=rx.cond(
                eh_usuario,
                "var(--green-9)",
                "var(--gray-3)",
            ),

            color=rx.cond(
                eh_usuario,
                "white",
                "var(--gray-12)",
            ),

            max_width="75%",
        ),

        # Espaço para empurrar mensagem do usuário
        rx.spacer(),

        align="start",
        width="100%",
    )


# ============================================================
# ÁREA DE CHAT
# ============================================================

def chat() -> rx.Component:

    return rx.card(

        rx.vstack(

            # Cabeçalho
            rx.hstack(

                rx.center(
                    rx.icon(
                        "bot",
                        size=22,
                        color="white",
                    ),

                    width="44px",
                    height="44px",
                    border_radius="12px",
                    background="var(--green-9)",
                ),

                rx.vstack(

                    rx.heading(
                        "Jarvis",
                        size="4",
                    ),

                    rx.text(
                        "Seu assistente pessoal para finanças",
                        size="2",
                        color_scheme="gray",
                    ),

                    spacing="0",
                    align="start",
                ),

                rx.spacer(),

                rx.badge(
                    rx.cond(
                        AppState.assistente_carregando,
                        "Consultando Ollama...",
                        "Ollama local",
                    ),
                    color_scheme="green",
                    variant="soft",
                ),

                align="center",
                width="100%",
            ),

            rx.divider(),

            # Mensagens
            rx.scroll_area(

                rx.vstack(
                    rx.foreach(
                        AppState.assistente_mensagens,
                        mensagem_balao,
                    ),

                    spacing="4",
                    width="100%",
                ),

                height="500px",
                width="100%",
                padding="1em",
            ),

            rx.divider(),

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

            # Campo de mensagem
            rx.form(
                rx.hstack(
                    rx.input(
                        placeholder="Digite sua dúvida financeira...",
                        value=AppState.assistente_mensagem,
                        on_change=AppState.set_assistente_mensagem,
                        size="3",
                        width="100%",
                        disabled=AppState.assistente_carregando,
                    ),
                    rx.button(
                        rx.icon(
                            "send",
                            size=18,
                        ),
                        type="submit",
                        size="3",
                        color_scheme="green",
                        disabled=AppState.assistente_carregando,
                    ),
                    width="100%",
                    spacing="3",
                ),
                on_submit=AppState.enviar_mensagem_assistente,
                width="100%",
            ),

            rx.text(
                "Você pode cadastrar despesas claras, como: "
                "'gastei R$ 25,90 em transporte'. O Enter envia a mensagem.",
                size="1",
                color_scheme="gray",
            ),

            spacing="4",
            width="100%",
        ),

        width="100%",
        max_width="1000px",
    )


# ============================================================
# DICAS LATERAIS
# ============================================================

def dicas() -> rx.Component:

    return rx.card(

        rx.vstack(
            rx.heading(
                "O que posso fazer?",
                size="4",
            ),

            rx.text(
                "Experimente perguntar:",
                size="2",
                color_scheme="gray",
            ),

            rx.button(
                rx.icon("plus", size=15),
                "Nova conversa",
                on_click=AppState.nova_conversa_assistente,
                variant="outline",
                width="100%",
            ),
            rx.cond(
                AppState.assistente_conversas.length() > 0,
                rx.vstack(
                    rx.heading("Histórico", size="3"),
                    rx.foreach(
                        AppState.assistente_conversas,
                        lambda item: rx.button(
                            rx.cond(
                                item["title"] != "",
                                item["title"],
                                "Conversa",
                            ),
                            on_click=AppState.abrir_conversa_assistente(item["id"]),
                            variant="soft",
                            width="100%",
                            justify="start",
                        ),
                    ),
                    width="100%",
                    align="start",
                    spacing="2",
                ),
                rx.fragment(),
            ),

            rx.vstack(

                rx.button(
                    "💰 Como economizar dinheiro?",
                    on_click=AppState.set_assistente_mensagem(
                        "Como posso economizar dinheiro?"
                    ),
                    variant="soft",
                    width="100%",
                    justify="start",
                ),

                rx.button(
                    "📊 Como organizar meu orçamento?",
                    on_click=AppState.set_assistente_mensagem(
                        "Como posso organizar meu orçamento?"
                    ),
                    variant="soft",
                    width="100%",
                    justify="start",
                ),

                rx.button(
                    "📈 Como controlar meus gastos?",
                    on_click=AppState.set_assistente_mensagem(
                        "Como posso controlar meus gastos?"
                    ),
                    variant="soft",
                    width="100%",
                    justify="start",
                ),

                rx.button(
                    "🎯 Como alcançar uma meta financeira?",
                    on_click=AppState.set_assistente_mensagem(
                        "Como posso alcançar minha meta financeira?"
                    ),
                    variant="soft",
                    width="100%",
                    justify="start",
                ),

                spacing="2",
                width="100%",
            ),

            spacing="3",
            align="start",
            width="100%",
        ),

        width="100%",
    )


# ============================================================
# PÁGINA
# ============================================================

def assistente() -> rx.Component:

    return rx.cond(
        AppState.autenticado,
        rx.hstack(

            sidebar(),

            rx.box(

                rx.vstack(

                # Título
                rx.vstack(

                    rx.heading(
                        "Jarvis 🤖",
                        size="8",
                    ),

                    rx.text(
                        "Converse com seu assistente financeiro pessoal.",
                        color_scheme="gray",
                        size="3",
                    ),

                    spacing="1",
                    align="start",
                ),

                # Conteúdo
                rx.hstack(

                    rx.box(
                        chat(),
                        flex="3",
                        min_width="0",
                    ),

                    rx.box(
                        dicas(),
                        flex="1",
                        min_width="250px",
                    ),

                    spacing="5",
                    align="start",
                    width="100%",
                ),

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
        ),
        auth_page(),
    )
