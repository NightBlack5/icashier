# Spec Delta

## Purpose

Defines reliable local production startup and browser-visible route behavior for the CashSave application. This capability supports repeatable smoke testing without requiring real Xano writes.

## ADDED Requirements

### Requirement: Production mode serves the public landing page
The application SHALL complete its local production startup and serve the public landing page without requiring an authenticated user or a successful Xano request.

#### Scenario: Start the app without an authenticated session
- **WHEN** a developer starts the application in production mode with its documented local configuration
- **THEN** the startup completes and the landing page at `/` returns a successful HTTP response

#### Scenario: Xano is unavailable while opening the landing page
- **WHEN** the Xano API is unavailable and a visitor opens `/`
- **THEN** the public landing page remains available without waiting for an Xano response

### Requirement: Registered routes are smoke-testable without mutating real data
The project SHALL provide a repeatable route smoke-test procedure for every registered page, and tests of authenticated data flows SHALL isolate or mock Xano rather than write to real user data.

#### Scenario: Visit each registered page without a session
- **WHEN** a developer follows the documented local route smoke-test procedure
- **THEN** public pages render and protected pages show the unauthenticated login state without an unhandled server error

#### Scenario: Exercise an authenticated flow in automated tests
- **WHEN** an automated test exercises an authenticated data flow
- **THEN** Xano responses are isolated or mocked and no remote user record is created, changed, or deleted
