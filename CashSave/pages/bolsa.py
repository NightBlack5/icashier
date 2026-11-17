import reflex as rx

from ..components.layout import app_layout
from ..state import AppState
from .auth import auth_page


def bolsa_conteudo() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.heading("Bolsa de Valores", size="8"),
                rx.text(
                    "Acompanhe ativos e indicadores com dados verificados.",
                    color="rgba(148,163,184,0.9)",
                ),
                spacing="1",
                align="start",
            ),
            rx.spacer(),
            rx.button(
                rx.icon("refresh-cw", size=16),
                "Atualizar",
                on_click=AppState.carregar_bolsa,
                variant="outline",
                disabled=AppState.bolsa_carregando,
            ),
            width="100%",
            align="center",
            flex_wrap="wrap",
        ),
        rx.cond(
            AppState.bolsa_erro != "",
            rx.callout(
                AppState.bolsa_erro,
                icon="triangle-alert",
                color_scheme="red",
                width="100%",
            ),
            rx.fragment(),
        ),
        rx.card(
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.heading("Destaques da B3", size="5"),
                        rx.text(
                            "Ações com maiores variações no pregão.",
                            size="2",
                            color="rgba(148,163,184,0.9)",
                        ),
                        spacing="1",
                        align="start",
                    ),
                    rx.spacer(),
                    rx.badge(
                        "Atualização a cada 5 min",
                        color_scheme="amber",
                        variant="soft",
                    ),
                    width="100%",
                    align="center",
                    flex_wrap="wrap",
                ),
                rx.text(
                    "Dados atrasados da brapi.dev, atualizados pela fonte a "
                    "cada cinco minutos; não são cotações em tempo real.",
                    size="2",
                    color="rgba(148,163,184,0.9)",
                ),
                rx.cond(
                    AppState.bolsa_movers_origem != "",
                    rx.cond(
                        AppState.bolsa_movers_referencia != "",
                        rx.text(
                            "Fonte: ",
                            AppState.bolsa_movers_origem,
                            " · Cotação mais recente: ",
                            AppState.bolsa_movers_referencia,
                            size="1",
                        ),
                        rx.text(
                            "Fonte: ",
                            AppState.bolsa_movers_origem,
                            size="1",
                        ),
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    AppState.bolsa_movers_atrasado,
                    rx.callout(
                        "A fonte não respondeu; exibindo o último ranking "
                        "verificado em cache.",
                        icon="clock-3",
                        color_scheme="amber",
                        width="100%",
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    AppState.bolsa_carregando,
                    rx.hstack(
                        rx.spinner(size="1"),
                        rx.text("Atualizando dados de mercado...", size="2"),
                        spacing="2",
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    (AppState.bolsa_altas.length() > 0)
                    | (AppState.bolsa_baixas.length() > 0),
                    rx.grid(
                        rx.vstack(
                            rx.heading("Ações em alta", size="3"),
                            rx.cond(
                                AppState.bolsa_grafico_altas.length() > 0,
                                rx.recharts.bar_chart(
                                    rx.recharts.cartesian_grid(
                                        stroke_dasharray="3 3",
                                    ),
                                    rx.recharts.x_axis(data_key="symbol"),
                                    rx.recharts.y_axis(unit="%"),
                                    rx.recharts.tooltip(),
                                    rx.recharts.bar(
                                        data_key="variation",
                                        name="Variação diária",
                                        fill="#10b981",
                                    ),
                                    data=AppState.bolsa_grafico_altas,
                                    width="100%",
                                    height=300,
                                ),
                                rx.text(
                                    "Nenhuma ação está em alta neste momento.",
                                    size="2",
                                ),
                            ),
                            width="100%",
                            align="start",
                            spacing="3",
                        ),
                        rx.vstack(
                            rx.heading("Maiores altas", size="3"),
                            rx.cond(
                                AppState.bolsa_altas.length() > 0,
                                rx.vstack(
                                    rx.foreach(
                                        AppState.bolsa_altas,
                                        lambda mover: rx.hstack(
                                            rx.vstack(
                                                rx.text(
                                                    mover["symbol"],
                                                    weight="bold",
                                                ),
                                                rx.text(
                                                    mover["name"],
                                                    size="1",
                                                ),
                                                align="start",
                                                spacing="1",
                                            ),
                                            rx.spacer(),
                                            rx.vstack(
                                                rx.text(
                                                    mover["variation_display"],
                                                    color="#10b981",
                                                    weight="bold",
                                                ),
                                                rx.text(
                                                    mover["price"],
                                                    size="1",
                                                ),
                                                align="end",
                                                spacing="1",
                                            ),
                                            width="100%",
                                            align="center",
                                            padding="0.5em 0",
                                            border_bottom=(
                                                "1px solid "
                                                "rgba(148,163,184,0.15)"
                                            ),
                                        ),
                                    ),
                                    width="100%",
                                    spacing="1",
                                ),
                                rx.text(
                                    "Nenhuma alta verificada.",
                                    size="2",
                                ),
                            ),
                            rx.heading("Maiores baixas", size="3"),
                            rx.cond(
                                AppState.bolsa_baixas.length() > 0,
                                rx.vstack(
                                    rx.foreach(
                                        AppState.bolsa_baixas,
                                        lambda mover: rx.hstack(
                                            rx.vstack(
                                                rx.text(
                                                    mover["symbol"],
                                                    weight="bold",
                                                ),
                                                rx.text(
                                                    mover["name"],
                                                    size="1",
                                                ),
                                                align="start",
                                                spacing="1",
                                            ),
                                            rx.spacer(),
                                            rx.vstack(
                                                rx.text(
                                                    mover["variation_display"],
                                                    color="#f87171",
                                                    weight="bold",
                                                ),
                                                rx.text(
                                                    mover["price"],
                                                    size="1",
                                                ),
                                                align="end",
                                                spacing="1",
                                            ),
                                            width="100%",
                                            align="center",
                                            padding="0.5em 0",
                                            border_bottom=(
                                                "1px solid "
                                                "rgba(148,163,184,0.15)"
                                            ),
                                        ),
                                    ),
                                    width="100%",
                                    spacing="1",
                                ),
                                rx.text(
                                    "Nenhuma baixa verificada.",
                                    size="2",
                                ),
                            ),
                            width="100%",
                            align="start",
                            spacing="3",
                        ),
                        columns=rx.breakpoints(initial="1", xl="2"),
                        spacing="5",
                        width="100%",
                    ),
                    rx.callout(
                        AppState.bolsa_indisponivel,
                        icon="chart-no-axes-combined",
                        color_scheme="gray",
                        width="100%",
                    ),
                ),
                width="100%",
                align="start",
                spacing="3",
            ),
            width="100%",
            class_name="cashsave-panel",
        ),
        rx.card(
            rx.vstack(
                rx.heading("Pesquisar ativos", size="4"),
                rx.hstack(
                    rx.input(
                        placeholder="Código ou nome do ativo",
                        value=AppState.bolsa_busca,
                        on_change=AppState.set_bolsa_busca,
                        width="100%",
                    ),
                    rx.select(
                        ["todas", "acao", "fii", "etf"],
                        value=AppState.bolsa_categoria,
                        on_change=AppState.set_bolsa_categoria,
                        aria_label="Filtrar por categoria",
                    ),
                    rx.select(
                        ["codigo", "nome"],
                        value=AppState.bolsa_ordenacao,
                        on_change=AppState.set_bolsa_ordenacao,
                        aria_label="Ordenar ativos",
                    ),
                    rx.button(
                        "Buscar",
                        on_click=AppState.pesquisar_ativos,
                        color_scheme="green",
                    ),
                    width="100%",
                    align="center",
                    flex_wrap="wrap",
                ),
                rx.cond(
                    AppState.bolsa_ativos.length() > 0,
                    rx.vstack(
                        rx.foreach(
                            AppState.bolsa_ativos,
                            lambda ativo: rx.hstack(
                                rx.vstack(
                                    rx.text(
                                        ativo["symbol"],
                                        weight="bold",
                                    ),
                                    rx.text(ativo["name"], size="2"),
                                    spacing="1",
                                    align="start",
                                ),
                                rx.spacer(),
                                rx.badge(ativo["category"]),
                                rx.cond(
                                    ativo["stale"] == "true",
                                    rx.badge(
                                        "Resultado desatualizado",
                                        color_scheme="amber",
                                    ),
                                    rx.fragment(),
                                ),
                                rx.button(
                                    "Ver detalhes",
                                    on_click=AppState.selecionar_ativo(
                                        ativo["symbol"]
                                    ),
                                    variant="soft",
                                    size="1",
                                ),
                                rx.button(
                                    rx.cond(
                                        ativo["favorito"] == "true",
                                        "Remover favorito",
                                        "Favoritar",
                                    ),
                                    on_click=AppState.alternar_favorito_bolsa(
                                        ativo["symbol"],
                                        ativo["category_code"],
                                    ),
                                    variant="outline",
                                    size="1",
                                ),
                                rx.text(
                                    "Fonte: ",
                                    ativo["source"],
                                    size="1",
                                ),
                                width="100%",
                                align="center",
                                flex_wrap="wrap",
                                padding="0.75em 0",
                                border_bottom="1px solid rgba(148,163,184,0.15)",
                            ),
                        ),
                        width="100%",
                        spacing="1",
                    ),
                    rx.cond(
                        AppState.bolsa_indisponivel != "",
                        rx.text(
                            AppState.bolsa_indisponivel,
                            size="2",
                            color="rgba(148,163,184,0.9)",
                        ),
                        rx.fragment(),
                    ),
                ),
                width="100%",
                align="start",
                spacing="3",
            ),
            width="100%",
            class_name="cashsave-panel",
        ),
        rx.card(
            rx.vstack(
                rx.heading("Ativos favoritos", size="4"),
                rx.text(
                    "Cotações só são exibidas após consulta a uma fonte "
                    "verificada, com origem e horário de referência.",
                    size="2",
                    color="rgba(148,163,184,0.9)",
                ),
                rx.cond(
                    AppState.bolsa_favoritos.length() > 0,
                    rx.vstack(
                        rx.foreach(
                            AppState.bolsa_favoritos,
                            lambda favorito: rx.hstack(
                                rx.vstack(
                                    rx.text(
                                        favorito["ativo_codigo"],
                                        weight="bold",
                                    ),
                                    rx.text(
                                        favorito["categoria_formatada"],
                                        size="2",
                                    ),
                                    align="start",
                                    spacing="1",
                                ),
                                rx.spacer(),
                                rx.button(
                                    "Consultar cotação",
                                    on_click=AppState.selecionar_ativo(
                                        favorito["ativo_codigo"]
                                    ),
                                    variant="soft",
                                    size="1",
                                ),
                                rx.button(
                                    "Remover",
                                    on_click=AppState.alternar_favorito_bolsa(
                                        favorito["ativo_codigo"],
                                        favorito["ativo_categoria"],
                                    ),
                                    variant="outline",
                                    size="1",
                                ),
                                width="100%",
                                align="center",
                                flex_wrap="wrap",
                                padding="0.75em 0",
                                border_bottom=(
                                    "1px solid rgba(148,163,184,0.15)"
                                ),
                            ),
                        ),
                        width="100%",
                        spacing="1",
                    ),
                    rx.text(
                        "Nenhum ativo favorito.",
                        size="2",
                        color="rgba(148,163,184,0.9)",
                    ),
                ),
                width="100%",
                align="start",
                spacing="3",
            ),
            width="100%",
            class_name="cashsave-panel",
        ),
        rx.card(
            rx.vstack(
                rx.heading("Comparar ativos", size="4"),
                rx.text(
                    "Compare desempenho de preço normalizado (base 100) em "
                    "períodos equivalentes. Indicadores específicos por "
                    "categoria não são comparados.",
                    size="2",
                    color="rgba(148,163,184,0.9)",
                ),
                rx.hstack(
                    rx.input(
                        placeholder="Códigos separados por vírgula",
                        value=AppState.bolsa_comparacao_ativos,
                        on_change=AppState.set_bolsa_comparacao_ativos,
                        width="100%",
                    ),
                    rx.select(
                        ["1 mês", "6 meses", "1 ano", "5 anos"],
                        value=AppState.bolsa_comparacao_periodo,
                        on_change=AppState.set_bolsa_comparacao_periodo,
                        aria_label="Período da comparação",
                    ),
                    rx.button(
                        "Comparar",
                        on_click=AppState.comparar_ativos_bolsa,
                        color_scheme="green",
                    ),
                    width="100%",
                    align="center",
                    flex_wrap="wrap",
                ),
                rx.cond(
                    AppState.bolsa_comparacao_aviso != "",
                    rx.callout(
                        AppState.bolsa_comparacao_aviso,
                        icon="triangle-alert",
                        color_scheme="amber",
                        width="100%",
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    AppState.bolsa_comparacao_series.length() > 0,
                    rx.vstack(
                        rx.grid(
                            rx.foreach(
                                AppState.bolsa_comparacao_desempenho,
                                lambda item: rx.vstack(
                                    rx.text(item["symbol"], size="2"),
                                    rx.heading(item["percentual"], size="4"),
                                    align="start",
                                ),
                            ),
                            columns=rx.breakpoints(initial="2", sm="4"),
                            spacing="3",
                            width="100%",
                        ),
                        rx.recharts.line_chart(
                            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
                            rx.recharts.x_axis(data_key="data"),
                            rx.recharts.y_axis(),
                            rx.recharts.tooltip(),
                            rx.recharts.legend(),
                            rx.foreach(
                                AppState.bolsa_comparacao_linhas,
                                lambda line: rx.recharts.line(
                                    data_key=line["symbol"],
                                    name=line["symbol"],
                                    stroke=line["color"],
                                    type_="monotone",
                                ),
                            ),
                            data=AppState.bolsa_comparacao_series,
                            width="100%",
                            height=300,
                        ),
                        rx.foreach(
                            AppState.bolsa_comparacao_fontes,
                            lambda fonte: rx.text(
                                fonte["symbol"],
                                " · Fonte: ",
                                fonte["source"],
                                " · Referência: ",
                                fonte["reference_at"],
                                " · ",
                                fonte["freshness"],
                                size="1",
                            ),
                        ),
                        width="100%",
                        spacing="3",
                        align="start",
                    ),
                    rx.fragment(),
                ),
                width="100%",
                align="start",
                spacing="3",
            ),
            width="100%",
            class_name="cashsave-panel",
        ),
        rx.card(
            rx.vstack(
                rx.heading("Alertas de preço", size="4"),
                rx.text(
                    "Alertas salvos não são monitorados em segundo plano. "
                    "Nenhuma notificação será enviada sem um avaliador "
                    "configurado e uma cotação verificada.",
                    size="2",
                    color="rgba(148,163,184,0.9)",
                ),
                rx.grid(
                    rx.input(
                        placeholder="Código do ativo",
                        value=AppState.bolsa_alerta_codigo,
                        on_change=AppState.set_bolsa_alerta_codigo,
                    ),
                    rx.select(
                        ["acao", "fii", "etf"],
                        value=AppState.bolsa_alerta_categoria,
                        on_change=AppState.set_bolsa_alerta_categoria,
                        aria_label="Categoria do ativo do alerta",
                    ),
                    rx.select(
                        [
                            "preco_acima",
                            "preco_abaixo",
                            "variacao_diaria_acima",
                            "variacao_diaria_abaixo",
                        ],
                        value=AppState.bolsa_alerta_condicao,
                        on_change=AppState.set_bolsa_alerta_condicao,
                        aria_label="Condição do alerta",
                    ),
                    rx.input(
                        placeholder="Limite de preço (R$)",
                        value=AppState.bolsa_alerta_preco,
                        on_change=AppState.set_bolsa_alerta_preco,
                    ),
                    rx.input(
                        placeholder="Limite de variação diária (%)",
                        value=AppState.bolsa_alerta_percentual,
                        on_change=AppState.set_bolsa_alerta_percentual,
                    ),
                    columns=rx.breakpoints(initial="1", sm="2", xl="3"),
                    spacing="3",
                    width="100%",
                ),
                rx.text(
                    "Preencha o limite correspondente à condição escolhida.",
                    size="2",
                    color="rgba(148,163,184,0.9)",
                ),
                rx.button(
                    "Salvar alerta",
                    on_click=AppState.salvar_alerta_bolsa,
                    color_scheme="green",
                ),
                rx.divider(),
                rx.heading("Alertas salvos", size="3"),
                rx.cond(
                    AppState.bolsa_alertas.length() > 0,
                    rx.vstack(
                        rx.foreach(
                            AppState.bolsa_alertas,
                            lambda alerta: rx.hstack(
                                rx.vstack(
                                    rx.text(
                                        alerta["ativo_codigo"],
                                        weight="bold",
                                    ),
                                    rx.text(
                                        alerta["condicao_formatada"],
                                        " ",
                                        alerta["limite_formatado"],
                                        " · ",
                                        alerta["ativo_categoria"],
                                        size="2",
                                    ),
                                    align="start",
                                    spacing="1",
                                ),
                                rx.spacer(),
                                rx.badge(
                                    alerta["monitoramento_status"],
                                    color_scheme="amber",
                                ),
                                rx.icon_button(
                                    rx.icon("trash-2", size=16),
                                    on_click=AppState.excluir_alerta_bolsa(
                                        alerta["id"]
                                    ),
                                    variant="ghost",
                                    color_scheme="red",
                                    aria_label="Excluir alerta",
                                ),
                                width="100%",
                                align="center",
                                flex_wrap="wrap",
                                padding="0.75em 0",
                                border_bottom=(
                                    "1px solid rgba(148,163,184,0.15)"
                                ),
                            ),
                        ),
                        width="100%",
                        spacing="1",
                    ),
                    rx.text(
                        "Nenhum alerta salvo.",
                        size="2",
                        color="rgba(148,163,184,0.9)",
                    ),
                ),
                width="100%",
                align="start",
                spacing="3",
            ),
            width="100%",
            class_name="cashsave-panel",
        ),
        rx.card(
            rx.vstack(
                rx.heading("Resumo da carteira", size="4"),
                rx.text(
                    "Patrimônio investido fica separado do caixa bancário. "
                    "Rentabilidade exclui proventos, exibidos em separado.",
                    size="2",
                    color="rgba(148,163,184,0.9)",
                ),
                rx.cond(
                    AppState.bolsa_carteira_erro != "",
                    rx.callout(
                        AppState.bolsa_carteira_erro,
                        icon="triangle-alert",
                        color_scheme="amber",
                        width="100%",
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    AppState.bolsa_carteira_aviso != "",
                    rx.callout(
                        AppState.bolsa_carteira_aviso,
                        icon="triangle-alert",
                        color_scheme="amber",
                        width="100%",
                    ),
                    rx.fragment(),
                ),
                rx.grid(
                    rx.vstack(
                        rx.text("Custo investido atual", size="2"),
                        rx.heading(
                            AppState.bolsa_carteira["custo_investido"],
                            size="5",
                        ),
                        align="start",
                    ),
                    rx.vstack(
                        rx.text("Total aplicado em compras", size="2"),
                        rx.heading(
                            AppState.bolsa_carteira["total_aplicado"],
                            size="5",
                        ),
                        align="start",
                    ),
                    rx.vstack(
                        rx.text("Valor de mercado", size="2"),
                        rx.heading(
                            AppState.bolsa_carteira["valor_mercado"],
                            size="5",
                        ),
                        align="start",
                    ),
                    rx.vstack(
                        rx.text("Resultado realizado", size="2"),
                        rx.heading(
                            AppState.bolsa_carteira["resultado_realizado"],
                            size="5",
                        ),
                        align="start",
                    ),
                    rx.vstack(
                        rx.text("Resultado não realizado", size="2"),
                        rx.heading(
                            AppState.bolsa_carteira["resultado_nao_realizado"],
                            size="5",
                        ),
                        align="start",
                    ),
                    rx.vstack(
                        rx.text("Rentabilidade simples", size="2"),
                        rx.heading(
                            AppState.bolsa_carteira["rentabilidade"],
                            size="5",
                        ),
                        align="start",
                    ),
                    columns=rx.breakpoints(initial="1", sm="2", xl="3"),
                    spacing="4",
                    width="100%",
                ),
                rx.grid(
                    rx.vstack(
                        rx.heading("Posições", size="3"),
                        rx.cond(
                            AppState.bolsa_carteira_posicoes.length() > 0,
                            rx.vstack(
                                rx.foreach(
                                    AppState.bolsa_carteira_posicoes,
                                    lambda posicao: rx.hstack(
                                        rx.vstack(
                                            rx.text(
                                                posicao["symbol"],
                                                weight="bold",
                                            ),
                                            rx.text(
                                                posicao["quantity"],
                                                " un. · ",
                                                posicao["category"],
                                                size="2",
                                            ),
                                            align="start",
                                            spacing="1",
                                        ),
                                        rx.spacer(),
                                        rx.vstack(
                                            rx.text(
                                                "Custo: ",
                                                posicao["cost_basis"],
                                                size="2",
                                            ),
                                            rx.text(
                                                "Mercado: ",
                                                posicao["market_value"],
                                                size="2",
                                            ),
                                            rx.cond(
                                                posicao["reference_at"] != "",
                                                rx.text(
                                                    "Fonte: ",
                                                    posicao["source"],
                                                    " · Referência: ",
                                                    posicao["reference_at"],
                                                    " · ",
                                                    posicao["freshness"],
                                                    size="1",
                                                ),
                                                rx.fragment(),
                                            ),
                                            rx.cond(
                                                posicao["stale"] == "true",
                                                rx.badge(
                                                    "Cotação desatualizada",
                                                    color_scheme="amber",
                                                ),
                                                rx.fragment(),
                                            ),
                                            align="end",
                                            spacing="1",
                                        ),
                                        width="100%",
                                        align="center",
                                        flex_wrap="wrap",
                                    ),
                                ),
                                width="100%",
                                spacing="2",
                            ),
                            rx.text(
                                "Nenhuma posição calculada.",
                                size="2",
                                color="rgba(148,163,184,0.9)",
                            ),
                        ),
                        align="start",
                        width="100%",
                        spacing="3",
                    ),
                    rx.vstack(
                        rx.heading("Distribuição por categoria", size="3"),
                        rx.cond(
                            AppState.bolsa_carteira_alocacao.length() > 0,
                            rx.vstack(
                                rx.foreach(
                                    AppState.bolsa_carteira_alocacao,
                                    lambda alocacao: rx.hstack(
                                        rx.text(alocacao["categoria"]),
                                        rx.spacer(),
                                        rx.text(
                                            alocacao["valor"],
                                            " · ",
                                            alocacao["percentual"],
                                        ),
                                        width="100%",
                                    ),
                                ),
                                width="100%",
                                spacing="2",
                            ),
                            rx.text(
                                "Indisponível sem valor de mercado verificável.",
                                size="2",
                                color="rgba(148,163,184,0.9)",
                            ),
                        ),
                        align="start",
                        width="100%",
                        spacing="3",
                    ),
                    columns=rx.breakpoints(initial="1", lg="2"),
                    spacing="4",
                    width="100%",
                ),
                rx.divider(),
                rx.heading("Fluxos mensais da carteira", size="3"),
                rx.text(
                    "A evolução mostra compras, vendas e proventos pagos. "
                    "Variação de mercado histórica indisponível sem cotações "
                    "verificadas.",
                    size="2",
                    color="rgba(148,163,184,0.9)",
                ),
                rx.cond(
                    AppState.bolsa_carteira_evolucao.length() > 0,
                    rx.recharts.bar_chart(
                        rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
                        rx.recharts.x_axis(data_key="periodo"),
                        rx.recharts.y_axis(),
                        rx.recharts.tooltip(),
                        rx.recharts.legend(),
                        rx.recharts.bar(
                            data_key="contribuicoes",
                            name="Compras",
                            fill="#10b981",
                        ),
                        rx.recharts.bar(
                            data_key="retiradas",
                            name="Vendas",
                            fill="#f59e0b",
                        ),
                        rx.recharts.bar(
                            data_key="proventos",
                            name="Proventos pagos",
                            fill="#6366f1",
                        ),
                        data=AppState.bolsa_carteira_evolucao,
                        width="100%",
                        height=300,
                    ),
                    rx.text(
                        "Sem movimentações para exibir.",
                        size="2",
                        color="rgba(148,163,184,0.9)",
                    ),
                ),
                width="100%",
                align="start",
                spacing="3",
            ),
            width="100%",
            class_name="cashsave-panel",
        ),
        rx.card(
            rx.vstack(
                rx.heading(
                    rx.cond(
                        AppState.bolsa_operacao_edicao_id != 0,
                        "Editar operação",
                        "Registrar operação",
                    ),
                    size="4",
                ),
                rx.grid(
                    rx.input(
                        placeholder="Código do ativo",
                        value=AppState.bolsa_operacao_codigo,
                        on_change=AppState.set_bolsa_operacao_codigo,
                    ),
                    rx.select(
                        ["acao", "fii", "etf"],
                        value=AppState.bolsa_operacao_categoria,
                        on_change=AppState.set_bolsa_operacao_categoria,
                        aria_label="Categoria do ativo",
                    ),
                    rx.select(
                        ["compra", "venda"],
                        value=AppState.bolsa_operacao_tipo,
                        on_change=AppState.set_bolsa_operacao_tipo,
                        aria_label="Tipo da operação",
                    ),
                    rx.input(
                        type="date",
                        value=AppState.bolsa_operacao_data,
                        on_change=AppState.set_bolsa_operacao_data,
                    ),
                    rx.input(
                        placeholder="Quantidade",
                        value=AppState.bolsa_operacao_quantidade,
                        on_change=AppState.set_bolsa_operacao_quantidade,
                    ),
                    rx.input(
                        placeholder="Preço unitário (R$)",
                        value=AppState.bolsa_operacao_preco,
                        on_change=AppState.set_bolsa_operacao_preco,
                    ),
                    rx.input(
                        placeholder="Custos (R$)",
                        value=AppState.bolsa_operacao_custos,
                        on_change=AppState.set_bolsa_operacao_custos,
                    ),
                    rx.input(
                        placeholder="Observações (opcional)",
                        value=AppState.bolsa_operacao_observacoes,
                        on_change=AppState.set_bolsa_operacao_observacoes,
                    ),
                    columns=rx.breakpoints(initial="1", sm="2", xl="4"),
                    spacing="3",
                    width="100%",
                ),
                rx.text(
                    "Compras incluem custos no custo médio; vendas descontam "
                    "custos do resultado realizado. Valores investidos não são "
                    "somados ao saldo bancário.",
                    size="2",
                    color="rgba(148,163,184,0.9)",
                ),
                rx.hstack(
                    rx.button(
                        rx.cond(
                            AppState.bolsa_operacao_edicao_id != 0,
                            "Salvar alterações",
                            "Registrar operação",
                        ),
                        on_click=AppState.salvar_operacao_bolsa,
                        color_scheme="green",
                    ),
                    rx.cond(
                        AppState.bolsa_operacao_edicao_id != 0,
                        rx.button(
                            "Cancelar",
                            on_click=AppState.cancelar_edicao_operacao_bolsa,
                            variant="outline",
                        ),
                        rx.fragment(),
                    ),
                    width="100%",
                    flex_wrap="wrap",
                ),
                rx.divider(),
                rx.heading("Histórico de operações", size="4"),
                rx.cond(
                    AppState.bolsa_operacoes.length() > 0,
                    rx.vstack(
                        rx.foreach(
                            AppState.bolsa_operacoes,
                            lambda operacao: rx.hstack(
                                rx.vstack(
                                    rx.text(
                                        operacao["ativo_codigo"],
                                        weight="bold",
                                    ),
                                    rx.text(
                                        operacao["data"],
                                        " · ",
                                        operacao["tipo"],
                                        " · ",
                                        operacao["quantidade"],
                                        " un.",
                                        size="2",
                                    ),
                                    spacing="1",
                                    align="start",
                                ),
                                rx.spacer(),
                                rx.vstack(
                                    rx.text(operacao["preco"]),
                                    rx.text(
                                        "Custos: ",
                                        operacao["custos"],
                                        size="1",
                                    ),
                                    spacing="1",
                                    align="end",
                                ),
                                rx.icon_button(
                                    rx.icon("pencil", size=16),
                                    on_click=AppState.editar_operacao_bolsa(
                                        operacao["id"]
                                    ),
                                    variant="ghost",
                                    aria_label="Editar operação",
                                ),
                                rx.icon_button(
                                    rx.icon("trash-2", size=16),
                                    on_click=AppState.excluir_operacao_bolsa(
                                        operacao["id"]
                                    ),
                                    variant="ghost",
                                    color_scheme="red",
                                    aria_label="Excluir operação",
                                ),
                                width="100%",
                                align="center",
                                flex_wrap="wrap",
                                padding="0.75em 0",
                                border_bottom="1px solid rgba(148,163,184,0.15)",
                            ),
                        ),
                        width="100%",
                        spacing="1",
                    ),
                    rx.text(
                        "Nenhuma operação de investimento registrada.",
                        size="2",
                        color="rgba(148,163,184,0.9)",
                    ),
                ),
                width="100%",
                align="start",
                spacing="3",
            ),
            width="100%",
            class_name="cashsave-panel",
        ),
        rx.card(
            rx.vstack(
                rx.heading("Proventos", size="4"),
                rx.grid(
                    rx.vstack(
                        rx.text("Total recebido", size="2"),
                        rx.heading(
                            AppState.bolsa_proventos_total_geral,
                            size="5",
                        ),
                        align="start",
                    ),
                    rx.vstack(
                        rx.text("Neste ano", size="2"),
                        rx.heading(
                            AppState.bolsa_proventos_total_ano,
                            size="5",
                        ),
                        align="start",
                    ),
                    rx.vstack(
                        rx.text("Neste mês", size="2"),
                        rx.heading(
                            AppState.bolsa_proventos_total_mes,
                            size="5",
                        ),
                        align="start",
                    ),
                    columns=rx.breakpoints(initial="1", sm="3"),
                    spacing="4",
                    width="100%",
                ),
                rx.text(
                    "Os totais consideram somente proventos pagos e suas "
                    "datas de pagamento. Anúncios não entram no recebido.",
                    size="2",
                    color="rgba(148,163,184,0.9)",
                ),
                rx.divider(),
                rx.heading("Registrar provento", size="4"),
                rx.grid(
                    rx.input(
                        placeholder="Código do ativo",
                        value=AppState.bolsa_provento_codigo,
                        on_change=AppState.set_bolsa_provento_codigo,
                    ),
                    rx.select(
                        ["acao", "fii", "etf"],
                        value=AppState.bolsa_provento_categoria,
                        on_change=AppState.set_bolsa_provento_categoria,
                        aria_label="Categoria do ativo do provento",
                    ),
                    rx.select(
                        ["dividendo", "jcp", "rendimento_fii", "outro"],
                        value=AppState.bolsa_provento_tipo,
                        on_change=AppState.set_bolsa_provento_tipo,
                        aria_label="Tipo de provento",
                    ),
                    rx.select(
                        ["pago", "anunciado"],
                        value=AppState.bolsa_provento_status,
                        on_change=AppState.set_bolsa_provento_status,
                        aria_label="Status do provento",
                    ),
                    rx.input(
                        placeholder="Valor (R$)",
                        value=AppState.bolsa_provento_valor,
                        on_change=AppState.set_bolsa_provento_valor,
                    ),
                    rx.input(
                        placeholder="Quantidade elegível (opcional)",
                        value=AppState.bolsa_provento_quantidade,
                        on_change=AppState.set_bolsa_provento_quantidade,
                    ),
                    rx.input(
                        type="date",
                        value=AppState.bolsa_provento_data_anuncio,
                        on_change=AppState.set_bolsa_provento_data_anuncio,
                        aria_label="Data do anúncio",
                    ),
                    rx.input(
                        type="date",
                        value=AppState.bolsa_provento_data_pagamento,
                        on_change=AppState.set_bolsa_provento_data_pagamento,
                        aria_label="Data de pagamento ou previsão",
                    ),
                    rx.input(
                        placeholder="Observações (opcional)",
                        value=AppState.bolsa_provento_observacoes,
                        on_change=AppState.set_bolsa_provento_observacoes,
                    ),
                    columns=rx.breakpoints(initial="1", sm="2", xl="3"),
                    spacing="3",
                    width="100%",
                ),
                rx.text(
                    "Data de pagamento obrigatória para marcar como pago; "
                    "anúncios podem ficar sem data de pagamento.",
                    size="2",
                    color="rgba(148,163,184,0.9)",
                ),
                rx.button(
                    "Registrar provento",
                    on_click=AppState.salvar_provento_bolsa,
                    color_scheme="green",
                ),
                rx.divider(),
                rx.heading("Histórico de proventos", size="4"),
                rx.cond(
                    AppState.bolsa_proventos.length() > 0,
                    rx.vstack(
                        rx.foreach(
                            AppState.bolsa_proventos,
                            lambda provento: rx.hstack(
                                rx.vstack(
                                    rx.hstack(
                                        rx.text(
                                            provento["ativo_codigo"],
                                            weight="bold",
                                        ),
                                        rx.badge(
                                            provento["status_formatado"],
                                            color_scheme=rx.cond(
                                                provento["status"] == "pago",
                                                "green",
                                                "amber",
                                            ),
                                        ),
                                        spacing="2",
                                    ),
                                    rx.text(
                                        provento["tipo_formatado"],
                                        " · ",
                                        provento["categoria_formatada"],
                                        " · Data: ",
                                        provento["data_referencia"],
                                        size="2",
                                    ),
                                    rx.cond(
                                        provento[
                                            "quantidade_elegivel_formatada"
                                        ]
                                        != "",
                                        rx.text(
                                            "Quantidade elegível: ",
                                            provento[
                                                "quantidade_elegivel_formatada"
                                            ],
                                            size="1",
                                        ),
                                        rx.fragment(),
                                    ),
                                    spacing="1",
                                    align="start",
                                ),
                                rx.spacer(),
                                rx.text(
                                    provento["valor_formatado"],
                                    weight="bold",
                                ),
                                width="100%",
                                align="center",
                                flex_wrap="wrap",
                                padding="0.75em 0",
                                border_bottom=(
                                    "1px solid rgba(148,163,184,0.15)"
                                ),
                            ),
                        ),
                        width="100%",
                        spacing="1",
                    ),
                    rx.text(
                        "Nenhum provento registrado.",
                        size="2",
                        color="rgba(148,163,184,0.9)",
                    ),
                ),
                width="100%",
                align="start",
                spacing="3",
            ),
            width="100%",
            class_name="cashsave-panel",
        ),
        rx.cond(
            AppState.bolsa_ativo_selecionado != "",
            rx.card(
                rx.vstack(
                    rx.heading(
                        AppState.bolsa_detalhe["symbol"],
                        size="5",
                    ),
                    rx.text(AppState.bolsa_detalhe["name"]),
                    rx.grid(
                        rx.vstack(
                            rx.text("Última cotação", size="2"),
                            rx.heading(
                                AppState.bolsa_detalhe["price"],
                                size="5",
                            ),
                            align="start",
                        ),
                        rx.vstack(
                            rx.text("Variação diária", size="2"),
                            rx.heading(
                                AppState.bolsa_detalhe["daily_change"],
                                size="5",
                            ),
                            align="start",
                        ),
                        rx.vstack(
                            rx.text("Categoria", size="2"),
                            rx.text(AppState.bolsa_detalhe["category"]),
                            align="start",
                        ),
                        rx.vstack(
                            rx.text("Métricas da categoria", size="2"),
                            rx.text(
                                AppState.bolsa_detalhe["category_metrics"]
                            ),
                            align="start",
                        ),
                        columns=rx.breakpoints(initial="1", sm="2"),
                        spacing="4",
                        width="100%",
                    ),
                    rx.text(
                        "Fonte: ",
                        AppState.bolsa_detalhe["source"],
                        " · Referência: ",
                        AppState.bolsa_detalhe["reference_at"],
                        " · ",
                        AppState.bolsa_detalhe["freshness"],
                        size="2",
                    ),
                    rx.cond(
                        AppState.bolsa_detalhe["stale"] == "true",
                        rx.badge(
                            "Cotação desatualizada",
                            color_scheme="amber",
                        ),
                        rx.fragment(),
                    ),
                    rx.hstack(
                        rx.select(
                            [
                                "Intraday",
                                "1 dia",
                                "1 semana",
                                "1 mês",
                                "6 meses",
                                "1 ano",
                                "5 anos",
                            ],
                            value=AppState.bolsa_periodo,
                            on_change=AppState.set_bolsa_periodo,
                            aria_label="Período do histórico",
                        ),
                        rx.button(
                            "Carregar histórico",
                            on_click=AppState.carregar_historico_bolsa,
                            variant="outline",
                        ),
                        width="100%",
                        align="center",
                        flex_wrap="wrap",
                    ),
                    rx.cond(
                        AppState.bolsa_historico.length() > 0,
                        rx.vstack(
                            rx.recharts.area_chart(
                                rx.recharts.cartesian_grid(
                                    stroke_dasharray="3 3",
                                ),
                                rx.recharts.area(
                                    data_key="preco",
                                    type_="monotone",
                                    stroke="#10b981",
                                    fill="#10b981",
                                    fill_opacity=0.15,
                                ),
                                rx.recharts.x_axis(data_key="data"),
                                rx.recharts.y_axis(),
                                rx.recharts.tooltip(),
                                data=AppState.bolsa_historico,
                                width="100%",
                                height=300,
                            ),
                            rx.text(
                                AppState.bolsa_historico_origem,
                                size="2",
                            ),
                            width="100%",
                            align="start",
                            spacing="2",
                        ),
                        rx.text(
                            AppState.bolsa_historico_mensagem,
                            size="2",
                            color="rgba(148,163,184,0.9)",
                        ),
                    ),
                    width="100%",
                    align="start",
                    spacing="3",
                ),
                width="100%",
                class_name="cashsave-panel",
            ),
            rx.fragment(),
        ),
        width="100%",
        spacing="4",
        align="start",
    )


def bolsa() -> rx.Component:
    return rx.cond(
        AppState.autenticado,
        app_layout("/bolsa", bolsa_conteudo()),
        auth_page(),
    )
