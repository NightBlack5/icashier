import reflex as rx

from ..state import AppState


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


def menu_item(label: str, icon: str, path: str, active: bool) -> rx.Component:
	return rx.link(
		rx.hstack(
			rx.icon(
				icon,
				size=18,
				color="var(--green-11)" if active else "var(--gray-10)",
				flex_shrink="0",
			),
			rx.text(
				label,
				size="2",
				weight="medium",
				display=rx.breakpoints(initial="none", md="block"),
				white_space="nowrap",
			),
			spacing="3",
			align="center",
			justify=rx.breakpoints(initial="center", md="start"),
			padding=rx.breakpoints(initial="0.7em", md="0.65em 0.8em"),
			width="100%",
			border_radius="8px",
			background="var(--green-3)" if active else "transparent",
			_hover={
				"background": "var(--green-4)" if active else "var(--gray-4)"
			},
		),
		href=path,
		title=label,
		aria_label=label,
		width="100%",
		color="var(--green-11)" if active else "var(--gray-12)",
		text_decoration="none",
	)


def app_sidebar(active_route: str) -> rx.Component:
	return rx.vstack(
		rx.hstack(
			rx.icon("piggy-bank", size=25, color="var(--green-9)"),
			rx.heading(
				"CashSave",
				size="5",
				display=rx.breakpoints(initial="none", md="block"),
			),
			width="100%",
			align="center",
			justify=rx.breakpoints(initial="center", md="start"),
			spacing="2",
			padding=rx.breakpoints(initial="0.4em", md="0.5em 0.8em"),
		),
		rx.divider(),
		rx.vstack(
			*[
				menu_item(label, icon, path, path == active_route)
				for label, icon, path in MENU
			],
			spacing="2",
			width="100%",
		),
		rx.spacer(),
		rx.divider(),
		rx.hstack(
			rx.avatar(
				src=AppState.avatar_url,
				fallback="U",
				size="2",
				radius="full",
				flex_shrink="0",
			),
			rx.text(
				AppState.nome_usuario,
				size="2",
				weight="medium",
				title=AppState.nome_usuario,
				display=rx.breakpoints(initial="none", md="block"),
				flex="1",
				min_width="0",
				overflow="hidden",
				text_overflow="ellipsis",
				white_space="nowrap",
			),
			width="100%",
			min_width="0",
			align="center",
			justify=rx.breakpoints(initial="center", md="start"),
			spacing="2",
			padding=rx.breakpoints(initial="0.4em", md="0.65em 0.8em"),
			border_radius="8px",
			background="var(--gray-3)",
		),
		rx.button(
			rx.icon("log-out", size=16),
			rx.text(
				"Sair",
				display=rx.breakpoints(initial="none", md="block"),
			),
			on_click=AppState.sair,
			variant="soft",
			color_scheme="gray",
			width="100%",
			justify_content="center",
			aria_label="Sair",
		),
		width=rx.breakpoints(initial="64px", md="238px"),
		height="100vh",
		min_height="100vh",
		padding=rx.breakpoints(initial="0.55em 0.4em", md="1em"),
		spacing="3",
		align="center",
		flex_shrink="0",
		position="sticky",
		top="0",
		background="linear-gradient(180deg, #0f1318 0%, #111923 100%)",
		border_right="1px solid rgba(148,163,184,0.18)",
	)


def app_layout(active_route: str, *content: rx.Component) -> rx.Component:
	return rx.hstack(
		app_sidebar(active_route),
		rx.box(
			rx.vstack(
				*content,
				spacing="5",
				align="start",
				width="100%",
				min_width="0",
			),
			padding=rx.breakpoints(initial="1em", md="2em 2.5em"),
			width="100%",
			min_width="0",
			min_height="100vh",
			background="linear-gradient(180deg, #0b0d10 0%, #10161d 100%)",
		),
		spacing="0",
		align="start",
		width="100%",
		min_height="100vh",
		background="#0b0d10",
	)
