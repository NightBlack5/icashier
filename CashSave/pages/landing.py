import reflex as rx


BG = "var(--cashsave-bg-deep)"
PANEL = "var(--cashsave-surface)"
PANEL_LIGHT = "var(--cashsave-surface-raised)"
GREEN = "var(--cashsave-green)"
MUTED = "var(--cashsave-muted)"


def marca() -> rx.Component:
    return rx.hstack(
        rx.center(
            rx.icon("piggy-bank", size=19, color=BG),
            width="36px",
            height="36px",
            border_radius="50%",
            background=GREEN,
        ),
        rx.heading(
            rx.fragment(
                rx.text("Cash", as_="span", color="white"),
                rx.text("Save", as_="span", color=GREEN),
            ),
            size="5",
            letter_spacing="-0.05em",
        ),
        spacing="2",
        align="center",
    )


def botao_acesso(
    rotulo: str = "Começar grátis",
    rota: str = "/cadastro",
) -> rx.Component:
    return rx.link(
        rx.button(
            rotulo,
            rx.icon("arrow-up-right", size=17),
            color=BG,
            background=GREEN,
            border_radius="999px",
            padding_x="1.35em",
            height="46px",
            font_weight="bold",
            box_shadow="0 8px 26px rgba(67, 218, 157, 0.16)",
            _hover={
                "background": "#79edbd",
                "transform": "translateY(-2px)",
                "box_shadow": "0 12px 32px rgba(67, 218, 157, 0.24)",
            },
            transition="all 180ms ease",
            class_name="landing-cta",
        ),
        href=rota,
        text_decoration="none",
    )


def link_secao(rotulo: str, secao: str) -> rx.Component:
    return rx.link(
        rotulo,
        href=f"#{secao}",
        color="#c0d0ca",
        font_size="0.92rem",
        font_weight="medium",
        text_decoration="none",
        _hover={"color": GREEN},
        transition="color 160ms ease",
    )


def cabecalho_landing() -> rx.Component:
    return rx.box(
        rx.flex(
            rx.link(marca(), href="#inicio", text_decoration="none"),
            rx.hstack(
                link_secao("Início", "inicio"),
                link_secao("Recursos", "recursos"),
                link_secao("Jarvis", "jarvis"),
                link_secao("Como funciona", "como-funciona"),
                spacing="6",
                display={"initial": "none", "lg": "flex"},
                align="center",
                class_name="landing-main-nav",
            ),
            rx.hstack(
                rx.link(
                    "Acessar",
                    href="/login",
                    color="#dce8e2",
                    font_weight="medium",
                    text_decoration="none",
                    _hover={"color": GREEN},
                    class_name="landing-login-link",
                ),
                botao_acesso("Criar conta"),
                spacing={"initial": "2", "sm": "4"},
                align="center",
            ),
            justify="between",
            align="center",
            width="100%",
            max_width="1280px",
            margin="0 auto",
            padding={"initial": "0.8em 1em", "md": "0.85em 1.5em"},
        ),
        position="sticky",
        top="0",
        z_index="20",
        width="100%",
        border_bottom="1px solid rgba(151, 190, 169, 0.1)",
        background="rgba(5, 13, 11, 0.82)",
        backdrop_filter="blur(18px)",
        class_name="cashsave-landing-header",
    )


def barra_categoria(
    nome: str,
    valor: str,
    largura: str,
    cor: str = GREEN,
) -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.text(nome, size="1", color="#c1d0ca"),
            rx.spacer(),
            rx.text(valor, size="1", weight="bold", color="white"),
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
            background="#1a302b",
        ),
        spacing="1",
        width="100%",
    )


def mini_indicador(
    titulo: str,
    valor: str,
    icone: str,
    variacao: str,
    destaque: bool = False,
) -> rx.Component:
    return rx.hstack(
        rx.center(
            rx.icon(icone, size=17, color=GREEN if destaque else "#a5bbb1"),
            width="36px",
            height="36px",
            border_radius="12px",
            background="rgba(99, 227, 170, 0.09)" if destaque else "rgba(255,255,255,0.045)",
        ),
        rx.vstack(
            rx.text(titulo, size="1", color=MUTED),
            rx.hstack(
                rx.text(valor, size="2", weight="bold", color="white"),
                rx.text(variacao, size="1", color=GREEN if destaque else "#9aada3"),
                spacing="2",
                align="center",
                flex_wrap="wrap",
            ),
            align="start",
            spacing="1",
        ),
        align="center",
        spacing="3",
        width="100%",
        padding="0.8em",
        border="1px solid rgba(159, 190, 175, 0.1)",
        border_radius="14px",
        background="rgba(255,255,255,0.025)",
    )


