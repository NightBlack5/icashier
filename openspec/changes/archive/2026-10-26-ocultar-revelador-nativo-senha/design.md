# Design

## Context

The authentication form already renders a custom icon button driven by Reflex state. Edge adds its own `::-ms-reveal` pseudo-element to password inputs.

## Goals / Non-Goals

**Goals:**
- Hide the Edge-native reveal and clear controls for password inputs.
- Preserve the custom accessible button and existing visibility event.

**Non-Goals:**
- Change password handling, browser support, or authentication behavior.

## Decisions

- Add a small local stylesheet under `assets/` and register it with `rx.App(stylesheets=[...])`. A stylesheet is required because pseudo-elements cannot be styled through normal component props.
- Target only `input[type="password"]::-ms-reveal` and `::-ms-clear` so unrelated controls remain unchanged.

## Risks / Trade-offs

- [Risk] Other browsers may use a different native reveal control → Keep the app's custom accessible control as the cross-browser visibility mechanism.

## Migration Plan

1. Add and register the stylesheet.
2. Compile the app and inspect the login form in Edge; verify the custom button still toggles visibility.