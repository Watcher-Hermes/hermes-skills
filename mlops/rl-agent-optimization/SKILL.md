---
name: rl-agent-optimization
id: rl-agent-optimization
title: "Reinforcement Learning / Multi-Armed Bandit Agent Optimization"
description: "Use Multi-Armed Bandit (MAB) and Reinforcement Learning to optimize an AI agent's decision-making — skill selection, model routing, and workflow choices. Covers Thompson Sampling, Epsilon-Greedy, reward engineering, shadow mode deployment, and cold-start mitigation."
tags: [mlops, reinforcement-learning, multi-armed-bandit, decision-optimization, agent-self-improvement]
trigger: "When the user asks about self-optimizing agent decisions, skill selection automation, model routing optimization, or building a learning feedback loop into their AI agent."
---

# RL / Multi-Armed Bandit Agent Optimization

## Philosophy

Rule-based systems are predictable but static. RL/MAB systems are adaptive but noisy. The optimal strategy is **hybrid**: rules handle the clear cases; MAB handles the ambiguous ones. Rules provide a safety net while the agent learns from experience.

## Core Architecture

```
User Query
    │
    ▼
┌──────────────────────────┐
│  Rule-Based Decision     │  ← First: check explicit rules
│  (Clear intent → action) │
└──────────┬───────────────┘
           │ Ambiguous / low confidence
           ▼
┌──────────────────────────┐
│  MAB Engine              │  ← Fallback: Thompson Sampling
│  (Best historical match) │      or Epsilon-Greedy
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  Action → Response       │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  Reward Signal           │  ← User correction, task completion,
│  (Feedback loop)         │      silence, or explicit approval
└──────────┬───────────────┘
           │
           ▼
     Update model
```

## Critical Workflow Order

Discovered empirically 14 June 2026 after a 622-skill seed produced 4.3% accuracy.

```
CORRECT ORDER:    reward_validation → fix_reward → seed_gradually → test_shadow → deploy
WRONG ORDER:      seed_all → test → find_empty_reward → backtrack
```

The wrong order wastes days. Validate the reward function first because:
- A bad reward function corrupts every MAB update (beta values inflate from false negatives)
- You cannot tell if MAB is bad or the reward signal is bad without separate validation
- Seeding 622 skills with neutral priors sounds productive but just turns MAB into a random selector (all arms equal)

## Implementation Status (v2.0 — 13 June 2026)

All 4 phases are **deployed and running** in this environment. See `references/implementation-v2-status.md` for the exact file layout and current stats.

### Phase 1 — Observation (Logging Infrastructure) [DEPLOYED]

Before any learning, collect data. Every decision gets logged as a structured JSONL entry:

```
{"timestamp","query_hash","query_length","category","selected_skill","rule_based","reward"}
```

**Key design decisions:**
- Log raw decisions, not just successes — you need negative examples to learn
- `query_hash` (MD5 first 12 chars) identifies the query without storing PII
- `rule_based: true/false` tracks whether the decision came from rules or MAB
- `reward` starts at 0 and is updated *after* user reaction via `update_reward()`

**v1.5 improvements:**
- `log_id` (UUID4) — each entry uniquely identifiable, no hash collision risk
- `selected_skills` as list — supports multi-skill chains, future chain-of-thought
- `auto_reward(user_message)` — automatic sentiment detection from user reply text
- `export_mab_data()` — direct MAB training data export (alpha/beta per skill)

**Reward scale:**
| Value | Signal | Source |
|-------|--------|--------|
| +1    | Positive | Thanks, approval, conversation closure |
| 0     | Neutral | Ongoing conversation, no feedback |
| -1    | Negative | User corrected ("that's wrong", "not what I meant") |
| -2    | Error | Major misdirection, wasted user time |

**Directory layout:**
```
rl_observation/
├── rl_skill_logger.py      ← Logger module v1.5 (log_id, auto_reward, list support)
├── skill_log.jsonl         ← Append-only log file
├── rl_stress_test.py       ← Cold-start mitigation stress test
└── TALIMAT_KILAVUZU.md     ← User training instructions
```

### Phase 1.5 — Cold-Start Mitigation (Stress Test)

Before enabling MAB for the first time, seed the log with synthetic data:

**Why:** A fresh MAB with zero observations selects randomly. The first 50-100 decisions would be worse than the rule system. Pre-seeding eliminates this degradation.

**Method:**
- Build 15+ scenarios covering all skills, categories, and outcomes (success/failure/neutral)
- Run ~100 iterations with 50ms delays
- Verify each skill has 3+ observations
- Then proceed to Phase 2 with warm-start MAB

