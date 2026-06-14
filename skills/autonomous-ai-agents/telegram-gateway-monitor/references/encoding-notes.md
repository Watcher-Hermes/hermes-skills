# Encoding Notes for Obsidian Logging

## Problem

PowerShell `Add-Content` (called from bash) does not preserve Turkish characters (ö, ş, ı, ğ, ü, ç, İ, Ş) when writing to Obsidian `.md` files. The output gets garbled:
```
- 2026-06-04 04:12 — Telegram bağlantı testi başarılı.
```
becomes:
```
- 2026-06-04 04:12 � Telegram ba�lant� testi ba�ar�l�.
```

## Root Cause

When bash calls `powershell.exe -NoProfile -Command "Add-Content ..."`, the encoding can shift to Windows-1252 or OEM codepage, neither of which maps Turkish characters correctly.

## Fix: write_file is the only reliable approach

```python
# Python approach via write_file tool (works in cron):
# 1. Read existing file with read_file
# 2. Append new line to content
# 3. Write everything back with write_file (UTF-8)

file_path = "C:\\Users\\marko\\OneDrive\\Belgeler\\Obsidian Vault\\Telegram Gateway Monitor.md"
# read_file returns content lines
# append: f"- 2026-06-04 04:12 - Telegram baglanti testi basarili.\n"
# write_file(path=file_path, content=new_content)
```

## Fallback (if write_file unavailable)

```powershell
# This works IF called directly from PowerShell (not via bash/powershell.exe nesting):
[System.IO.File]::AppendAllText($path, "`n- 2026-06-04 04:12 - ...", [System.Text.Encoding]::UTF8)
```

But from bash this is fragile due to quote escaping. **Prefer `write_file` tool.**

## Safe characters to use

If Turkish chars are causing issues, use ASCII-safe replacements:
- `baglanti` instead of `bağlantı`
- `basarili` instead of `başarılı`
- `sorun` instead of `sorun` (already safe)
- `tarih` instead of `tarih` (already safe)

This matches existing patterns in log files where previous cron runs already used `basarili`.
