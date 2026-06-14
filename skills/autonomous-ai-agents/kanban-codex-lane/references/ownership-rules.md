## Ownership Rules

1. Hermes owns the Kanban lifecycle. Codex must never call `kanban_complete`, `kanban_block`, `kanban_create`, gateway messaging, or any Hermes board CLI as a substitute for the worker.
2. Hermes owns final acceptance. Treat Codex commits/diffs as untrusted patches until reviewed and verified.
3. Hermes owns test execution. Codex may run tests, but those runs are advisory; repeat required verification from Hermes with the repo's canonical wrapper.
4. Hermes owns safety. If Codex changes safety boundaries, risk gates, live trading behavior, or secrets handling, reject the lane even if tests pass.
5. Hermes owns cleanup. Kill stuck Codex processes and remove temporary worktrees when they are no longer needed.