def painel_resumo_ilustrativo() -> rx.Component:
    alturas = ["42%", "66%", "50%", "82%", "58%", "92%", "70%", "100%"]
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.text("VISÃO GERAL", size="1", weight="bold", color=GREEN, letter_spacing="0.12em"),
                rx.text("Seu dinheiro, em perspectiva", size="3", weight="bold", color="white"),
                align="start",
                spacing="1",
            ),
            rx.spacer(),
            rx.center(
                rx.icon("ellipsis", size=18, color="#a6b8b0"),
                width="34px",
                height="34px",
                border="1px solid rgba(159, 190, 175, 0.14)",
                border_radius="10px",
            ),
            width="100%",
            align="center",
        ),
        rx.box(
            rx.text(
                "DEMONSTRAÇÃO · DADOS ILUSTRATIVOS",
                size="1",
                color="#9ab0a6",
                letter_spacing="0.08em",
            ),
            padding="0.5em 0.7em",
            border="1px solid rgba(99, 227, 170, 0.16)",
            border_radius="999px",
            background="rgba(99, 227, 170, 0.055)",
            width="fit-content",
        ),
        rx.vstack(
            rx.text("Saldo do mês", size="2", color=MUTED),
            rx.heading("R$ 4.280,00", size="7", color="white", letter_spacing="-0.055em"),
            rx.hstack(
                rx.icon("arrow-up-right", size=14, color=GREEN),
                rx.text("Exemplo de acompanhamento", size="1", color=GREEN),
                spacing="1",
                align="center",
            ),
            align="start",
            spacing="1",
            width="100%",
            padding="1.1em",
            border="1px solid rgba(99, 227, 170, 0.18)",
            border_radius="16px",
            background="linear-gradient(130deg, rgba(21, 64, 48, 0.82), rgba(11, 31, 26, 0.9))",
        ),
        rx.grid(
            mini_indicador("Receitas", "R$ 6.850", "arrow-down-left", "ilustrativo", True),
            mini_indicador("Despesas", "R$ 2.570", "arrow-up-right", "ilustrativo"),
            columns="2",
            spacing="3",
            width="100%",
        ),
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.text("Movimentação", size="2", weight="bold", color="white"),
                    rx.text("Exemplo de visualização mensal", size="1", color=MUTED),
                    align="start",
                    spacing="1",
                ),
                rx.spacer(),
                rx.icon("chart-no-axes-combined", size=18, color=GREEN),
                width="100%",
                align="center",
            ),
            rx.flex(
                *[
                    rx.box(
                        rx.box(
                            width="100%",
                            height="100%",
                            border_radius="999px",
                            background=(
                                "linear-gradient(180deg, #7aefbe, #27a977)"
                                if index in (3, 5, 7)
                                else "linear-gradient(180deg, #367c60, #1d4638)"
                            ),
                            class_name="landing-chart-bar",
                        ),
                        height=height,
                        width="9%",
                        border_radius="999px",
                        background="rgba(255,255,255,0.035)",
                        class_name=f"landing-chart-column landing-chart-column-{index + 1}",
                    )
                    for index, height in enumerate(alturas)
                ],
                width="100%",
                height="84px",
                align="end",
                justify="between",
                padding_top="0.6em",
                class_name="landing-chart",
            ),
            rx.hstack(
                *[
                    rx.text(label, size="1", color="#839990")
                    for label in ["S", "T", "Q", "Q", "S", "S", "D", "M"]
                ],
                width="100%",
                justify="between",
            ),
            spacing="3",
            width="100%",
            padding="1em",
            border="1px solid rgba(159, 190, 175,  0.1)",
            border_radius="16px",
            background="rgba(8, 20, 17, 0.82)",
        ),
        width="100%",
        padding="1.1em",
        spacing="3",
        border="1px solid rgba(151, 190, 169, 0.18)",
        border_radius="24px",
        background="linear-gradient(150deg, rgba(17, 37, 31, 0.98), rgba(7, 17, 15, 0.97))",
        box_shadow="0 32px 90px rgba(0, 0, 0, 0.48)",
        class_name="landing-dashboard",
    )


def cartao_flutuante(
    icone: str,
    titulo: str,
    detalhe: str,
    classe: str,
) -> rx.Component:
    return rx.hstack(
        rx.center(
            rx.icon(icone, size=18, color=BG),
            width="38px",
            height="38px",
            border_radius="13px",
            background=GREEN,
            flex_shrink="0",
        ),
        rx.vstack(
            rx.text(titulo, size="1", weight="bold", color="white"),
            rx.text(detalhe, size="1", color=MUTED),
            align="start",
            spacing="1",
        ),
        align="center",
        spacing="3",
        padding="0.8em 1em",
        border="1px solid rgba(151, 190, 169, 0.17)",
        border_radius="16px",
        background="rgba(13, 29, 24, 0.94)",
        box_shadow="0 16px 42px rgba(0, 0, 0, 0.32)",
        backdrop_filter="blur(14px)",
        class_name=f"landing-float-card {classe}",
    )


