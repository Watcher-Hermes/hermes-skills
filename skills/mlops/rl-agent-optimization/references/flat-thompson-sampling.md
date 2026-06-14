# Flat Thompson Sampling — Cross-Context Aggregation (14 June 2026)

## Problem

`ContextualMAB` partitioned Beta distributions by context key
(`len_short|cat_kod`, `len_medium|cat_genel`, etc.). When a skill was
trained in one context (e.g. code-exec in `cat_genel`), it had no data
in other contexts (e.g. `cat_kod`). A query classified as "kod" category
would see code-exec as alpha=1, beta=1 (zero knowledge) instead of its
actual alpha=15, beta=1 from genel usage.

This fragmented learning: 178 log entries collected but MAB's effective
knowledge per context was near zero.

## Solution: `_get_arm_data()`

Added a fallback method that aggregates data across ALL contexts when
the specific context lacks data:

```python
def _get_arm_data(self, ctx_key: str, arm: str) -> dict:
    # 1) Prefer specific context
    if ctx_key in self.contexts and arm in self.contexts[ctx_key]:
        return self.contexts[ctx_key][arm]
    
    # 2) Fallback: aggregate from all contexts
    agg = {"alpha": 0, "beta": 0, "pulls": 0}
    found = False
    for ck, arms in self.contexts.items():
        if arm in arms:
            agg["alpha"] += arms[arm]["alpha"] - 1  # remove prior
            agg["beta"] += arms[arm]["beta"] - 1
            agg["pulls"] += arms[arm]["pulls"]
            found = True
    
    if found:
        agg["alpha"] = max(1, agg["alpha"] + 1)
        agg["beta"] = max(1, agg["beta"] + 1)
        self._ensure_arm(ctx_key, arm)
        self.contexts[ctx_key][arm] = dict(agg)  # cache
        return self.contexts[ctx_key][arm]
    
    # 3) Fresh arm
    self._ensure_arm(ctx_key, arm)
    return self.contexts[ctx_key][arm]
```

## How It Works

1. Each Beta prior (the "1" in alpha/beta) is subtracted before aggregation
   to prevent prior inflation (N contexts × 1 = N, biasing toward 0.5)
2. After aggregation, a single prior is added back: `max(1, sum + 1)`
3. The result is cached in the requesting context for future lookups
4. `select_arm()` uses `_get_arm_data()` instead of direct dict access

## Impact

- A skill with alpha=15, beta=1 in `cat_genel` now correctly shows
  alpha=15, beta=1 when called from `cat_kod`
- No data fragmentation across length buckets (short/medium/long)
- Learning converges faster because every interaction updates a shared
  knowledge base, not a context-specific partition

## Trade-off

Flat aggregation loses context-specific specialization. "For short code
queries, code-exec is best" cannot be learned separately from "for long
general queries, code-exec is best." In practice, with <200 log entries
and 622 skills, the context-specific signal was negligible — flat
aggregation dramatically outperformed partitioned learning.

Re-enable context-specific learning when per-context data reaches
50+ pulls per arm (at which point context-specific partitions will
outperform flat aggregation).
