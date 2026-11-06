# sidebar-footer Specification

## Purpose

TBD: Update Purpose after archive.

## Requirements

### Requirement: Show authenticated user footer

The authenticated sidebar SHALL show the user's avatar fallback and name without collapsing the name column to zero width.

#### Scenario: User footer fits the sidebar

- **WHEN** the authenticated layout is rendered
- **THEN** the avatar, user name, and logout action are aligned within the sidebar without an empty gap caused by a collapsed text column.

### Requirement: Preserve logout behavior

The sidebar logout action SHALL continue to invoke the existing logout event.

#### Scenario: Logging out from the sidebar

- **WHEN** the user activates the logout button
- **THEN** the existing session logout flow is invoked.

