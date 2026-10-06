## Purpose

Apresentar a tela inicial do CashSave com o resumo financeiro, ainda com valores de exemplo.

## ADDED Requirements

### Requirement: Tela Visão Geral
O sistema SHALL exibir na rota `/` quatro cartões de resumo, um gráfico dos últimos seis meses, os próximos vencimentos, atalhos de acesso rápido e um banner do assistente.

#### Scenario: Abrir a tela inicial
- **WHEN** o usuário abre a rota `/`
- **THEN** os quatro cartões, o gráfico, os próximos vencimentos, os atalhos e o banner são exibidos

### Requirement: Valores de exemplo nesta fase
Enquanto não houver integração com o Xano, os valores financeiros exibidos SHALL ser fixos e de exemplo.

#### Scenario: Cartões sem dados reais
- **WHEN** a tela Visão Geral é exibida
- **THEN** os cartões mostram valores fixos de exemplo e não dados do usuário
