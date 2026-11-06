# Spec Delta

## Purpose

Preserve a user's profile photo across authenticated sessions by returning the saved avatar metadata when the user signs in. This keeps the account identity consistent after logout and login.

## ADDED Requirements

### Requirement: Login restores the saved profile avatar
The login response SHALL include the authenticated user's persisted avatar metadata when a profile photo exists.

#### Scenario: User signs in after uploading a profile photo
- **WHEN** the user successfully signs in after a previous session ended
- **THEN** the login response includes the saved avatar metadata and the app displays the profile photo instead of the fallback avatar

#### Scenario: User has no profile photo
- **WHEN** the user successfully signs in without a saved avatar
- **THEN** the login response leaves the avatar empty and the app displays its normal fallback avatar

### Requirement: Summary loading preserves the profile avatar
The authenticated financial summary response SHALL include the user's persisted avatar metadata so loading account data does not clear the profile photo.

#### Scenario: App loads account data after login
- **WHEN** the app loads the financial summary for a user with a saved avatar
- **THEN** the summary's user record includes the avatar metadata and the profile photo remains visible