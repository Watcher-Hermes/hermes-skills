# reward_v2 Smoke Test — Gate Checks (14 June 2026)

## Purpose

Three mechanical checks that MUST pass before the seed path opens. Unlike
`ref_label_isabet` (secondary, informational), these are concrete rule-based
tests that measure whether reward_v2's behavioral signals work correctly.

## Test Structure

15 scenarios across 3 categories (net, tuzak, sessizlik). Each scenario
provides: `prev_msg`, `next_msg`, `silence_sec`. The test harness maps
these to reward_v2's input interface. A `PREV_SKILL_MAP` ensures each
scenario has the correct prev_skill for testing correction behavior.

## The Three Gates

### Gate 1: silence_blindness
```
Rule:  abs(reward[13] - reward[14]) < 0.1
Pass:  reward treats scenarios 13 and 14 identically
       (same silence_sec=86400, same empty next_msg, same prev_skill match)
Fail:  reward fabricates context not in its input, or uses silence as
       a standalone signal
```

### Gate 2: correction_over_tone
```
Rule:  reward[7] < 0
Pass:  correction fires despite positive tone in next_msg
       ("tesekkurler ama bu olmadi" — "thanks" tone + correction signal)
Fail:  tone still beats correction; the whole behavioral reform failed
```

### Gate 3: retry_not_positive
```
Rule:  reward[9] < 0
Pass:  "tekrar dene" produces negative reward, not positive
       (the old auto_reward's single failure mode is fixed)
Fail:  "dene" keyword still triggers positive tone
```

## Critical Methodology Rule

**A test must not modify the system it's testing.** Procedure:

1. Before first run: `cp reward_v2.py reward_v2_frozen.py`
2. Point test import at `reward_v2_frozen` (read-only)
3. Run test
4. If a bug is found mid-test (max/min, empty fallback, prev_skill mismatch):
   STOP. Fix the SOURCE file. Update the frozen copy. Re-run.
   NEVER patch the source between "read test output" and "report result."

This is non-negotiable. A mid-test patch invalidates every measurement
that follows because the system under test changed during observation.

## Harness Design: prev_skill Independence

Each scenario gets an explicit `prev_skill` via `PREV_SKILL_MAP`. This is
necessary because the JSON spec's `runner_input_fields` (prev_msg, next_msg,
silence_sec) do not include skill — yet correction testing requires knowing
whether the current skill differs from the previous one.

Design rule: **prev_skill lives in the test harness, not in reward_v2's input
interface.** reward_v2 receives `current_skill` and `previous_entries` (which
contain a skill per entry). The test harness controls which skill goes into
the previous entry. This separation keeps reward_v2's interface clean while
allowing the test to probe correction behavior.

## Calibration Reference (14 June 2026 — Frozen v2)

```
Gate 1: reward(13)=0.050, reward(14)=0.050, diff=0.000 ✅  (corr=0.00, empty msg handled)
Gate 2: reward(7)=-0.300 ✅  (correction fires despite positive tone)
Gate 3: reward(9)=-0.300 ✅  ("tekrar dene" no longer positive)
All 3 PASS → seed path opened
Secondary ref_label_isabet: 9/15 = 60% (informational only)
```

## Calibration History

| Attempt | Gate 1 | Gate 2 | Gate 3 | Root cause of failure |
|---------|--------|--------|--------|-----------------------|
| v1 (no prev_skill map) | PASS diff=0.075 | FAIL 0.900 | FAIL 0.600 | max(0, -0.3) bug + missing prev_skill |
| v2 (prev_skill map added) | PASS diff=0.000 | FAIL 0.900 | FAIL 0.600 | max bug still present |
| v3 (max→min fix) | PASS diff=0.000 | FAIL 0.600 | FAIL 0.300 | correction still too weak for progression+tone |
| v4 (correction overrides progression+tone) | PASS diff=0.000 | PASS -0.300 | PASS -0.300 | correction beats progression and tone now |
| v5 (empty msg fix, frozen) | PASS diff=0.000 | PASS -0.300 | PASS -0.300 | empty msg hash fallback removed; all 3 stable |
