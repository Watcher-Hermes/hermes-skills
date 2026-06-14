# Dolphin 3.0 8B Model Switch — Workflow Reference

## Context

Switching LM Studio from Qwen3-32B (or any loaded model) to Dolphin 3.0 8B on Windows host with no vision API available.

## Via CLI (Recommended — Fast, Reliable)

```bash
# 1. Load Dolphin directly (auto-detects settings for 8B models)
lms load cognitivecomputations.dolphin3.0-llama3.1-8b -y
# → Loads in ~9-10s, 4.37 GiB

# 2. Start API server
lms server start --port 1234

# 3. Verify
lms ps
curl http://localhost:1234/v1/models
```

## Via GUI (Mouse/Keyboard — When Specifically Requested)

### Problem

LM Studio is an **Electron app** (`Chrome_WidgetWin_1` class). UIA automation tools cannot enumerate internal UI elements. Even when the window is found:

- `uiautomation` can find the window but buttons/lists/text are invisible to it
- `hermesmouse.py element "LM Studio" list` returns minimal structure (Chrome Legacy Window)
- OCR would be needed to identify visual elements

### Steps That Work

1. **Ensure GUI is open and in front**:

```bash
# If LM Studio is running headless (server only, no GUI):
taskkill /F /IM "LM Studio.exe"
sleep 2
start "" "C:\Users\marko\AppData\Local\Programs\LM Studio\LM Studio.exe"
sleep 8
```

2. **Get window position** from `~/.lmstudio/.internal/ui-state/global.json` — key `lastActiveWindowBounds`.

3. **Focus window** via `EnumWindows` + `SetForegroundWindow` (window title "LM Studio", class `Chrome_WidgetWin_1`).

4. **Click coordinate-based** — model selector is roughly at center of window. Click, then type model name, then click load area. This is imprecise — `lms` CLI is far more reliable.

## Key Caveats

| Issue | Details |
|-------|---------|
| Server restart | `lms load` does NOT restart API server. Always run `lms server start` after. |
| Stale IP | `169.254.250.216:1234` goes stale after restart. Use `localhost:1234`. |
| Small model auto-detect | Dolphin 8B loads fine without `--gpu` or `--identifier` flags (auto-detects full GPU offload). |
| LM Studio 0.4.x | Uses `lms` CLI installed with LM Studio at `~/.lmstudio/bin/lms.exe`. |
