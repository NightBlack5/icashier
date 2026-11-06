# Design

## Context

The assistant currently routes all non-transaction messages to `FinancialOrchestrator`, so a request to create a PDF receives a textual financial answer. Reflex 0.9.12's `rx.download` accepts PDF bytes, allowing the chat event to trigger a direct browser download.

## Goals / Non-Goals

**Goals:**
- Recognize explicit PDF expense-report requests deterministically before calling the financial model.
- Generate a PDF from only the authenticated user's transactions already loaded in AppState.
- Confirm the download in chat and preserve the normal question path.

**Non-Goals:**
- Add filters, custom date ranges, charts, or income reporting in the first version.
- Send transaction data to the language model or add a new Xano endpoint.

## Decisions

- Add a small deterministic intent detector that requires both a PDF term and an expense/spending term. This prevents unrelated financial questions from being intercepted.
- Generate the PDF in a dedicated report module using ReportLab, filtering only `tipo == "despesa"`, sorting by transaction date, and calculating totals from integer cents.
- Return `rx.download(data=..., filename=..., mime_type="application/pdf")` from the existing chat event after storing the user and assistant messages.

## Risks / Trade-offs

- [Risk] No expense transactions exist → Generate a valid PDF with an explicit empty-state message and a zero total.
- [Risk] Very long descriptions or large histories exceed a page → Use a paginated table with repeated headers.

## Migration Plan

1. Add ReportLab and the report generator, intent detection, and download event path.
2. Test intent routing, expense-only totals, empty reports, and valid PDF bytes.
3. Run the full test suite and Reflex compile; no data migration or Xano deployment is required.