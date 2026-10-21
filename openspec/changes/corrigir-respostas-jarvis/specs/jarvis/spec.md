# Jarvis Specification

## ADDED Requirements

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
