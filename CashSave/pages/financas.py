import reflex as rx

from ..components.layout import app_layout
from ..state import AppState
from .auth import auth_page


def transacao_item(item: dict) -> rx.Component:
    cor = rx.cond(item["tipo"] == "receita", "#10b981", "#ff5c5c")
    sinal = rx.cond(item["tipo"] == "receita", "+", "-")
    return rx.hstack(
        rx.vstack(
            rx.text(item["descricao"], weight="medium"),
            rx.text(
                item["data"],
                " · ",
                item["tipo"],
                size="1",
                color="#9ca3af",
            ),
            spacing="0",
            align="start",
        ),
        rx.spacer(),
        rx.text(
            sinal,
            " ",
            item["valor_formatado"],
            color=cor,
            weight="bold",
        ),
        rx.icon_button(
            rx.icon("trash-2", size=16),
            on_click=AppState.excluir_transacao(item["id"]),
            variant="ghost",
            color_scheme="red",
            aria_label="Excluir transação",
        ),
        width="100%",
        align="center",
        padding="0.8em",
        border_bottom="1px solid #292929",
    )


def conta_item(item: dict) -> rx.Component:
    return rx.hstack(
        rx.vstack(
            rx.text(item["nome"], weight="medium"),
            rx.text(item["tipo"], size="1", color="#9ca3af"),
            spacing="0",
            align="start",
        ),
        rx.spacer(),
        rx.text(
            "Saldo inicial: ",
            item["saldo_inicial_formatado"],
            size="2",
        ),
        width="100%",
        padding="0.7em",
        border_bottom="1px solid #292929",
    )


def valor_item(item: dict, chave_nome: str, remover) -> rx.Component:
    return rx.hstack(
        rx.vstack(
            rx.text(item[chave_nome], weight="medium"),
            rx.text(item["valor_formatado"], size="2", color="#9ca3af"),
            spacing="0",
            align="start",
        ),
        rx.spacer(),
        rx.icon_button(
            rx.icon("trash-2", size=16),
            on_click=remover(item["id"]),
            variant="ghost",
            color_scheme="red",
            aria_label="Excluir",
        ),
        width="100%",
        padding="0.7em",
        border_bottom="1px solid #292929",
    )


def secao(titulo: str, *children: rx.Component) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(titulo, size="4"),
            *children,
            width="100%",
            align="start",
            spacing="3",
        ),
        width="100%",
        background="linear-gradient(180deg, rgba(17,24,39,0.96), rgba(15,23,42,0.96))",
        border="1px solid rgba(148,163,184,0.15)",
        border_radius="18px",
        padding="1.2em",
    )


