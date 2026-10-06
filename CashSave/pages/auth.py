import reflex as rx

from ..state import AppState


BACKGROUND = "#031513"
CARD_BACKGROUND = "rgba(3, 19, 22, 0.94)"
FIELD_BACKGROUND = "#061c20"
FIELD_BORDER = "#173638"
GREEN = "#12e5a0"
MUTED = "#a2b5b5"


def campo_email() -> rx.Component:
    return rx.hstack(
        rx.icon("mail", size=18, color="#91a6a8"),
        rx.input(
            placeholder="E-mail ou número de telefone",
            type="text",
            value=rx.cond(
                AppState.lembrar_email == "true",
                AppState.auth_email_salvo,
                AppState.auth_email,
            ),
            on_change=AppState.set_auth_email,
            required=True,
            variant="soft",
            background="transparent",
            border="none",
            box_shadow="none",
            color="white",
            placeholder_color="#82999a",
            width="100%",
            height="44px",
            padding="0",
            _focus={"outline": "none", "box_shadow": "none"},
        ),
        align="center",
        spacing="3",
        width="100%",
        padding_x="0.85em",
        border=f"1px solid {FIELD_BORDER}",
        border_radius="11px",
        background=FIELD_BACKGROUND,
        transition="border-color 150ms ease",
        _focus_within={"border_color": GREEN},
    )


def campo_senha() -> rx.Component:
    return rx.hstack(
        rx.icon("lock-keyhole", size=18, color="#91a6a8"),
        rx.input(
            placeholder="Senha",
            type=rx.cond(AppState.senha_visivel, "text", "password"),
            value=AppState.auth_password,
            on_change=AppState.set_auth_password,
            required=True,
            min_length=rx.cond(AppState.cadastro, 8, 1),
            variant="soft",
            background="transparent",
            border="none",
            box_shadow="none",
            color="white",
            placeholder_color="#82999a",
            width="100%",
            height="44px",
            padding="0",
            _focus={"outline": "none", "box_shadow": "none"},
        ),
        rx.icon_button(
            rx.icon(
                rx.cond(AppState.senha_visivel, "eye-off", "eye"),
                size=18,
                color="#91a6a8",
            ),
            on_click=AppState.alternar_visibilidade_senha,
            variant="ghost",
            size="1",
            aria_label=rx.cond(
                AppState.senha_visivel,
                "Ocultar senha",
                "Mostrar senha",
            ),
        ),
        align="center",
        spacing="3",
        width="100%",
        padding_left="0.85em",
        padding_right="0.45em",
        border=f"1px solid {FIELD_BORDER}",
        border_radius="11px",
        background=FIELD_BACKGROUND,
        transition="border-color 150ms ease",
        _focus_within={"border_color": GREEN},
    )


def campo_nome() -> rx.Component:
    return rx.hstack(
        rx.icon("user-round", size=18, color="#91a6a8"),
        rx.input(
            placeholder="Seu nome",
            value=AppState.auth_name,
            on_change=AppState.set_auth_name,
            required=True,
            variant="soft",
            background="transparent",
            border="none",
            box_shadow="none",
            color="white",
            placeholder_color="#82999a",
            width="100%",
            height="44px",
            padding="0",
            _focus={"outline": "none", "box_shadow": "none"},
        ),
        align="center",
        spacing="3",
        width="100%",
        padding_x="0.85em",
        border=f"1px solid {FIELD_BORDER}",
        border_radius="11px",
        background=FIELD_BACKGROUND,
        _focus_within={"border_color": GREEN},
    )