def previa_painel() -> rx.Component:
    return rx.box(
        rx.box(
            position="absolute",
            inset="10% 12%",
            border_radius="50%",
            background="radial-gradient(circle, rgba(55, 197, 138, 0.19), transparent 68%)",
            filter="blur(22px)",
            class_name="landing-visual-glow",
        ),
        rx.box(
            painel_resumo_ilustrativo(),
            position="relative",
            z_index="1",
            width="100%",
            max_width="560px",
            transform="rotateY(-7deg) rotateX(2deg)",
            class_name="landing-dashboard-wrap",
        ),
        cartao_flutuante(
            "bot",
            "Jarvis",
            "Pronto para ajudar",
            "landing-float-card--jarvis",
        ),
        cartao_flutuante(
            "target",
            "Metas em foco",
            "Acompanhe no seu ritmo",
            "landing-float-card--goals",
        ),
        position="relative",
        display="flex",
        align_items="center",
        justify_content="center",
        width={"initial": "100%", "lg": "48%"},
        min_height={"initial": "auto", "md": "530px"},
        padding={"initial": "1.5em 0.4em", "md": "2.5em"},
        class_name="landing-hero-visual",
    )


def hero() -> rx.Component:
    return rx.box(
        rx.box(
            position="absolute",
            top="-220px",
            right="-180px",
            width="740px",
            height="740px",
            border_radius="50%",
            background="radial-gradient(circle, rgba(31, 137, 92, 0.2), transparent 68%)",
            pointer_events="none",
            class_name="landing-hero-orb landing-hero-orb--one",
        ),
        rx.box(
            position="absolute",
            bottom="-250px",
            left="-220px",
            width="620px",
            height="620px",
            border_radius="50%",
            background="radial-gradient(circle, rgba(32, 99, 75, 0.15), transparent 68%)",
            pointer_events="none",
            class_name="landing-hero-orb landing-hero-orb--two",
        ),
        rx.flex(
            rx.vstack(
                rx.hstack(
                    rx.center(
                        rx.icon("sparkles", size=15, color=GREEN),
                        width="28px",
                        height="28px",
                        border_radius="50%",
                        background="rgba(99, 227, 170, 0.1)",
                    ),
                    rx.text(
                        "FINANÇAS MAIS CLARAS. PLANOS MAIS SEUS.",
                        size="1",
                        weight="bold",
                        color=GREEN,
                        letter_spacing="0.1em",
                    ),
                    spacing="2",
                    align="center",
                ),
                rx.heading(
                    "Seu dinheiro merece uma inteligência à altura dos seus planos.",
                    size="9",
                    line_height="1.02",
                    letter_spacing="-0.06em",
                    color="white",
                    max_width="680px",
                    class_name="landing-hero-title",
                ),
                rx.text(
                    "Organize suas finanças, entenda seus hábitos e tome decisões "
                    "mais conscientes com a ajuda de um assistente financeiro inteligente.",
                    size="4",
                    line_height="1.7",
                    color="#a8bbb2",
                    max_width="590px",
                ),
                rx.hstack(
                    botao_acesso(),
                    rx.link(
                        rx.button(
                            rx.icon("play", size=15),
                            "Conheça os recursos",
                            variant="outline",
                            color="#e6f0eb",
                            border_color="rgba(168, 195, 181, 0.28)",
                            border_radius="999px",
                            height="46px",
                            padding_x="1.2em",
                            background="rgba(255,255,255,0.025)",
                            _hover={
                                "background": "rgba(255,255,255,0.07)",
                                "border_color": "rgba(99, 227, 170, 0.4)",
                            },
                        ),
                        href="#recursos",
                        text_decoration="none",
                    ),
                    spacing="3",
                    flex_wrap="wrap",
                    align="center",
                ),
                rx.flex(
                    rx.hstack(
                        rx.center(rx.icon("check", size=13, color=GREEN), width="20px", height="20px", border_radius="50%", background="rgba(99,227,170,0.1)"),
                        rx.text("Receitas e despesas", size="1", color="#afc0b7"),
                        spacing="2",
                        align="center",
                    ),
                    rx.hstack(
                        rx.center(rx.icon("check", size=13, color=GREEN), width="20px", height="20px", border_radius="50%", background="rgba(99,227,170,0.1)"),
                        rx.text("Metas financeiras", size="1", color="#afc0b7"),
                        spacing="2",
                        align="center",
                    ),
                    rx.hstack(
                        rx.center(rx.icon("check", size=13, color=GREEN), width="20px", height="20px", border_radius="50%", background="rgba(99,227,170,0.1)"),
                        rx.text("Assistente Jarvis", size="1", color="#afc0b7"),
                        spacing="2",
                        align="center",
                    ),
                    spacing={"initial": "3", "sm": "5"},
                    flex_wrap="wrap",
                    width="100%",
                ),
                align="start",
                spacing="5",
                width={"initial": "100%", "lg": "48%"},
                max_width="650px",
                class_name="landing-hero-copy",
            ),
            previa_painel(),
            direction={"initial": "column", "lg": "row"},
            align="center",
            justify="between",
            width="100%",
            max_width="1280px",
            margin="0 auto",
            padding={"initial": "3.5em 1.25em 4.5em", "md": "5.5em 1.75em 6em"},
            gap={"initial": "1.5em", "lg": "2em"},
            position="relative",
            z_index="1",
        ),
        id="inicio",
        position="relative",
        overflow="hidden",
        width="100%",
        background=(
            "radial-gradient(ellipse at 82% 36%, rgba(32, 112, 78, 0.15), transparent 44%), "
            "linear-gradient(125deg, #050d0b 0%, #091813 52%, #0b2118 100%)"
        ),
        class_name="landing-hero",
    )


