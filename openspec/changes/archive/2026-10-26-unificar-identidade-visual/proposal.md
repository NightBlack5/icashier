# Proposal

## Why

As telas autenticadas usam barras laterais, fundos e espaçamentos diferentes, o que faz o CashSave parecer um conjunto de páginas desconectadas. Unificar o shell visual deixa a navegação mais clara e dá continuidade ao padrão escuro do Jarvis em todas as áreas do app.

## What Changes

- Padronizar navegação lateral, indicação da rota ativa, fundo e área principal nas telas autenticadas.
- Ajustar hierarquia, espaçamento e largura responsiva para que conteúdo e controles sejam mais fáceis de percorrer em desktop e celular.
- Preservar rotas, dados, textos funcionais e ações existentes.

## Capabilities

### New Capabilities
- `authenticated-app-shell`: comportamento e apresentação compartilhados para navegação e estrutura das páginas autenticadas.

### Modified Capabilities

## Impact

- Afeta `CashSave/CashSave.py`, as páginas autenticadas em `CashSave/pages/` e um novo componente compartilhado de layout.
- Não altera APIs, dependências, autenticação ou contratos do Xano.