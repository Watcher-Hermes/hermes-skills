# RL Agent Optimization — Deployment Status (v2.0)

**Date:** 13 June 2026
**Environment:** Hermes Agent on Windows 10 (Git Bash)
**Provider:** deepseek

## File Layout

All files under: `C:\Users\marko\AppData\Local\hermes\rl_observation\`

| File | Size | Purpose |
|------|------|---------|
| `rl_skill_logger.py` | 9 KB | Logger v1.5 — UUID log_id, auto_reward, export_mab_data, classify_query |
| `rl_mab_engine.py` | 13 KB | MAB Engine v2.0 — ContextualMAB, Thompson Sampling, Sliding Window, Multi-Reward |
| `rl_decision_layer.py` | 9 KB | Hybrid Decision — 28 rules + ContextualMAB, Shadow/Hybrid mode |
| `rl_integration.py` | 3 KB | CLI bridge for live message logging |
| `rl_stress_test.py` | 5 KB | Cold-start synthetic data seeder |
| `skill_log.jsonl` | 56 KB | Live log (143 entries as of deploy) |
| `TALIMAT_KILAVUZU.md` | 2 KB | User training instructions |

## Current Stats (live as of 14 June 2026 07:53)

```
Total entries: 178
Skills tracked: 28 (on top of 44 seed)
Categories: 9 (genel, arama, kod, analiz, guvenlik, goruntu, ogrenme, yardim, yapilandirma)
Sources: 160 rule-based, 18 MAB
MAB ratio: 10.1%
Rewards: 39 positive, 31 negative, 108 neutral
Positive rate: 21.9% | Negative rate: 17.4%
Threshold: 0.70 (auto_tune active, adjusts ±0.05 every 10 decisions)
```

## Integration Point

**nexus-core-omega-v5** execution sequence step 9.5 — ZORUNLU RL SKILL LOG.
Every message response calls `rl_integration.py` with the current query and skill.

## Maintenance

Cron job: `RL Log Bakim` (job_id: 555c122488d1)
- Schedule: `0 4 * * *` (daily at 04:00)
- Actions: log rotation at 5MB, pruning to 1000 entries, 30-day half-life decay
