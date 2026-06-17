---
name: reymen-web-search-tool
category: software-development
version: 1.0.0
description: R>eYMeN projesine web_search_tool.py ekleme ve motor.py'ye kaydetme adimlari
tags: [skill, hermes, reymen, web-search]
---

# reymen-web-search-tool

R>eYMeN projesine DuckDuckGo web arama tool'u ekler.

## Dosyalar

| Dosya | Yol |
|-------|-----|
| web_search_tool.py | `tools/web_search_tool.py` |
| motor.py kaydı | `motor.py` → `_plugin_moduller_yukle()` listesine **tools.web_search_tool** eklenir |

## Test

```bash
python -m py_compile tools/web_search_tool.py
python -c "from tools.web_search_tool import run; print(run('Python dili', 'duckduckgo'))"
```

## API

```
WEB_ARAMA("sorgu", "duckduckgo")
  -> DuckDuckGo'da ara, ozet don
```