def cabecalho_secao(
    eyebrow: str,
    titulo: str,
    texto: str,
    alinhamento: str = "start",
) -> rx.Component:
    return rx.vstack(
        rx.text(
            eyebrow.upper(),
            size="1",
            weight="bold",
            color=GREEN,
            letter_spacing="0.14em",
        ),
        rx.heading(
            titulo,
            size="8",
            line_height="1.05",
            letter_spacing="-0.055em",
            color="white",
            max_width="760px",
        ),
        rx.text(
            texto,
            size="3",
            line_height="1.7",
            color=MUTED,
            max_width="680px",
        ),
        align=alinhamento,
        spacing="3",
        width="100%",
    )


def recurso_financas() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.box(
                    "01  /  FINANÇAS",
                    padding="0.45em 0.7em",
                    border="1px solid rgba(99, 227, 170, 0.18)",
                    border_radius="999px",
                    color=GREEN,
                    font_size="0.7rem",
                    letter_spacing="0.08em",
                ),
                rx.heading("Tenha clareza sobre o que entra e sai.", size="5", color="white", line_height="1.1"),
                rx.text(
                    "Registre receitas e despesas e veja suas movimentações organizadas em um só lugar.",
                    size="2",
                    color=MUTED,
                    line_height="1.65",
                ),
                align="start",
                spacing="3",
                width="100%",
            ),
            rx.spacer(),
            rx.center(
                rx.icon("arrow-down-up", size=20, color=GREEN),
                width="46px",
                height="46px",
                border_radius="15px",
                background="rgba(99, 227, 170, 0.09)",
                flex_shrink="0",
            ),
            width="100%",
            align="start",
        ),
        rx.vstack(
            rx.hstack(
                rx.hstack(rx.icon("arrow-down-left", size=15, color=GREEN), rx.text("Entrada", size="1", color="#c2d2ca"), spacing="2"),
                rx.spacer(),
                rx.text("Registro organizado", size="1", color="#81978c"),
                width="100%",
            ),
            rx.divider(border_color="rgba(159, 190, 175, 0.12)"),
            rx.hstack(
                rx.hstack(rx.icon("arrow-up-right", size=15, color="#e7a987"), rx.text("Saída", size="1", color="#c2d2ca"), spacing="2"),
                rx.spacer(),
                rx.text("Por categoria", size="1", color="#81978c"),
                width="100%",
            ),
            spacing="3",
            width="100%",
            padding="1em",
            border="1px solid rgba(159, 190, 175, 0.1)",
            border_radius="15px",
            background="rgba(4, 14, 11, 0.55)",
        ),
        align="start",
        spacing="4",
        width="100%",
        min_height="270px",
        padding="1.4em",
        border="1px solid rgba(159, 190, 175, 0.13)",
        border_radius="22px",
        background="linear-gradient(145deg, rgba(18, 39, 31, 0.92), rgba(10, 23, 19, 0.94))",
        class_name="landing-feature-card landing-feature-finance",
    )


def recurso_jarvis() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.center(
                rx.icon("bot", size=19, color=BG),
                width="42px",
                height="42px",
                border_radius="14px",
                background=GREEN,
            ),
            rx.vstack(
                rx.text("JARVIS", size="1", weight="bold", color=GREEN, letter_spacing="0.12em"),
                rx.heading("Converse. Organize. Siga.", size="4", color="white"),
                align="start",
                spacing="1",
            ),
            spacing="3",
            align="center",
        ),
        rx.text(
            "O assistente já disponível no CashSave ajuda a registrar receitas e despesas por conversa.",
            size="2",
            color=MUTED,
            line_height="1.65",
        ),
        rx.box(
            rx.hstack(
                rx.icon("message-circle", size=17, color=GREEN),
                rx.text("Registros por conversa", size="2", weight="medium", color="#e3eee8"),
                spacing="2",
                align="center",
            ),
            padding="0.9em",
            border="1px solid rgba(99, 227, 170, 0.15)",
            border_radius="14px",
            background="rgba(99, 227, 170, 0.045)",
            width="100%",
        ),
        rx.link(
            rx.hstack(
                rx.text("Conheça o Jarvis", size="2", weight="bold", color=GREEN),
                rx.icon("arrow-up-right", size=16, color=GREEN),
                spacing="2",
                align="center",
            ),
            href="/assistente",
            text_decoration="none",
        ),
        align="start",
        spacing="4",
        width="100%",
        min_height="270px",
        padding="1.4em",
        border="1px solid rgba(99, 227, 170, 0.18)",
        border_radius="22px",
        background=(
            "radial-gradient(ellipse at 100% 0%, rgba(42, 171, 120, 0.13), transparent 46%), "
            "linear-gradient(145deg, rgba(17, 40, 32, 0.97), rgba(8, 20, 17, 0.96))"
        ),
        class_name="landing-feature-card landing-feature-jarvis",
    )


