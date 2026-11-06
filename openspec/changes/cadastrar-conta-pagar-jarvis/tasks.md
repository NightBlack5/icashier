# Tasks

## 1. Bill Intent and Clarification

- [x] 1.1 Add a deterministic parser for pending-bill wording, amount, description, and explicit due dates; verify exact and colloquial examples plus delete/payment wording in unit tests.
- [x] 1.2 Add conversation-scoped pending-bill clarification for missing amount, description, or due date; verify no Xano request occurs before all required values are present.
- [ ] 1.3 Preserve the original bill and merge short user replies across consecutive clarification turns in the active conversation; test a missing-description reply such as “é de Luz” followed by a date-only reply, ensuring the completed bill reaches Xano instead of transaction parsing or general Q&A.

## 2. Authenticated Creation

- [x] 2.1 Create bills through the authenticated Xano endpoint, resolve only existing user categories/accounts, and update local state only after an ID response; verify payload and confirmed-state tests.
- [x] 2.2 Cover Xano rejection and missing-ID responses; verify the assistant reports failure without claiming or locally adding an unconfirmed bill.

## 3. Integration Verification

- [ ] 3.1 Run the full offline test suite, Reflex dry compile, and OpenSpec validation after the multi-turn clarification regression is fixed; verify existing transaction-batch and read-only-question tests remain green.
