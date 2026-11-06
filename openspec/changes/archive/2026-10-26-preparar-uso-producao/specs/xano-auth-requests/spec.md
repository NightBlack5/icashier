# xano-auth-requests Specification

## Purpose

Define how CashSave sends authenticated requests to its Xano API group.

## ADDED Requirements

### Requirement: Authenticated Xano requests include the session token

The application SHALL send the current session token in the `Authorization` header using the Bearer scheme for every authenticated Xano request.

#### Scenario: Request with an active session

- **WHEN** the application sends a request to Xano while a session token is present
- **THEN** the request contains `Authorization: Bearer <session-token>`

#### Scenario: Request without a session

- **WHEN** the application sends a request without a session token
- **THEN** the request does not contain an Authorization header

### Requirement: Authenticated user data accepts JSON values

The application SHALL accept the JSON types returned for authenticated user fields without rejecting a valid session response, and SHALL expose only validated strings to text and avatar UI fields.

#### Scenario: API returns a numeric user identifier

- **WHEN** Xano returns an authenticated user record containing a numeric identifier and string profile fields
- **THEN** the application retains the user record and renders the name, email, and avatar without a state type error

### Requirement: Local browser storage uses supported value types

The application SHALL store dismissed-notification identifiers using the string values supported by Reflex browser storage and SHALL recover safely from invalid stored JSON.

#### Scenario: Dismissed notifications persist locally

- **WHEN** a user dismisses a notification
- **THEN** the identifier is serialized to browser storage and is not shown again in that browser

#### Scenario: Browser storage contains invalid notification data

- **WHEN** dismissed-notification storage is empty, malformed, or not a list of strings
- **THEN** the application continues with an empty valid set of dismissed identifiers
