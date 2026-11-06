# Design

## Context

The app already creates pending bills through an authenticated Xano endpoint
that requires a description, amount in cents, and due date. The calendar state
adds an item locally only after the endpoint returns an ID. The assistant's
read-only guard currently catches broad words such as “apagar” and “pagar”,
which can reject bill-registration language before it reaches any write flow.

## Goals / Non-Goals

**Goals:**
- Keep pending-bill intent separate from transaction entry, payment, and deletion.
- Hold a bill request until its required fields are complete.
- Reuse the existing authenticated endpoint and bill-list state.
- Preserve explicit Xano confirmation and error handling.

**Non-Goals:**
- Mark an existing bill paid or delete it through Jarvis.
- Invent a due date, category, or account.
- Change the Xano data model or create another endpoint.

## Decisions

- Add a deterministic bill-intent parser that runs before the generic read-only
  refusal and transaction parser. Restrict its “apagar” typo recognition to
  context that describes having a bill, so a plain delete request stays outside
  the creation flow.
- Represent an incomplete bill request as pending assistant state. When date,
  description, or amount is missing, ask for that field and defer the API call;
  do not substitute today's date.
- Parse an explicit due date from the initial request or a direct reply to
  Jarvis's due-date question. Bind that reply only to the unresolved bill in the
  current conversation.
- Preserve the unresolved bill across consecutive clarification turns: recover
  the latest bill request associated with an unanswered bill clarification,
  then apply subsequent user replies in order. A reply such as “é de Luz”
  completes the missing description; a later date-only reply completes the
  same bill instead of falling through to transaction parsing or general
  financial Q&A. Do not bind replies to a bill when there is no unresolved bill
  clarification in the active conversation.
- Use the existing `POST contas_a_pagar` request with cent values and optional
  category/account IDs only when resolved from the authenticated user's loaded
  data. Update local state and confirm only after the response contains an ID.
- Keep transaction batches and ordinary financial questions on their existing
  paths; use a distinct pending-bill classifier to avoid broadening transaction
  writes.

## Risks / Trade-offs

- [Risk] Natural language can make “apagar” mean delete rather than “a pagar” →
  require bill-ownership context and test deletion wording separately.
- [Risk] A date reply may refer to another topic → accept it only when the
  current conversation has an unresolved bill clarification and use that
  conversation's latest pending bill.
- [Risk] The local endpoint definition may differ from the deployed Xano
  workspace → keep API errors visible and verify the live endpoint before
  relying on the integration.

## Migration Plan

1. Add parser and conversation-state regression tests.
2. Implement intent discrimination, clarification, and confirmed bill creation.
3. Validate offline tests and Reflex compilation; verify the endpoint in the
   target Xano workspace before enabling the flow for real users.
4. Roll back by disabling the assistant bill-intent branch; existing calendar
   bill management remains unchanged.
