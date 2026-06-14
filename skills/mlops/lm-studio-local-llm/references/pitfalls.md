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