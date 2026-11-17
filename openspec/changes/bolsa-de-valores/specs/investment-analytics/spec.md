# Spec Delta

## Purpose

Defines portfolio analysis and user-specific investment research tools that clearly distinguish observed values, calculations, and unavailable monitoring.

## ADDED Requirements

### Requirement: Portfolio analysis separates value categories
The portfolio view SHALL distinguish contributed cost basis, current market value, realized and unrealized results, returns, allocation, and received proventos.

#### Scenario: Viewing the portfolio dashboard
- **WHEN** a user opens their portfolio
- **THEN** available totals and allocation are shown with their calculation period and missing market values are identified

#### Scenario: Calculating portfolio return
- **WHEN** verified market values are available for all current positions
- **THEN** simple return is calculated as realized plus unrealized result divided by total purchase outlay, including purchase costs; proventos are shown separately

#### Scenario: Reviewing portfolio evolution
- **WHEN** the user selects an evolution period
- **THEN** the chart distinguishes contributions, withdrawals, market changes, and received proventos when those values can be calculated from stored data

### Requirement: Favorites are private to each user
The system SHALL allow an authenticated user to add or remove assets from a persisted favorites list, and SHALL display only provider-backed market data for those assets.

#### Scenario: Managing favorites
- **WHEN** a user adds or removes an asset
- **THEN** the change is saved for that user and does not change another user's favorites

### Requirement: Asset comparisons use equivalent data
The system SHALL compare at least two selected assets over equivalent available periods and SHALL omit indicators that are unavailable or incompatible across asset categories.

#### Scenario: Comparing assets across categories
- **WHEN** a user compares assets of different categories
- **THEN** the system compares supported normalized price performance and does not present incompatible category-specific indicators as equivalent

#### Scenario: A comparison period is incomplete
- **WHEN** one selected asset lacks verified observations for the full selected period
- **THEN** the missing range is identified and no unsupported performance value is inferred

#### Scenario: Comparing different asset categories
- **WHEN** the selected assets have different categories
- **THEN** only normalized price performance is compared, and category-specific indicators are omitted

### Requirement: Alert definitions are honest about monitoring
The system SHALL allow users to save price and percentage alert conditions for their own assets, but SHALL claim active monitoring or deliver an alert only when a configured evaluation process has actually checked a verified quote.

#### Scenario: No alert evaluator is configured
- **WHEN** a user saves an alert and no background evaluator is available
- **THEN** the alert is clearly marked as not monitored and no notification is fabricated

#### Scenario: Saving an alert condition
- **WHEN** a user saves a price or daily-percentage threshold
- **THEN** the condition is persisted for that user and remains explicitly not monitored until an evaluator checks verified market data

#### Scenario: An evaluator checks a quote
- **WHEN** a configured evaluator compares a verified quote with an active user's condition
- **THEN** the system records and presents the alert result with the quote source and evaluation time

### Requirement: Investor profile informs educational context only
Investment education SHALL use the available investor-profile answers as contextual information, disclose when that information is incomplete, and SHALL NOT claim guaranteed suitability or personalized buy/sell advice.

#### Scenario: Profile information is incomplete
- **WHEN** investment content is presented without a completed profile
- **THEN** the content remains general and the system does not infer a risk profile from missing answers

#### Scenario: Profile is available
- **WHEN** educational content references the user's profile
- **THEN** it explains the profile context and relevant risks without treating it as a recommendation or guarantee