def recurso_graficos() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.box(
                    "02  /  VISÃO GERAL",
                    padding="0.45em 0.7em",
                    border="1px solid rgba(99, 227, 170, 0.18)",
                    border_radius="999px",
                    color=GREEN,
                    font_size="0.7rem",
                    letter_spacing="0.08em",
                ),
                rx.heading("Transforme movimentações em uma visão mais clara.", size="5", color="white", line_height="1.1"),
                rx.text(
                    "Consulte resumos e gráficos para acompanhar suas finanças e entender seus hábitos.",
                    size="2",
                    color=MUTED,
                    line_height="1.65",
                ),
                align="start",
                spacing="3",
            ),
            rx.spacer(),
            rx.icon("chart-no-axes-combined", size=22, color=GREEN),
            width="100%",
            align="start",
        ),
        rx.hstack(
            rx.text("Resumo financeiro", size="1", color="#acc0b6"),
            rx.spacer(),
            rx.text("EXEMPLO ILUSTRATIVO", size="1", color=GREEN),
            width="100%",
        ),
        rx.hstack(
            rx.box(width="12%", height="38px", border_radius="6px 6px 2px 2px", background="#285540", class_name="landing-chart-bar"),
            rx.box(width="12%", height="60px", border_radius="6px 6px 2px 2px", background="#397f5e", class_name="landing-chart-bar"),
            rx.box(width="12%", height="45px", border_radius="6px 6px 2px 2px", background="#285540", class_name="landing-chart-bar"),
            rx.box(width="12%", height="79px", border_radius="6px 6px 2px 2px", background=GREEN, class_name="landing-chart-bar"),
            rx.box(width="12%", height="55px", border_radius="6px 6px 2px 2px", background="#397f5e", class_name="landing-chart-bar"),
            rx.box(width="12%", height="90px", border_radius="6px 6px 2px 2px", background=GREEN, class_name="landing-chart-bar"),
            width="100%",
            height="100px",
            align="end",
            justify="between",
            padding_x="0.5em",
        ),
        spacing="4",
        align="start",
        width="100%",
        min_height="270px",
        padding="1.4em",
        border="1px solid rgba(159, 190, 175, 0.13)",
        border_radius="22px",
        background="linear-gradient(145deg, rgba(17, 34, 30, 0.95), rgba(9, 20, 19, 0.96))",
        class_name="landing-feature-card landing-feature-analytics",
    )


def recurso_contas_metas() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.center(
                rx.icon("calendar-days", size=19, color=GREEN),
                width="42px",
                height="42px",
                border_radius="14px",
                background="rgba(99, 227, 170, 0.09)",
            ),
            rx.vstack(
                rx.text("ROTINA FINANCEIRA", size="1", weight="bold", color=GREEN, letter_spacing="0.1em"),
                rx.heading("Contas e metas no seu ritmo.", size="4", color="white"),
                align="start",
                spacing="1",
            ),
            spacing="3",
            align="center",
        ),
        rx.text(
            "Organize vencimentos e acompanhe objetivos para manter seus próximos passos à vista.",
            size="2",
            color=MUTED,
            line_height="1.65",
        ),
        rx.hstack(
            rx.center(rx.icon("calendar-check", size=17, color="#a8c9b8"), width="36px", height="36px", border_radius="12px", background="rgba(255,255,255,0.04)"),
            rx.vstack(
                rx.text("Calendário", size="2", weight="bold", color="white"),
                rx.text("Datas importantes em contexto", size="1", color=MUTED),
                align="start",
                spacing="1",
            ),
            spacing="3",
            align="center",
            width="100%",
        ),
        rx.hstack(
            rx.center(rx.icon("target", size=17, color=GREEN), width="36px", height="36px", border_radius="12px", background="rgba(99,227,170,0.08)"),
            rx.vstack(
                rx.text("Metas financeiras", size="2", weight="bold", color="white"),
                rx.text("Acompanhe seu progresso", size="1", color=MUTED),
                align="start",
                spacing="1",
            ),
            spacing="3",
            align="center",
            width="100%",
        ),
        align="start",
        spacing="4",
        width="100%",
        min_height="270px",
        padding="1.4em",
        border="1px solid rgba(159, 190, 175, 0.13)",
        border_radius="22px",
        background="linear-gradient(145deg, rgba(18, 35, 38, 0.92), rgba(9, 20, 22, 0.96))",
        class_name="landing-feature-card landing-feature-routine",
    )


