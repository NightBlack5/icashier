# Assistant submit

## ADDED Requirements

### Requirement: Submit assistant messages with Enter
The assistant message composer SHALL submit the current message when the user
presses Enter in the input, while preserving the visible send button.

#### Scenario: Send with Enter
- **WHEN** the user types a non-empty question and presses Enter
- **THEN** the current assistant send event is triggered once

#### Scenario: Send with the button
- **WHEN** the user clicks the send button
- **THEN** the same assistant send event is triggered
