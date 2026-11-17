# Design

## Context

See `proposal.md` for the motivation and capability boundaries. The application is a Reflex app with authenticated route handlers and shared state in `CashSave/state.py`. It sends bearer-authenticated requests to Xano, whose existing financial endpoints filter records by `$auth.id`. The UI already uses `rx.recharts` for an area chart; `requirements.txt` contains no separate market-data or chart provider. The investor-profile answers currently live in Reflex `LocalStorage`, and Jarvis uses `FinancialContextService` / `FinancialOrchestrator` alongside the existing conversation API.

## Goals / Non-Goals

**Goals:**
- Keep the feature within Reflex and Xano and reuse their current authenticated request, navigation, and state patterns.
- Keep provider-specific payloads and credentials behind a server-side adapter and a normalized market-data contract.
- Make portfolio calculations deterministic, testable, and reproducible from the user's operations.
- Preserve existing financial accounts, cash transactions, and Jarvis conversations without implicitly combining their balances or creating a second assistant.

**Non-Goals:**
- Claim exchange real-time data, acquire a provider subscription on the user's behalf, or execute brokerage orders.
- Add a scheduler or claim that alerts are monitored when no evaluator is deployed.
- Persist or trust browser profile answers as authorization data, execute brokerage orders, or calculate tax obligations.

## Decisions

### Keep the current application and chart stack

Add authenticated investment routes and menu entries through the shared Reflex layout. Keep event handlers in the current `AppState` integration and put pure calculations and provider normalization in focused modules. Use the existing Recharts components for time-series and allocation views rather than adding a chart dependency. This follows the installed stack and avoids a second frontend runtime.

### Prioritize the market overview

Put the delayed-data status, daily market-movers chart, and gainers/losers lists before search, favorites, portfolio, alerts, and operation forms. Build the rankings only from active B3 stocks with positive trading volume and provider-reported daily change; show their last observed prices, percentage changes, source, and reference time. Keep the existing per-asset historical chart for searched assets. When the provider or data is unavailable, show an empty state instead of example values.

### Separate market data from user-owned records

Define a provider-neutral server-side interface for search, quote, history, and ranked market movers. Normalize each result with symbol, category where applicable, source, reference timestamp, freshness classification, and available fields. Use the `brapi.dev` adapter for supported B3 stocks, FIIs, and ETFs. Resolve `CASHSAVE_BRAPI_TOKEN` from server environment configuration only; never render it into Reflex state or frontend code. Read the environment before creating the provider service. Cache observations for at most 300 seconds, keyed by provider/request, and retain the original source and timestamp on stale results. An absent token or failed request yields an explicit unavailable state; do not silently fall back to another plan or provider.

The market overview requests both provider-sorted directions, excludes inactive stocks and observations without positive volume, and verifies selected prices, percentage changes, and quote timestamps before building up to five gainers and five losers. The chart plots only positive verified daily changes. Provider failures remain independent from Xano portfolio failures so the market overview can still render when portfolio routes are unavailable.

The current normalized quote contract supports symbol, asset category, BRL price, optional daily percentage change, source, reference timestamp, freshness, and stale status. Search results support symbol, name, category, source, and stale status; history supports timestamped prices and provenance. No category-specific fundamentals are currently verified or rendered, so those metrics remain explicitly unavailable until a provider supplies them under approved terms.

User-owned operations, received proventos, favorites, and alert definitions belong in separate Xano tables and authenticated endpoints. Endpoints derive ownership from `$auth.id`, validate related records and inputs on the server, and never trust a client-supplied owner or calculated total. Market observations are not copied into durable portfolio records unless the selected provider's terms permit it.

#### Provider selection

