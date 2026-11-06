# Design

## Context

The dashboard has a shared shell in `CashSave/CashSave.py`, while Jarvis and Finanças define their own sidebars and Calendário imports the finance sidebar. Their route highlighting, spacing, and backgrounds have drifted. The existing Reflex app already uses a dark Radix theme with green accents and responsive breakpoints.

## Goals / Non-Goals

**Goals:**
- Provide one authenticated shell and one source of truth for navigation items and active-route styling.
- Keep page content fluid and the navigation usable at narrow viewport widths.
- Preserve each page's existing content and event handlers.

**Non-Goals:**
- Change authentication, Xano APIs, finance calculations, or page workflows.
- Redesign public landing and authentication experiences in this change.
- Add a new dependency or replace the existing visual theme.

## Decisions

- Put `app_sidebar` and `app_layout` in `CashSave/components/layout.py`. This module can be imported by the main app and page modules without introducing a circular import through `CashSave/CashSave.py`.
- Keep `page_layout(route, *content)` as a compatibility wrapper in the main app, but delegate its presentation to `app_layout`.
- Use the same menu definition for dashboard, Jarvis, Finanças, and Calendário. Mark the active link through its existing route argument; on narrow screens keep icon navigation visible while reducing its width.
- Use responsive sizing through Reflex breakpoints for sidebar width and content padding. Keep page-specific cards and interaction logic local to their owning pages.
- Use green for primary navigation accents, red for pending outflows, and amber only for alerts; avoid decorative orange accents that do not match the app palette.

## Risks / Trade-offs

- [Risk] Responsive prop combinations may differ across Reflex versions → Compile the app after introducing the shared component and fix any unsupported styling props before migrating more pages.
- [Risk] A narrow icon-only menu can be less discoverable → Keep accessible labels and link titles while hiding only visible text at the narrow breakpoint.

## Migration Plan

1. Add the shared shell, then migrate the dashboard, Jarvis, Finanças, and Calendário wrappers.
2. Compile and run existing tests; inspect the authenticated routes at desktop and narrow widths.
3. Roll back by restoring the previous route wrappers if the shared shell causes a rendering regression; page state and backend contracts remain untouched.