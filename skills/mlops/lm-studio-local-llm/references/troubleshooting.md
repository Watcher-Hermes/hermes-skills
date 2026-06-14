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