# Spec Delta

## ADDED Requirements

### Requirement: Ground investment answers in verified user context
Jarvis SHALL answer investment questions using verified market data and calculations from the authenticated user's portfolio, distinguishing facts, calculations, estimates, and unavailable information.

#### Scenario: Asking about the user's portfolio
- **WHEN** an authenticated user asks about their portfolio
- **THEN** Jarvis uses only that user's calculated investment records and does not invent holdings, results, or proventos

#### Scenario: Asking about a market quote without verified data
- **WHEN** the current market quote is missing, stale, or unavailable
- **THEN** Jarvis identifies that limitation and does not state an unsupported quote or performance value as fact

#### Scenario: Asking from an asset detail page
- **WHEN** the user asks a question while viewing an asset
- **THEN** Jarvis receives that asset's verified page context, including its source and reference time when available

#### Scenario: Investment records include another owner
- **WHEN** a returned investment record identifies a different authenticated owner
- **THEN** Jarvis rejects the context and does not receive that record

### Requirement: Keep investment guidance educational
Investment responses SHALL explain concepts and risks without promising returns or presenting personalized buy or sell instructions as guaranteed or professionally suitable advice.

#### Scenario: Asking whether to buy or sell an asset
- **WHEN** a user asks Jarvis for a personalized buy or sell decision
- **THEN** Jarvis provides educational information and relevant risks without asserting a guaranteed or personalized recommendation

#### Scenario: Investor profile is absent or local-only
- **WHEN** the investor profile is missing or stored only in browser storage
- **THEN** it is not used as permission or suitability proof, and answers remain general with relevant risks

### Requirement: Preserve the existing Jarvis conversation
Investment context SHALL extend the existing Jarvis experience and conversation history without creating a separate assistant identity or independent conversation store.

#### Scenario: Asking an investment question in an existing conversation
- **WHEN** a user asks an investment question in Jarvis
- **THEN** the existing conversation flow and history are used with the additional investment context
