# Reward Validation Methodology

## Why Validate Before Training

A reward function with <70% accuracy on a labeled test set corrupts MAB faster than none. False positives inflate alpha; false negatives inflate beta.

## Golden Set Construction

Build 15+ hand-labeled messages: 5 positive, 5 negative, 5 neutral.
Each: `{"message": "...", "manual": +1/0/-1, "auto": +1/0/-1}`

## Procedure

```python
for entry in golden_set:
    auto = auto_reward(entry["message"])
    correct += (auto == entry["manual"])
accuracy = correct / len(golden_set)
# Gate: accuracy < 70% → FIX REWARD FIRST
```

## Results (14 June 2026)

| Version | Accuracy | Failure |
|---------|----------|---------|
| v1 (old) | 67% | "degil/hayir/tekrar" → false negatives |
| v2 (phrase) | 93% | "dene" → false positive (removed) |

## Gate Rule

- **>= 70%**: usable. Proceed to seed.
- **< 70%**: STOP. Fix keyword list, retest.
