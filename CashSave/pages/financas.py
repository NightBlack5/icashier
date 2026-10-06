import reflex as rx

from ..state import AppState
from .auth import auth_page


MENU = [
    ("Visão Geral", "layout-dashboard", "/app"),
    ("Assistente IA", "bot", "/assistente"),
    ("Finanças", "trending-up", "/financas"),
    ("Calendário", "calendar", "/calendario"),
    ("Preferências", "settings", "/perfil"),
    ("Sobre", "info", "/sobre"),
    ("Suporte", "life-buoy", "/suporte"),
    ("Apoiar o CashSave", "heart", "/apoiar"),
]


def sidebar() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon("piggy-bank", size=25, color="#10b981"),
            rx.heading("CashSave", size="5"),
            spacing="2",
            align="center",
        ),
        rx.divider(),
        rx.vstack(
            *[
                rx.link(
                    rx.hstack(rx.icon(icon, size=17), label, spacing="3"),
                    href=path,
                    width="100%",
                    color="#d1d5db",
                    padding="0.6em",
                    text_decoration="none",
                )
                for label, icon, path in MENU
            ],
            spacing="2",
            width="100%",
        ),
        rx.spacer(),
        rx.divider(),
        rx.vstack(
            rx.text(AppState.nome_usuario, weight="bold", size="2"),
            rx.text(AppState.email_usuario, size="1", color="#9ca3af"),
            rx.button(
                "Sair",
                on_click=AppState.sair,
                variant="soft",
                color_scheme="gray",
                width="100%",
            ),
            spacing="2",
            width="100%",
            align="start",
        ),
        width="238px",
        height="100vh",
        padding="1em",
        spacing="3",
        align="start",
        flex_shrink="0",
        position="sticky",
        top="0",
        background="#111111",
        border_right="1px solid #292929",
    )


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
        background="#121212",
        border="1px solid #353535",
    )


