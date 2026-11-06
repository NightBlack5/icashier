# monetary-input-formatting Specification

## Purpose

Monetary input fields display values in Brazilian notation after editing, helping users verify amounts while preserving the existing cent-based financial data model.

## Requirements

### Requirement: Format monetary values after editing

Editable monetary fields SHALL display thousands separators and two decimal places using Brazilian notation when focus leaves the field.

#### Scenario: User enters a whole amount with thousands

- **WHEN** the user enters `20031` and leaves a monetary field
- **THEN** the field displays `20.031,00`

#### Scenario: User enters an amount with cents

- **WHEN** the user enters `20031,5` and leaves a monetary field
- **THEN** the field displays `20.031,50`

### Requirement: Preserve monetary input and storage behavior

Formatting a monetary field SHALL preserve the amount represented by the user's input and the existing storage in cents.

#### Scenario: User saves a formatted amount

- **WHEN** the user saves a formatted monetary value
- **THEN** the same numeric amount is sent to the existing financial action and stored in cents

