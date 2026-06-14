---
name: lm-studio-local-llm
description: "LM Studio local LLM operations — Windows install, GGUF model import/load, GPU offload configuration, server management, API testing, and model swapping. Sibling to ollama-local-llm."
title: "Lm Studio Local LLM"
version: 1.2.0
platforms: [windows]
tags: [lm-studio, local-llm, gpu-offload, gguf, windows, lms-cli]
category: mlops
audience: user
---

# LM Studio Local LLM

Use this skill for installing, configuring, and operating LM Studio on Windows — importing GGUF models, setting GPU offload for VRAM-limited GPUs, managing the inference server, and testing via API.

## When to use

- Installing/reinstalling LM Studio on Windows
- Importing a GGUF model into LM Studio (from HuggingFace or local file)
- Loading a model with GPU offload configuration
- Starting/stopping the local API server
- Testing model inference
- Swapping between models
- Debugging "Failed to load model" errors

## Windows Installation

### Fresh install

```powershell
# Download from lmstudio.ai (or use the button on the site)
# Silent install (NSIS-based):
Start-Process -FilePath 'C:\Users\marko\Downloads\LM-Studio-0.4.16-2-x64.exe' -ArgumentList '/S' -Wait -NoNewWindow
```

Installed to: `C:\Program Files\LM Studio\LM Studio.exe`

### CLI tool (`lms`)

Installed with LM Studio at: `C:\Users\marko\.lmstudio\bin\lms.exe`
Must be in PATH or called with full path / `export PATH="$PATH:/c/Users/marko/.lmstudio/bin"`

### Model storage

Models directory: `C:\Users\marko\.lmstudio\models\`

LM Studio auto-detects GGUF files in subdirectories under this path.
Structure: `models/<model_name>/<file>.gguf`

---

## Model Management (`lms` CLI)

### List cached models

```bash
lms ls
```

### Import a GGUF file

```bash
# Copy mode (keeps original in downloads)
lms import -y -c "/path/to/model.gguf"

