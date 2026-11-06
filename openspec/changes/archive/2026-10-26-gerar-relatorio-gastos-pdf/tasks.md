# Tasks

## 1. Expense PDF Generation

- [x] 1.1 Add a paginated PDF generator and ReportLab dependency; test expense filtering, totals, empty state, and PDF signature.
- [x] 1.2 Detect explicit expense-PDF requests in Jarvis and return a download event; test that report requests bypass the model and ordinary questions remain unchanged.

## 2. Integration Verification

- [x] 2.1 Run the full test suite, Reflex dry compile, and OpenSpec validation; verify 51 tests pass, the app compiles, and the chat event returns a download without calling the model.