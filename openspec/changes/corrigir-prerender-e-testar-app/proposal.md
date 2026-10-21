# Proposal

## Why

`reflex compile --dry` passes, but `reflex run --env prod --single-port` currently fails while prerendering `/`, so there is no running local app to test in a browser. The project also has only four unit tests and no repeatable route-level smoke coverage for the main screens.

## What Changes

- Diagnose and correct the production prerender/startup failure without changing the app's user-facing flows.
- Add repeatable tests for the registered pages and important UI/state flows, using isolated or mocked Xano responses so tests do not mutate real user data.
- Document and run the production-mode smoke-test procedure and its limits.

## Capabilities

### New Capabilities
- `reflex-app-runtime`: Production-mode startup and registered pages remain available for local smoke testing, including when no authenticated session is present.

### Modified Capabilities

## Impact

- Reflex configuration and route/page components in `CashSave/`.
- Automated tests in `tests/`.
- Local run and verification instructions in `README.md`.
- The Xano backend is not changed or written to by automated tests.