def auth_page() -> rx.Component:
    return rx.box(
        rx.image(
            src="/login-background.svg",
            alt="",
            position="absolute",
            inset="0",
            width="100%",
            height="100%",
            object_fit="cover",
            pointer_events="none",
            user_select="none",
        ),
        rx.center(
            rx.vstack(
                rx.vstack(
                    rx.heading(
                        rx.fragment(
                            rx.text("Cash", as_="span", color="white"),
                            rx.text("Save", as_="span", color=GREEN),
                        ),
                        size="8",
                        letter_spacing="-0.045em",
                    ),
                    rx.text(
                        "Controle hoje. Conquiste amanhã.",
                        size="2",
                        color=MUTED,
                        text_align="center",
                    ),
                    align="center",
                    spacing="1",
                    width="100%",
                ),
                rx.vstack(
                    rx.heading(
                        rx.cond(
                            AppState.cadastro,
                            "Crie sua conta",
                            "Bem-vindo de volta!",
                        ),
                        size="5",
                        color="white",
                    ),
                    rx.text(
                        rx.cond(
                            AppState.cadastro,
                            "Cadastre-se para começar a cuidar melhor do seu dinheiro.",
                            "Entre para acessar sua conta e continuar cuidando do seu dinheiro.",
                        ),
                        size="2",
                        line_height="1.55",
                        color=MUTED,
                    ),
                    align="start",
                    spacing="1",
                    width="100%",
                    margin_top="28px",
                ),
                rx.vstack(
                    rx.cond(AppState.cadastro, campo_nome(), rx.fragment()),
                    campo_email(),
                    campo_senha(),
                    rx.cond(
                        AppState.cadastro,
                        rx.fragment(),
                        rx.hstack(
                            rx.checkbox(
                                "Lembrar de mim",
                                checked=AppState.lembrar_email == "true",
                                on_change=AppState.set_lembrar_email,
                                size="1",
                                color_scheme="green",
                            ),
                            rx.spacer(),
                            rx.link(
                                "Esqueceu sua senha?",
                                href="/suporte",
                                size="1",
                                color=GREEN,
                                text_decoration="none",
                                _hover={"color": "#70f5c5"},
                            ),
                            width="100%",
                            align="center",
                        ),
                    ),
                    spacing="2",
                    width="100%",
                    margin_top="8px",
                ),
                rx.box(
                    rx.cond(
                        AppState.erro != "",
                        rx.callout(
                            AppState.erro,
                            icon="triangle-alert",
                            color_scheme="red",
                            width="100%",
                            background="rgba(127, 29, 29, 0.2)",
                        ),
                        rx.fragment(),
                    ),
                    margin_top="12px",
                ),
                rx.button(
                    rx.cond(
                        AppState.carregando,
                        "Aguarde...",
                        rx.cond(AppState.cadastro, "Criar conta", "Entrar"),
                    ),
                    rx.cond(
                        AppState.carregando,
                        rx.spinner(size="1"),
                        rx.icon("arrow-right", size=17),
                    ),
                    on_click=AppState.autenticar,
                    type="submit",
                    disabled=AppState.carregando,
                    width="100%",
                    height="40px",
                    color="#032019",
                    weight="bold",
                    background=GREEN,
                    border_radius="999px",
                    _hover={
                        "background": "#39f0b2",
                        "transform": "translateY(-1px)",
                    },
                    transition="all 150ms ease",
                    margin_top="9px",
                ),
                rx.hstack(
                    rx.box(
                        width="100%",
                        height="1px",
                        background="#294044",
                    ),
                    rx.text("ou", size="1", color=MUTED, white_space="nowrap"),
                    rx.box(
                        width="100%",
                        height="1px",
                        background="#294044",
                    ),
                    spacing="3",
                    align="center",
                    width="100%",
                    margin_top="20px",
                ),
                rx.cond(
                    AppState.cadastro,
                    rx.fragment(),
                    rx.button(
                        rx.text(
                            "G",
                            color="transparent",
                            font_size="20px",
                            font_weight="bold",
                            background_image=(
                                "linear-gradient(135deg, #4285F4 0 25%, "
                                "#34A853 25% 50%, #FBBC05 50% 75%, "
                                "#EA4335 75%)"
                            ),
                            background_clip="text",
                        ),
                        "Entrar com o Google",
                        on_click=AppState.login_google,
                        variant="outline",
                        width="100%",
                        height="40px",
                        color="white",
                        border="1px solid #294044",
                        border_radius="999px",
                        background="transparent",
                        _hover={
                            "background": "rgba(255, 255, 255, 0.04)",
                            "border_color": "#496366",
                        },
                        margin_top="12px",
                    ),
                ),
                rx.hstack(
                    rx.text(
                        rx.cond(
                            AppState.cadastro,
                            "Já tem uma conta?",
                            "Não tem uma conta?",
                        ),
                        size="2",
                        color=MUTED,
                    ),
                    rx.button(
                        rx.cond(
                            AppState.cadastro,
                            "Entrar",
                            "Cadastre-se",
                        ),
                        on_click=AppState.alternar_cadastro,
                        variant="ghost",
                        size="2",
                        color=GREEN,
                        padding="0",
                        min_width="0",
                        _hover={"background": "transparent", "color": "#70f5c5"},
                    ),
                    spacing="1",
                    justify="center",
                    align="center",
                    width="100%",
                    margin_top="32px",
                ),
                width="100%",
                max_width="400px",
                min_height="560px",
                padding=rx.breakpoints(
                    initial="24px 24px 28px",
                    sm="40px 32px 22px",
                ),
                spacing="0",
                align="stretch",
                border="1px solid #173638",
                border_radius="16px",
                background=CARD_BACKGROUND,
                box_shadow="0 24px 80px rgba(0, 0, 0, 0.38)",
                backdrop_filter="blur(16px)",
                box_sizing="border-box",
            ),
            width="100%",
            min_height="100vh",
            padding=rx.breakpoints(initial="16px", sm="24px"),
            position="relative",
            z_index="1",
        ),
        width="100%",
        min_height="100vh",
        overflow="hidden",
        position="relative",
        background=(
            "radial-gradient(ellipse at 8% 0%, rgba(0, 163, 110, 0.18), transparent 29%), "
            "radial-gradient(ellipse at 98% 88%, rgba(0, 166, 115, 0.12), transparent 36%), "
            f"{BACKGROUND}"
        ),
    )
