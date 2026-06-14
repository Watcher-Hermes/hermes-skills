# Windows Gateway Cleanup + Restart Notebook

## Problem
- Existing gateway processes ignore `.env` token updates.
- Restart by scheduled task alone did not move state from `disconnected` to `connected`.

## Working procedure
1. Update `C:\Users\marko\AppData\Local\hermes\.env` to the new `TELEGRAM_BOT_TOKEN=...`.
2. Reset state file so the gateway does not consider last run authoritative:
   - `C:\Users\marko\AppData\Local\hermes\gateway_state.json`
   - Set `platforms.telegram.state = "disconnected"` and clear `updated_at`.
3. Stop known gateway child processes, then start the scheduled task.
4. Wait for state to settle to `connected`.

## Cleanup snippet
`powershell.exe -NoProfile -Command "Stop-Process -Id 9616,10192,19280,24328 -Force -ErrorAction SilentlyContinue; Start-Sleep 3; Start-ScheduledTask -TaskName Hermes_Gateway"`

## Verification
- `python -c "import json; ...\nprint(json.load(open('C:\\Users\\marko\\AppData\\Local\\hermes\\gateway_state.json'))['platforms']['telegram']['state'])"`
- After restart, state can return `retrying`; Telegram token rejection is surfaced in `error_message`.

## Failure rule
If gateway reports `The token ... was rejected by the server.`:
- Do **not** retry token editing in `.env`.
- Request a fresh token via BotFather and repeat from step 1.
