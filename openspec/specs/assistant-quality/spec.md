# assistant-quality Specification

## Purpose

TBD: Update Purpose after archive.

## Requirements

### Requirement: Confirm only financial operations accepted by Xano

O Jarvis SHALL derive success confirmations from a transaction response that
contains an ID. If Xano rejects a transaction or does not confirm it, the Jarvis
SHALL report the failed item and SHALL NOT claim it was registered. For a batch,
it SHALL report confirmed items separately from failed items.

#### Scenario: Confirmed transaction

- **WHEN** Xano returns an ID for a submitted transaction
- **THEN** the Jarvis may include that transaction in the local state and
  describe it as registered

#### Scenario: Rejected transaction

- **WHEN** Xano rejects a submitted transaction or returns no transaction ID
- **THEN** the Jarvis SHALL report that the transaction was not confirmed and
  SHALL NOT add it to local state

#### Scenario: Partially confirmed batch

- **WHEN** Xano confirms some transactions but rejects a later transaction
- **THEN** the Jarvis SHALL retain only confirmed transactions locally, identify
  the failed item, and SHALL NOT report the full batch totals as final

### Requirement: No fabricated identity or actions

The assistant SHALL not invent facts about the CashSave organization, user,
financial records, or completed actions.

#### Scenario: User asks to record an expense

- **WHEN** the user asks the assistant to create, edit, delete, or register a
  financial record
- **THEN** it clearly explains that the current assistant is read-only and does
  not claim the operation was performed

### Requirement: Deterministic answers for observed finances

The assistant SHALL use backend calculations for questions about totals, saldo,
categories, budgets, and goals instead of asking the language model to invent
those values.

#### Scenario: User asks about current expenses

- **WHEN** the user asks for current totals or categories
- **THEN** the response uses the loaded user's calculated data and distinguishes
  observed values from estimates

### Requirement: Educational model responses remain grounded

The assistant SHALL constrain Ollama answers to the supplied context and
prohibit invented organization descriptions, user data, and completed actions.

#### Scenario: User asks for generic advice

- **WHEN** the user asks an educational financial question without requiring a
  current account value
- **THEN** Ollama returns advice without fabricating CashSave facts or claiming
  access to unavailable data

