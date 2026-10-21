# Assistant quality

## ADDED Requirements

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
