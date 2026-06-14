## Contextual Bandit (Advanced)

When basic MAB plateaus, add context features to differentiate decisions:

**Context features for agent decisions:**
- Query length (short/medium/long)
- Query category (code/security/search/analysis/general)
- Time of day
- Current active mode
- Previous 3 queries' categories

Each context gets its own set of bandit arms — the system learns "for long code queries, skill X is best" separately from "for short general queries, no skill is best."