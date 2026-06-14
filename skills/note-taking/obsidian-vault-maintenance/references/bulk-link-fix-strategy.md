# Obsidian Vault Bulk Link Fix Strategy

## Context

Hermes skills were synced to Obsidian vault, creating `{{skills/XXX}}` links that needed conversion to `[[XXX]]`.
Additionally, old `Hermes/Skills/xxx/yyy` paths needed conversion to `[[yyy]]`.

## Strategy Overview

**Phase 0: Inventory (what links exist)**
- Scan all .md files with regex `\\[\\[([^\\]]+?)\\]\\]`
- Collect every unique bare target (strip `|`, `#`)
- Build `existing` set from ALL .md stems + full relpaths
- Classify broken links by pattern

**Phase 1: Regex bulk fix (highest volume first)**
1. `skills/XXX` → `[[XXX]]` — most common pattern
2. `Hermes/Skills/xxx/yyy` → `[[yyy]]`
3. `Hermes/Cron/XXX` → `[[XXX]]`
4. `Hermes/XXX` → `[[XXX]]`

Each pass: `re.sub(r'\\[\\[prefix/([^\\]]+?)\\]\\]', r'[[\\\\1]]', content)` — but verify with lambda for safety.

**Phase 2: Stub pages (lowest effort fix)**
For links that point to nothing and are legitimate pages:
- Create a stub `.md` with `> redirect to [[target]]` or `see [[XXX]]`
- Pages: `Cron`, `gece-gelistirme`, `MOC - Windows Otomasyon`, `subprocess-hata-cozme`

**Phase 3: Remaining broken links (manual per-file)**
- Each file has 1-2 remaining links
- Fix with `path.replace()` or targeted `re.sub()`
- Example: `[[Hermes/Skills/MOC - X]]` → `[[MOC - X]]`

**Phase 4: Verification**
Re-run the same scanner — compare before/after counts.
Acceptable: 0-3 broken links (legitimate cross-vault links like Russian notes).

## Phase 5: Pipe-Format Link Detection

**Critical lesson:** When a link uses `[[hedef|görünen]]` format (pipe with display text), the regex in Phase 0 strips the `|görünen` part. But when you later do `str.replace('[[hedef]]', ...)`, the actual content still has `[[hedef|görünen]]` — the replace does NOT match.

**Fix:** Always check content for the full string (including pipe) before replacing:
```python
if '[[hedef|görünen]]' in content:
    content = content.replace('[[hedef|görünen]]', '\`hedef\`')
```

**Detection:** When a broken link from Phase 0 doesn't match during manual replace, grep the file for the bare target name — the pipe format is the culprit.

## Phase 6: Special Internal Link Categories

Some Obsidian wikilinks in Hermes vault are **not broken** even though they appear in the broken list:

| Pattern | Status | Reason |
|---------|--------|--------|
| `[[_Skills_index]]` | ✅ SAĞLAM | Vault'ta `_Skills_index.md` mevcut |
| `[[_creative_index]]` | ✅ SAĞLAM | Her kategori altında `_kategori_index.md` var |
| `[[_README\|açıklama]]` | ❌ KIRIK | `_README.md` vault'ta yok — GitHub repo kalıntısı |

Rule of thumb: If the target starts with `_` followed by a skill category name (`_creative`, `_software-development`, `_devops`, etc.), it's a legitimate index file. Only `_README` is genuinely broken.

## Key Gotchas

1. **Order matters:** Apply `skills/XXX` fix LAST, because it's the most general pattern and can interfere with other fixes.
2. **`execute_code` limit:** 50 tool calls max — use direct `open(path, 'w').write(content)` instead of `from hermes_tools import write_file` to avoid burning tool calls.
3. **relpath vs basename:** A link `[[autonomous-ai-agents/_autonomous-ai-agents_index]]` will NOT match basename-only lookup. Use `endswith('/' + target)` with full relpaths.
4. **Speed:** Regex + direct I/O processes ~300 files in under 2 seconds.
5. **Python 3.14 re.sub gotcha:** Backtick in replacement pattern (`\\\\` `` ` ` `` `\\\\1`) can break with certain regex. Prefer `lambda m: f'[[{m.group(1)}]]'` for safety.
