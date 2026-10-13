import reflex as rx


BG = "#061518"
PANEL = "#0b2024"
PANEL_LIGHT = "#10292d"
GREEN = "#25e5a0"
MUTED = "#a8bdba"


def marca() -> rx.Component:
    return rx.hstack(
        rx.center(
            rx.icon("piggy-bank", size=19, color=BG),
            width="34px",
            height="34px",
            border_radius="50%",
            background=GREEN,
        ),
        rx.heading(
            rx.fragment(
                rx.text("Cash", as_="span", color="white"),
                rx.text("Save", as_="span", color=GREEN),
            ),
            size="5",
            letter_spacing="-0.04em",
        ),
        spacing="2",
        align="center",
    )


def botao_acesso(rotulo: str = "Começar grátis") -> rx.Component:
    return rx.link(
        rx.button(
            rotulo,
            rx.icon("arrow-right", size=17),
            color=BG,
            background=GREEN,
            border_radius="999px",
            padding_x="1.4em",
            height="46px",
            _hover={"background": "#51f0b6", "transform": "translateY(-2px)"},
            transition="all 160ms ease",
        ),
        href="/login",
        text_decoration="none",
    )


def barra_categoria(nome: str, valor: str, largura: str, cor: str) -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.text(nome, size="2", color="#e0eeeb"),
            rx.spacer(),
            rx.text(valor, size="2", weight="bold", color="white"),
            width="100%",
        ),
        rx.box(
            rx.box(
                width=largura,
                height="100%",
                background=cor,
                border_radius="999px",
            ),
            width="100%",
            height="6px",
            border_radius="999px",
            background="#19383b",
        ),
        spacing="1",
        width="100%",
    )


def previa_painel() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.hstack(
                rx.hstack(
                    rx.center(
                        rx.icon("piggy-bank", size=15, color=BG),
                        width="25px",
                        height="25px",
                        border_radius="50%",
                        background=GREEN,
                    ),
                    rx.text("CashSave", weight="bold", color="white"),
                    spacing="2",
                    align="center",
                ),
                rx.spacer(),
                rx.icon("search", size=17, color="#a8bdba"),
                width="100%",
            ),
            rx.vstack(
                rx.text("Prévia ilustrativa", size="1", color=MUTED),
                rx.text("Seu resumo financeiro", size="2", color="#e0eeeb"),
                rx.heading("R$ 2.487,32", size="6", color="white"),
                rx.hstack(
                    rx.icon("trending-up", size=15, color=GREEN),
                    rx.text("+12,5% este mês", size="1", color=GREEN),
                    spacing="1",
                    align="center",
                ),
                align="start",
                spacing="1",
                width="100%",
                padding="1em",
                border="1px solid #1d6553",
                border_radius="16px",
                background="linear-gradient(135deg, #103b36, #10272b)",
            ),
            rx.grid(
                *[
                    rx.vstack(
                        rx.center(
                            rx.icon(icon, size=17, color=BG),
                            width="38px",
                            height="38px",
                            border_radius="50%",
                            background=GREEN,
                        ),
                        rx.text(label, size="1", color="#d0dfdc"),
                        align="center",
                        spacing="1",
                    )
                    for label, icon in [
                        ("Adicionar", "plus"),
                        ("Contas", "wallet"),
                        ("Metas", "target"),
                        ("Resumo", "chart-no-axes-combined"),
                    ]
                ],
                columns="4",
                width="100%",
                padding_y="0.4em",
            ),
            rx.vstack(
                rx.hstack(
                    rx.text("Seus gastos", weight="bold", color="white"),
                    rx.spacer(),
                    rx.text("Visão do mês", size="1", color=GREEN),
                    width="100%",
                ),
                barra_categoria("Alimentação", "R$ 642,30", "68%", "#ff925c"),
                barra_categoria("Transporte", "R$ 318,20", "42%", "#55b8ff"),
                barra_categoria("Lazer", "R$ 276,50", "34%", "#b78cff"),
                spacing="3",
                width="100%",
                padding="1em",
                border="1px solid #20383b",
                border_radius="16px",
                background=PANEL,
            ),
            rx.hstack(
                rx.text("Resumo", size="1", color=GREEN),
                rx.spacer(),
                rx.text("Finanças", size="1", color=MUTED),
                rx.spacer(),
                rx.text("Perfil", size="1", color=MUTED),
                width="100%",
                padding_top="0.5em",
            ),
            width="100%",
            height="100%",
            padding="1.2em",
            spacing="4",
            border="7px solid #183237",
            border_radius="38px",
            background=BG,
            box_shadow="0 28px 90px rgba(0, 0, 0, 0.55)",
        ),
        width="min(370px, 100%)",
        min_height="530px",
        padding="0.5em",
        border="1px solid #285247",
        border_radius="46px",
        background="#0c1c20",
        transform="rotate(2deg)",
    )