def recurso_perfil() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.center(
                rx.icon("scan-heart", size=19, color=GREEN),
                width="42px",
                height="42px",
                border_radius="14px",
                background="rgba(99, 227, 170, 0.09)",
            ),
            rx.vstack(
                rx.text("PERFIL FINANCEIRO", size="1", weight="bold", color=GREEN, letter_spacing="0.1em"),
                rx.heading("Conheça melhor seu momento.", size="4", color="white"),
                align="start",
                spacing="1",
            ),
            spacing="3",
            align="center",
        ),
        rx.text(
            "Compartilhe seu contexto no seu tempo e veja uma leitura orientativa do seu perfil de investidor.",
            size="2",
            color=MUTED,
            line_height="1.65",
        ),
        rx.hstack(
            rx.badge("Conservador", color_scheme="green", variant="soft"),
            rx.badge("Moderado", color_scheme="green", variant="soft"),
            rx.badge("Arrojado", color_scheme="green", variant="soft"),
            spacing="2",
            flex_wrap="wrap",
        ),
        rx.text(
            "Informativo: não substitui orientação financeira individual.",
            size="1",
            color="#859990",
        ),
        align="start",
        spacing="4",
        width="100%",
        min_height="270px",
        padding="1.4em",
        border="1px solid rgba(159, 190, 175, 0.13)",
        border_radius="22px",
        background="linear-gradient(145deg, rgba(27, 35, 31, 0.94), rgba(11, 20, 18, 0.96))",
        class_name="landing-feature-card landing-feature-profile",
    )


def recursos() -> rx.Component:
    return rx.vstack(
        cabecalho_secao(
            "O que você pode fazer",
            "Uma visão mais completa da sua vida financeira.",
            "Ferramentas para organizar o dia a dia, acompanhar objetivos e entender melhor suas movimentações.",
        ),
        rx.grid(
            recurso_financas(),
            recurso_jarvis(),
            recurso_graficos(),
            recurso_contas_metas(),
            recurso_perfil(),
            columns={"initial": "1", "md": "2", "xl": "3"},
            spacing="4",
            width="100%",
            class_name="landing-feature-grid",
        ),
        id="recursos",
        width="100%",
        max_width="1280px",
        margin="0 auto",
        padding={"initial": "4.5em 1.25em", "md": "7em 1.75em"},
        spacing="5",
        class_name="landing-section landing-scroll-reveal",
    )


