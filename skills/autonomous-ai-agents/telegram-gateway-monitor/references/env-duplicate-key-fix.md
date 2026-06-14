# .env Duplicate Key Fix

## Symptom
- `WARNING agent.auxiliary_client: resolve_provider_client: openrouter requested but OpenRouter credential pool has no usable entries`
- `HTTP 401: Missing Authentication header`
- `cron`/gateway başlar ama gateway çalışmıyor

## Why this happens
`.env` içinde aynı anahtar birden fazla satıra yazılmışsa, Hermes credential havuzu geçersiz olur.

## Detection
```bash
grep '^OPENROUTER_API_KEY=*** -n /c/Users/marko/AppData/Local/hermes/.env
```

## Fix (one-shot cleanup)
```python
from pathlib import Path
p = Path('C:/Users/marko/AppData/Local/hermes/.env')
lines = p.read_text(encoding='utf-8').splitlines()
seen = set()
out = []
for line in lines:
    key = line.split('=', 1)[0]
    if key in seen or not key:
        continue
    seen.add(key)
    out.append(line)
p.write_text('\n'.join(out) + '\n', encoding='utf-8')
```

## Then
```powershell
powershell.exe -NoProfile -Command "Start-ScheduledTask -TaskName Hermes_Gateway"
hermes gateway status
```
