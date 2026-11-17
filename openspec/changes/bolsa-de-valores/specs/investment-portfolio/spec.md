# Spec Delta

## Purpose

Defines secure, user-owned investment operations and received proventos, with reproducible portfolio calculations that remain distinct from bank balances.

## ADDED Requirements

### Requirement: Investment records belong to the authenticated user
Every investment operation, portfolio record, and provento SHALL be accessed only through authenticated requests and restricted on the server to the owner identified by the session.

#### Scenario: User reads their portfolio
- **WHEN** an authenticated user requests investment records
- **THEN** only records owned by that session's user are returned

#### Scenario: User attempts to access another portfolio
- **WHEN** a request references an operation or record owned by a different user
- **THEN** the server denies the request without revealing the other user's financial data

### Requirement: Users can record investment operations
The system SHALL persist buy and sell operations with asset, operation type, date, positive quantity, unit price, and applicable costs, and SHALL validate all values before saving.

#### Scenario: Recording a valid purchase
- **WHEN** a user submits a purchase with valid asset, date, quantity, price, and costs
- **THEN** the operation is saved under that user's ownership

#### Scenario: Selling more units than available
- **WHEN** a user submits a sale exceeding the available quantity at that point in the operation history
- **THEN** the operation is rejected and the persisted portfolio remains unchanged

### Requirement: Portfolio calculations use weighted average cost
The system SHALL calculate quantity, weighted-average acquisition cost, invested cost basis, market value, realized result, unrealized result, return, and allocation from valid operations and verified market data.

#### Scenario: Recording a sale
- **WHEN** a sale is calculated
- **THEN** realized result uses the weighted-average cost basis immediately before the sale and sale costs, while the remaining position retains that average cost

#### Scenario: Current quote is unavailable
- **WHEN** an asset has no verified current market quote
- **THEN** cost basis remains available but current market value and unrealized result are marked unavailable rather than replaced by cost basis

#### Scenario: Viewing portfolio performance
- **WHEN** the portfolio summary is shown
- **THEN** realized and unrealized results are displayed separately and market value is not labeled as profit

### Requirement: Operation changes preserve portfolio consistency
Users SHALL be able to edit or delete their own operations only when the resulting chronological operation history remains valid.

#### Scenario: Editing an operation
- **WHEN** an edit would make a later sale exceed the available quantity
- **THEN** the edit is rejected and the original operation and calculations remain unchanged

### Requirement: Received proventos are distinct from announcements
The system SHALL record received dividends, JCP, FII distributions, and other proventos separately from announced but unpaid amounts.

#### Scenario: Recording a received payment
- **WHEN** a user registers a provento as paid
- **THEN** the saved record includes the related asset, amount, eligible quantity when known, and payment date

#### Scenario: Viewing received-provento totals
- **WHEN** a user views the provento history
- **THEN** totals are available for all time, the current year, and the current month based on payment date

#### Scenario: Provento is announced but unpaid
- **WHEN** a distribution has been announced but its payment has not occurred
- **THEN** it is not included in received-provento totals

#### Scenario: Paid provento has no payment date
- **WHEN** a user submits a provento as paid without a valid payment date
- **THEN** the record is rejected

### Requirement: Investment values do not become bank cash automatically
Investment holdings, sale proceeds, and proventos SHALL remain separate from available bank-account balances unless an explicit, non-duplicating transfer is recorded.

#### Scenario: Investment position appears in consolidated wealth
- **WHEN** consolidated wealth includes an investment position
- **THEN** the position is identified as invested assets and is not added to available account cash
