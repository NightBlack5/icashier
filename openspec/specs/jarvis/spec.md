# jarvis Specification

## Purpose

TBD: Update Purpose after archive.

## Requirements

### Requirement: Ground financial answers in application data

The assistant SHALL use locally calculated application data for common
financial questions and SHALL NOT present contradictory or invented monetary
values.

#### Scenario: Asking how to save money

- **WHEN** the user asks how to save money, reduce spending, or organize a
  budget
- **THEN** the response uses the current calculated totals and gives general
  guidance without inventing balances, goals, or expenses.

### Requirement: Show the current assistant sidebar identity

The assistant page SHALL show the authenticated user's avatar fallback and name
without collapsing the name column to zero width.

#### Scenario: Opening Jarvis

- **WHEN** the authenticated assistant page is rendered
- **THEN** the sidebar footer is aligned and the user name is visible.

### Requirement: exibir Jarvis

The interface SHALL call the assistant Jarvis in menus, headers, the page title, and the initial greeting.

#### Scenario: abrir a página da assistente

- **WHEN** a pessoa abre `/assistente`
- **THEN** a página exibe o nome Jarvis

### Requirement: preservar funcionamento

Renaming the assistant SHALL preserve the `/assistente` route, Enter-to-send behavior, and existing financial capabilities.

#### Scenario: enviar mensagem

- **WHEN** a pessoa envia uma pergunta
- **THEN** a mensagem é processada pelo mesmo fluxo existente
