# Proposal

## Why

The Xano login endpoint currently declares the incoming credential as a `password` input, while `security.check_password` expects the original text value. The Xano-provided fix is to declare the input as `text password` so validation receives the user's entered value.

## What Changes

- Match the checked-in login endpoint to Xano's `text password` input declaration.
- Add a regression test so the endpoint does not revert to `password password`.
- Preserve the existing password check, token creation, and avatar response fields.

## Capabilities

### New Capabilities
- `login-password-input`: Pass the entered password text to the existing Xano password verification step.

### Modified Capabilities

## Impact

- Affects `xano/api/cashsave/auth/login_POST.xs` and `tests/test_xano_schema.py` only.
- No API deployment, credential changes, or password handling in the client.