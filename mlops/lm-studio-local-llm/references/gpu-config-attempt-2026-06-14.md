# LM Studio GPU Config Attempt — 14 Jun 2026

## Goal
Configure all models in LM Studio to use GPU (NVIDIA CUDA) for faster inference.

## Current State
- Backend: `llama.cpp-win-x86_64-nvidia-cuda-avx2` (NVIDIA CUDA)
- JIT model loading: ON (`justInTimeModelLoading: true`)
- `lms` CLI: NOT installed (`cliInstalled: false`)
- Active model: `dolphin-8b`
- `lms` not in PATH

## What Was Tried

### 1. API endpoints — ALL FAILED
```bash
GET  /api/models          → "Unexpected endpoint"
GET  /api/active-model    → "Unexpected endpoint"
GET  /api/server/status   → "Unexpected endpoint"
POST /v1/models/load      → "Unexpected endpoint"
```

### 2. GUI Automation (blind)
- Sent `Ctrl+,` to open settings (confirmed: settings opened)
- Clicked at `(743, 125)` for "Model" category in settings sidebar (approximately)
- Dragged slider at `(950, 180)` → `(1400, 180)` (approximately)

**Problem:** Could not confirm if clicks hit the right targets because:
- DeepSeek V4 Flash has NO vision support (`unknown variant 'image_url'`)
- Tesseract OCR returned garbled output (dark theme + overlapping windows)

### 3. Tesseract OCR (partial success)
Tesseract 5.5.0 is installed at `C:\Program Files\Tesseract-OCR\tesseract.exe`
OCR of the full LM Studio window region was garbled — dark UI theme confused Tesseract.

## Known Working Method (not attempted this session)
GUI: Settings → Model tab → GPU Offload slider → Maximum
CLI: If `lms` were installed: `lms load <model> --gpu max -y`

## Key Files (under `~/.lmstudio/`)
| File | Purpose |
|------|---------|
| `.internal/backend-preferences-v1.json` | CUDA backend confirmed |
| `.internal/http-server-config.json` | JIT mode, port 1234 |
| `settings.json` | App settings, `cliInstalled: false` |
| `.internal/model-data.json` | dolphin-8b & qwen3-32b load timestamps |
