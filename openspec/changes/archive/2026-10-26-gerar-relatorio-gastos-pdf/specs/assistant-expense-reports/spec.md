# Spec Delta

## Purpose

Allow Jarvis to deliver a real PDF expense report based on the authenticated user's saved transactions, rather than answering a file-generation request with generic financial advice.

## ADDED Requirements

### Requirement: Generate an expense report PDF on request
Jarvis SHALL generate and download a PDF when an authenticated user asks for a PDF report of their expenses.

#### Scenario: User requests a PDF of expenses
- **WHEN** the user asks Jarvis for their expenses or spending in PDF format
- **THEN** Jarvis creates a PDF from that user's loaded transactions and starts a file download

### Requirement: Report only expense transactions with a total
The PDF SHALL list the authenticated user's expense transactions and their total without including income as an expense.

#### Scenario: User has expenses and income
- **WHEN** the report is generated from transactions that include both expenses and income
- **THEN** it lists only expenses and shows the sum of those expenses

#### Scenario: User has no expenses
- **WHEN** the authenticated user has no expense transactions
- **THEN** the PDF states that no expenses were found and shows a zero total

### Requirement: Keep report generation separate from ordinary questions
Requests that do not ask for an expense PDF SHALL continue through the existing assistant response flow.

#### Scenario: User asks a financial question
- **WHEN** the user asks a question without requesting an expense PDF
- **THEN** Jarvis responds through its existing contextual financial assistant flow