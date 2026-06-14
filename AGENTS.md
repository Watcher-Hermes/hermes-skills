# Hermes Skills — Agent Instructions

## Repository Overview

This repository contains all skills for **Hermes Agent** (Nous Research). Skills are reusable procedural knowledge — task-specific workflows, tools configurations, environment setups, and reference guides that the agent loads on demand.

**Total skills:** 1.184
**License:** Apache 2.0
**Agent:** [Hermes Agent](https://get-hermes.ai/) (>=0.8.0)

## Repository Structure

```
hermes-skills/
├── skills/                 # All 1,184 skills organized under here
│   ├── ecc/                    # ECC skills — AI/ML workflows, dev patterns (262)
│   ├── windows-automation/     # Windows automation scripts (42)
│   ├── windows-shortcuts/      # Windows shortcut references (149)
│   ├── software-development/   # Full-stack dev scaffolds, testing (34)
│   ├── devops/                 # Backup, cron, monitoring (13)
│   ├── creative/               # ASCII art, design, video (22)
│   ├── media/                  # YouTube, GIF, music (8)
│   ├── note-taking/            # Obsidian, Notion (12)
│   ├── github/                 # PR, issues, auth (6)
│   ├── mlops/                  # Model training, inference (24)
│   ├── autonomous-ai-agents/   # Multi-agent, Claude Code (23)
│   ├── data-science/           # Jupyter, HF Hub (3)
│   ├── research/               # ArXiv, papers (8)
│   ├── security/               # Pentest, encryption (10)
│   ├── productivity/           # Email, camera, PDF (26)
│   ├── gaming/                 # Game trainers, emulators (6)
│   ├── android/                # APK modding (1)
│   ├── apple/                  # iOS/macOS (5)
│   ├── user-preferences/       # Persona, startup config (17)
│   ├── hermes-agent/           # Hermes config (1)
│   ├── mcp/                    # MCP client (1)
│   ├── self-improvement/       # Nightly auto-improvement (1)
│   ├── hermes-mouse-klavye/    # Mouse/keyboard automation (1)
│   ├── mouse-klavye-ctypes/    # Ctypes mouse lib (1)
│   └── AmbientEar/, Hermes\ Memor/, LiveTranscriber/  # Audio tools
├── AGENTS.md              # This file
├── README.md
└── manifest.json
```

## Skill Format

Every skill is a directory with a `SKILL.md` file. Each `SKILL.md` has YAML frontmatter:

```yaml
---
name: example-skill
title: "Example Skill"
description: "What this skill does"
audience: user          # user | contributor | maintainer
tags: [tag1, tag2]
related_skills: [other-skill]
triggers: [trigger-word]
category: mlops         # optional
---
```

### Audience Classification

| Audience | Count | Purpose |
|----------|-------|---------|
| **user** | 848 | Daily use — AI/ML tools, automation, media, creative, gaming |
| **contributor** | 287 | Code development — patterns, frameworks, testing, scaffold |
| **maintainer** | 49 | System maintenance — devops, audit, cron, backup, cleanup |

Source: NVIDIA/NemoClaw AGENTS.md skill organization pattern.

## Quick Reference

| Task | Command |
|------|---------|
| List all skills | `hermes skills list` |
| Filter by audience | `hermes skills list --filter audience:contributor` |
| Load a skill | `hermes skill load <name>` |
| View skill content | `hermes skill view <name>` |
| Create a new skill | `hermes skill create <name>` |
| Search skill content | `hermes skills search <query>` |
| Run skill catalog export | `hermes curator export` |

## Adding a New Skill

1. Create a directory under `skills/` (or under a category directory)
2. Add a `SKILL.md` with frontmatter (name, title, description, audience, tags)
3. Run catalog sync:
   ```bash
   hermes curator sync
   ```

## Commit Conventions

Conventional Commits format:

```
<type>(<scope>): <description>
```

Types: `feat` (new skill), `fix` (skill correction), `docs` (documentation),
`refactor` (restructure), `chore` (tooling, sync), `perf` (optimization).

Examples:
```
feat(ecc): add react-native-patterns skill
fix(devops): correct backup cron schedule
docs: update audience classification table
chore(sync): regenerate catalog metadata
```

## Maintaining Skills

- Keep `audience` field accurate — it powers Hermes Studio filtering
- Update `tags` when a skill gains new capabilities
- Mark deprecated skills with `status: deprecated` in frontmatter
- Orphaned skills (unused >90 days) should be moved to archive
- When deleting a skill, use `absorbed_into` if content is merged elsewhere

## Security

- No API keys, tokens, or credentials in SKILL.md content
- Use `.env` references for secrets
- Report vulnerabilities through NVIDIA PSIRT (see SECURITY.md upstream)
- Never commit `.env` or `auth.json` files