def cabecalho_landing() -> rx.Component:
    return rx.hstack(
        rx.link(marca(), href="#inicio", text_decoration="none"),
        rx.spacer(),
        rx.hstack(
            rx.link("Início", href="#inicio", color="#d2dfdc"),
            rx.link("Recursos", href="#recursos", color="#d2dfdc"),
            rx.link("Como funciona", href="#como-funciona", color="#d2dfdc"),
            spacing="6",
            display={"initial": "none", "md": "flex"},
        ),
        rx.spacer(),
        botao_acesso("Acessar"),
        align="center",
        width="100%",
        max_width="1180px",
        margin="0 auto",
        padding="1.2em 1.5em",
        position="relative",
        z_index="1",
    )


def hero() -> rx.Component:
    return rx.box(
        rx.box(
            position="absolute",
            top="-120px",
            right="-100px",
            width="520px",
            height="520px",
            border_radius="50%",
            background="radial-gradient(circle, rgba(27, 220, 151, 0.16), transparent 68%)",
            pointer_events="none",
        ),
        rx.vstack(
            cabecalho_landing(),
            rx.flex(
                rx.vstack(
                    rx.text(
                        "SEU DINHEIRO, MAIS INTELIGENTE",
                        size="2",
                        weight="bold",
                        color=GREEN,
                        letter_spacing="0.14em",
                    ),
                    rx.heading(
                        rx.fragment(
                            rx.text("Cash", as_="span", color="white"),
                            rx.text("Save", as_="span", color=GREEN),
                        ),
                        size="9",
                        line_height="0.95",
                        letter_spacing="-0.065em",
                    ),
                    rx.heading(
                        "Organize seu dinheiro e faça seus planos crescerem.",
                        size="7",
                        line_height="1.08",
                        color="white",
                        max_width="620px",
                    ),
                    rx.text(
                        "Acompanhe receitas e despesas, cuide das contas do mês "
                        "e avance nas suas metas em um só lugar.",
                        size="4",
                        line_height="1.65",
                        color=MUTED,
                        max_width="560px",
                    ),
                    rx.hstack(
                        botao_acesso(),
                        rx.link(
                            rx.button(
                                "Conheça os recursos",
                                variant="outline",
                                color="white",
                                border_color="#45605d",
                                border_radius="999px",
                                height="46px",
                                padding_x="1.2em",
                            ),
                            href="#recursos",
                            text_decoration="none",
                        ),
                        spacing="3",
                        flex_wrap="wrap",
                        align="center",
                    ),
                    rx.text(
                        "Gratuito para começar · Seus dados protegidos por conta",
                        size="2",
                        color="#819a96",
                    ),
                    align="start",
                    spacing="5",
                    width="100%",
                ),
                rx.center(
                    previa_painel(),
                    width="100%",
                    padding="2em",
                ),
                direction={"initial": "column", "md": "row"},
                align="center",
                justify="between",
                width="100%",
                max_width="1180px",
                margin="0 auto",
                padding={"initial": "2em 1.5em 4em", "md": "3em 1.5em 5em"},
                gap="2em",
            ),
            width="100%",
            spacing="0",
        ),
        id="inicio",
        position="relative",
        overflow="hidden",
        width="100%",
        background=(
            "radial-gradient(ellipse at 72% 15%, rgba(22, 125, 91, 0.32), transparent 38%), "
            "linear-gradient(115deg, #061518 8%, #071c20 58%, #0b2c27 100%)"
        ),
    )


def cartao_recurso(icone: str, titulo: str, texto: str) -> rx.Component:
    return rx.vstack(
        rx.center(
            rx.icon(icone, size=22, color=BG),
            width="50px",
            height="50px",
            border_radius="16px",
            background=GREEN,
        ),
        rx.heading(titulo, size="4", color="white"),
        rx.text(texto, size="2", line_height="1.6", color=MUTED),
        align="start",
        spacing="3",
        width="100%",
        padding="1.3em",
        min_height="200px",
        border="1px solid #1b3939",
        border_radius="18px",
        background="linear-gradient(145deg, #0d2225, #09191c)",
    )


def recursos() -> rx.Component:
    return rx.vstack(
        rx.vstack(
            rx.text(
                "PRINCIPAIS RECURSOS",
                size="2",
                weight="bold",
                color=GREEN,
                letter_spacing="0.12em",
            ),
            rx.heading(
                "Tudo o que você precisa para cuidar bem do seu dinheiro.",
                size="7",
                color="white",
                max_width="760px",
            ),
            align="start",
            spacing="3",
        ),
        rx.grid(
            cartao_recurso(
                "chart-no-axes-combined",
                "Controle de gastos",
                "Registre receitas e despesas e acompanhe o seu saldo com clareza.",
            ),
            cartao_recurso(
                "target",
                "Metas financeiras",
                "Defina objetivos, acompanhe o progresso e avance no seu ritmo.",
            ),
            cartao_recurso(
                "calendar-days",
                "Contas e vencimentos",
                "Organize os próximos pagamentos e visualize as datas importantes.",
            ),
            cartao_recurso(
                "shield-check",
                "Privacidade por usuário",
                "Acesse seus dados em uma conta protegida e separada.",
            ),
            columns={"initial": "1", "sm": "2", "lg": "4"},
            spacing="4",
            width="100%",
        ),
        id="recursos",
        width="100%",
        max_width="1180px",
        margin="0 auto",
        padding={"initial": "4em 1.5em", "md": "6em 1.5em"},
        spacing="5",
    )


