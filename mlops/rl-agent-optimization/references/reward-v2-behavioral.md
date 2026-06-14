# Behavioral Reward (reward_v2) — 14 June 2026

## Problem

auto_reward measures **tone** (does the user sound happy?), not **outcome** (did the skill actually work?). A user can say "thanks" out of politeness (false positive) or "no" to an unrelated question (false negative).

## Architecture: 4 Signals

### 1. Correction Signal
- **Trigger**: Same query_hash repeated OR same skill selected in consecutive messages
- **Strength**: hash match = -0.6, skill-only match = -0.3
- **Priority**: Correction **e_z_e_r** progression and tone when active
- **Implementation**: Check last 3 entries from previous_entries list

### 2. Progression Signal
- **Trigger**: Category change between consecutive messages
- **Strength**: category change = +0.5, same-category different query = +0.2
- **Low priority**: Zeroed out if correction is active

### 3. Tone Signal
- **Trigger**: auto_reward() on user_reply text
- **Strength**: reward × 0.4 (medium weight)
- **Low priority**: Zeroed out if correction is active

### 4. Silence Signal
- **Trigger**: silence_seconds > 120
- **Strength**: >5min = -0.3, >2min = -0.15
- **Modulator only**: Never used alone. Combines with other signals.

## Aggregation Logic

```python
# 1. Calculate raw components
# 2. If correction < 0: progression = 0, tone = 0
# 3. reward = correction + progression + tone
# 4. If silence < 0 and correction < 0: reward += silence (amplified)
# 5. Clamp to [-1.0, 1.0]
```

## CRITICAL: max/min Trap

```python
# WRONG — max() keeps larger value, 0.0 > -0.3
components["correction"] = max(components["correction"], -0.3)  # stays 0!

# CORRECT — min() keeps smaller (more negative) value  
components["correction"] = min(components["correction"], -0.3)  # becomes -0.3
```

## CRITICAL: Empty Message Correction Hazard

When `next_msg` is empty/None (user silent), do NOT fall back to `prev_msg`:

```python
# WRONG — creates false hash match → incorrect -0.6 correction
current_query = next_msg if next_msg else prev_msg

# CORRECT — let empty pass through; reward_v2 sets hash="" 
current_query = next_msg  # empty string is fine
```

In `compute_behavioral_reward`:
```python
# Empty message → no hash → no correction match possible
if current_query and current_query.strip():
    current_hash = _hash_query(current_query)
else:
    current_hash = ""  # never matches any prev_hash
```

**Without this fix, all silence scenarios (13, 14) get -0.9 instead of -0.6, and silence_blindness check becomes unprovable because both sides are inflated identically.**

## File Locations

- Implementation: `rl_observation/rl_reward_v2.py` → `compute_behavioral_reward()`
- Smoke test: `rl_observation/rl_reward_v2_smoke_test.py`
- Integration: called from `rl_skill_logger.py` log_skill_decision when user_reply provided

## Smoke Test Gate Checks

| # | Check | Rule |
|---|-------|------|
| 1 | silence_blindness | \|reward(13) - reward(14)\| < 0.1 |
| 2 | correction_over_tone | reward(7) < 0 |
| 3 | retry_not_positive | reward(9) < 0 |

All 3 must PASS before seed path opens.
