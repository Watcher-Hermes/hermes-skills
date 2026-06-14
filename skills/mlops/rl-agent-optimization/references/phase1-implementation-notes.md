# Phase 1 Implementation — RL Observation Logger

Built: 13 June 2026
System: Hermes Agent on Windows
Log file: `C:\Users\marko\AppData\Local\hermes\rl_observation\skill_log.jsonl`
The Logger module: `C:\\Users\\marko\\AppData\\Local\\hermes\\rl_observation\\rl_skill_logger.py`

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 13 June 2026 | Initial logger - query_hash, single skill, manual reward |
| v1.5 | 13 June 2026 | log_id (UUID), selected_skills (list), auto_reward(), export_mab_data() |

## The Logger Interface (v1.5)

### `log_skill_decision(query, selected_skills, rule_based, reward, category, mode, user_reply, additional)`
Called once per skill selection. Returns the generated `log_id` for future reward updates.

**v1.5 changes:**
- `selected_skills` accepts both string and list - always stored as list internally
- `user_reply` parameter triggers `auto_reward()`; if a positive/negative signal is detected, reward is set automatically
- Returns `log_id` (UUID4) instead of just True

### `update_reward(log_id, new_reward)`
Called when user feedback arrives later. Now **log_id based** (not hash based), so it updates the exact record.

### `update_reward_by_hash(query_hash, new_reward)`
Legacy interface for backward compatibility.

### `auto_reward(user_message) -> int`
Detects user sentiment from message text:
- **+1 (positive):** tesekkur, tamam, oldu, harika, cozuldu, mukemmel, dogru, super
- **-1 (negative):** yanlis, hayir, istemedi, anlamadin, tekrar, duzelt, hatali, olmamis
- **0 (neutral):** everything else
Negative signals are checked first (user may mix positive and negative).

### `export_mab_data() -> dict`
Prepares data for MAB engine. Returns {skill_name: {alpha, beta, total}} where alpha = non-negative count, beta = negative count. Direct input for Thompson Sampling seeding.

### `get_stats()`
Returns {total_entries, skills, categories, rewards, by_source}.

### `classify_query(query)`
Rule-based keyword classification:

## Architecture Decisions

### JSONL format (not SQLite, not CSV)
- **Why:** Append-only, no schema migrations, grep/awk friendly, trivially parsable by any tool
- **Trade-off:** No random access by key — but we never need it. Sequential scan over thousands of lines is fast enough.
- **Trade-off:** Concurrent write risk — mitigated by single-agent architecture (only one session writing at a time)

### MD5 truncation for query_hash
- `hashlib.md5(query.encode()).hexdigest()[:12]`
- 12 hex chars = 48 bits of entropy. Collision risk is negligible for this use case (< 1 in 10^14 for 10K entries).
- Avoids storing raw user queries in the log while still identifying repeated queries.

### Reward update via file rewrite
- `update_reward()` reads the entire file, updates the matching entry, rewrites the file.
- **Why not append-only:** Simpler code, no need for a secondary index table.
- **Failure mode:** If interrupted mid-write, the last entry is lost. Acceptable for a learning system.
- **Optimization:** When the log exceeds 10K entries, implement weekly rotation (`skill_log_YYYYMMDD.jsonl`).

## The Logger Interface

### `log_skill_decision(query, selected_skill, rule_based, reward, category, mode, additional)`
Called once per skill selection. The `category` auto-classifies if not provided.

### `update_reward(query_hash, new_reward)`
Called when user feedback arrives. Updates the most recent entry matching the hash.

### `get_stats()`
Returns `{total_entries, skills: {name: count}, categories: {name: count}}`

### `classify_query(query)`
Rule-based keyword classification:
- `kod` → kod, kodla, yaz, script, python, program
- `guvenlik` → güvenlik, exploit, cve, zafiyet
- `arama` → tor, arama, ara, bul, internet
- `analiz` → analiz, incele, kontrol, log
- `goruntu` → ekran, gör, screen, vision
- `ogrenme` → öğren, eğitim, ders, ne demek
- `yapilandirma` → ayar, yapılandır, kur, config
- `yardim` → yardım, help, ne yapabilirsin
- `genel` → fallback

## Nexus-core Integration

Added to the execution sequence as step 9.5 (between 3lu-kontrol-sistemi and daily log write):

```
9.5. RL SKILL LOG — log_skill_decision(...) with:
     - selected_skill: skill called (or "none")
     - rule_based: True (rule) or False (MAB)
     - reward: 0 (default, updated on user reaction)
     - category: auto-classified
```

## Query Implementation Pattern

When calling from a response flow:
```python
python -c "import sys; sys.path.insert(0,r'C:\Users\marko\AppData\Local\hermes\rl_observation'); from rl_skill_logger import log_skill_decision; log_skill_decision(query='user query text', selected_skill='skill-name', category='analiz')"
```

## Phase 2 Readiness

The logger is ready for MAB integration. The `skill_log.jsonl` file accumulates learning data. When Phase 2 begins:
1. Parse all entries where `rule_based=True` as training data
2. For each skill, compute success rate from reward values
3. Seed Thompson Sampling Beta distributions with (success_count, failure_count)
4. Switch to hybrid mode: rules for confident matches, MAB for ambiguous ones

## Known Gaps

- No log rotation yet — will need it when file exceeds ~10MB
- No secondary index for fast reward updates — acceptable at current scale
- Category classification is rule-based — could be replaced with an embedding + classifier
