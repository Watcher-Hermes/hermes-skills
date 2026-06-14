# Telegram Gateway Setup Notes

## Bot Token Setting

`hermes config set telegram.bot_token <token>` does NOT work because Hermes converts config keys to env var names, and dots are invalid there. Use the Python approach instead:

```bash
python - <<'PY'
from hermes_cli.config import save_env_value
save_env_value('TELEGRAM_BOT_TOKEN', '<token>')
PY
```

## Gateway Status

```bash
hermes gateway status
hermes status --all
```

Telegram shows as `configured` when `TELEGRAM_BOT_TOKEN` is present.

## Home Channel

- `telegram:Q !` means DM with user Q.
- To set a home channel, use `/sethome` in the target Telegram chat, or configure `TELEGRAM_HOME_CHANNEL`.

## Cron Job

- Use `every 30m` (or any duration) with `repeat: forever`.
- If the first run shows `schedule: once in ...`, re-run `update` with the same schedule; Hermes caches it until next scheduler cycle.
- `run` triggers an immediate execution without altering the schedule.

## Auto-Repair Sequence

1. Read `TELEGRAM_BOT_TOKEN` from env (checks `.env`).
2. Send test message to `telegram:Q !`.
3. On failure:
   - Check `hermes gateway status`.
   - Restart gateway via Hermes CLI or platform docs.
   - Re-verify token and retry once.