**Implementation:** `rl_stress_test.py` — standalone, no agent involvement.

**References:** `references/stress-test-methodology.md`, `references/user-training-instructions.md`

### Phase 2 — MAB Engine (Thompson Sampling)

Thompson Sampling balances exploration vs exploitation naturally via Beta distributions:

```python
class ThompsonSamplingMAB:
    def __init__(self):
        # Each arm (skill) has a Beta(alpha, beta) distribution
        self.alpha = {}  # success count
        self.beta = {}   # failure count

    def select_arm(self, available_arms):
        # Sample from each arm's distribution, pick highest
        samples = {arm: np.random.beta(self.alpha.get(arm, 1),
                                       self.beta.get(arm, 1))
                   for arm in available_arms}
        return max(samples, key=samples.get)

    def update(self, arm, reward):
        # reward = 1 (success) or 0 (failure)
        if reward == 1:
            self.alpha[arm] = self.alpha.get(arm, 1) + 1
        else:
            self.beta[arm] = self.beta.get(arm, 1) + 1
```

**Alternative: Epsilon-Greedy** (simpler, less data-efficient):
- 90% of the time: pick the arm with highest historical success rate
- 10% of the time: pick a random arm (exploration)

### Phase 3 — Shadow Mode Deployment

Never switch from rules to MAB cold-turkey. Run in shadow mode:

1. **Rules make the real decision** — system behaves normally
2. **MAB makes a parallel decision** — logged for comparison
3. **Track divergence rate** — when MAB disagrees with rules, who was right?
4. **Switch threshold** — only switch when MAB matches or exceeds rule accuracy for 100+ consecutive decisions
5. **Emergency rollback** — keep the last-known-good rule snapshot

### Phase 4 — Hybrid Decision Layer

The final system doesn't replace rules — it supplements them:

```python
# Threshold is configurable; lower = more MAB decisions
# CALIBRATION HISTORY:
#   0.80 = initial (90% rule / 10% MAB — MAB learns too slowly)
#   0.70 = after auto_reward fix (14 June 2026 — target: 80/20 split)
#   auto_tune adjusts ±0.05 every 10 decisions based on MAB accuracy
#   Final stable range: 0.60-0.75 depending on MAB confidence
CONFIDENCE_THRESHOLD = 0.70

def decide(query, rules, mab):
    rule_result = rules.match(query)

    if rule_result.confidence > CONFIDENCE_THRESHOLD:
        # Clear match → use rule
        return rule_result.action, True

    # Ambiguous → consult MAB
    mab_action = mab.select_arm(get_available_skills(query))

    # Log and return
    log_decision(query, mab_action, rule_based=False)
    return mab_action, False
```

**Threshold tuning rule of thumb:**
- Above 0.80: MAB starves (<10% decisions), learns too slowly
- 0.70-0.80: balanced (15-25% MAB), good for initial learning
- Below 0.65: MAB dominates, rules become irrelevant
- Start high (0.80), lower after 50+ MAB decisions show >60% accuracy
- Never set below 0.55 — rules are the safety net

### Phase 4.5 — Skill Seed (v2.3 — 14 June 2026, staged deployment)

**Problem (v2.1):** MAB only knew skills that had been used before. A never-used skill could never be chosen, creating a cold-start trap per skill rather than per system.

**Initial approach (v2.1, abandoned):** Pre-seed all 622 skills into the MAB engine with neutral priors. Shadow test showed 4.3% accuracy — all arms equal meant Thompson Sampling was a random selector.

**Actual approach (v2.3, deployed per user instruction):** Staged seeding. Seed one category at a time (windows-shortcuts, ~10-15 skills) as a pilot, shadow-test for 50+ queries, then expand to the next category. A narrow but proven set beats a wide but flat one.

**Current seed (14 June 2026):** 44 skills in `skill_seed.json`:
- 29 active skills (with usage data from log, total>0)
- 15 windows-shortcuts seeded as pilot (total=0, neutral alpha=1/beta=1)

**Mechanism:**
```python
# skill_seed.json — generated from skills_list, updated on skill changes
# Loaded by ContextualMAB._load_seed() at engine init
{
  "skill-name": {"alpha": 1, "beta": 1, "total": 0, "category": "ecc"}
}
```

**Seed inheritance:** When a skill is first used in a new context (e.g. "kod"), `_ensure_arm()` checks the genel seed context first and inherits the seed alpha/beta values rather than starting fresh at 1/1. This prevents data fragmentation across contexts.

**Flat Thompson Sampling (v2.2 — 14 June 2026):** `_get_arm_data()` aggregates Beta data across ALL contexts when the specific context lacks data, preventing the context-fragmentation problem where 178 log entries are invisible because they were logged under a different context key. See `references/flat-thompson-sampling.md` for the algorithm.

