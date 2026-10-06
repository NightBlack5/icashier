from pathlib import Path

import reflex as rx


PIX_CHAVE = ""
PIX_QRCODE = "/qrcode_pix.png"
PIX_QRCODE_DISPONIVEL = (
    Path(__file__).resolve().parents[2]
    / "assets"
    / "qrcode_pix.png"
).is_file()


def cartao_pix() -> rx.Component:
    conteudo_qrcode = (
        rx.image(
            src=PIX_QRCODE,
            alt="QR Code Pix",
            width="240px",
            height="240px",
            object_fit="contain",
            background="white",
            border_radius="8px",
        )
        if PIX_QRCODE_DISPONIVEL
        else rx.vstack(
            rx.icon(
                "qr-code",
                size=48,
                color="var(--gray-9)",
            ),
            rx.text(
                "QR Code Pix ainda não configurado",
                size="2",
                color_scheme="gray",
                text_align="center",
            ),
            spacing="3",
            align="center",
            justify="center",
            width="240px",
            height="240px",
        )
    )

    chave_pix = (
        rx.vstack(
            rx.text(
                "Chave Pix:",
                size="2",
                color_scheme="gray",
            ),
            rx.text(
                PIX_CHAVE,
                size="4",
                font_family="monospace",
                text_align="center",
            ),
            rx.button(
                rx.icon("copy", size=16),
                "Copiar chave Pix",
                on_click=[
                    rx.set_clipboard(PIX_CHAVE),
                    rx.toast.success("Chave Pix copiada!"),
                ],
                width="100%",
                size="3",
                color_scheme="green",
            ),
            spacing="3",
            align="center",
            width="100%",
        )
        if PIX_CHAVE.strip()
        else rx.callout(
            "A chave Pix ainda não foi configurada. Nenhum pagamento pode ser enviado por esta tela.",
            icon="info",
            color_scheme="gray",
            width="100%",
        )
    )

    return rx.card(
        rx.vstack(
            rx.heading("Apoiar via Pix", size="5"),
            rx.center(
                conteudo_qrcode,
                padding="1em",
                border="1px solid var(--gray-6)",
                border_radius="16px",
                background="var(--gray-2)",
            ),
            rx.center(
                chave_pix,
                width="100%",
                padding="1em",
                border_radius="10px",
                background="var(--gray-3)",
            ),
            spacing="4",
            align="center",
            width="100%",
        ),
        width="100%",
        padding="1.5em",
    )


def conteudo_apoiar() -> rx.Component:
    return rx.vstack(
        rx.center(
            rx.icon("heart", size=30, color="white"),
            width="64px",
            height="64px",
            border_radius="16px",
            background="linear-gradient(135deg, #ec4899, #e11d48)",
        ),
        rx.heading(
            "Apoiar o CashSave",
            size="8",
            text_align="center",
        ),
        rx.card(
            rx.vstack(
                rx.text(
                    "O CashSave é um aplicativo gratuito criado para ajudar "
                    "pessoas a organizarem melhor suas finanças e tomarem "
                    "decisões mais conscientes sobre o uso do dinheiro.",
                    size="3",
                ),
                rx.text(
                    "Se o app está sendo útil para você, seu apoio é totalmente "
                    "opcional e ajuda a manter o projeto ativo, além de "
                    "contribuir para melhorias e novas funcionalidades no futuro.",
                    size="3",
                ),
                rx.text(
                    "Qualquer valor é bem-vindo. Obrigado por apoiar o CashSave 🚀",
                    size="3",
                ),
                spacing="4",
                align="start",
            ),
            width="100%",
            padding="1.5em",
        ),
        cartao_pix(),
        spacing="5",
        align="center",
        width="100%",
        max_width="720px",
        margin_x="auto",
    )