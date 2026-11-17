# Proposal

## Why

The editor currently reports a large number of diagnostics, but the live count differs from the earlier screenshot (230 now versus 278). Current checks identify a malformed Xano query condition that causes cascading errors, alongside Pylance unused-symbol warnings.

## What Changes

- Fix reproducible root causes behind current project diagnostics, starting with the Xano PATCH query syntax.
- Remove genuine unused Python symbols while preserving import side effects and required test callback signatures.
- Re-run the same editor diagnostics and focused project checks; do not suppress rules or treat cascading messages as independent defects.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. This is an implementation-only maintenance change with no intended user-visible behavior or API contract changes; `.openspec.yaml` sets `skip_specs: true`.

## Impact

- Xano investment operation PATCH schema and its focused schema checks.
- Python modules and tests currently reporting Pylance warnings.
- No dependency, data-model, API behavior, or remote Xano workspace changes are intended.