**Shadow test (14 June 2026):** 23 queries across 10 categories showed MAB accuracy of 4.3% with 28 seeded skills and neutral priors. Root cause: insufficient pulls per arm (avg 6.3) and beta-skew from auto_reward false negatives. Recommendation: keep MAB in hybrid mode with threshold 0.70+ until 20+ pulls per commonly-used skill accumulate (~2-3 weeks at current usage rate). See `references/shadow-test-results.md` for full results.

**Maintenance:** Regenerate `skill_seed.json` whenever skills are added/removed. Keep the staged approach: add skills in category batches, not all at once. Run a shadow divergence check after each batch before expanding.

**Directory layout (current):**
```
rl_observation/
├── rl_skill_logger.py          ← Logger v1.5
├── rl_mab_engine.py            ← MAB v2.1 (Contextual + Seed)
├── rl_decision_layer.py        ← Hybrid karar katmani
├── rl_integration.py           ← CLI bridge
├── skill_log.jsonl             ← Append-only log
├── skill_seed.json             ← 44 skill seed (29 active + 15 windows-shortcuts pilot)
├── .gitignore                  ← log/cache/png hariç
├── monitor_log.py              ← İzleme
├── visualize_log.py            ← Görselleştirme
├── rl_stress_test.py           ← Cold-start test
└── TALIMAT_KILAVUZU.md         ← Doküman
```

## Contextual Bandit (Advanced)

When basic MAB plateaus, add context features to differentiate decisions:

**Context features for agent decisions:**
- Query length (short/medium/long)
- Query category (code/security/search/analysis/general)
- Time of day
- Current active mode
- Previous 3 queries' categories

Each context gets its own set of bandit arms — the system learns "for long code queries, skill X is best" separately from "for short general queries, no skill is best."

## Risk Mitigation

### Reward Hacking
The system will optimize whatever you reward. If you only reward speed, it gives shallow answers. If you only reward silence, it says nothing.

**Solution:** Multi-component reward:
```
reward = α * task_complete + β * (1 / corrections) + γ * quality_score - δ * cost
```

### Cold Start
With no data, MAB explores randomly. In the first 50-100 decisions, performance is worse than rules.

**Solution:** Seed the MAB with prior data from rule-based decisions. Use the first 50-100 rule decisions as initial training data before enabling MAB mode.

### Stability / Non-Stationarity
Users change. What worked last month may not work today. MAB adapts slowly.

**Solution:** Implement a sliding window (last 500 decisions) or exponential decay (older data weighted less).

## Integration with Hermes Agent

The integration point is **nexus-core-omega-v5** execution sequence step 9.5 (ZORUNLU RL SKILL LOG). Every message response ends with a call to the CLI bridge.

### CLI Integration Bridge

Every user message should log the selected skill. Use the integration script:

```bash
python /c/Users/marko/AppData/Local/hermes/rl_observation/rl_integration.py \
  --query "<user query, 100 chars max>" \
  --skill "<skill name or 'none'>" \
  --mode "<active mode>" \
  --rule-based
```

With user feedback (auto-reward):
```bash
python /c/Users/marko/AppData/Local/hermes/rl_observation/rl_integration.py \
  --query "<query>" \
  --skill "<skill>" \
  --user-reply "<user's reply to previous response>"
```

Get stats:
```bash
python /c/Users/marko/AppData/Local/hermes/rl_observation/rl_integration.py --action stats
python /c/Users/marko/AppData/Local/hermes/rl_observation/rl_integration.py --action mab-data
```

### Cron Monitoring Pattern

Two cron jobs run daily for RL system health:

| Time | Job | Purpose |
|------|-----|---------|
| 20:00 | RL Günlük Rapor | Toplu istatistik + karşılaştırmalı analiz |
| 21:00 | GitHub Push | RL kod değişikliklerini yedekleme |

