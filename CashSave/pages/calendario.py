import calendar
from datetime import date

import reflex as rx


class CalendarioState(rx.State):
    mes: int = 10
    ano: int = 2026

    @rx.var
    def nome_mes(self) -> str:
        nomes = [
            "",
            "Janeiro",
            "Fevereiro",
            "Março",
            "Abril",
            "Maio",
            "Junho",
            "Julho",
            "Agosto",
            "Setembro",
            "Outubro",
            "Novembro",
            "Dezembro",
        ]
        return nomes[self.mes]

    @rx.var
    def dias_calendario(self) -> list[dict]:
        """
        Cria as células do calendário.
        A semana começa no domingo.
        """

        primeiro_dia = date(self.ano, self.mes, 1)

        # Python considera segunda-feira = 0.
        # Aqui transformamos para domingo = 0.
        inicio = (primeiro_dia.weekday() + 1) % 7

        quantidade_dias = calendar.monthrange(self.ano, self.mes)[1]

        # Mês anterior
        if self.mes == 1:
            mes_anterior = 12
            ano_anterior = self.ano - 1
        else:
            mes_anterior = self.mes - 1
            ano_anterior = self.ano

        dias_mes_anterior = calendar.monthrange(
            ano_anterior,
            mes_anterior,
        )[1]

        dias = []

        # Dias do mês anterior
        for i in range(inicio):
            dia = dias_mes_anterior - inicio + i + 1

            dias.append(
                {
                    "dia": dia,
                    "mes_atual": False,
                    "hoje": False,
                }
            )

        # Dias do mês atual
        hoje = date.today()

        for dia in range(1, quantidade_dias + 1):
            eh_hoje = (
                dia == hoje.day
                and self.mes == hoje.month
                and self.ano == hoje.year
            )

            dias.append(
                {
                    "dia": dia,
                    "mes_atual": True,
                    "hoje": eh_hoje,
                }
            )

        # Completa a última semana
        proximo_dia = 1

        while len(dias) % 7 != 0:
            dias.append(
                {
                    "dia": proximo_dia,
                    "mes_atual": False,
                    "hoje": False,
                }
            )

            proximo_dia += 1

        return dias

    def mes_anterior(self):
        if self.mes == 1:
            self.mes = 12
            self.ano -= 1
        else:
            self.mes -= 1

    def proximo_mes(self):
        if self.mes == 12:
            self.mes = 1
            self.ano += 1
        else:
            self.mes += 1


def cabecalho_calendario() -> rx.Component:
    return rx.hstack(
        rx.vstack(
            rx.heading(
                "Calendário Financeiro",
                size="8",
            ),
            rx.text(
                "Gerencie suas contas e vencimentos",
                color_scheme="gray",
                size="4",
            ),
            spacing="1",
            align="start",
        ),

        rx.spacer(),

        rx.button(
            rx.icon("plus", size=18),
            "Nova Conta",
            color_scheme="green",
            size="3",
        ),

        width="100%",
        align="center",
    )


def titulo_mes() -> rx.Component:
    return rx.hstack(
        rx.button(
            rx.icon("chevron-left", size=22),
            on_click=CalendarioState.mes_anterior,
            variant="ghost",
            color_scheme="gray",
            size="3",
        ),

        rx.spacer(),

        rx.heading(
            f"{CalendarioState.nome_mes} {CalendarioState.ano}",
            size="5",
        ),

        rx.spacer(),

        rx.button(
            rx.icon("chevron-right", size=22),
            on_click=CalendarioState.proximo_mes,
            variant="ghost",
            color_scheme="gray",
            size="3",
        ),

        width="100%",
        align="center",
    )


def dia_calendario(item: dict) -> rx.Component:
    return rx.box(
        rx.text(
            item["dia"],
            size="3",
            weight="medium",
            color=rx.cond(
                item["mes_atual"],
                "var(--gray-12)",
                "var(--gray-8)",
            ),
        ),

        width="100%",
        height="82px",
        padding="0.8em",
        border="1px solid var(--gray-5)",
        border_radius="12px",

        background=rx.cond(
            item["mes_atual"],
            "transparent",
            "var(--gray-3)",
        ),

        border_color=rx.cond(
            item["hoje"],
            "var(--green-9)",
            "var(--gray-5)",
        ),

        color=rx.cond(
            item["hoje"],
            "var(--green-9)",
            "var(--gray-12)",
        ),

        box_shadow=rx.cond(
            item["hoje"],
            "0 0 0 1px var(--green-9)",
            "none",
        ),

        _hover={
            "background": "var(--gray-3)",
            "border_color": "var(--green-7)",
        },

        transition="all 0.15s ease",
    )


def calendario_mensal() -> rx.Component:
    dias_semana = [
        "Dom",
        "Seg",
        "Ter",
        "Qua",
        "Qui",
        "Sex",
        "Sáb",
    ]

    return rx.card(
        rx.vstack(
            titulo_mes(),

            # Cabeçalho dos dias da semana
            rx.grid(
                *[
                    rx.center(
                        rx.text(
                            dia,
                            size="3",
                            weight="medium",
                            color_scheme="gray",
                        ),
                        padding_bottom="0.3em",
                    )
                    for dia in dias_semana
                ],
                columns="7",
                gap="0.35em",
                width="100%",
            ),

            # Dias
            rx.grid(
                rx.foreach(
                    CalendarioState.dias_calendario,
                    dia_calendario,
                ),
                columns="7",
                gap="0.35em",
                width="100%",
            ),

            spacing="4",
            width="100%",
        ),

        width="100%",
        padding="1.5em",
        border_radius="16px",
    )


def proximas_contas() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.icon(
                    "calendar",
                    size=21,
                    color="var(--green-9)",
                ),

                rx.heading(
                    "Próximas Contas",
                    size="4",
                ),

                spacing="3",
                align="center",
            ),

            rx.center(
                rx.vstack(
                    rx.center(
                        rx.icon(
                            "calendar-days",
                            size=42,
                            color="var(--gray-9)",
                        ),

                        width="72px",
                        height="72px",
                    ),

                    rx.text(
                        "Nenhuma conta registrada",
                        size="3",
                        color_scheme="gray",
                    ),

                    rx.link(
                        "Adicionar conta",
                        href="/calendario",
                        color="var(--green-9)",
                        size="3",
                        weight="medium",
                    ),

                    spacing="3",
                    align="center",
                ),

                width="100%",
                min_height="260px",
            ),

            spacing="5",
            width="100%",
        ),

        width="100%",
        min_width="340px",
        padding="1.5em",
        border_radius="16px",
    )


def conteudo_calendario() -> rx.Component:
    return rx.vstack(
        cabecalho_calendario(),

        rx.grid(
            calendario_mensal(),
            proximas_contas(),

            columns="2fr 1fr",
            gap="1.5em",
            width="100%",
            align_items="start",
        ),
        spacing="5",
        align="start",
        width="100%",
    )