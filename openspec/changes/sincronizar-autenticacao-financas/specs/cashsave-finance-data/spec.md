# cashsave-finance-data Specification

## MODIFIED Requirements

### Requirement: User-owned financial records

Financial accounts, transactions, bills, budgets, goals, recurring entries, and preferences SHALL be associated with the authenticated Xano user. Custom categories SHALL be user-owned, while system categories MAY have no owner. APIs SHALL restrict each user's data to that user.

#### Scenario: Isolating a user's financial data

- **WHEN** an API reads or changes a user's financial records
- **THEN** it authenticates the user and restricts access to records whose `usuario_id` matches that user

### Requirement: User preferences and assistant history

The data model SHALL store one preference record per user for currency, locale, timezone, and notification settings, including due-date, budget, and goal notifications. Assistant conversations and messages SHALL use the existing Xano conversation and message tables.

#### Scenario: Retrieving a user's preferences and chat history

- **WHEN** an authenticated user requests preferences or assistant history
- **THEN** the API returns only that user's preference record and conversations

## ADDED Requirements

### Requirement: Load the authenticated financial workspace

The authenticated summary endpoint SHALL return the current user's profile, transactions, accounts, categories, bills, budgets, goals, recurring entries, and preferences, scoped to the authenticated user.

#### Scenario: Loading the financial workspace

- **WHEN** an authenticated user requests the summary
- **THEN** the response includes the user's financial collections and preferences without exposing another user's records

### Requirement: Filter and export transactions

The application SHALL allow the user to filter their transactions by description, type, category, account, and supported period, and export the currently filtered transactions as a CSV file.

#### Scenario: Exporting filtered transactions

- **WHEN** the user applies transaction filters and requests CSV export
- **THEN** the downloaded CSV contains the filtered transactions with date, type, description, amount, and category

### Requirement: Manage recurring entries

The application SHALL support authenticated recurring income and expense entries with an amount, frequency, next occurrence date, and active state. Users SHALL be able to create, pause, resume, and delete their recurring entries.

#### Scenario: Processing due occurrences

- **WHEN** financial data is loaded and an active recurring entry has an occurrence due on or before the current date
- **THEN** the application records the occurrence as a transaction, prevents recording the same recurrence occurrence twice, and advances the next occurrence date

#### Scenario: Managing a recurring entry

- **WHEN** an authenticated user creates, pauses, resumes, or deletes a recurring entry
- **THEN** the Xano API changes only a recurring entry owned by that user and the application reflects the confirmed result

### Requirement: Notify about financial deadlines and limits

The application SHALL generate dismissible notifications, respecting each user's notification preferences, for pending bills due within seven days, active budgets at or above 80% of their limit within the configured period, and active goals whose target date is within 30 days and whose target has not been reached.

#### Scenario: Showing an enabled financial notification

- **WHEN** a financial item meets its notification threshold and the corresponding preference is enabled
- **THEN** the application displays a notification that the user can dismiss

#### Scenario: Disabling a notification category

- **WHEN** the user disables a notification preference
- **THEN** the application does not generate notifications for that category

### Requirement: Track goal contributions

The application SHALL allow a user to add a positive contribution to their own financial goal, without increasing the current amount beyond the goal's target.

#### Scenario: Contributing to a goal

- **WHEN** the user submits a contribution for an existing goal
- **THEN** the application requests the updated goal and caps its current amount at the target amount
