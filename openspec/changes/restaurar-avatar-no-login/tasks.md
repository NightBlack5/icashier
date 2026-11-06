# Tasks

## 1. Login Avatar Contract

- [x] 1.1 Include `avatar_url` in the Xano login user projection and response; verify the checked-in endpoint exposes the nullable field.
- [x] 1.2 Add a regression test for the login projection and response, then verify it passes with the focused Xano schema test.
- [x] 1.3 Preserve the deployed summary endpoint's filters, totals, and response while adding `avatar_url`; verify its schema regression test.

## 2. Integration Verification

- [x] 2.1 Run the full test suite, Reflex dry compile, and OpenSpec validation; verify 41 tests pass and the app compiles.
- [x] 2.2 Publish the updated login endpoint and verify by read-only pull that the remote projection and response include `avatar_url`.
- [x] 2.3 Publish the updated summary endpoint and verify by read-only pull that the live user projection includes `avatar_url`.
- [ ] 2.4 Verify in the authenticated browser that logging out and back in restores the saved profile photo.