# Move mode (default)
lms import -y "/path/to/model.gguf"
```

**Note:** Import attempts HuggingFace lookup which may timeout. If it times out, manually copy the file to `~/.lmstudio/models/<name>/` and LM Studio will find it on next `lms ls`.

### Manual copy (fallback)

```bash
mkdir -p "/c/Users/marko/.lmstudio/models/ModelName/"
cp "/c/Users/marko/Downloads/model.gguf" "/c/Users/marko/.lmstudio/models/ModelName/"
```

### View loaded models (JSON)

```bash
lms ps --json
```

Returns: model key, display name, size, architecture, quantization, identifier, context length, status.

---

## LM Studio Internal Config Files

When the GUI is unavailable and you need to verify or troubleshoot settings without opening LM Studio:

| File (under `~/.lmstudio/`) | Purpose |
|-----------------------------|---------|
| `settings.json` | Main app settings: language, UI, chat, developer mode, JIT model loading, default context length |
| `.internal/backend-preferences-v1.json` | Active backend engine (e.g. `llama.cpp-win-x86_64-nvidia-cuda-avx2`) |
| `.internal/http-server-config.json` | Server port, JIT mode, CORS, network interface, logging |
| `.internal/internal-engine-index.json` | Full engine metadata: CUDA support, llama.cpp version, GPU make |
| `.internal/model-data.json` | Model load timestamps and sources |
| `.internal/conversation-config.json` | Active conversation, view mode, font settings |
| `models/` | Directory per publisher, each containing `.gguf` files |

**Key finding:** LM Studio's internal API (`/api/models`, `/api/active-model`, `/api/server/status`) does NOT exist — all return `Unexpected endpoint or method`. GPU offload configuration cannot be changed via API endpoints. It must be done via GUI (Settings → Model → GPU Offload slider) or `lms` CLI.

### JIT Model Loading & GPU

The `http-server-config.json` setting `justInTimeModelLoading: true` (default) means LM Studio loads the model on first API request and unloads it after inactivity. This is fine for GPU offload — the model still loads with whatever GPU layers were configured — but means there's a ~10s cold-start delay on first request after idle.

To check if JIT is active:
```bash
cat /c/Users/marko/.lmstudio/.internal/http-server-config.json | python -c "import sys,json; d=json.load(sys.stdin); print('JIT:', d.get('justInTimeModelLoading'))"
```

To verify CUDA backend is selected:
```bash
cat /c/Users/marko/.lmstudio/.internal/backend-preferences-v1.json
# Should show: "llama.cpp-win-x86_64-nvidia-cuda-avx2"
```

### Setting Default GPU Offload (GUI)

There is NO API endpoint to change per-model GPU offload settings. To set all models to use maximum GPU:

1. Open LM Studio GUI
2. Click the gear icon (Settings) — either in sidebar bottom-left or top-right
3. Navigate to **Model** or **Loading** tab
4. Set **GPU Offload / GPU Layers** slider to **Maximum** (or -1 for all layers)
5. Apply/Save
6. Each subsequent model load will use these GPU layers by default

`lms load` CLI commands with `--gpu max` also achieve this per-session, but the GUI setting makes it permanent.

## GPU Offload Configuration (CRITICAL)

### Hardware baseline

| Component | Spec |
|-----------|------|
| GPU | NVIDIA GeForce RTX 4070 Laptop GPU |
| VRAM | 4 GB |
| RAM | 32 GB (shared with OS) |

### Offload rules per model size

| Model Size | `--gpu` Value | Expected Result |
|-----------|---------------|-----------------|
| ≤8B (e.g., Dolphin 8B) | `--gpu max` | Full GPU offload, fast inference |
| 14B–32B Q4_K_M (~20 GB) | `--gpu 0.5` | Partial offload (~50% layers), ~59s load time, CPU-bound inference |
| 32B Q5_K_M (~23 GB) | `--gpu 0.5` | Works but SLOW (mostly CPU, ~21.6 GiB RAM) |
| 32B any quant | ❌ `--gpu max` | Failed to load |
| 32B any quant | ❌ `--gpu off` | Failed to load |

### Load command patterns

```bash
# Estimate resource requirements first (safest)
lms load <model-key> --gpu max --estimate-only -y

# Auto-detect (default — no --gpu flag)
lms load <model-key> -y

# Partial GPU offload (recommended for 14B+ models on 4GB VRAM)
lms load <model-key> --gpu 0.5 -y --identifier <short-name>

# Full GPU offload (small models only)
lms load <model-key> --gpu max -y
```

### Key identifier parameter

Always set `--identifier <name>` on load — this becomes the API model name:
```bash
lms load qwen3-32b-obliterated-i1 --gpu 0.5 -y --identifier qwen3-32b
```
API then uses: `"model": "qwen3-32b"` in requests.

### Context length

Default context upon load is 8192. Max depends on model architecture:
```bash
lms load <model> --context-length 16384 -y
```
Maximum for Qwen3-32B: 40960 tokens.

---

## API Server

### Start server

```bash
lms server start --port 1234
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

## Model Swapping

LM Studio serves ONE model at a time via the API. To swap:

1. **Unload current:**
   ```bash
   lms unload <identifier>
   ```
2. **Load new (simple — auto-detects settings for small models ≤8B):**
   ```bash
   lms load <model-key> -y
   ```
   Small models (4-8GB) load in ~10s with auto-detected GPU offload. No `--gpu` or `--identifier` flags needed.

3. **Load new (with GPU offload for 14B+ models):**
   ```bash
   lms load <new-model-key> --gpu <ratio> -y --identifier <name>
   ```

4. **Restart server (REQUIRED — `lms load` does NOT start/restart the API server):**
   ```bash
   lms server start --port 1234
   ```

