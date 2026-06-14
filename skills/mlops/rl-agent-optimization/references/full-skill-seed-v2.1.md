# Full Skill Seed — v2.1 → v2.3 (14 June 2026)

## Problem

ContextualMAB only knew skills that appeared in the log file (skill_log.jsonl). 
With hundreds of skills in the Hermes library and only 28 ever logged, the rest were 
invisible to the bandit. A never-used skill could never be chosen, creating a 
per-skill cold-start trap.

## Initial Attempt (v2.1 — abandoned)

The original plan was to seed all 622 skills at once. Shadow test showed **4.3% accuracy**
— all arms equal meant Thompson Sampling was a random selector. Abandoned same day.

## Deployed Solution (v2.3 — staged seeding per user instruction)

Seed one category at a time. Start small, prove the mechanism, then expand.

**Current seed (14 June 2026):** 44 skills
- 29 active skills (with usage data from log, total>0)
- 15 windows-shortcuts seeded as pilot (total=0, neutral alpha=1/beta=1)

**Next step:** After windows-shortcuts pilot accumulates 50+ queries, expand to the next category.

## Symptom Detection

```bash
python rl_integration.py --action mab-data
# If any skill is missing from the output, it's not in MAB
# Check: total unique skills in output vs skills_list count
```

Before fix: MAB knew 28 skills of hundreds total
After fix: MAB knows all seeded skills (currently 44 in pilot window)

## Implementation

### 1. Generate seed file

Run from Python after any skill change:

```python
from hermes_tools import skills_list
# skills_list returns all skills
# Build seed dict: {name: {"alpha": 1, "beta": 1, "total": 0, "category": cat}}
# Save to: rl_observation/skill_seed.json
```

### 2. MAB engine loads seed at init

`ContextualMAB.__init__()` calls `self._load_seed()` which:
- Reads `skill_seed.json` from `rl_observation/`
- Seeds all skills under `len_medium|cat_genel` context (catch-all)
- Each skill gets alpha=1, beta=1, pulls=0 (neutral prior)

### 3. Seed inheritance across contexts

`_ensure_arm(ctx_key, arm)` now checks genel seed first:

```python
ctx_genel = "len_medium|cat_genel"
if ctx_genel in self.contexts and arm in self.contexts[ctx_genel]:
    # Inherit seed values instead of starting fresh
    seed = self.contexts[ctx_genel][arm]
    self.contexts[ctx_key][arm] = {
        "alpha": seed["alpha"],
        "beta": seed["beta"],
        "pulls": seed["pulls"]
    }
```

This prevents data fragmentation: a skill that learned alpha=14, beta=1 in
"genel" context will inherit those values when first used in "kod" context.

### 4. Cold-start penalty

In `select_arm()`, skills with pulls=0 get a 0.8x multiplier on their
Beta sample, making MAB slightly prefer skills with usage history:

```python
if pulls == 0:
    samples[arm] *= 0.8
```

## File Locations

- Seed data: `rl_observation/skill_seed.json` (44 entries, ~3KB)
- MAB engine: `rl_observation/rl_mab_engine.py` (ContextualMAB class)
- Decision layer: `rl_observation/rl_decision_layer.py` (RLDecisionLayer)

## Maintenance

Regenerate skill_seed.json when:
- New skills are installed (`hermes skills install`)
- Skills are removed
- After curator consolidation

Keep the staged approach: add skills in category batches (10-15 per batch), shadow-test for 50+ queries between batches, then expand to the next category.

Regeneration command:
```python
# From skills_list() output, build seed JSON
# Save to C:\\Users\\marko\\AppData\\Local\\hermes\\rl_observation\\skill_seed.json
```