**20:00 job structure (self-contained skill prompt):**
1. `rl_integration.py --action stats` + `--action mab-data` → ham veri
2. session_search ile önceki günün raporunu bul
3. Karşılaştırmalı rapor hazırla (MAB karar oranı, negatif trend, threshold değeri, en başarılı/en sorunlu skill'ler)
4. **Format kuralı: Telegram uyumlu, tablo kullanma.** Rapor şu yapıda olmalı:
   ```
   **RL SİSTEMİ — GÜNLÜK RAPOR [GG.AA.YYYY HH:MM]**

   Toplam: X | Kural: X | MAB: X
   Pozitif: X | Negatif: X | Nötr: X
   MAB karar oranı: X%

   En başarılı skill'ler (alpha/beta):
   - skill1 — α:X/β:X (%XX) ✅
   - skill2 — α:X/β:X (%XX) ✅

   En sorunlu skill'ler (yüksek beta):
   - skill3 — α:X/β:X (%XX) ⚠️

   Threshold: X (auto_tune)

   Önceki güne göre değişim:
   + MAB karar sayısı: X → X
   + Negatif reward: X → X
   + Toplam kayıt artışı: X

   Değerlendirme: 1-2 cümlelik yorum
   ```

**21:00 job structure (workdir: hermes-backup):**
1. RL kod dosyalarını `AppData/Local/hermes/rl_observation/` → `hermes-backup/rl_observation/` e kopyala
2. `git status` + `git diff --stat`
3. Değişiklik varsa → add, commit ("auto-sync YYYY-MM-DD_HH:MM"), push
4. Raporu Telegram'a gönder

### Log Maintenance

A cron job runs daily at 04:00:
- Rotates log file at 5MB (skill_log_YYYYMMDD.jsonl)
- Prunes to keep only last 1000 entries
- 30-day half-life exponential decay on old weights

### For Hermes Agent specifically:

1. **Logger installed at:** `C:\Users\marko\AppData\Local\hermes\rl_observation\rl_skill_logger.py`
2. **Log file:** `C:\Users\marko\AppData\Local\hermes\rl_observation\skill_log.jsonl`
3. **Integration point:** nexus-core-omega-v5 execution sequence step 9.5 (after task completion, before daily log write)
4. **Call from agent response (PREFERRED):**
   ```bash
   python /c/Users/marko/AppData/Local/hermes/rl_observation/rl_integration.py \
     --query "..." --skill "..." --mode "..."
   ```
5. **Reward update on user correction:**
   ```bash
   python /c/Users/marko/AppData/Local/hermes/rl_observation/rl_integration.py \
     --update-reward "<log_id>" --new-reward -1
   ```

### Generic integration pattern (any agent framework):
1. Hook into the agent's post-decision lifecycle
2. Log: {timestamp, query_context, action_taken, decision_source, initial_reward}
3. Hook into the post-response lifecycle
4. Update reward based on user feedback signal
5. Periodically train/recalibrate MAB from accumulated log

### Reward Validation (Required Before Any MAB Training)

Before touching MAB thresholds, seed data, or shadow mode, **validate the reward function.** A reward function with <70% accuracy on a labeled test set will corrupt MAB faster than no reward function at all.

**Method:** Build a 15-message golden set covering positive, negative, and neutral cases. Run auto_reward against manual labels. Gate at 70% accuracy. See `references/reward-validation-methodology.md` for the exact golden set and procedure.

**Current state (14 June 2026):** auto_reward v1 (keyword-only) validated at 93% on the 15-case golden set. Known limitation: measures tone, not outcome. reward_v2 (behavioral) in development — adds correction/progression/silence signals.

### Pitfalls

- **Reward function is everything.** A bad reward function is worse than no RL at all. The system will optimize whatever you measure — measure the wrong thing and you get pathological behavior.
- **Full Deep RL (DQN/PPO) is overkill** for skill selection. The state space is small (current query features → skill choice). MAB handles this with zero neural network complexity.
- **Don't log full query text** — use hashes. The log file grows indefinitely and PII is a concern.
- **Shadow mode is not optional.** Never flip the switch without knowing what the MAB would have done differently.
- **Manual override must always exist.** The user should be able to say "use skill X, forget what MAB says."
- **MAB needs minimum data.** With fewer than 10-20 data points per arm, Thompson Sampling is essentially random. Start logging before you start optimizing.
- **auto_reward keyword list is a silent data corruption vector.** Single-word negative keywords ("degil", "hayir", "olmaz", "tekrar") in auto_reward trigger -1 on normal conversational speech, inflating beta values across multiple skills. Symptoms: 5+ skills show beta=7+ while alpha stays 1-3. Fix: use phrase-level patterns ("yanlis oldu", "calismadi", "hata verdi") instead of single words, or implement a confirmation gate before applying negative rewards.
- **Monitor MAB data health regularly.** Check `rl_integration.py --action mab-data` weekly. Look for: (a) skills where beta > alpha+3 — likely false negatives, (b) skills with <3 total pulls — not enough data, (c) MAB decision ratio <15% — threshold may be too high. Run stats every 3-5 days after any auto_reward changes to catch drift early.
- **Never seed all skills at once in a single context.** Seeding 622 skills (or more) into one "genel" context with neutral priors (alpha=1, beta=1) turns MAB into a random selector. With all arms equal, Thompson Sampling produces uniform random picks. Result: 4.3% accuracy on a 23-query shadow test. Strategy: seed one category at a time (e.g. "windows-shortcuts" first, ~10-15 skills), shadow-test for 50+ queries, then expand to the next category. A narrow but proven set beats a wide but flat set.
- **Tone-based reward does not measure skill success.** auto_reward at 93% accuracy still only tells you if the user's next message sounds happy, not whether the selected skill actually solved the problem. A user can say "thanks" out of politeness (false positive) or "no" to an unrelated question (false negative). reward_v2 adds behavioral signals (correction/progression/silence) to bridge this gap. Do not promote a skill based on tone alone — wait for behavioral confirmation.
- **A test that modifies the system it's testing produces invalid results.** If you discover a bug mid-test (max→min, empty-message correction, missing prev_skill), STOP the test. Record the failure. Fix the bug as a SEPARATE task. Re-freeze the system. Re-run from scratch. Running patches mid-test means the final result measures a system that never existed at any single point in the window. Three concrete rules: (1) Take a frozen snapshot before the first test run (copy the module, point the test import at the copy). (2) The test script is READ-ONLY: calls functions, never writes files, never patches imports at runtime. (3) If a bug is found during testing, the fix goes into the SOURCE module. The frozen copy is updated after the fix, then the test is re-run. The test NEVER modifies its own subject.
- **Empty/correction hazard with null next_msg.** When `next_msg` is empty/None (user is silent), do NOT fall back to `prev_msg` as `current_query` inside the test harness or reward_v2. The fallback creates false hash equality with the previous entry, triggering an incorrect -0.6 correction signal. Fix: let empty `next_msg` pass through as-is; reward_v2 handles it by setting `current_hash = ""` so no hash match can occur. ALSO gate the entire correction block: when `is_empty_message=True`, skip the correction for-loop entirely (not just the hash check). Silence is a SEPARATE signal (silence_seconds), not a subtype of correction. Verify with: reward(13) and reward(14) must show corr=0.00, not -0.30 from stale skill-level correction.
- **Cron/background entries create neutral-only streaks.** When the system runs unattended (cron jobs, background maintenance), every decision logs with reward=0 because there's no user reply to auto_reward. This inflates the neutral count without providing learning signal. Don't mistake "growing total entries" for "growing training data." Monitor positive+negative count separately from total count. If neutral entries grow but pos/neg stays flat, the streak is cron noise, not learning progress. Current baseline (14 June 2026): ~16 neutral entries per 76 minutes during unattended operation.
- **max/min trap in correction logic.** `max(current_correction, -0.3)` returns `0.0` because `0.0 > -0.3`. The debug print shows the assignment happening, but the value is silently clobbered. Use `min(current_correction, -0.3)` instead — the more negative (stronger signal) survives. Root-cause pattern: `components["correction"]` appears 0.0 in the final dict despite skill-match code path being entered. Test by: log both `components["correction"]` before and after the assignment, or add a direct `print(f"correction after: {components['correction']}")` right after the min/max line.

## Related Skills

- `global-model-selection` — Static model benchmarks; complementary to MAB (MAB learns dynamic preferences, benchmarks give initial priors)
- `hibrit-ai-yonlendirme-kurali` — Rule-based model routing; MAB can enhance the ambiguous cases
- `nexus-core-omega-v5` — Contains the execution sequence integration point (step 9.5)

## References

- `references/implementation-v2-status.md` — Actual deployed state, file layout, current stats
- `references/success-gate-framework.md` — 30-day kazanc degerlendirmesi, 4 basari kriteri, karar kurali (14 June 2026)
- `references/phase1-implementation-notes.md` — Logger architecture and full interface docs (v1.5)
- `references/user-training-instructions.md` — What to tell users about RL feedback signals
- `references/stress-test-methodology.md` — Cold-start mitigation via synthetic data seeding
- `references/auto-reward-keyword-tune.md` — auto_reward false negative diagnosis and phrase-level fix (14 June 2026)
- `references/flat-thompson-sampling.md` — Cross-context Beta aggregation for low-data regimes
- `references/shadow-test-results.md` — 23-query shadow test results and MAB readiness criteria
- `references/reward-validation-methodology.md` — Golden set approach, 15-test validation, gate at 70% (14 June 2026)
- `references/reward-v2-behavioral.md` — Four-component behavioral reward: correction, progression, tone, silence (14 June 2026)
- `references/smoke-test-gate-checks.md` — Three-gate validation protocol for reward_v2: silence_blindness, correction_over_tone, retry_not_positive (14 June 2026)
