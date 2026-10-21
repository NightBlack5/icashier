# Tasks

## 1. Diagnose and fix production startup

- [x] 1.1 Reproduce `reflex run --env prod --single-port` and record the non-secret failure details, then isolate the cause of the `/` prerender timeout.
- [x] 1.2 Apply the smallest root-cause fix and add a regression test proving the public landing route does not depend on an authenticated session or Xano response; run the focused test and `reflex compile --dry`.

## 2. Add isolated app-flow coverage

- [x] 2.1 Add route smoke coverage for every page registered in `CashSave/CashSave.py`, verifying public routes render and protected routes show the unauthenticated state without real Xano calls.
- [x] 2.2 Add or expand mocked tests for the primary authentication and finance state/request flows, including invalid input and API failure cases; verify the full unittest suite passes without network access.
- [x] 2.3 Document the route-by-route smoke procedure, expected results, test commands, and real-Xano limitations in `README.md`; verify each documented local command is runnable.

## 3. Verify production integration

- [ ] 3.1 Start the app using the documented production command and verify `/` and every registered route in a browser, including the login state on protected routes and no unhandled server errors. Pending: routes load, but the Reflex event WebSocket still reports `Connection Error`.
- [x] 3.2 Run the full unit suite, `reflex compile --dry`, and `openspec validate corrigir-prerender-e-testar-app`; record which Xano behaviors remain unverified without a dedicated test account.
