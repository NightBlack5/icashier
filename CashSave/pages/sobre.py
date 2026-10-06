import reflex as rx


def hero_sobre() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.box(
                rx.hstack(
                    rx.icon("book-open", size=17),
                    rx.text(
                        "Educação Financeira",
                        size="2",
                        weight="medium",
                    ),
                    spacing="2",
                    align="center",
                ),
                padding="0.55em 1em",
                border_radius="999px",
                background="rgba(0, 180, 140, 0.12)",
                color="var(--green-9)",
            ),
            rx.heading(
                rx.text(
                    "Organize suas finanças com ",
                    as_="span",
                ),
                rx.text(
                    "inteligência",
                    as_="span",
                    color="var(--green-9)",
                ),
                size="9",
                weight="bold",
                text_align="center",
                line_height="1.1",
            ),
            rx.text(
                "Um aplicativo educativo e prático para ajudar você a controlar seus gastos, "
                "não esquecer vencimentos e organizar melhor seu dinheiro.",
                size="5",
                color="var(--gray-9)",
                text_align="center",
                max_width="760px",
                line_height="1.5",
            ),
            rx.hstack(
                rx.link(
                    rx.button(
                        "Começar agora",
                        rx.icon("arrow-right", size=18),
                        color_scheme="green",
                        size="3",
                    ),
                    href="/",
                ),
                rx.link(
                    rx.button(
                        "Saiba mais",
                        variant="outline",
                        size="3",
                    ),
                    href="#recursos",
                ),
                spacing="3",
                justify="center",
            ),
            spacing="5",
            align="center",
            justify="center",
            width="100%",
            min_height="390px",
        ),
        width="100%",
        background=(
            "radial-gradient(circle at 50% 0%, "
            "rgba(0, 180, 140, 0.12), transparent 55%)"
        ),
        border_radius="18px",
        padding="2em",
    )


def card_recurso(
    icone: str,
    titulo: str,
    descricao: str,
) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.center(
                rx.icon(
                    icone,
                    size=24,
                    color="var(--green-9)",
                ),
                width="48px",
                height="48px",
                border_radius="10px",
                background="rgba(0, 180, 140, 0.12)",
            ),
            rx.heading(
                titulo,
                size="4",
                weight="bold",
            ),
            rx.text(
                descricao,
                size="3",
                color="var(--gray-9)",
                line_height="1.5",
            ),
            spacing="4",
            align="start",
            width="100%",
        ),
        width="100%",
        min_height="190px",
        padding="1.5em",
        border_radius="14px",
        background="rgba(20, 20, 20, 0.55)",
        border="1px solid var(--gray-5)",
        _hover={
            "border_color": "var(--green-7)",
            "transform": "translateY(-2px)",
        },
        transition="all 0.2s ease",
    )


def recursos() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading(
                "O que você pode fazer",
                size="7",
                text_align="center",
            ),
            rx.text(
                "Ferramentas simples e poderosas para transformar sua relação com o dinheiro.",
                size="4",
                color="var(--gray-9)",
                text_align="center",
            ),
            rx.grid(
                card_recurso(
                    "brain",
                    "Assistente com IA",
                    "Nossa inteligência artificial ajuda você a organizar suas "
                    "finanças de forma educativa e responsável.",
                ),
                card_recurso(
                    "wallet",
                    "Controle Financeiro",
                    "Planilhas intuitivas para registrar receitas, despesas e "
                    "visualizar seu balanço mensal.",
                ),
                card_recurso(
                    "calendar",
                    "Calendário de Contas",
                    "Nunca mais esqueça um vencimento com alertas personalizados "
                    "e calendário visual.",
                ),
                card_recurso(
                    "shield-check",
                    "Dados Seguros",
                    "Suas informações são protegidas com recursos de segurança "
                    "e boas práticas de privacidade.",
                ),
                columns="2",
                spacing="5",
                width="100%",
                max_width="950px",
            ),
            spacing="5",
            align="center",
            width="100%",
        ),
        id="recursos",
        width="100%",
        padding_y="4em",
    )


def sobre_projeto() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(
                "Sobre o CashSave",
                size="6",
            ),
            rx.text(
                "O CashSave foi criado para tornar a educação financeira "
                "mais simples, acessível e prática.",
                size="4",
                color="var(--gray-10)",
                line_height="1.6",
            ),
            rx.text(
                "A proposta é reunir em um único lugar ferramentas para "
                "acompanhar receitas, despesas, contas e organização financeira, "
                "além de oferecer um assistente inteligente para ajudar o usuário "
                "a entender melhor suas próprias finanças.",
                size="3",
                color="var(--gray-9)",
                line_height="1.7",
            ),
            rx.text(
                "O CashSave tem foco educacional e não substitui um profissional "
                "financeiro.",
                size="3",
                color="var(--gray-9)",
                line_height="1.6",
            ),
            spacing="4",
            align="start",
        ),
        width="100%",
        max_width="950px",
        padding="2em",
        border_radius="16px",
    )


def conteudo_sobre() -> rx.Component:
    return rx.vstack(
        hero_sobre(),
        recursos(),
        sobre_projeto(),
        spacing="5",
        align="center",
        width="100%",
    )