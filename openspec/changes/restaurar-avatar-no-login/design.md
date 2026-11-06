# Design

## Context

The login endpoint now returns `avatar_url`, but the deployed `GET /resumo` query still projects only ID, name, email, and creation date. `AppState` replaces its user and avatar state with the summary response immediately after login, so the missing summary field clears the restored photo.

## Goals / Non-Goals

**Goals:**
- Return the user's saved avatar metadata as part of the existing login user object.
- Return the same metadata in the financial summary's user object.
- Add regression checks for both endpoint projections and response shapes.

**Non-Goals:**
- Change password validation, token creation, upload behavior, or avatar URL parsing.
- Deploy or publish Xano endpoints from the local workspace.

## Decisions

- Add `avatar_url` to the login and summary user projections. The summary endpoint must retain its existing date filters, aggregate totals, and response fields while adding the avatar.
- Keep the login response shape unchanged apart from the new nullable field so the current Python login handler can restore the photo.
- Keep the field nullable so users without a photo continue using the fallback avatar.

## Risks / Trade-offs

- [Risk] The deployed Xano endpoints may remain unchanged after local source updates → Preview and publish both changed endpoints before expecting persistence in the live app.

## Migration Plan

1. Preserve the deployed summary endpoint's existing behavior and add the avatar field to its user projection.
2. Run focused Xano schema tests, the full suite, and Reflex compilation.
3. Preview and publish the login and summary endpoints through the established Xano workflow; no data migration is needed.