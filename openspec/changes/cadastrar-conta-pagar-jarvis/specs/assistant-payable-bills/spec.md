# Spec Delta

## Purpose

Jarvis helps authenticated users record unpaid bills as pending items in their
financial calendar, while keeping missing information and destructive or payment
requests explicit and safe.

## ADDED Requirements

### Requirement: Recognize requests to create a pending bill

Jarvis SHALL distinguish requests to register a bill as pending from requests
to pay or delete an existing record.

#### Scenario: User describes a bill to pay

- **WHEN** an authenticated user says they have a bill to pay, names the bill,
  and provides a positive amount
- **THEN** Jarvis treats it as a request to create a pending bill, not as a
  request to pay or delete a record

#### Scenario: Colloquial wording for a pending bill

- **WHEN** an authenticated user says “tenho uma conta apagar conta de luz
  200 reais” or uses the equivalent phrase “conta a pagar”
- **THEN** Jarvis recognizes the intended pending-bill registration and does not
  answer with a generic read-only refusal

#### Scenario: User requests payment or deletion of an existing bill

- **WHEN** a user explicitly asks Jarvis to pay or delete an existing bill
- **THEN** Jarvis does not treat the request as creation of a new pending bill
  and does not change any existing record

### Requirement: Collect required bill information before saving

Jarvis SHALL collect a bill description, positive amount, and due date before
creating a pending bill, and SHALL NOT assume a missing due date.

#### Scenario: Due date is missing

- **WHEN** a user provides the description and amount of a pending bill but no
  due date
- **THEN** Jarvis asks for the due date and sends no create request until the
  user provides a valid date

#### Scenario: Amount or description is missing

- **WHEN** a user asks to register a bill without a usable amount or description
- **THEN** Jarvis asks for the missing information and sends no create request

#### Scenario: User supplies the requested due date

- **WHEN** the user replies to Jarvis's due-date question with a valid date
- **THEN** Jarvis uses that date for the pending bill under discussion without
  asking the user to repeat its description or amount

#### Scenario: User answers multiple bill clarification questions

- **WHEN** Jarvis asks for a missing bill description, the user supplies it,
  Jarvis then asks for the due date, and the user supplies a valid date
- **THEN** Jarvis combines the original bill request and both replies, creates
  the pending bill without treating the date as a separate financial question,
  and does not ask the user to repeat previously supplied information

### Requirement: Confirm only bills accepted by Xano

Jarvis SHALL create a pending bill only for the authenticated user and SHALL
confirm creation only after Xano returns the saved bill with an ID.

#### Scenario: Xano confirms bill creation

- **WHEN** Xano returns a saved pending bill with an ID
- **THEN** Jarvis adds the confirmed bill to the local pending-bill list and
  tells the user its description, amount, and due date

#### Scenario: Xano rejects or does not confirm bill creation

- **WHEN** Xano rejects the request or returns no bill ID
- **THEN** Jarvis reports that the bill was not confirmed and does not add it to
  the local pending-bill list
