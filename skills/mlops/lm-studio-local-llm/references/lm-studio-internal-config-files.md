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