# RL Backup Architecture — Two-Tier Design (14 June 2026)

## Problem

RL/MAB observation logs (`skill_log.jsonl`) contain PII — `user_reply_preview` stores raw user text. Git repositories (especially public ones) must not receive PII. At the same time, the MAB engine's state (alpha/beta/pulls) must be machine-agnostically recoverable for cross-machine migration.

## Solution: Two-Tier Backup

```
TIER 1 — git-friendly snapshot
├── Path: rl_observation/rl_mab_snapshot.json
├── Content: {skill_name: {alpha, beta, pulls, confidence}}
├── PII: NONE (only numeric stats, no text)
├── Size: ~5 KB (43 skills)
├── Frequency: daily (21:00 cron)
├── Restore: rl_mab_engine.load_snapshot(json.load(...))
└── Purpose: state recovery on new machine

TIER 2 — OneDrive full log
├── Path: Obsidian Vault/Hermes/RL_Yedek/skill_log_YYYYMMDD.jsonl
├── Content: Full JSONL (query_hash, skills, reward, user_reply_preview, etc.)
├── PII: YES (user_reply_preview plain text)
├── Size: ~64 KB (grows ~1-2 KB/day)
├── Frequency: daily (21:00 cron)
├── Restore: copy back to rl_observation/skill_log.jsonl
└── Purpose: full audit trail, reward relabeling, research
```

## Implementation

`rl_observation/rl_backup.py` — standalone script, no agent involvement:

```python
# Step 1: Export MAB snapshot (PII-free) → rl_observation/
from rl_mab_engine import mab
snapshot = mab.export_snapshot()  # {skill: {alpha, beta, pulls}}
with open("rl_mab_snapshot.json", "w") as f:
    json.dump(snapshot, f, indent=2)

# Step 2: Copy full log → OneDrive (date-stamped)
shutil.copy2("skill_log.jsonl", one_drive_path)
```

### Cron Integration

```
21:00 cron:
  1. cd /c/Users/marko/AppData/Local/hermes/rl_observation/
  2. python rl_backup.py     → snapshot + OneDrive copy
  3. cd /c/path/to/git/repo  → add snapshot, commit, push
```

### `.gitignore` rules for `rl_observation/`

```
skill_log.jsonl       ← PII (user_reply_preview)
skill_log_*.jsonl     ← rotated logs
__pycache__/
*.pyc
rl_skill_chart.png
```

### MAB `export_snapshot()` method

Patched into `rl_mab_engine.py` on 14 June 2026 after losing the method to a force-push wipe:

```python
def export_snapshot(self):
    """Export PII-free alpha/beta/pulls for all skills across all contexts."""
    snapshot = {}
    for skill, data in self._get_flat_data().items():
        snapshot[skill] = {
            "alpha": data["alpha"],
            "beta": data["beta"],
            "pulls": data["total"],
            "confidence": data["alpha"] / (data["alpha"] + data["beta"])
        }
    return snapshot
```

### Recovery on New Machine

```bash
# 1. Clone repo
git clone <repo>
# 2. Copy snapshot to rl_observation/
cp rl_mab_snapshot.json rl_observation/
# 3. Load snapshot into MAB at init
mab = ContextualMAB()
mab.load_snapshot("rl_mab_snapshot.json")
# 4. (Optional) Copy historical log from OneDrive backup
cp OneDrive/Hermes/RL_Yedek/skill_log_*.jsonl rl_observation/skill_log.jsonl
```

## Why Two Tiers?

| Criterion | Single tier (git only) | Single tier (OneDrive only) | Two tiers ✓ |
|-----------|----------------------|---------------------------|-------------|
| PII safe | ❌ (log has PII) | ✅ | ✅ |
| Cross-machine recovery | ✅ (instant clone) | ❌ (manual OneDrive setup) | ✅ |
| Full audit trail | ❌ (no text) | ✅ | ✅ |
| Open source friendly | ❌ (PII leak) | ✅ (no git) | ✅ |
| Automated (no user action) | ✅ | ❌ (needs cloud login) | ✅ |