5. **Verify:**
   ```bash
   lms ps --json
   ```

### Server endpoint after restart

After LM Studio process kill + restart, the auto-detected IP (e.g. `169.254.250.216`) becomes stale. Always use `localhost:1234` after a restart.

---

## Hermes Provider Configuration

For using LM Studio as a Hermes provider:

```bash
# Define the provider
hermes config set providers.lmstudio.base_url "http://localhost:1234/v1"
hermes config set providers.lmstudio.api_key ""

# Set as active provider (model name = lms --identifier value)
hermes config set model "lmstudio/qwen3-32b"
hermes config set provider "lmstudio"
```

---

## GUI-Based Model Switching (Mouse/Keyboard)

When using mouse/keyboard to switch models in LM Studio's GUI window:

### Finding the LM Studio Window

LM Studio is an Electron app (`Chrome_WidgetWin_1`). UIA sees it as `Pane`, not `Window`:

```bash
# UIA search — works if window is visible:
python hermesmouse.py element "LM Studio" list
# → "[ControlType.Pane] \"Chrome Legacy Window\" ..."
```

**Known window geometry (from session 14-Jun-2026):**
```
Sol: 708  Üst: 20  Sağ: 1540  Alt: 906
Genişlik: 832  Yükseklik: 886
```
These coordinates are for a ~832x886 window positioned center-left on a 1920x1200 display. Use them for:
- Cropping screenshots before OCR: `img.crop((708, 20, 1540, 906))`
- Targeting mouse clicks at known UI regions within the window

### OCR (Tesseract) ile Model Seçme (Önerilen)

UIA element ağacı kapalı olduğu için OCR ile metin bulma kullanılır:

```bash
# Önce LM Studio'nun pencere konumunu öğren (global.json'dan)
# Varsayılan: ~x=709-1534, y=22-896

# Tüm metinleri listele (LM Studio bölgesinde)
python hermesmouse.py ocr-list --region 886 27 1037 1098

# Belirli metni bul
python hermesmouse.py ocr-find "Dolphin" --region 886 27 1037 1098

# Metne tıkla
python hermesmouse.py ocr-click "Select a model" --region 886 27 1037 1098
```

**Bağımlılık:** Tesseract 5.5.0+ kurulu olmalı:
```powershell
winget install tesseract-ocr.tesseract
```

### Workflow: OCR ile Model Değiştirme (Adım Adım)

```bash
# 1. "Select a model" butonuna tıkla
python hermesmouse.py ocr-click "Select a model"

# 2. Arama kutusuna dolphin yaz
python hermesmouse.py type "dolphin"

# 3. Dolphin modeline tıkla (arama sonucu)
python hermesmouse.py ocr-click "Dolphin"

# 4. "Load Model" butonuna tıkla (varsa)
python hermesmouse.py ocr-click "Load"
```

### When GUI Is Hidden (Arka Planda Çalışıyor)

LM Studio server can run with GUI minimized to system tray. If API is accessible, use `lms` CLI instead:

```bash
# See running models
lms ps --json

# Load new model via CLI (may need server restart)
lms load cognitivecomputations.dolphin3.0-llama3.1-8b --gpu max -y --identifier dolphin-8b

# Restart server
lms server start --port 1234
```

### GUI'yi Açmak İçin Yeniden Başlatma

```bash
taskkill /F /IM "LM Studio.exe"
sleep 2
start "" "C:\\Users\\marko\\AppData\\Local\\Programs\\LM Studio\\LM Studio.exe"
sleep 8   # GUI'nin açılmasını bekle
```

### Vision Not Available Fallback

When active Hermes model doesn't support `vision_analyze` (confirmed: DeepSeek V4 Flash via nous provider does NOT support vision — `unknown variant 'image_url', expected 'text'` hatası):