Research checked on 2026-11-16 found that `brapi.dev` documents B3 stocks, FIIs, ETFs, and historical data. Its [pricing page](https://brapi.dev/pricing) lists the Pro plan with a five-minute update cadence and commercial use on paid plans; the user selected Pro as the integration target. The [API documentation](https://brapi.dev/docs) and [historical-data documentation](https://brapi.dev/docs/acoes/historico) describe the supported market-data endpoints.

The published five-minute cadence describes provider updates; it does not establish exchange real-time access. Deployment must supply a token associated with the selected Pro tier and remain subject to the applicable provider and exchange terms. No subscription has been purchased and no token has been supplied as part of this change. Until a valid token is configured, market data remains unavailable.

All brapi.dev observations are classified as delayed, with source and provider reference time shown wherever the UI presents market data. The interface must not label them real-time. A 300-second cache aligns requests with the selected plan's published cadence and must not extend or obscure the provider's source timestamp.

### Recompute portfolio state from operations

Use Python `Decimal` for quantity and unit-price arithmetic, keep unit prices and costs in integer centavos, and round monetary outputs half-up to integer centavos at the currency boundary. The portfolio service replays operations by date and operation ID using weighted-average cost: purchase costs increase basis; sale costs reduce net proceeds; a sale realizes the difference against the average basis immediately before the sale. Reject a sale that makes the position negative. Recompute the affected asset's history after edits or deletions and reject any mutation that invalidates a later operation. Xano mutation endpoints enforce ownership and the same validity constraint before committing; the UI never supplies authoritative totals. The target Xano workspace must run the history check and mutation with its confirmed transaction/serialization guarantee.

Use the observed market quote only to calculate market value and unrealized result. With no verified quote, retain cost basis and mark market value, unrealized result, and allocation portions that depend on it as unavailable. Keep all holdings and proventos separate from cash accounts unless the user records a distinct transfer.

Show proventos with their announced/paid status and dates. Only paid records with a payment date contribute to all-time, current-year, and current-month received totals; eligible quantity is optional and entered amounts remain in centavos.

Portfolio simple return is `(realized result + unrealized result) / total purchase outlay`, with purchase costs included in outlay and proventos reported separately. It is unavailable when any open position lacks a verified market quote; historical market change is likewise unavailable without verified historical observations.

Asset comparisons normalize verified prices to a base of 100 and expose no category-specific metrics. A comparison is calculated only when all selected series contain the same observed dates; otherwise the missing dates are listed and performance is omitted.

### Reuse existing Jarvis and profile context

Extend the existing financial context builder and answer flow with the authenticated user's investment operations, verified quote metadata, and the currently viewed asset. Continue using the same Jarvis identity, model integration, and conversation history. Do not fetch portfolio data for a different user or let the model create unsupported totals; deterministic calculations supply financial values. The existing investor profile is browser-local, so it may inform educational wording in the active session but never access control or a suitability guarantee.

Investment context is fetched through the current authenticated Xano session and owner-checked when owner IDs are present. It contains deterministic portfolio totals, paid proventos, and current-asset provenance only; absent quotes remain unavailable. Local profile context contributes only its educational label and risk caveat, never authorization or a buy/sell decision.

### Keep alerts explicit until an evaluator exists

Persist alert conditions and their monitoring state. The repository currently has no identified background evaluator; therefore, saved conditions remain visibly unmonitored and generate no notifications until a real scheduled evaluator is configured. Do not poll a provider on every render or turn an ordinary user request into a claim of continuous monitoring.

### Stage integration additively

Add Xano schema and endpoints without changing existing cash transaction semantics. Implement in the requested sequence: market-data foundation and dashboard; asset search and detail; operation and provento persistence/calculation; portfolio analysis and user tools; then Jarvis context, responsive hardening, tests, and documentation. A provider with no verified commercial display rights or credentials remains disabled while the rest of the module presents honest empty states.

## Risks / Trade-offs

- [The configured token does not have the selected tier or permitted use] → Require a valid Pro account and applicable usage rights; surface provider errors and do not claim the five-minute cadence for an unverified configuration.
- [Provider rate limits or stale responses distort displayed values] → Cache only within the provider's terms, retain timestamps, label stale data, and surface request failures.
- [A sale, edit, or deletion invalidates later operations] → Revalidate the entire affected chronological history server-side before committing and cover the cases with deterministic tests.
- [Concurrent operations race while checking available quantity] → Perform validation and mutation in one backend transaction or reject the operation if Xano cannot guarantee that consistency.
- [A portfolio total is mistaken for cash or profit] → Label cost basis, market value, realized result, unrealized result, and proventos separately; never add holdings to bank cash implicitly.
- [Jarvis receives missing or unverified market context] → Pass explicit source, timestamp, and availability metadata and require the answer path to disclose missing data.
- [No alert worker is available] → Save configuration without claiming active monitoring and document the future evaluator boundary.
- [The existing profile is browser-local] → Use it only as optional educational context in the current session; do not imply cross-device profile persistence.

## Migration Plan

1. Add investment-specific Xano tables and authenticated endpoints with owner checks; leave current financial tables and routes unchanged.
2. Deploy the Reflex code with investment navigation, empty/unavailable provider states, and no credentials required for startup.
3. Configure `CASHSAVE_BRAPI_TOKEN` locally from an account with the selected Pro tier and applicable usage rights; do not commit or expose the token.
4. Verify a user's portfolio and Jarvis context against isolated test accounts before enabling the live investment route broadly.
5. Roll back by hiding the new routes/navigation and disabling the provider adapter; retain user investment records unless a separately approved data migration requires otherwise. Existing cash records and Jarvis histories remain untouched.
