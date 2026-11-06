# password-visibility-control Specification

## Purpose

Password fields provide one clear, accessible show/hide control across supported browsers without changing how password values are entered or submitted.

## Requirements

### Requirement: Show one password visibility control

The authentication form SHALL display only the CashSave show/hide control and SHALL suppress duplicate browser-native reveal controls where supported.

#### Scenario: User views a password field in Edge

- **WHEN** the login form displays a password field
- **THEN** only one visibility icon is shown and it toggles the password between hidden and visible

