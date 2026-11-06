# Spec Delta

## Purpose

The authenticated app shell provides a consistent navigation and content frame across CashSave pages. It keeps users oriented as they move between financial tools and adapts the frame to narrower screens.

## ADDED Requirements

### Requirement: Consistent authenticated navigation
Every authenticated page SHALL use the same navigation structure and clearly identify the current route.

#### Scenario: User navigates between authenticated pages
- **WHEN** the user opens any authenticated route
- **THEN** the shared navigation is displayed and the matching destination is visibly active

### Requirement: Responsive authenticated content frame
The authenticated layout SHALL keep navigation and page content usable without horizontal overflow on desktop and narrow screens.

#### Scenario: User opens the app on a narrow screen
- **WHEN** an authenticated page is displayed in a narrow viewport
- **THEN** navigation remains available, content fits the available width, and primary controls do not overlap

### Requirement: Preserve authenticated page behavior
Visual updates to the authenticated shell SHALL preserve existing routes, page data, and user actions.

#### Scenario: User uses a page action after the visual update
- **WHEN** the user activates an existing navigation or page control
- **THEN** the same route or application action is invoked as before the update