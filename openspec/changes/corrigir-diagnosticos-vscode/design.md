# Design

## Context

See `proposal.md` for the motivation. The current workspace scan reports 230 diagnostics, not the 278 shown in the earlier screenshot. The first actionable Xano error is at the `where` condition in `xano/api/cashsave/investimentos/operacoes/operacao_id_PATCH.xs`; subsequent unknown-variable errors appear to cascade from it. Pylance separately reports unused imports, local variables, and test callback parameters.

## Goals / Non-Goals

**Goals:**
- Resolve actual root causes and remeasure the complete diagnostics set after each root fix.
- Preserve route registration, test behavior, and the existing diagnostic rules.
- Add or adjust focused checks only where they protect the corrected behavior.

**Non-Goals:**
- Change financial, authentication, or other application behavior.
- Publish schemas to Xano, change remote data, or resolve issues not represented by current project diagnostics.
- Suppress diagnostics globally or perform unrelated refactoring.

## Decisions

- Fix parser errors before acting on dependent diagnostics. Re-run the workspace Problems scan after the Xano syntax correction so cascades can be distinguished from independent findings.
- Use the exact reported source and rule for remaining diagnostics. Remove genuinely unused symbols; preserve imports required for module side effects and preserve callable signatures where tests implement provider protocols.
- Validate the result with the same Problems scan, Pylance workspace diagnostics, the focused Xano schema tests, and existing project checks relevant to changed files.
- Prefer source corrections over configuration suppressions. Suppression would conceal future regressions and is not equivalent to resolving the reported issue.

## Risks / Trade-offs

- [The initial count differs from the screenshot and cascaded messages may disappear after the root fix] → Use the current complete diagnostics scan as the baseline, record remaining independent findings, and do not claim the screenshot count itself was reproduced.
- [An apparently unused import may trigger route registration] → Verify import paths and route tests before removing or rewriting such an import.

## Migration Plan

No deployment or data migration is planned. Apply source changes locally, run focused validation, then run the broader applicable tests and compile checks. Roll back only the specific source edits if validation exposes a regression; do not revert unrelated worktree changes.
