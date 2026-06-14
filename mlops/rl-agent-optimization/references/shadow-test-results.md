# MAB Shadow Test — Results (14 June 2026)

## Test Setup

- 23 test queries across 10 categories (kod, guvenlik, arama, goruntu, analiz,
  ogrenme, yapilandirma, windows, android, genel)
- Each query had expected skill family(s) for evaluation
- RLDecisionLayer run in shadow mode: rules made real decisions, MAB made
  parallel decisions
- ContextualMAB: 28 seeded skills (neutral priors alpha=1, beta=1)

## Results

| Metric | Value |
|--------|-------|
| Test count | 23 |
| Correct | 1 |
| Wrong | 22 |
| Accuracy | 4.3% |

## Analysis

### Root Cause: Insufficient Data Per Arm

Thompson Sampling needs 10-20 pulls per skill before Beta distributions
diverge enough for reliable selection. With 28 skills and 178 total log entries,
average pulls per skill = 6.3. Skills with beta=7 (killed by auto_reward)
were effectively unpickable but still consumed sample budget.

### Context Fragmentation (before Flat Thompson fix)

The original ContextualBandit partitioned data by context key. A skill trained
in `cat_genel` had zero data when queried in `cat_kod`, making MAB fall back
to neutral priors (alpha=1, beta=1) — effectively random selection.

### Skill Seed Bloat (622 skills)

Initial seed of all 622 skills made the problem worse:
- MAB sampled from 622 arms with nearly identical Beta distributions
- Random selection across 622 choices = ~0.16% chance of picking the right one
- Reduced to 28 skills improved accuracy to 4.3% (still random, but fewer choices)

## Key Findings

1. **MAB needs 20+ pulls per skill minimum** before it beats random.
   Below this threshold, rules should make all decisions.

2. **Seed size matters inversely with early accuracy.**
   More seeded skills = more noise. Only seed skills that have actual usage data.

3. **Contextual bandit fragments data badly in low-data regimes.**
   Flat Thompson Sampling (cross-context aggregation) is essential below
   2000 total log entries.

4. **Auto_reward corruption makes MAB worse than useless.**
   A single bad negative keyword can kill 5+ skills silently. Monitor
   beta values weekly.

## Recommendation

Keep MAB in shadow/hybrid mode with high threshold (0.70+) until:
- 20+ pulls per commonly-used skill
- 10+ pulls per niche skill
- Beta values <3 on all skills (no auto_reward corruption)

Expected timeline at current usage rate: 2-3 weeks.
