# Spec Delta

## Purpose

Defines reliable market-data behavior for browsing Brazilian assets while making source, timestamp, delay, and data availability visible to users.

## ADDED Requirements

### Requirement: Market values have verified provenance
Every displayed market value SHALL come from a configured data source and include its source and reference timestamp. The interface SHALL identify whether the value is real-time, delayed, or historical when that information is available.

#### Scenario: Displaying a provider quote
- **WHEN** a configured provider returns a quote
- **THEN** the quote is shown with its source, reference time, and known freshness classification

#### Scenario: No configured market-data provider
- **WHEN** no provider is configured or a quote cannot be verified
- **THEN** the interface states that the data is unavailable and does not display a fabricated or hard-coded quote

### Requirement: Delayed market data is not presented as real-time
The system SHALL disclose the known update cadence of delayed market data and SHALL NOT identify delayed observations as real-time.

#### Scenario: Displaying a brapi Pro observation
- **WHEN** the configured brapi.dev Pro provider returns a quote or historical observations
- **THEN** the interface identifies brapi.dev as the source, shows the provider reference time, and discloses the published five-minute update cadence as delayed data

### Requirement: Market movers use verified daily changes
The system SHALL show up to five provider-ranked daily gainers and losers from active B3 stocks with positive trading volume, including observed price, percentage change, source, and reference time. Gainers have positive daily changes and losers have negative daily changes. The chart SHALL plot only verified positive changes.

#### Scenario: Provider returns market movers
- **WHEN** the configured provider returns active stocks with positive trading volume and daily change
- **THEN** the dashboard shows up to five largest positive changes and five most negative changes in separately ordered lists, charts only positive changes, and labels the data with source and reference time

#### Scenario: Market movers are unavailable
- **WHEN** the provider is not configured or returns no eligible daily changes
- **THEN** the dashboard shows an explicit unavailable or empty state and no fabricated rankings or chart values

### Requirement: Users can search supported assets
The system SHALL let users search supported Brazilian equities, FIIs, and ETFs by ticker or name, and filter results by asset category.

#### Scenario: Searching by ticker or name
- **WHEN** the user enters a ticker or company/fund name
- **THEN** matching assets returned by the configured source are shown with their category

#### Scenario: Filtering by category
- **WHEN** the user selects an asset category
- **THEN** results contain only matching assets supported by the configured source

### Requirement: Asset details disclose missing information
An asset detail view SHALL show only provider-backed quote, trading, historical, and category-specific indicator values, together with their source and reference date. Missing values SHALL be identified as unavailable rather than inferred.

#### Scenario: Provider lacks an indicator
- **WHEN** an asset has no verified value for a requested indicator
- **THEN** that indicator is omitted or explicitly marked unavailable with its missing reference information

### Requirement: Historical charts reflect available periods
The system SHALL let users select supported historical periods and SHALL plot only verified observations returned for that period.

#### Scenario: Requested period has observations
- **WHEN** the selected asset and period have historical observations
- **THEN** the chart shows those observations and identifies the period and data source

#### Scenario: Requested period has no observations
- **WHEN** the source cannot provide observations for the selected period
- **THEN** the chart displays an explicit unavailable or empty state without extrapolating prices

### Requirement: Market-data failures are explicit
Provider errors, rate limits, and stale cached observations SHALL not be represented as successful fresh quotes.

#### Scenario: Provider request fails
- **WHEN** a market-data request fails or is rate-limited
- **THEN** the user receives an explicit unavailable or stale-data state and the last verified timestamp when cached data is shown

#### Scenario: Configured plan does not include a requested feature
- **WHEN** the provider rejects a request because the configured account plan lacks the required feature
- **THEN** the interface explains that the feature is unavailable on the current plan and shows no unverified or fabricated market data
