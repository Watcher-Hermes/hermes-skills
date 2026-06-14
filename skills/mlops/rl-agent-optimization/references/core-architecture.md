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