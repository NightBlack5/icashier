# Proposal

## Why

Money fields currently behave differently across pages: transactions format after focus leaves the field, while bills use an unformatted numeric input. A consistent Brazilian currency format makes large values easier to verify before saving.

## What Changes

- Use editable text inputs for monetary amounts so Brazilian thousands and decimal separators can be displayed.
- Apply the same currency formatting on blur to transaction and bill amount fields.
- Keep numeric parsing and cent-based storage unchanged.

## Capabilities

### New Capabilities
- `monetary-input-formatting`: Display monetary field values in Brazilian currency notation after editing.

### Modified Capabilities

## Impact

- Affects the transaction and bill forms in `CashSave/pages/` and the matching `AppState` value-formatting handler.
- No Xano schema, financial calculations, or dependency changes.