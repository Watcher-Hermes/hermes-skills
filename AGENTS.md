# Hermes Skills — Agent Instructions

## Repository Overview

This repository contains all skills for **Hermes Agent** (Nous Research). Skills are reusable procedural knowledge — task-specific workflows, tools configurations, environment setups, and reference guides that the agent loads on demand.

**Total skills:** 1.184
**License:** Apache 2.0
**Agent:** [Hermes Agent](https://get-hermes.ai/) (>=0.8.0)

## Repository Structure

```
hermes-skills/
├── ecc/                    # ECC skills — AI/ML workflows, dev patterns (262 skills)
│   ├── react-patterns/
│   ├── rust-patterns/
│   ├── django-patterns/
│   ├── python-testing/
│   └── ...
├── windows-automation/     # Windows automation scripts (42 skills)
├── windows-shortcuts/      # Windows keyboard shortcut references (149 skills)
├── software-development/   # Full-stack dev scaffolds, testing (34 skills)
├── devops/                 # Backup, cron, monitoring (13 skills)
├── creative/               # ASCII art, design, video (22 skills)
├── media/                  # YouTube, GIF, music (8 skills)
├── note-taking/            # Obsidian, Notion (12 skills)
├── github/                 # PR, issues, auth (6 skills)
├── mlops/                  # Model training, inference (24 skills)
├── autonomous-ai-agents/   # Multi-agent, Claude Code (23 skills)
├── data-science/           # Jupyter, HF Hub (3 skills)
├── research/               # ArXiv, papers (8 skills)
├── security/               # Pentest, encryption (10 skills)
├── productivity/           # Email, camera, PDF (26 skills)
├── gaming/                 # Game trainers, emulators (6 skills)
├── android/                # APK modding (1 skill)
├── apple/                  # iOS/macOS (5 skills)
├── user-preferences/       # Persona, startup config (17 skills)
├── hermes-agent/           # Hermes config (1 skill)
├── mcp/                    # MCP client (1 skill)
├── self-improvement/       # Nightly auto-improvement (1 skill)
├── *root skills*           # ~460 standalone AI/ML skills (prompt engineering,
│                           #   model selection, eval, architecture...)
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
