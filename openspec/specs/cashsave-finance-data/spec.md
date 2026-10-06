# cashsave-finance-data Specification

## Purpose

Define the persistent data model for CashSave financial accounts, transactions, budgets, recurring entries, goals, and user preferences in Xano.

## Requirements

### Requirement: User-owned financial records

Financial accounts, transactions, bills, budgets, goals, and preferences SHALL be associated with the authenticated Xano user. Custom categories SHALL be user-owned, while system categories MAY have no owner.

#### Scenario: Isolating a user's financial data

- **WHEN** an API reads or changes a user's financial records
- **THEN** it authenticates the user and restricts access to records whose `usuario_id` matches that user

### Requirement: Transactions and due dates

The data model SHALL store income and expense transactions with an amount in cents, transaction date, and optional account, category, and notes. Bills SHALL separately store an amount in cents, due date, status, optional payment date, recurrence setting, and notes.

#### Scenario: Recording a pending bill

- **WHEN** a user creates an unpaid bill with a due date
- **THEN** the bill can be represented as pending and queried for the financial calendar

### Requirement: Budget and goal tracking

The data model SHALL store user budgets with optional category scope, limit in cents, periodicity, and date range. It SHALL store financial goals with target and current amounts in cents, optional target date, and status.

#### Scenario: Summarizing budget and goal progress

- **WHEN** an API retrieves budgets or goals for a user
- **THEN** it can return the configured limits, targets, periods, and current goal progress

### Requirement: User preferences and assistant history

The data model SHALL store one preference record per user for currency, locale, timezone, and notification settings. Assistant conversations and messages SHALL use the existing Xano conversation and message tables.

#### Scenario: Retrieving a user's preferences and chat history

- **WHEN** an authenticated user requests preferences or assistant history
- **THEN** the API returns only that user's preference record and conversations
