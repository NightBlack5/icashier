# Proposal

## Why

When a user asks Jarvis for a PDF of their expenses, the assistant currently responds with generic financial text and does not create a file. Users need the requested report to be generated from their actual authenticated transaction data.

## What Changes

- Recognize requests for an expense report in PDF format before sending other prompts to the language model.
- Generate a downloadable PDF from the authenticated user's loaded expense transactions, with transaction details and a total.
- Confirm completion in the chat and keep ordinary financial questions on the existing assistant path.

## Capabilities

### New Capabilities
- `assistant-expense-reports`: Generate and download a PDF report of the authenticated user's expenses on request.

### Modified Capabilities

## Impact

- Affects assistant intent handling and chat events, adds a PDF report generator and a ReportLab dependency, and adds focused tests.
- No Xano endpoints, financial records, or authentication behavior change.