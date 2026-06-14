# GPU Offload GUI Configuration — 14 June 2026

## Goal
Configure all LM Studio models to use GPU (NVIDIA RTX 4070, 4GB VRAM) for inference via GUI settings.

## Active Model
- Provider: custom (nous)
- Model: stepfun/step-3.7-flash:free (DeepSeek V4 Flash variant)
- **No vision support** — vision_analyze fails with `unknown variant 'image_url'`

## LM Studio State

### Window Geometry (1920x1200 display)
```
Sol: 708  Ust: 20  Sag: 1540  Alt: 906
Genislik: 832  Yukseklik: 886
```

### Installed Models
1. `dolphin-8b` (active on API)
2. `qwen3-32b-obliterated-i1`
3. `cognitivecomputations.dolphin3.0-llama3.1-8b`
4. `text-embedding-nomic-embed-text-v1.5` (embedding)

### Backend
- Engine: `llama.cpp-win-x86_64-nvidia-cuda-avx2` v2.22.0
- CUDA support: confirmed via `internal-engine-index.json`
- JIT model loading: enabled (`justInTimeModelLoading: true`)

### API Endpoints Tested (all FAIL)
| Endpoint | Method | Result |
|----------|--------|--------|
| `/api/models` | GET | `Unexpected endpoint or method` |
| `/api/active-model` | GET | `Unexpected endpoint or method` |
| `/api/server/status` | GET | `Unexpected endpoint or method` |
| `/v1/models/load` | POST | `Unexpected endpoint or method` |
| `/api` | GET | `Unexpected endpoint or method` |

**Conclusion:** LM Studio has NO API for GPU/config changes. Config MUST go through GUI or `lms` CLI.

## GUI Configuration Attempts

### Attempt 1: Ctrl+, (Settings shortcut)
- Electron standard shortcut for Preferences
- `SendKeys::SendWait("^{,}")` → Settings opened successfully

### Attempt 2: Click "Model" category (sidebar)
- Coordinates: (743, 125) — estimated sidebar center + 2nd category
- `pyautogui.click(743, 125)` → uncertain if correct

### Attempt 3: OCR via Tesseract
- Tesseract 5.5.0 installed at `C:\Program Files\Tesseract-OCR\`
- Pre-processing chain: crop → 4x upscale → invert → contrast×3 → sharpen → OTSU threshold
- **Result: FAIL** — Tesseract reads Windows Terminal text behind LM Studio, NOT LM Studio UI elements
- Sidebar labels, settings panel text, GPU Offload label — all undetectable
- Root cause: Electron web-rendered dark-theme UI with small custom fonts

### Attempt 4: Keyboard navigation in Settings
- `pyautogui.press('tab', presses=5)` → navigate to GPU Offload slider
- `pyautogui.press('right', presses=20)` → slide to maximum
- `pyautogui.press('enter')` → apply
- `pyautogui.press('escape')` → close settings
- **Result:** Uncertain — no feedback mechanism without vision

### Attempt 5: Screenshot-based OCR variants
- Inverted image: picks up terminal text
- BW threshold: picks up terminal text  
- Cropped to LM Studio only (708,20,1540,906): still terminal background interference
- Sol panel only (708,20,900,906): no sidebar labels detected
- 8x upscale of sidebar: only "ws PowerShell" and "Vindows decide" (terminal bleed)

## Key Findings

1. **Tesseract CANNOT read Electron dark-theme UI.** Pre-processing doesn't help. The font rendering and color scheme are fundamentally incompatible with Tesseract's training.
2. **LM Studio has no GPU config API.** Don't waste time on `/api/*` or `/v1/models/load` endpoints.
3. **Keyboard navigation is the best fallback** when vision is unavailable. Tab through form elements, use arrow keys on sliders.
4. **`lms` CLI is the ONLY reliable programmatic path.** `lms load <model> --gpu max -y --identifier <name>` works when GUI automation fails.
5. **Two skills overlap:** `lm-studio` (Turkish summary) and `lm-studio-local-llm` (English, canonical). Prefer the latter.
