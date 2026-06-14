# Gateway Process Environment Caching

## Symptom
```
RuntimeError: Provider 'deepseek' is set in config.yaml but no API key was found.
```

...even though `.env` has a **valid** `DEEPSEEK_API_KEY=sk-...` (verified via binary read, not a `***` placeholder).

## Root Cause

The gateway process reads `.env` **once at process startup** and caches those environment variables for its entire lifetime. If:

| Scenario | What happens |
|----------|-------------|
| `.env` was written/updated **after** the gateway process started | Gateway never sees the new key |
| A stale gateway PID is still running from an earlier config | Old PID still has the old/cached env |
| The Scheduled Task auto-started before `.env` was populated | Gateway launched with empty env |
| Previous provider switch left a different key name in .env | Gateway looks for `DEEPSEEK_API_KEY` but only `NOUS_API_KEY` exists |

The **main agent** (CLI chat) re-reads config.yaml each turn so it always sees updates. The gateway does NOT — it's a long-lived process.

## Diagnosis — Stale Error vs Current Error

The most common trap: looking at gateway.log and seeing "no API key found" and assuming it's a current problem.

```bash
# 1. Get gateway start time from log
grep "Starting Hermes Gateway" ***REMOVED-BASE64***.log | tail -1

# 2. Get last "no API key" error time
grep "no API key was found" ***REMOVED-BASE64***.log | tail -1

# 3. Compare
#    If error timestamp < gateway start timestamp → stale, already fixed
#    If error timestamp > gateway start timestamp → current problem
```

## Fix

```powershell
# 1. Kill any running gateway (all Python processes)
powershell.exe -NoProfile -Command "Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -match 'gateway' -or $_.CommandLine -match 'hermes' } | Stop-Process -Force"

# 2. Verify .env has the key
python3 -c "
with open(r'C:\Users\marko\AppData\Local\hermes\.env', 'rb') as f:
    for line in f.read().split(b'\n'):
        if b'DEEPSEEK_API_KEY' in line:
            val = line.split(b'=', 1)[1].strip()
            print(f'Key: {\"VALID\" if len(val) > 30 and val.startswith(b\"sk-\") else \"INVALID\"} (len={len(val)})')
"

# 3. Start fresh via Scheduled Task
powershell.exe -NoProfile -Command "Start-ScheduledTask -TaskName Hermes_Gateway"

# 4. Wait 20s, verify new PID
sleep 20
cat ***REMOVED-BASE64***_state.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'PID: {d.get(\"pid\")}')"
```

After this, check log for clean startup:
```bash
grep "API key\|Agent error" ***REMOVED-BASE64***.log | tail -3
```

No "API key" errors after the new startup → fixed.

## Prevention

When changing `.env` (adding/updating any API key), **always restart the gateway**:

```powershell
powershell.exe -NoProfile -Command "Restart-ScheduledTask -TaskName Hermes_Gateway"
```

Never assume a running gateway will pick up `.env` changes — it won't until the process dies and restarts.
