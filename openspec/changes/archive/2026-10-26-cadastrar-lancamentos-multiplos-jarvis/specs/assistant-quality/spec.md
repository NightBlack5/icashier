## ADDED Requirements

### Requirement: Confirm only financial operations accepted by Xano

O Jarvis SHALL derive success confirmations from a transaction response that
contains an ID. If Xano rejects a transaction or does not confirm it, the Jarvis
SHALL report the failed item and SHALL NOT claim it was registered. For a batch,
it SHALL report confirmed items separately from failed items.

#### Scenario: Confirmed transaction

- **WHEN** Xano returns an ID for a submitted transaction
- **THEN** the Jarvis may include that transaction in the local state and
  describe it as registered

#### Scenario: Rejected transaction

- **WHEN** Xano rejects a submitted transaction or returns no transaction ID
- **THEN** the Jarvis SHALL report that the transaction was not confirmed and
  SHALL NOT add it to local state

#### Scenario: Partially confirmed batch

- **WHEN** Xano confirms some transactions but rejects a later transaction
- **THEN** the Jarvis SHALL retain only confirmed transactions locally, identify
  the failed item, and SHALL NOT report the full batch totals as final