def financas_conteudo() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.heading("Finanças", size="8", color="white"),
                rx.text("Receitas, despesas e planejamento", color="rgba(148,163,184,0.9)"),
                spacing="1",
                align="start",
            ),
            rx.spacer(),
            rx.button(
                rx.icon("refresh-cw", size=16),
                "Atualizar",
                on_click=AppState.atualizar_dados,
                variant="outline",
            ),
            width="100%",
            align="center",
        ),
        rx.cond(
            AppState.erro != "",
            rx.callout(AppState.erro, icon="triangle-alert", color_scheme="red"),
            rx.fragment(),
        ),
        rx.grid(
            rx.card(
                rx.vstack(
                    rx.text("Receitas", color="rgba(148,163,184,0.9)", size="2"),
                    rx.heading(AppState.total_receitas, color="#10b981", size="6"),
                ),
                background="linear-gradient(180deg, rgba(17,24,39,0.96), rgba(15,23,42,0.96))",
                border="1px solid rgba(148,163,184,0.15)",
                border_radius="18px",
                padding="1.1em",
            ),
            rx.card(
                rx.vstack(
                    rx.text("Despesas", color="rgba(148,163,184,0.9)", size="2"),
                    rx.heading(AppState.total_despesas, color="#ff5c5c", size="6"),
                ),
                background="linear-gradient(180deg, rgba(17,24,39,0.96), rgba(15,23,42,0.96))",
                border="1px solid rgba(148,163,184,0.15)",
                border_radius="18px",
                padding="1.1em",
            ),
            rx.card(
                rx.vstack(
                    rx.text("Saldo estimado", color="rgba(148,163,184,0.9)", size="2"),
                    rx.heading(AppState.saldo_total, color="white", size="6"),
                ),
                background="linear-gradient(180deg, rgba(17,24,39,0.96), rgba(15,23,42,0.96))",
                border="1px solid rgba(148,163,184,0.15)",
                border_radius="18px",
                padding="1.1em",
            ),
            columns=rx.breakpoints(initial="1", lg="3"),
            spacing="4",
            width="100%",
        ),
        rx.grid(
            secao(
                "Nova transação",
                rx.hstack(
                    rx.select(
                        ["despesa", "receita"],
                        value=AppState.tipo_transacao,
                        on_change=AppState.set_tipo_transacao,
                        width="140px",
                    ),
                    rx.input(
                        placeholder="Descrição",
                        value=AppState.transacao_descricao,
                        on_change=AppState.set_transacao_descricao,
                        width="100%",
                    ),
                    width="100%",
                    align="center",
                    spacing="2",
                ),
                rx.hstack(
                    rx.input(
                        placeholder="Valor em reais",
                        type="text",
                        value=AppState.transacao_valor,
                        on_change=AppState.set_transacao_valor,
                        on_blur=AppState.formatar_transacao_valor,
                        width="180px",
                    ),
                    rx.input(
                        type="date",
                        value=AppState.transacao_data,
                        on_change=AppState.set_transacao_data,
                        width="180px",
                    ),
                    rx.button(
                        "Salvar",
                        on_click=AppState.criar_transacao,
                        color_scheme="green",
                    ),
                    width="100%",
                    align="center",
                    spacing="2",
                    flex_wrap="wrap",
                ),
            ),
            secao(
                "Planejamento",
                rx.vstack(
                    rx.cond(
                        AppState.orcamentos.length() > 0,
                        rx.foreach(
                            AppState.orcamentos[:3],
                            lambda item: rx.text(
                                f"{item['nome']}: {item['valor_formatado']}",
                                color="rgba(148,163,184,0.9)",
                            ),
                        ),
                        rx.text("Nenhum orçamento ativo.", color="#9ca3af"),
                    ),
                    rx.divider(),
                    rx.cond(
                        AppState.metas_com_progresso.length() > 0,
                        rx.foreach(
                            AppState.metas_com_progresso[:2],
                            lambda item: rx.text(
                                f"{item['nome']}: {item['progresso_percentual']}% concluído",
                                color="rgba(148,163,184,0.9)",
                            ),
                        ),
                        rx.text("Nenhuma meta cadastrada.", color="#9ca3af"),
                    ),
                    width="100%",
                    align="start",
                    spacing="2",
                ),
            ),
            columns=rx.breakpoints(initial="1", lg="2"),
            spacing="4",
            width="100%",
            align_items="start",
        ),
        secao(
            "Transações recentes",
            rx.hstack(
                rx.input(
                    placeholder="Buscar descrição",
                    value=AppState.transacao_busca,
                    on_change=AppState.set_transacao_busca,
                    width="100%",
                ),
                rx.select(
                    ["todas", "despesa", "receita"],
                    value=AppState.transacao_filtro_tipo,
                    on_change=AppState.set_transacao_filtro_tipo,
                ),
                width="100%",
                align="center",
                flex_wrap="wrap",
            ),
            rx.cond(
                AppState.transacoes_filtradas.length() > 0,
                rx.vstack(
                    rx.foreach(AppState.transacoes_filtradas[:5], transacao_item),
                    width="100%",
                    spacing="0",
                ),
                rx.text(
                    "Nenhuma transação corresponde aos filtros.",
                    color="#9ca3af",
                ),
            ),
        ),
        width="100%",
        spacing="4",
        align="start",
        background="#0b0d10",
        padding="0",
    )


def financas() -> rx.Component:
    return rx.cond(
        AppState.autenticado,
        app_layout(
            "/financas",
            rx.vstack(
                financas_conteudo(),
                width="100%",
                align="start",
                min_width="0",
            ),
        ),
        auth_page(),
    )
