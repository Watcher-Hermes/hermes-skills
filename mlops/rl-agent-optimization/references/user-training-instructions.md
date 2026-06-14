# User Training Instructions — RL Feedback Signals

Give to any user/contributor who will interact with the RL-equipped system.

## Your Role in the Learning Loop

The system is in **Observation Phase** — collecting data before the MAB engine activates. Every interaction trains the system. You do NOT need to change how you work. Just be aware that your natural reactions are the reward signal.

## What To Do

### Normal Operation — Keep Working as Usual
Use the system for whatever you need. The logger captures skill selections automatically with a unique `log_id`.

### Positive Feedback (Reward = +1)
When the system answers correctly or completes a task well, **one of these in your reply signals success:**
  - "Tesekkurler", "Tamam", "Oldu", "Harika", "Cozuldu"
  - "Mukemmel", "Dogru", "Super", "Anlasildi"

### Negative Feedback (Reward = -1)
When the system gets it wrong, **one of these signals the error:**
  - "Yanlis", "Hayir", "Bunu istemedim", "Anlamadin"
  - "Tekrar", "Duzelt", "Hatali", "Olmamis", "Tekrar yap"

These are automatically detected by `auto_reward()`. No extra effort needed.

### Neutral (Reward = 0)
Continuing a conversation with no clear approval or correction — the system stays at neutral. This is fine.

## Why It Matters

- The MAB engine seeds its Thompson Sampling Beta distributions from accumulated rewards
- A skill with mostly +1 rewards gets a higher success probability and is selected more often
- A skill with mostly -1 rewards is tried less frequently
- More diverse queries across different categories (code, security, search, analysis) helps the system learn which skill fits which context

## What NOT To Do

- Do NOT try to "game" the reward system — artificial signals corrupt the training data
- Do NOT worry about missing a signal — neutral is a valid state
- Do NOT change your speaking style — the system adapts to you, not you to it

## Current Status

- Logger: v1.5 (log_id, auto_reward, skill lists, MAB export)
- Observation data: growing from real interactions
- Next phase: MAB engine goes live on trigger