def como_funciona() -> rx.Component:
    passos = [
        ("01", "Crie sua conta", "Acesse o CashSave com seu e-mail."),
        ("02", "Registre sua rotina", "Adicione contas, receitas e despesas."),
        ("03", "Acompanhe seus planos", "Veja seus resumos, metas e vencimentos."),
    ]
    return rx.box(
        rx.flex(
            rx.vstack(
                rx.text(
                    "SIMPLES, COMPLETO E FEITO PARA VOCÊ",
                    size="2",
                    weight="bold",
                    color=GREEN,
                    letter_spacing="0.1em",
                ),
                rx.heading(
                    "Pequenas decisões hoje. Mais tranquilidade amanhã.",
                    size="7",
                    color="white",
                    line_height="1.1",
                ),
                rx.text(
                    "Uma forma prática de entender seu dinheiro e transformar "
                    "seus objetivos em próximos passos.",
                    color=MUTED,
                    line_height="1.7",
                ),
                rx.vstack(
                    *[
                        rx.hstack(
                            rx.center(
                                rx.text(numero, size="2", weight="bold", color=BG),
                                width="34px",
                                height="34px",
                                border_radius="50%",
                                background=GREEN,
                                flex_shrink="0",
                            ),
                            rx.vstack(
                                rx.text(titulo, weight="bold", color="white"),
                                rx.text(texto, size="2", color=MUTED),
                                spacing="1",
                                align="start",
                            ),
                            spacing="3",
                            align="center",
                            width="100%",
                        )
                        for numero, titulo, texto in passos
                    ],
                    spacing="4",
                    width="100%",
                    padding_top="1em",
                ),
                align="start",
                spacing="4",
                width="100%",
            ),
            rx.vstack(
                rx.hstack(
                    rx.icon("sparkles", color=GREEN, size=22),
                    rx.text("Seu progresso, em perspectiva", weight="bold", color="white"),
                    spacing="3",
                    align="center",
                ),
                rx.text(
                    "Receitas, despesas, contas e metas reunidas em uma visão "
                    "simples para ajudar você a tomar decisões com mais confiança.",
                    color=MUTED,
                    line_height="1.7",
                ),
                rx.hstack(
                    rx.vstack(
                        rx.text("ORGANIZAÇÃO", size="1", color=MUTED),
                        rx.text("Um passo de cada vez", weight="bold", color="white"),
                        spacing="1",
                    ),
                    rx.spacer(),
                    rx.icon("arrow-up-right", color=GREEN),
                    width="100%",
                    padding="1em",
                    border="1px solid #265447",
                    border_radius="14px",
                    background="#0a2824",
                ),
                align="start",
                spacing="4",
                width="100%",
                padding="1.5em",
                border="1px solid #1b3939",
                border_radius="22px",
                background="linear-gradient(145deg, #10282b, #0a1b1e)",
            ),
            direction={"initial": "column", "md": "row"},
            align="center",
            gap="3em",
            width="100%",
            max_width="1180px",
            margin="0 auto",
            padding_x="1.5em",
        ),
        id="como-funciona",
        width="100%",
        padding={"initial": "1em 1.5em 5em", "md": "2em 1.5em 7em"},
        background=(
            "radial-gradient(ellipse at 80% 50%, rgba(20, 139, 100, 0.12), transparent 42%), "
            "#07191c"
        ),
    )


def chamada_final() -> rx.Component:
    return rx.vstack(
        rx.icon("piggy-bank", size=34, color=GREEN),
        rx.heading(
            "Seu próximo passo começa agora.",
            size="7",
            color="white",
            text_align="center",
        ),
        rx.text(
            "Comece a organizar sua vida financeira com o CashSave.",
            color=MUTED,
            text_align="center",
        ),
        botao_acesso("Entrar no CashSave"),
        id="baixar",
        width="100%",
        align="center",
        spacing="4",
        padding={"initial": "4em 1.5em", "md": "6em 1.5em"},
        background=(
            "linear-gradient(180deg, #07191c, #08251f)"
        ),
    )


def landing_page() -> rx.Component:
    return rx.vstack(
        hero(),
        recursos(),
        como_funciona(),
        chamada_final(),
        rx.hstack(
            marca(),
            rx.spacer(),
            rx.text("CashSave · Organização financeira para sua rotina.", size="2", color=MUTED),
            width="100%",
            max_width="1180px",
            margin="0 auto",
            padding="1.5em",
        ),
        width="100%",
        min_height="100vh",
        spacing="0",
        background=BG,
    )
