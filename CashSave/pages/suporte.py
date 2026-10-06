import reflex as rx


EMAIL_SUPORTE = "CashSaveFinance@gmail.com"
WHATSAPP_EXIBIDO = "+55 (11) 94453-7652"
WHATSAPP_LINK = "https://wa.me/5511944537652"
INSTAGRAM_LINK = "#"
TIKTOK_LINK = "#"

FAQ = [
    (
        "Como funciona o assistente de IA?",
        "O assistente Fin responde dúvidas sobre organização financeira e ajuda "
        "a pensar em orçamentos. Ele tem caráter educativo.",
    ),
    (
        "Posso exportar meus dados?",
        "Em breve você poderá exportar suas receitas e despesas em planilha.",
    ),
    (
        "Como funcionam os alertas de contas?",
        "Você será avisado sobre contas que vencem nos próximos dias.",
    ),
    (
        "Meus dados estão seguros?",
        "Seus dados ficam em um banco de dados protegido por login. "
        "Detalhes sobre segurança serão publicados junto com a versão final.",
    ),
    (
        "O aplicativo funciona offline?",
        "Não. O CashSave precisa de conexão com a internet para carregar e salvar seus dados.",
    ),
    (
        "Como cancelo minha conta?",
        "Entre em contato pelo e-mail de suporte pedindo o cancelamento.",
    ),
]


def icone_colorido(icone: str, cor: str) -> rx.Component:
    return rx.center(
        rx.icon(
            icone,
            size=18,
            color=f"var(--{cor}-9)",
        ),
        width="40px",
        height="40px",
        border_radius="10px",
        background=f"var(--{cor}-3)",
    )


def cartao_contato(
    icone: str,
    cor: str,
    titulo: str,
    legenda: str,
    texto_link: str,
    href: str,
    externo: bool = False,
) -> rx.Component:
    link_conteudo = (
        rx.hstack(
            rx.text(texto_link, size="3"),
            rx.icon("external-link", size=14),
            spacing="1",
            align="center",
        )
        if externo
        else rx.text(texto_link, size="3")
    )
    return rx.card(
        rx.vstack(
            icone_colorido(icone, cor),
            rx.text(
                titulo,
                size="3",
                weight="bold",
                margin_top="0.5em",
            ),
            rx.text(
                legenda,
                size="2",
                color_scheme="gray",
            ),
            rx.link(
                link_conteudo,
                href=href,
                is_external=externo,
                color="var(--green-9)",
            ),
            spacing="1",
            align="start",
        ),
        width="100%",
    )


def botao_social(icone: str, fundo: str, href: str) -> rx.Component:
    return rx.link(
        rx.center(
            rx.icon(icone, size=20, color="white"),
            width="44px",
            height="44px",
            border_radius="10px",
            background=fundo,
        ),
        href=href,
        is_external=True,
    )


def cartao_redes() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.text("Redes Sociais", size="3", weight="bold"),
            rx.hstack(
                botao_social(
                    "camera",
                    "linear-gradient(135deg, #f59e0b, #ec4899, #8b5cf6)",
                    INSTAGRAM_LINK,
                ),
                botao_social(
                    "music-2",
                    "var(--gray-3)",
                    TIKTOK_LINK,
                ),
                spacing="3",
            ),
            spacing="3",
            align="start",
        ),
        width="100%",
    )


def pergunta_faq(pergunta: str, resposta: str) -> rx.Component:
    return rx.accordion.item(
        header=rx.text(pergunta, size="3", weight="medium"),
        content=rx.text(resposta, size="2", color_scheme="gray"),
    )


def conteudo_suporte() -> rx.Component:
    return rx.vstack(
        rx.center(
            rx.vstack(
                rx.center(
                    rx.icon("circle-help", size=30, color="white"),
                    width="64px",
                    height="64px",
                    border_radius="16px",
                    background="linear-gradient(135deg, #10b981, #0d9488)",
                ),
                rx.heading("Central de Suporte", size="8"),
                rx.text(
                    "Estamos aqui para ajudar! Encontre respostas rápidas ou "
                    "entre em contato conosco.",
                    size="4",
                    color_scheme="gray",
                    text_align="center",
                    max_width="640px",
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            width="100%",
        ),
        rx.grid(
            cartao_contato(
                "mail",
                "blue",
                "E-mail",
                "Resposta em até 24h",
                EMAIL_SUPORTE,
                f"mailto:{EMAIL_SUPORTE}",
            ),
            cartao_contato(
                "message-square",
                "green",
                "WhatsApp",
                "Chat ao vivo",
                WHATSAPP_EXIBIDO,
                WHATSAPP_LINK,
                externo=True,
            ),
            cartao_redes(),
            columns="3",
            spacing="4",
            width="100%",
            margin_top="1em",
        ),
        rx.card(
            rx.vstack(
                rx.heading("Perguntas Frequentes", size="6"),
                rx.accordion.root(
                    *[
                        pergunta_faq(pergunta, resposta)
                        for pergunta, resposta in FAQ
                    ],
                    type="single",
                    collapsible=True,
                    width="100%",
                ),
                spacing="4",
                align="start",
                width="100%",
            ),
            width="100%",
            padding="1.5em",
        ),
        spacing="4",
        align="center",
        width="100%",
        max_width="960px",
        margin_x="auto",
    )