# Technical audit specification

## Purpose

Define the evidence and reporting requirements for a read-only technical audit
of the CashSave application.

## ADDED Requirements

### Requirement: Evidence-based audit report
The repository SHALL contain an audit report that distinguishes verified,
partial, failed, unverified, and not-applicable areas, with file evidence and
safe reproduction details where possible.

#### Scenario: Report a concrete defect
- **WHEN** a defect is observed in code or execution
- **THEN** the report records its priority, evidence, impact, probable cause,
  recommended remediation, and a verification test without claiming it is fixed

### Requirement: Safe verification
The audit SHALL use only non-destructive local checks and SHALL document
limitations caused by unavailable external services, accounts, or production
infrastructure.

#### Scenario: External Xano behavior is unavailable
- **WHEN** a flow requires a live Xano workspace or a test account
- **THEN** the report marks it unverified and states the exact evidence needed
  for confirmation

### Requirement: No sensitive disclosure
The audit SHALL not print or persist secret values from environment files,
authentication tokens, passwords, or private user data.

#### Scenario: Report configuration safely
- **WHEN** configuration or authentication code is cited as evidence
- **THEN** the report names variables and code locations without including
  their secret values
