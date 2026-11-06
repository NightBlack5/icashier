# login-password-input Specification

## Purpose

Ensure Xano password verification receives the exact password text submitted by the user, while continuing to compare it against the stored hash and reject invalid credentials.

## Requirements

### Requirement: Verify the submitted password text

The login endpoint SHALL pass the submitted password text unchanged to the password verification operation and SHALL create a session only after verification succeeds.

#### Scenario: User submits the correct password

- **WHEN** the submitted password matches the stored password hash
- **THEN** the endpoint verifies it and returns an authenticated session

#### Scenario: User submits an incorrect password

- **WHEN** the submitted password does not match the stored password hash
- **THEN** the endpoint rejects the login and does not create an authentication token

