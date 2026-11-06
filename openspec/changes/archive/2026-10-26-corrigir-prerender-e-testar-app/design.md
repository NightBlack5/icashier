# Design

## Context

See proposal.md - Why. The root route is a static landing page, while dashboard and finance routes depend on `AppState` and Xano. `reflex compile --dry` succeeds, but the production run stops during prerender before a local server can be smoke-tested. The repository currently uses `unittest` and has no browser-test dependency.

## Goals / Non-Goals

**Goals:**
- Reproduce and diagnose the production prerender failure before changing runtime behavior.
- Keep public routes independent of Xano availability and preserve authenticated-route behavior.
- Cover the registered route set and key state/request behavior with isolated tests and a documented browser smoke pass.

**Non-Goals:**
- Publish or modify Xano APIs, create remote test accounts, or mutate real financial records.
- Add a test framework or browser automation dependency unless the existing tools prove insufficient and the need is reviewed.
- Change the visual design or product behavior as a workaround for a build failure.

## Decisions

- Reproduce the production failure with bounded logs and inspect the underlying cause before selecting a code fix. Do not treat a longer timeout, skipped prerender, or a dry compile as proof that the production startup issue is resolved.
- Use the existing `unittest` runner for deterministic state and request tests. Mock Xano responses for authenticated behavior so test execution is offline and side-effect-free.
- Use the existing production-mode Reflex command for an integration smoke pass, then check every registered route in a browser with no session. Public pages must render, and protected pages must show their unauthenticated state.
- Keep real-Xano verification separate from the automated suite; it requires a designated test account and is reported as unverified when those prerequisites are absent.

## Risks / Trade-offs

- [The production timeout may be caused by generated runtime or environment state rather than a page component] → Capture the full relevant failure and process/port state before editing, then verify the fix from a clean startup.
- [A mocked backend cannot prove the remote Xano workspace is correctly published] → Report mocked coverage and real-backend verification separately.
- [A route returning HTTP 200 may still contain a rendering or navigation defect] → Check page content and protected-route behavior in the browser, not only HTTP status.
