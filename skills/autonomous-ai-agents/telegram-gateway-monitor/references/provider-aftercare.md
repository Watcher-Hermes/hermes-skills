# Provider Aftercare — Gateway + Model Provider Switch Diagnostics

## Origin: 2026-06-11 acil durum
- User: "telegram baglantı koptu"
- Gateway process dead (exit -1073741510)
- Restarted → "connected" → user said "hata var hala"
- Real issue: `model.provider` switch to `deepseek` but `.env` had literal `***` as API key

## What Happened

1. `model.provider` changed from `openrouter` to `deepseek` via `hermes config set`
2. Gateway restarted — state showed "connected"
3. Send test → "sent" returned successfully
4. BUT: gateway.log showed `RuntimeError: Provider 'deepseek' is set in config.yaml but no API key was found`
5. Root cause: `.env` contained `DEEPSEEK_API_KEY=***` (3 literal asterisks, not a real key)
6. Full fix: switched provider back to `nous` (which has a valid key in .env)

## Critical Insight

| Component | API Key Source |
|-----------|---------------|
| Main agent (CLI chat) | `config.yaml` → `providers.<name>.api_key` |
| Gateway process | Process environment → `.env` → `X_API_KEY` env var |

The gateway does NOT read `providers.deepseek.api_key` from config.yaml. It only looks for `DEEPSEEK_API_KEY` in its process environment (which is sourced from `.env`).

## Diagnostic Commands

### Check if .env has a real key (not placeholder)
```python
with open(r'C:\Users\marko\AppData\Local\hermes\.env', 'rb') as f:
    for line in f.read().split(b'\n'):
        if b'DEEPSEEK_API_KEY' in line:
            val = line.split(b'=', 1)[1].strip()
            print(f'Len: {len(val)}, Raw: {val}')
            # len=3 and val=b'***' → placeholder (INVALID)
            # len>30 and starts with b'sk-' → valid key
```

### Check gateway log for agent errors after restart
```bash
grep "Agent error\|RuntimeError\|API key" ***REMOVED-BASE64***.log | tail -10
```
If `RuntimeError: Provider 'X' ... no API key was found` appears AFTER the most recent restart time → the provider's key is missing from `.env`.

### Verify provider switch didn't break things
```bash
# 1. Status
***REMOVED-BASE64***-agent/venv/Scripts/hermes.exe gateway status
# 2. State
cat ***REMOVED-BASE64***_state.json | python3 -c "import sys,json;d=json.load(sys.stdin);tg=d.get('platforms',{}).get('telegram',{});print(f'State: {tg.get(\"state\")}, PID: {d.get(\"pid\")}')"
# 3. Send test
***REMOVED-BASE64***-agent/venv/Scripts/hermes.exe send --to "telegram:Q !" "[test] Provider check."
# 4. Wait 5s and check for NEW errors
sleep 5 && grep "Agent error" ***REMOVED-BASE64***.log | tail -3
```

## Config Source of Truth

The API key in `config.yaml` under `providers.deepseek.api_key` is used by the CLI agent but NOT by the gateway. Both the CLI agent and the gateway read from `.env` for runtime credentials, but the config.yaml provider config acts as fallback for the CLI.
