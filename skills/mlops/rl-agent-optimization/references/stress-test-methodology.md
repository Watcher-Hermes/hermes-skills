# Cold-Start Mitigation — Stress Test Methodology

## The Problem

A fresh MAB engine with zero observations chooses randomly (cold start). This means the first 50-100 decisions after MAB goes live are worse than the rule-based system it replaces. Users perceive degradation and reject the change.

## The Solution: Pre-Seed with Synthetic Data

Before enabling the MAB engine, run a stress test that generates structured synthetic interaction logs. This gives the MAB meaningful priors from day one.

## Stress Test Design (rl_stress_test.py)

### Scenario Pool

Create 15+ diverse scenarios covering the full decision space:

| Component | Detail |
|-----------|--------|
| Skills | All skills the agent might select (5-20) |
| Categories | All query categories the classifier handles |
| Outcomes | Positive (success), Negative (failure), Neutral |
| Modes | All active agent modes (L99, CLI, FORENSIC, etc.) |

Each scenario has: `{query, skills, reward, category, mode, reply}`

### Execution

```
15 scenarios × 6-7 batches = ~100 synthetic log entries
50ms delay between entries (avoids filesystem contention)
```

### Distribution Balance

- **~40% positive** — skills that should succeed get high alpha
- **~30% negative** — some skills should show failure patterns
- **~30% neutral** — captures the "no feedback" state
- **Categories spread evenly** — prevents category starvation

### Output

The log file after stress test is immediately usable by `export_mab_data()`:
- Each skill has `{alpha, beta, total}` counts
- Thompson Sampling Beta(a,b) distributions have meaningful shape parameters
- Cold start is replaced with warm start

## Integration

1. Run stress test after any skill catalog change
2. Run stress test before enabling MAB for the first time
3. Optional: run periodically to refresh priors (especially after user behavior shifts)

## Verification

After stress test, run:
```python
from rl_skill_logger import get_stats, export_mab_data
stats = get_stats()
mab = export_mab_data()
# Check: total > 80, each major skill has >3 observations
```

## Hermes-Specific Path

```
C:\Users\marko\AppData\Local\hermes\rl_observation\rl_stress_test.py
```

Run with: `cd rl_observation && python rl_stress_test.py`
