# Tasks

## 1. Resolve Current Root Causes

- [x] 1.1 Correct the malformed condition in the investment operation PATCH schema and verify the Xano diagnostic cascade is reduced with the workspace Problems scan and `tests/test_xano_schema.py`.
- [x] 1.2 Resolve the current Pylance unused-symbol warnings without breaking route imports or test callback contracts; verify with Pylance workspace diagnostics and the affected tests.

## 2. Verify the Workspace

- [x] 2.1 Re-run the complete Problems scan and Pylance workspace diagnostics, fix any remaining independent project-source findings, and verify no actionable diagnostics remain without suppressing rules.
- [x] 2.2 Run the relevant unit tests, `reflex compile --dry`, and `openspec validate corrigir-diagnosticos-vscode`; confirm all pass and no unrelated worktree changes were altered.