def demonstracao_jarvis() -> rx.Component:
    return rx.box(
        rx.flex(
            rx.vstack(
                rx.hstack(
                    rx.center(
                        rx.icon("bot", size=19, color=BG),
                        width="42px",
                        height="42px",
                        border_radius="14px",
                        background=GREEN,
                    ),
                    rx.text(
                        "JARVIS · SEU ASSISTENTE FINANCEIRO",
                        size="1",
                        weight="bold",
                        color=GREEN,
                        letter_spacing="0.1em",
                    ),
                    spacing="3",
                    align="center",
                ),
                rx.heading(
                    "Uma conversa simples. Menos trabalho na rotina.",
                    size="8",
                    color="white",
                    line_height="1.05",
                    letter_spacing="-0.05em",
                    max_width="560px",
                ),
                rx.text(
                    "O Jarvis já faz parte do CashSave. Conte o que aconteceu e ele pode ajudar a registrar receitas e despesas na conversa.",
                    size="3",
                    color=MUTED,
                    line_height="1.75",
                    max_width="540px",
                ),
                rx.hstack(
                    rx.icon("info", size=16, color="#a3b8ad"),
                    rx.text(
                        "Esta conversa é apenas uma demonstração visual.",
                        size="2",
                        color="#a3b8ad",
                    ),
                    spacing="2",
                    align="center",
                ),
                rx.link(
                    rx.hstack(
                        rx.text("Explorar o Jarvis", weight="bold", color=GREEN),
                        rx.icon("arrow-right", size=16, color=GREEN),
                        spacing="2",
                        align="center",
                    ),
                    href="/assistente",
                    text_decoration="none",
                ),
                align="start",
                spacing="4",
                width="100%",
            ),
            rx.vstack(
                rx.hstack(
                    rx.hstack(
                        rx.center(
                            rx.icon("bot", size=15, color=BG),
                            width="30px",
                            height="30px",
                            border_radius="50%",
                            background=GREEN,
                        ),
                        rx.vstack(
                            rx.text("Jarvis", size="2", weight="bold", color="white"),
                            rx.text("DEMONSTRAÇÃO ESTÁTICA", size="1", color="#81988d", letter_spacing="0.06em"),
                            align="start",
                            spacing="0",
                        ),
                        spacing="2",
                        align="center",
                    ),
                    rx.spacer(),
                    rx.box(
                        rx.text("EXEMPLO", size="1", weight="bold", color=GREEN, letter_spacing="0.08em"),
                        padding="0.45em 0.7em",
                        border="1px solid rgba(99, 227, 170, 0.18)",
                        border_radius="999px",
                        background="rgba(99, 227, 170, 0.06)",
                    ),
                    width="100%",
                    align="center",
                    padding_bottom="1em",
                    border_bottom="1px solid rgba(159, 190, 175, 0.12)",
                ),
                rx.vstack(
                    rx.box(
                        rx.text("Gastei R$ 45 no almoço.", size="2", color="white", line_height="1.5"),
                        align_self="end",
                        max_width="88%",
                        padding="0.85em 1em",
                        border="1px solid rgba(99, 227, 170, 0.18)",
                        border_radius="16px 16px 4px 16px",
                        background="rgba(50, 130, 92, 0.2)",
                        class_name="landing-chat-user",
                    ),
                    rx.hstack(
                        rx.text("Jarvis está digitando", size="1", color="#a9bdb2"),
                        rx.hstack(
                            rx.box(width="4px", height="4px", border_radius="50%", background=GREEN, class_name="landing-typing-dot landing-typing-dot--one"),
                            rx.box(width="4px", height="4px", border_radius="50%", background=GREEN, class_name="landing-typing-dot landing-typing-dot--two"),
                            rx.box(width="4px", height="4px", border_radius="50%", background=GREEN, class_name="landing-typing-dot landing-typing-dot--three"),
                            spacing="1",
                            align="center",
                        ),
                        align="center",
                        spacing="2",
                        class_name="landing-typing",
                    ),
                    rx.hstack(
                        rx.center(
                            rx.icon("bot", size=14, color=BG),
                            width="26px",
                            height="26px",
                            border_radius="50%",
                            background=GREEN,
                            flex_shrink="0",
                        ),
                        rx.box(
                            rx.text(
                                "Despesa registrada! Seu gasto foi adicionado à categoria Alimentação.",
                                size="2",
                                color="#e4eee8",
                                line_height="1.55",
                            ),
                            max_width="100%",
                            padding="0.85em 1em",
                            border="1px solid rgba(159, 190, 175, 0.12)",
                            border_radius="4px 16px 16px 16px",
                            background="rgba(255,255,255,0.045)",
                            class_name="landing-chat-reply",
                        ),
                        align="start",
                        spacing="2",
                        width="100%",
                    ),
                    width="100%",
                    spacing="4",
                    padding_y="1.2em",
                    align="stretch",
                ),
                rx.hstack(
                    rx.text("Demonstração: nenhuma transação foi criada.", size="1", color="#81988d"),
                    rx.spacer(),
                    rx.icon("sparkles", size=15, color=GREEN),
                    width="100%",
                    padding_top="0.9em",
                    border_top="1px solid rgba(159, 190, 175, 0.1)",
                ),
                spacing="0",
                width="100%",
                max_width="540px",
                padding="1.2em",
                border="1px solid rgba(159, 190, 175, 0.15)",
                border_radius="22px",
                background="linear-gradient(145deg, rgba(18, 38, 31, 0.96), rgba(8, 19, 16, 0.98))",
                box_shadow="0 28px 80px rgba(0,0,0,0.32)",
                class_name="landing-chat-card",
            ),
            direction={"initial": "column", "lg": "row"},
            align="center",
            justify="between",
            width="100%",
            max_width="1280px",
            margin="0 auto",
            padding={"initial": "4.5em 1.25em", "md": "6.5em 1.75em"},
            gap={"initial": "2.5em", "lg": "4em"},
        ),
        id="jarvis",
        width="100%",
        background=(
            "radial-gradient(ellipse at 88% 50%, rgba(31, 136, 91, 0.12), transparent 40%), "
            "linear-gradient(180deg, #071411, #091a16)"
        ),
        class_name="landing-section landing-scroll-reveal",
    )


def passo(
    numero: str,
    titulo: str,
    texto: str,
    icone: str,
) -> rx.Component:
    return rx.vstack(
        rx.center(
            rx.icon(icone, size=20, color=GREEN),
            width="48px",
            height="48px",
            border="1px solid rgba(99, 227, 170, 0.22)",
            border_radius="16px",
            background="rgba(99, 227, 170, 0.08)",
            class_name="landing-step-icon",
        ),
        rx.text(numero, size="1", weight="bold", color=GREEN, letter_spacing="0.12em"),
        rx.heading(titulo, size="3", color="white"),
        rx.text(texto, size="2", color=MUTED, line_height="1.6"),
        align="start",
        spacing="3",
        width="100%",
        padding="1.1em",
        border="1px solid rgba(159, 190, 175, 0.1)",
        border_radius="18px",
        background="rgba(255, 255, 255, 0.022)",
        class_name="landing-step",
    )


