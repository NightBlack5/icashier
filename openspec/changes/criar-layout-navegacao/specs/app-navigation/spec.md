## Purpose

Permitir que o usuário navegue entre as telas do CashSave por uma barra lateral comum a todas as páginas.

## ADDED Requirements

### Requirement: Barra lateral com menu principal
O sistema SHALL exibir, em todas as telas, uma barra lateral com os itens Visão Geral, Assistente IA, Finanças, Calendário, Sobre, Suporte e Apoiar o CashSave.

#### Scenario: Exibição do menu
- **WHEN** o usuário abre qualquer tela do aplicativo
- **THEN** a barra lateral mostra os sete itens do menu

### Requirement: Destaque do item ativo
O sistema SHALL destacar no menu o item correspondente à tela atual.

#### Scenario: Tela de Suporte aberta
- **WHEN** o usuário está na rota `/suporte`
- **THEN** o item "Suporte" aparece destacado em verde

### Requirement: Navegação para telas existentes
Os itens do menu cujas telas já existem SHALL levar o usuário à respectiva rota.

#### Scenario: Abrir o assistente
- **WHEN** o usuário clica em "Assistente IA"
- **THEN** a aplicação abre a rota `/assistente`

#### Scenario: Telas ainda não criadas
- **WHEN** o usuário clica em um item cuja tela ainda não foi implementada
- **THEN** a aplicação exibe a página padrão de rota não encontrada
