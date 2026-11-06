# Design

## Context

The checked-in Xano login endpoint declares the input as `password password`. The Xano-provided correction is `text password`, which leaves the submitted value available for the existing `security.check_password` operation.

## Goals / Non-Goals

**Goals:**
- Match the local endpoint to the input declaration supplied by Xano.
- Keep the existing password comparison, rejection condition, token creation, and avatar response intact.
- Add a schema test that locks the input type.

**Non-Goals:**
- Publish or modify Xano remotely.
- Log, return, or persist the submitted plaintext password.

## Decisions

- Change only the input type from `password` to `text`; the input name remains `password` so the existing `$input.password` references continue to work.
- Preserve `security.check_password` and its successful-result precondition unchanged.

## Risks / Trade-offs

- [Risk] A future schema edit could restore Xano's auto-hashing input type → Assert the exact `text password` declaration in the schema regression test.

## Migration Plan

1. Update the checked-in Xano source and focused schema test.
2. Run the Xano schema test, full test suite, Reflex compile, and OpenSpec validation.
3. Keep remote review/publish under the Xano workflow; this change itself only synchronizes the repository source.