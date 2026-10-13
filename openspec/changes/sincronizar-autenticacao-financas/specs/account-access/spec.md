# account-access Specification

## Purpose

Define registration, login, and profile-photo behavior for CashSave accounts.

## ADDED Requirements

### Requirement: Register an account

The application SHALL provide a registration flow that collects a name, email, phone number, password, password confirmation, and explicit consent to the displayed data-use statement. It SHALL reject incomplete or invalid input before submitting registration to Xano.

The phone field SHALL format Brazilian numbers as the user types, supporting both `(DD) 1234-5678` and `(DD) 91234-5678`, and SHALL limit the number to at most 11 digits.

#### Scenario: Submitting valid registration details

- **WHEN** a visitor submits a name, email, phone with a valid DDD, matching password confirmation, and a password of at least eight characters containing a letter and a digit after accepting the data-use statement
- **THEN** the application sends the registration details to Xano and establishes a session when Xano returns an authentication token

#### Scenario: Submitting invalid registration details

- **WHEN** a required registration field is missing, the phone is invalid, the passwords differ, the password does not meet the minimum rule, or consent is not accepted
- **THEN** the application displays a validation error and does not submit the registration request

#### Scenario: Formatting a phone number during entry

- **WHEN** a visitor types or pastes a Brazilian phone number into the registration phone field
- **THEN** the field displays the corresponding DDD and local number with parentheses, spacing, and a hyphen, and ignores non-digits beyond the supported 11 digits

### Requirement: Sign in to an account

The application SHALL allow a visitor to sign in using an email and password, retain the email only when the visitor selects “Lembrar de mim”, and require a token returned by Xano before treating sign-in as successful.

#### Scenario: Successful sign-in

- **WHEN** Xano accepts the submitted email and password and returns an authentication token
- **THEN** the application stores the session and directs the user to the authenticated application

#### Scenario: Sign-in without credentials or token

- **WHEN** the email or password is empty, or Xano does not return an authentication token
- **THEN** the application reports an error and does not establish an authenticated session

### Requirement: Manage the authenticated user's profile photo

The application SHALL allow an authenticated user to upload or remove their own profile photo through authenticated Xano endpoints and reflect the returned avatar URL in the profile.

#### Scenario: Uploading a profile photo

- **WHEN** an authenticated user uploads a supported image and Xano returns the updated user
- **THEN** the application updates the displayed profile photo using the returned avatar URL

#### Scenario: Removing a profile photo

- **WHEN** an authenticated user removes their profile photo and Xano confirms the update
- **THEN** the application clears the displayed avatar URL
