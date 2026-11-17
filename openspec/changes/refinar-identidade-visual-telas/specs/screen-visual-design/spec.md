## ADDED Requirements

### Requirement: Consistent premium visual design
The application SHALL use a consistent dark emerald visual language across public and authenticated screens, with readable contrast, clear hierarchy, and visually coherent surfaces and controls.

#### Scenario: User moves between screens
- **WHEN** a user navigates between public, authentication, and authenticated screens
- **THEN** colors, typography, surfaces, focus states, and interactive feedback remain visually consistent.

### Requirement: Responsive and accessible visual presentation
The visual design SHALL adapt to narrow viewports and respect reduced-motion preferences without obscuring content or controls.

#### Scenario: User views a screen on a narrow device
- **WHEN** the viewport becomes narrow or the user requests reduced motion
- **THEN** content and controls remain legible and usable without unnecessary animation.

### Requirement: Preserve existing application behavior
Visual changes SHALL preserve routes, data, and existing user actions.

#### Scenario: User activates an existing control
- **WHEN** the user uses a navigation item, form, or page action after the visual refresh
- **THEN** it continues to invoke the same route or application behavior.
