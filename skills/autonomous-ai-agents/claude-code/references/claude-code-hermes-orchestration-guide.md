# Claude Code — Hermes Orchestration Guide

Delegate coding tasks to [Claude Code](https://code.claude.com/docs/en/cli-reference) (Anthropic's autonomous coding agent CLI) via the Hermes terminal. Claude Code v2.x can read files, write code, run shell commands, spawn subagents, and manage git workflows autonomously.

## Important

This guide is a navigation index. For Windows-specific orchestration details (VS Code bridge, VT stack, clipboard injection, focus management), load the dedicated reference:

```
skill_view(name="claude-code", file_path="references/windows-orchestration-bridge.md")
```

## Two Modes

| Mode | When to Use | Key File |
|------|-------------|----------|
| **VS Code GUI Bridge** | User wants to see changes in VS Code, or `claude` CLI unavailable | `references/windows-orchestration-bridge.md` |
| **CLI Print Mode** | Fully autonomous, no approval needed, terminal-only | `claude-code-cli-autonomous` skill |

## Orchestration Pattern

```
🧠 Hermes (analysis + strategy)
   → 1. Scan code, find issue, determine fix strategy
   → 2. Prepare structured task prompt (files + what to fix)
   → 3. Send to Claude Code (via VS Code bridge or CLI pipe)
🛠️ Claude Code (implements fix + runs tests)
🔍 Hermes (verify result + save as skill/memory)
```