import reflex as rx


# ============================================================
# ESTADO DO ASSISTENTE
# ============================================================

class AssistenteState(rx.State):
    mensagens: list[dict[str, str]] = [
        {
            "tipo": "ia",
            "texto": (
                "Olá! 👋 Eu sou o assistente financeiro do CashSave. "
                "Posso ajudar você a organizar suas finanças, analisar "
                "seus gastos e planejar seu orçamento."
            ),
        }
    ]

    mensagem: str = ""

    @rx.event
    def atualizar_mensagem(self, texto: str):
        self.mensagem = texto

    @rx.event
    def enviar_mensagem(self):
        texto = self.mensagem.strip()

        if not texto:
            return

        # Adiciona mensagem do usuário
        self.mensagens.append(
            {
                "tipo": "usuario",
                "texto": texto,
            }
        )

        # Resposta provisória.
        # Depois podemos trocar isso pela IA real.
        resposta = (
            "Entendi! 👍 Essa é uma resposta provisória do CashSave. "
            "Quando conectarmos a IA, vou conseguir analisar seus dados "
            "financeiros e responder de forma personalizada."
        )

        self.mensagens.append(
            {
                "tipo": "ia",
                "texto": resposta,
            }
        )

        self.mensagem = ""


# ============================================================
# SIDEBAR
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
                        "Assistente Financeiro",
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
                    "Online",
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
                        AssistenteState.mensagens,
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

            # Campo de mensagem
            rx.hstack(

                rx.input(
                    placeholder="Digite sua dúvida financeira...",
                    value=AssistenteState.mensagem,

                    on_change=AssistenteState.atualizar_mensagem,

                    size="3",
                    width="100%",
                ),

                rx.button(
                    rx.icon(
                        "send",
                        size=18,
                    ),

                    on_click=AssistenteState.enviar_mensagem,

                    size="3",
                    color_scheme="green",
                ),

                width="100%",
                spacing="3",
            ),

            rx.text(
                "O assistente ainda está em modo de demonstração.",
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

            rx.vstack(

                rx.button(
                    "💰 Como economizar dinheiro?",
                    variant="soft",
                    width="100%",
                    justify="start",
                ),

                rx.button(
                    "📊 Como organizar meu orçamento?",
                    variant="soft",
                    width="100%",
                    justify="start",
                ),

                rx.button(
                    "📈 Como controlar meus gastos?",
                    variant="soft",
                    width="100%",
                    justify="start",
                ),

                rx.button(
                    "🎯 Como alcançar uma meta financeira?",
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

    return rx.hstack(

        sidebar(),

        rx.box(

            rx.vstack(

                # Título
                rx.vstack(

                    rx.heading(
                        "Assistente IA 🤖",
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
    )
