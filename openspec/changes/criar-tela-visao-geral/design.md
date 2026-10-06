# Design: criar-tela-visao-geral

## Context

A tela Visão Geral é a primeira que o usuário vê. Ela resume saldo, receitas, despesas e contas a pagar, e dá acesso rápido às demais áreas.

## Decisions

1. O gráfico usa `rx.recharts.area_chart` do Reflex, com uma série para receitas e outra para despesas.
2. Os dados do gráfico e dos cartões são constantes no código até a integração com o Xano.
3. Os atalhos apontam para as rotas do menu.

## Risks / Trade-offs

O componente de gráfico é sensível à versão do Reflex. Atalhos para telas inexistentes levam a uma página não encontrada.

Nota de processo: esta mudança foi documentada em formato OpenSpec depois de a implementação já ter sido feita. As mudanças seguintes seguem a ordem proposta, specs, design, tarefas e só então código.
