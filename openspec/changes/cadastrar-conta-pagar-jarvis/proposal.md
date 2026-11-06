# Proposal

## Why

When a user tells Jarvis they have a bill to pay, such as a R$ 200 electricity
bill, the assistant mistakes “conta a pagar” for a request to pay or delete a
record and refuses. The app already supports pending bills with due dates, so
Jarvis should recognize this intent and help register the bill without claiming
it was saved before Xano confirms it.

## What Changes

- Distinguish requests to create a pending bill from requests to pay or delete
  an existing record.
- Collect a missing due date through a follow-up question rather than assuming
  a date.
- Preserve the pending bill's details across multiple clarification turns in
  the same conversation, so a description reply followed by a date reply still
  completes the original registration request.
- Register a pending bill only after its description, positive amount, and due
  date are known, then confirm only after Xano returns a saved record.
- Keep requests to pay or delete existing bills outside this creation flow.

## Capabilities

### New Capabilities
- `assistant-payable-bills`: Recognize and create user-authorized pending bills through Jarvis.

### Modified Capabilities
- None.

## Impact

- Jarvis intent parsing, conversation state, and Xano request handling in
  `CashSave/`.
- Existing authenticated `POST contas_a_pagar` endpoint and pending-bill state
  in `CashSave/state.py` and `xano/api/cashsave/contas_a_pagar_POST.xs`.
- Offline tests for intent recognition, due-date follow-up, and confirmed
  creation; no new API endpoint or dependency is expected.
