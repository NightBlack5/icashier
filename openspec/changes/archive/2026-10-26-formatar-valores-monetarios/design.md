# Design

## Context

The transaction amount input already uses a text field and formats with the shared Brazilian currency helper on blur. The bill input in the calendar uses `type="number"`, so it cannot show Brazilian thousands separators or comma decimals.

## Goals / Non-Goals

**Goals:**
- Make the bill amount field follow the same blur formatting as transaction amounts.
- Keep parsing and cent-based API payloads unchanged.
- Cover the formatter with regression tests for thousands and decimal input.

**Non-Goals:**
- Add a live input mask that changes the cursor while typing.
- Change formatting for display-only amounts or alter financial persistence.

## Decisions

- Change the bill amount field to a text input and format its state on blur using the existing `_formatar_entrada_reais` helper. This reuses the established parser and avoids introducing a second currency-formatting implementation.
- Keep the input unformatted while focused so the user can edit digits naturally; apply grouping and two decimal places after blur.

## Risks / Trade-offs

- [Risk] Invalid text cannot be formatted on blur → Leave the entered text unchanged and let the existing save validation display its error.

## Migration Plan

1. Add a bill-value formatting event and wire it to the calendar field.
2. Test whole values, localized decimals, and existing cent conversion.
3. Run the full test suite and Reflex compile; no data migration is required.