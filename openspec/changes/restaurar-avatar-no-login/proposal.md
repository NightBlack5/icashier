# Proposal

## Why

After a user signs out and signs in again, the profile photo is replaced by the fallback avatar. The login endpoint omitted the persisted avatar, and the subsequent financial summary response also omitted it, overwriting the restored value during page loading.

## What Changes

- Include the stored avatar metadata in the authenticated user's login response.
- Preserve the stored avatar metadata in the authenticated financial summary response.
- Add a regression check that the login contract returns the avatar field.

## Capabilities

### New Capabilities
- `avatar-session-restoration`: Restore persisted profile avatar data when a user authenticates.

### Modified Capabilities

## Impact

- Affects the Xano login and summary endpoints under `xano/api/cashsave/` and their schema regression tests.
- No dependency, route, credential, or authentication-validation changes.