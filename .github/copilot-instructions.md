# OpenSpec workflow

When handling a request that changes application code, configuration, dependencies, tests, or data structures in this repository, keep the OpenSpec documentation in sync automatically. The user does not need to invoke an `/opsx-*` command.

Before editing:

1. Read `openspec/config.yaml`, inspect the relevant main specs, and run `openspec list` to find active changes.
2. Reuse an active change only when it clearly covers the request. Otherwise create a change with a concise kebab-case name.
3. Following the configured schema, write or update the proposal, relevant delta specs, design, and tasks before implementing. Do not invent requirements unrelated to the requested work.
4. If the scope or expected behavior is materially ambiguous, ask the user before committing to a specification.

During and after implementation:

1. Keep the change's tasks aligned with the actual implementation. Mark a task complete only after doing the work and its relevant verification.
2. Run `openspec validate <change-name>` and the smallest relevant tests or checks. Report any verification that could not be completed; do not claim it passed.
3. Keep the change available for review. Archive it only when the user asks to finalize it or the established workflow for the request calls for archiving.

Apply these instructions to work performed by Copilot in this repository. They do not monitor or automatically document edits made manually in the editor or by external tools.
