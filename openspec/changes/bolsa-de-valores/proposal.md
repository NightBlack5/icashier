# Proposal

## Why

CashSave currently organizes personal cash flow but does not provide a trustworthy way to research investments or track a user's investment positions. A provider-backed, user-owned investment area would extend the product while keeping market facts, portfolio calculations, and educational guidance clearly separated.

## What Changes

- Add a responsive Bolsa de Valores dashboard that prioritizes a market chart and provider-ranked daily gainers/losers, followed by asset search and details; show source, reference time, and explicit freshness or unavailability states.
- Introduce a server-side, provider-independent market-data boundary with a `brapi.dev` adapter for B3 assets. The selected Pro plan has a published five-minute update cadence; market observations must be identified as delayed, never real-time. Calls require a server-side `CASHSAVE_BRAPI_TOKEN` from an account whose plan and terms authorize CashSave's use. Without it, show explicit unavailability and never substitute invented or hard-coded quotes.
- Persist user-owned investment operations and received proventos through authenticated Xano APIs. Calculate positions, cost basis, realized and unrealized results, returns, and portfolio allocation from validated operations without mixing market value with profit or bank cash.
- Add portfolio analysis, evolution, favorites, asset comparisons, and configurable alerts, respecting available data and the absence of background processing.
- Extend the existing Jarvis with investment and current-page context, using authenticated data and existing conversation infrastructure. Keep responses educational and distinguish observed data, calculations, estimates, and missing information.
- Reuse the investor-profile experience already in progress, without treating a category or profile as a guaranteed suitability decision.
- Keep order execution, custody, brokerage connections, guaranteed returns, and personalized buy/sell recommendations out of scope.

## Capabilities

### New Capabilities

- `investment-market-data`: Provider-neutral market data, asset discovery and details, provenance, freshness, caching, and unavailable-data behavior.
- `investment-portfolio`: Authenticated investment operations and received proventos, ownership isolation, financial validation, and portfolio calculations.
- `investment-analytics`: Portfolio views, evolution, favorites, comparisons, alerts, and investor-profile-aware educational context.

### Modified Capabilities

- `jarvis`: Extend the existing assistant's behavior to answer investment questions using verified market data and the authenticated user's investment context.

## Impact

- Reflex: add authenticated routes and navigation, investment views, state and calculation/service modules; reuse the current `AppState`, layout, and Recharts components.
- Xano: add user-owned investment tables and authenticated endpoints for operations, proventos, favorites, and any supported alert configuration.
- Market data: add a server-side `brapi.dev` adapter and environment-based configuration. The provider token must never reach the browser; the module must show an explicit unavailable state until a valid token is configured.
- Jarvis: extend the existing context/orchestration flow and conversation endpoint; do not create a second assistant or expose data across users.
- Testing: add focused calculation, API ownership, validation, provider failure, unavailable-data, and assistant-context tests. No purchase or sale order execution is introduced.
