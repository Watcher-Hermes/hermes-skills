# GitHub Repo Assessment Workflow

Step-by-step workflow for evaluating a third-party GitHub repo before installing into Hermes.

## Step 1 — Quick Scan (30 seconds)

```bash
# Get basic info
curl -s "https://api.github.com/repos/owner/repo" | python3 -c "
import sys, json
r = json.load(sys.stdin)
print(f\"Stars: {r['stargazers_count']}  Forks: {r['forks_count']}\")
print(f\"Language: {r['language']}\")
print(f\"License: {r['license']['spdx_id'] if r.get('license') else 'N/A'}\")
print(f\"Updated: {r['updated_at']}\")
print(f\"Description: {r['description']}\")
"
```

Check: stars ≥ 100? Active (updated <6mo)? Clear license? Known author?

## Step 2 — README Analysis

Read the full README. Answer:
- What does it do? (one sentence)
- Does it support Hermes explicitly?
- Is it a skill/tool/integration/course?
- Installation instructions — are they clear for Windows?
- Any security warnings or prerequisites?

## Step 3 — Directory Structure

Check repo root. Look for:
- `SKILL.md` files — Hermes-native skills
- `.claude/skills/` — Claude Code skills (also compatible)
- `scripts/` — installation helpers
- `requirements.txt` / `package.json` — dependencies
- `Makefile` / `Dockerfile` — build requirements

## Step 4 — Security Scan

### Script scan — Check ALL .py/.sh files for:
- `eval()` / `exec()` / `__import__()` — code injection risk
- `os.system()` / `subprocess` without timeout or sandbox — arbitrary command execution
- `curl` / `wget` / `requests.get()` to unverified URLs — phone-home risk
- Hardcoded API keys, tokens, passwords — credential leak
- `input()` in non-interactive scripts — will hang

### Dependency scan:
- requirements.txt: known packages only? Any typosquats? (e.g. `torch` vs `torrch`)
- package.json: similar check
- Check for `install.sh` / `install.ps1` — what does it actually do?

### Fork integrity check:
```bash
# If it's a fork, compare key files with upstream
# Same hash = no modification
curl -s "https://api.github.***REMOVED-BASE64***_skills.py" | python3 -c "import sys,json; print(json.load(sys.stdin)['sha'])"
curl -s "https://api.github.***REMOVED-BASE64***_skills.py" | python3 -c "import sys,json; print(json.load(sys.stdin)['sha'])"
```

## Step 5 — Scoring

| Criterion | Max | Criteria |
|-----------|:---:|----------|
| Hermes compatibility | 2 | Native SKILL.md=2, MCP plugin=1.5, generic agent=1, no agent support=0 |
| Coverage gap | 2 | Fills missing capability=2, overlaps partially=1, already covered=0 |
| Code quality | 2 | Tests+CI+docs=2, minimal=1, spaghetti=0 |
| Security | 2 | Clean scan=2, minor issues=1, dangerous patterns=0 (reject) |
| Freshness | 1 | Active (<3mo)=1, stable but old=0.5, abandoned=0 |
| Language | 1 | Turkish/English=1, Chinese with English code=0.5, only Chinese=0 |

**Thresholds:** ≥7 → Install full. 4-6 → Install per-module. <4 → Skip.

## Step 6 — Installation

### Method priority:
1. **Hermes-compatible (SKILL.md):** Copy dir → `~/.hermes/skills/` → sync
2. **npx skills add:** Only for repos with `.claude/skills/` at root. Windows pitfall: add `--yes` flag.
3. **Clone + Python script:** For repos with `scripts/install_skills.py`. Use `--type all --force --json`.
4. **Pip/Pipx:** For Python CLI tools. Use `pipx` for isolation.

### Post-install:
```bash
skills_list()                          # verify appearance
skill_view(name)                       # check content
sync_skills_to_obsidian.py             # sync to Obsidian vault
```

## Real Examples from 2026-06-14

### Example 1: fancyboi999/ai-engineering-from-scratch-zh
- **Score: 8/10** — 388 skills + 99 prompts, MIT, clean code, Hermes-compatible
- **Security:** Clean — scripts only copy .md files, no code execution
- **Pitfall hit:** `npx skills add` found only 2 skills (root .claude/skills/). Had to clone + `scripts/install_skills.py --type all --force`.
- **Result:** 489 artifacts installed

### Example 2: backnotprop/plannotator
- **Score: 5/10** — Useful Obsidian integration, but adds browser friction to terminal workflow. No Hermes support.
- **Security:** Binary install + plugin system — higher blast radius.
- **Result:** Skipped

### Example 3: AxDSan/mnemosyne
- **Score: 7/10** — Native Hermes plugin, 23 tools, BEAM benchmark leader. But replaces existing memory system.
- **Security:** MIT, PyPI package, clean. Risk: memory migration needed.
- **Result:** Pending user decision (memory replacement = high impact)

### Example 4: x-glacier/kali-pentest
- **Score: 8/10** — 269 tools, 16 playbooks, native SKILL.md, Kali VM compatible.
- **Security:** Markdown only — no code execution risk. SSH to Kali VM is user-controlled.
- **Result:** Ready to install

### Example 5: escoffier-labs/brigade
- **Score: 4/10** — Overlaps with Hermes' existing memory/cron/skill system. Complex setup.
- **Security:** PyPI package, clean code. But duplicates existing functionality.
- **Result:** Skipped
