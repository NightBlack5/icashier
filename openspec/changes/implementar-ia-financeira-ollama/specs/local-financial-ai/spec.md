# Local financial AI

## ADDED Requirements

### Requirement: Backend-only Ollama access
The assistant SHALL call Ollama from the backend using configurable local
connection settings, bounded timeouts, input/output limits, and explicit errors.

#### Scenario: Ollama is unavailable
- **WHEN** the local Ollama service cannot be reached or times out
- **THEN** the assistant shows an explicit unavailable message and does not
  fabricate a financial answer

### Requirement: Authorized minimal financial context
The assistant SHALL use only the authenticated user's already-loaded financial
state and SHALL never expose tokens or send direct browser requests to Ollama.

#### Scenario: User has no authenticated session
- **WHEN** an unauthenticated user submits a financial question
- **THEN** the request is rejected locally and no Ollama call is made

### Requirement: Deterministic financial calculations
The assistant SHALL calculate monetary totals, comparisons, budget deviations,
goal progress, and projections outside the language model using integer cents or
equivalent exact arithmetic.

#### Scenario: Insufficient history for projection
- **WHEN** the available transaction history cannot support a meaningful
  projection
- **THEN** the result states the insufficiency and does not present false
  precision

### Requirement: Validated read-only responses
The assistant SHALL validate the Ollama response envelope, bound conversation
history and response size, and never execute model-generated SQL, code, or
financial writes.

#### Scenario: Ollama returns invalid JSON
- **WHEN** the model response cannot be validated against the expected envelope
- **THEN** the assistant reports an invalid response error and does not append it
  as a successful financial answer

### Requirement: Local assistant UI
The existing assistant page SHALL provide loading state, errors, conversation
history, suggested questions, and responses from the local service without
breaking existing navigation.

#### Scenario: Ask a question with mocked local service
- **WHEN** an authenticated state submits a valid question and the client is
  mocked to return a valid response
- **THEN** the UI state contains the user question and validated assistant answer
