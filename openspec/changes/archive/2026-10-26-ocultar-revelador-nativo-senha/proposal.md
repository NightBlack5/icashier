# Proposal

## Why

The password field displays both the browser's native reveal control and CashSave's custom visibility button. This duplicates controls and makes the login form look broken.

## What Changes

- Hide the browser-native password reveal control in supported browsers.
- Keep CashSave's custom show/hide button and its accessible label as the single visibility control.

## Capabilities

### New Capabilities
- `password-visibility-control`: Provide one consistent, accessible show/hide control for password fields.

### Modified Capabilities

## Impact

- Affects the global app stylesheet and its registration in the Reflex app.
- Does not change password values, authentication, or the existing visibility state handler.