- **This is a model limitation, not a tool bug** — the error `unknown variant 'image_url'` means the model only accepts text inputs
- Use Ollama's local vision model (llava-llama3) via `screen-vision-analiz` skill for screenshot analysis
- Or use window config bounds + coordinate-approximation for clicks
- Or use `lms` CLI for model ops instead of GUI automation
- Or ask the user to describe what they see on screen
- Or switch Hermes provider to a vision-capable model temporarily

## Troubleshooting

### "Failed to load model" with all offload settings

Try `--gpu 0.5` specifically — both `--gpu max` and `--gpu off` may fail for large models on limited VRAM.

### Model loads but inference is extremely slow

Check RAM usage — if >90% of physical RAM is consumed by the model, swap pressure causes slowdowns.
Solution: Use a smaller quant (Q4_K_S instead of Q5_K_M) or a smaller base model (8B–14B range).

### "Failed to load model" with no detail

Model file may be corrupted. Check with:
```bash
sha256sum "/path/to/model.gguf"
```
Compare with expected hash from HuggingFace.

### `lms import` hangs on "Attempting to find the model on Hugging Face"

The import tool does a reverse lookup on HuggingFace that can hang. Kill it and manually copy the GGUF file to the models directory instead.

### GGUF version mismatch

LM Studio 0.4.16 uses llama.cpp 2.22.0 which supports GGUFv3. Newer GGUF formats may require a runtime update:
```bash
lms runtime update
```

---

- **LM Studio has NO API endpoints for GPU/config changes** — `/api/*` endpoints and `POST /v1/models/load` all return errors. Config changes MUST go through GUI (Settings) or `lms` CLI.
- **DeepSeek V4 Flash has no vision** — `vision_analyze` returns `unknown variant 'image_url'` because the model is text-only. Don't retry; switch provider or use Ollama vision model.
- **Two skills overlap: `lm-studio` and `lm-studio-local-llm`** — `lm-studio` is a Turkish summary, `lm-studio-local-llm` is the canonical English reference with more detail and linked files. Prefer `lm-studio-local-llm` for operations.
- **JIT mode causes cold start delay** — first API request after idle takes ~10s to load model into GPU memory. Subsequent requests are fast until idle timeout.

## Pitfalls

- **`--gpu max` silently fails for large models** — always test with `--estimate-only` first
- **`--gpu off` (CPU-only) also fails for some large models** — the GPU runtime seems required even for partial offload
- **Reasoning models need higher `max_tokens`** — first response is often empty with just `reasoning_content`
- **Always set `--identifier`** — without it, API uses the full indexed model key which is harder to type
- **Server must be restarted after model swap** — running `lms load` alone doesn't update the server
- **Model name in API ≠ GGUF filename** — LM Studio normalizes names (lowercase, removes quant suffix). Check with `/v1/models`
- **QT quantification (i1, iMATRIX) names are preserved** — `obliterated.i1` stays in the model key
- **`lms` CLI is NOT installed by default** — `settings.json` has `cliInstalled: false`. When `lms` commands fail with "command not found", check if the CLI was installed separately. LM Studio GUI does NOT auto-install the CLI tool; it must be done via `Settings > Developer > Install lmstudio CLI` or by running the bundled `lms.exe` from `~/.lmstudio/bin/lms.exe`
- **Electron GUI is opaque to UIA automation** — LM Studio uses `Chrome_WidgetWin_1` class. `uiautomation` and `hermesmouse.py element` can find the window but cannot enumerate or click internal UI elements (model lists, buttons, text fields). For programmatic model switching, always prefer `lms load` CLI over GUI automation.
- **GUI model switching için OCR kullan** — fare/klavye ile model değiştirmek gerekiyorsa `hermesmouse.py ocr-find/ocr-click` kullan (Tesseract gerekli). Önce `ocr-list` ile görünür metinleri tara, sonra hedef metne tıkla.
- **Server IP changes after restart** — `169.254.250.216` is an auto-assigned IP that goes stale after process restart. Always default to `localhost:1234` after restarting LM Studio.
