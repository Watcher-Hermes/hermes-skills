# → "Server is now running on port 1234"
```

Default bind: `127.0.0.1`. For LAN: `--bind 0.0.0.0` + `--cors`.

### Test inference via API

```bash
curl -s http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "<identifier>",
    "messages": [
      {"role": "system", "content": "Kısa cevap ver."},
      {"role": "user", "content": "Merhaba!"}
    ],
    "temperature": 0.7,
    "max_tokens": 100
  }' | python -c "import sys,json; r=json.load(sys.stdin); print(r['choices'][0]['message']['content'])"
```

### Reasoning models (Qwen3, DeepSeek-R1 variants)

Qwen3-32B is a reasoning model — it produces `reasoning_content` before `content`.
The first response may be empty (`content: ""`) if `max_tokens` is too low since reasoning tokens consume the budget.

**Fix:** Increase `max_tokens` to 200+ for reasoning models, or set system prompt to suppress reasoning.

### List available API models

```bash
curl -s http://localhost:1234/v1/models
```

### Detect which model is actively serving

`/v1/models` lists ALL cached models — not just the one currently loaded in memory.
To see which model is **actively loaded and serving**, send a minimal test inference and read the `model` field:

```bash
curl -s -X POST http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"test"}],"max_tokens":1}' \
  | python -c "import sys,json; print(json.load(sys.stdin).get('model','?'))"
```

This returns the active model ID (e.g. `dolphin-8b`) directly. Use this when:
- `lms` CLI is not in PATH or unavailable
- You're in a bash (git-bash) session without `lms` access
- GUI is minimized/hidden and you can't see which model is loaded
- You want a quick one-liner confirmation without running `lms ps --json`

**Note:** LM Studio's internal API endpoints (`/api/models`, `/api/active-model`, `/api/server/status`) do NOT exist — they all return `Unexpected endpoint or method` errors. Do not attempt them; use `/v1/chat/completions` as above instead.

---