def como_funciona() -> rx.Component:
    return rx.vstack(
        cabecalho_secao(
            "Como funciona",
            "Organizar sua vida financeira pode ser mais simples.",
            "Um fluxo direto para você entender seu dinheiro e avançar nos seus objetivos.",
        ),
        rx.grid(
            passo("01", "Crie sua conta", "Comece pelo cadastro e acesse sua área pessoal.", "user-round-plus"),
            passo("02", "Organize informações", "Adicione contas e deixe sua rotina financeira em contexto.", "wallet"),
            passo("03", "Registre movimentações", "Acompanhe receitas e despesas conforme acontecem.", "arrow-down-up"),
            passo("04", "Converse com Jarvis", "Use o assistente para facilitar seus registros.", "bot"),
            passo("05", "Acompanhe seus planos", "Consulte resumos e siga suas metas no seu ritmo.", "chart-no-axes-combined"),
            columns={"initial": "1", "sm": "2", "xl": "5"},
            spacing="3",
            width="100%",
            class_name="landing-steps",
        ),
        rx.hstack(
            rx.text("Comece quando quiser. Avance no seu próprio ritmo.", size="2", color="#a8bcb2"),
            rx.spacer(),
            botao_acesso("Criar minha conta"),
            width="100%",
            align="center",
            flex_wrap="wrap",
            gap="1em",
            padding_top="1em",
        ),
        id="como-funciona",
        width="100%",
        max_width="1280px",
        margin="0 auto",
        padding={"initial": "4.5em 1.25em", "md": "7em 1.75em"},
        spacing="5",
        class_name="landing-section landing-scroll-reveal",
    )


def chamada_final() -> rx.Component:
    return rx.box(
        rx.box(
            position="absolute",
            inset="0",
            background="radial-gradient(ellipse at 50% 120%, rgba(55, 180, 125, 0.23), transparent 60%)",
            pointer_events="none",
        ),
        rx.vstack(
            rx.center(
                rx.icon("sparkles", size=22, color=GREEN),
                width="54px",
                height="54px",
                border_radius="18px",
                background="rgba(99, 227, 170, 0.1)",
            ),
            rx.heading(
                "Comece a cuidar melhor do seu dinheiro.",
                size="8",
                color="white",
                line_height="1.05",
                letter_spacing="-0.055em",
                text_align="center",
                max_width="760px",
            ),
            rx.text(
                "Organize sua rotina financeira e dê o próximo passo nos seus planos.",
                size="3",
                color=MUTED,
                text_align="center",
                max_width="560px",
                line_height="1.7",
            ),
            botao_acesso("Começar gratuitamente"),
            align="center",
            spacing="4",
            width="100%",
            max_width="820px",
            margin="0 auto",
            padding={"initial": "4.5em 1.25em", "md": "7em 1.75em"},
            position="relative",
            z_index="1",
        ),
        id="comece",
        width="100%",
        position="relative",
        overflow="hidden",
        background="linear-gradient(180deg, #081713 0%, #07120f 100%)",
        class_name="landing-final landing-scroll-reveal",
    )


def rodape() -> rx.Component:
    return rx.flex(
        rx.vstack(
            rx.link(marca(), href="#inicio", text_decoration="none"),
            rx.text(
                "Organização financeira para a vida real.",
                size="2",
                color=MUTED,
            ),
            align="start",
            spacing="2",
        ),
        rx.hstack(
            link_secao("Início", "inicio"),
            link_secao("Recursos", "recursos"),
            link_secao("Como funciona", "como-funciona"),
            rx.link("Sobre", href="/sobre", color="#c0d0ca", text_decoration="none", _hover={"color": GREEN}),
            rx.link("Acessar", href="/login", color="#c0d0ca", text_decoration="none", _hover={"color": GREEN}),
            spacing={"initial": "3", "md": "5"},
            flex_wrap="wrap",
            align="center",
            justify={"initial": "start", "md": "end"},
        ),
        direction={"initial": "column", "md": "row"},
        justify="between",
        align={"initial": "start", "md": "center"},
        gap="1.5em",
        width="100%",
        max_width="1280px",
        margin="0 auto",
        padding={"initial": "1.6em 1.25em 2em", "md": "1.8em 1.75em 2.2em"},
        border_top="1px solid rgba(159, 190, 175,  0.12)",
        class_name="cashsave-landing-footer",
    )


def landing_page() -> rx.Component:
    return rx.vstack(
        cabecalho_landing(),
        hero(),
        recursos(),
        demonstracao_jarvis(),
        como_funciona(),
        chamada_final(),
        rodape(),
        width="100%",
        min_height="100vh",
        spacing="0",
        background=BG,
        class_name="cashsave-landing",
    )