def financas_conteudo() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.heading("Finanças", size="8"),
                rx.text("Receitas, despesas e planejamento", color="#9ca3af"),
                spacing="1",
                align="start",
            ),
            rx.spacer(),
            rx.button(
                rx.icon("refresh-cw", size=16),
                "Atualizar",
                on_click=AppState.carregar_dados,
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
            rx.card(rx.vstack(rx.text("Receitas"), rx.heading(AppState.total_receitas, color="#10b981"))),
            rx.card(rx.vstack(rx.text("Despesas"), rx.heading(AppState.total_despesas, color="#ff5c5c"))),
            rx.card(rx.vstack(rx.text("Saldo estimado"), rx.heading(AppState.saldo_total))),
            columns="3",
            spacing="4",
            width="100%",
        ),
        secao(
            "Nova transação",
            rx.select(
                ["despesa", "receita"],
                value=AppState.tipo_transacao,
                on_change=AppState.set_tipo_transacao,
                width="100%",
            ),
            rx.input(
                placeholder="Descrição",
                value=AppState.transacao_descricao,
                on_change=AppState.set_transacao_descricao,
                width="100%",
            ),
            rx.input(
                placeholder="Valor em reais",
                type="number",
                min="0.01",
                step="0.01",
                value=AppState.transacao_valor,
                on_change=AppState.set_transacao_valor,
                width="100%",
            ),
            rx.input(
                type="date",
                value=AppState.transacao_data,
                on_change=AppState.set_transacao_data,
                width="100%",
            ),
            rx.button(
                "Salvar transação",
                on_click=AppState.criar_transacao,
                color_scheme="green",
            ),
        ),
        secao(
            "Transações",
            rx.cond(
                AppState.transacoes.length() > 0,
                rx.vstack(
                    rx.foreach(AppState.transacoes, transacao_item),
                    width="100%",
                    spacing="0",
                ),
                rx.text("Ainda não há transações.", color="#9ca3af"),
            ),
        ),
        rx.grid(
            secao(
                "Contas",
                rx.input(
                    placeholder="Nome da conta",
                    value=AppState.nova_conta_nome,
                    on_change=AppState.set_nova_conta_nome,
                ),
                rx.select(
                    ["conta_corrente", "poupanca", "carteira", "cartao_credito", "outro"],
                    value=AppState.nova_conta_tipo,
                    on_change=AppState.set_nova_conta_tipo,
                ),
                rx.input(
                    placeholder="Instituição (opcional)",
                    value=AppState.nova_conta_instituicao,
                    on_change=AppState.set_nova_conta_instituicao,
                ),
                rx.input(
                    placeholder="Saldo inicial em reais",
                    type="number",
                    step="0.01",
                    value=AppState.nova_conta_saldo,
                    on_change=AppState.set_nova_conta_saldo,
                ),
                rx.button("Adicionar conta", on_click=AppState.criar_conta, color_scheme="green"),
                rx.foreach(AppState.contas, conta_item),
            ),
            secao(
                "Categorias",
                rx.input(
                    placeholder="Nome da categoria",
                    value=AppState.nova_categoria_nome,
                    on_change=AppState.set_nova_categoria_nome,
                ),
                rx.select(
                    ["despesa", "receita"],
                    value=AppState.nova_categoria_tipo,
                    on_change=AppState.set_nova_categoria_tipo,
                ),
                rx.button("Adicionar categoria", on_click=AppState.criar_categoria),
                rx.foreach(
                    AppState.categorias,
                    lambda item: rx.text(item["nome"], " · ", item["tipo"]),
                ),
            ),
            columns="2",
            spacing="4",
            width="100%",
            align_items="start",
        ),
        rx.grid(
            secao(
                "Orçamentos",
                rx.input(
                    placeholder="Nome",
                    value=AppState.orcamento_nome,
                    on_change=AppState.set_orcamento_nome,
                ),
                rx.input(
                    placeholder="Limite em reais",
                    type="number",
                    step="0.01",
                    value=AppState.orcamento_limite,
                    on_change=AppState.set_orcamento_limite,
                ),
                rx.input(
                    type="date",
                    value=AppState.orcamento_inicio,
                    on_change=AppState.set_orcamento_inicio,
                ),
                rx.input(
                    type="date",
                    value=AppState.orcamento_fim,
                    on_change=AppState.set_orcamento_fim,
                ),
                rx.button("Criar orçamento", on_click=AppState.criar_orcamento, color_scheme="green"),
                rx.foreach(
                    AppState.orcamentos,
                    lambda item: valor_item(
                        item,
                        "nome",
                        AppState.excluir_orcamento,
                    ),
                ),
            ),
            secao(
                "Metas financeiras",
                rx.input(
                    placeholder="Nome da meta",
                    value=AppState.meta_nome,
                    on_change=AppState.set_meta_nome,
                ),
                rx.input(
                    placeholder="Valor objetivo em reais",
                    type="number",
                    step="0.01",
                    value=AppState.meta_objetivo,
                    on_change=AppState.set_meta_objetivo,
                ),
                rx.input(
                    type="date",
                    value=AppState.meta_data_alvo,
                    on_change=AppState.set_meta_data_alvo,
                ),
                rx.button("Criar meta", on_click=AppState.criar_meta, color_scheme="green"),
                rx.foreach(
                    AppState.metas,
                    lambda item: valor_item(
                        item,
                        "nome",
                        AppState.excluir_meta,
                    ),
                ),
            ),
            columns="2",
            spacing="4",
            width="100%",
            align_items="start",
        ),
        width="100%",
        spacing="4",
        align="start",
    )


def financas() -> rx.Component:
    return rx.cond(
        AppState.autenticado,
        rx.hstack(
            sidebar(),
            rx.vstack(
                financas_conteudo(),
                width="100%",
                padding="2em",
                align="start",
            ),
            width="100%",
            min_height="100vh",
            spacing="0",
            align="start",
            background="#0f0f0f",
        ),
        auth_page(),
    )
