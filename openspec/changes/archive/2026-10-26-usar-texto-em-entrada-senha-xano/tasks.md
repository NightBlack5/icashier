# Tasks

## 1. Xano Login Input

- [x] 1.1 Change the local login input to `text password` without modifying password verification, token creation, or avatar fields; verify the endpoint keeps `$input.password` unchanged.
- [x] 1.2 Add a regression test for the exact input declaration and ensure `password password` is absent.

## 2. Verification

- [x] 2.1 Run the focused schema test, full suite, Reflex dry compile, and OpenSpec validation; verify 53 tests pass and no remote endpoint was changed by this sync.