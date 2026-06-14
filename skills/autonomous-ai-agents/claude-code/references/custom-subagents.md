## Custom Subagents

Define specialized agents in `.claude/agents/` (project), `~/.claude/agents/` (personal), or via `--agents` CLI flag (session):

### Agent Location Priority
1. `.claude/agents/` — project-level, team-shared
2. `--agents` CLI flag — session-specific, dynamic
3. `~/.claude/agents/` — user-level, personal

### Creating an Agent
```markdown