# Qwen3-32B-obliterated.i1-Q5_K_M — Test Report

**Test Date:** 13 June 2026
**Hardware:** RTX 4070 Laptop GPU (4GB VRAM), 32GB RAM
**LM Studio:** 0.4.16-2
**Runtime:** llama.cpp 2.22.0 (CUDA)

## Model Details

- **Model:** mradermacher/Qwen3-32B-obliterated-i1-GGUF
- **Quant:** Q5_K_M
- **File size:** 23.2 GB
- **GGUF version:** 3
- **SHA256:** `***REMOVED-BASE64***`

## Load Attempts

| Config | Result | Time | RAM Usage |
|--------|--------|------|-----------|
| `--gpu max` | ❌ Failed to load | N/A | N/A |
| `--gpu off` | ❌ Failed to load | N/A | N/A |
| `--gpu 0.5` | ✅ Loaded | 59.16s | 21.62 GiB |

**Estimate (--gpu max --estimate-only):** 787 MiB GPU, 22.40 GiB total

## Inference Test

- First API call: Reasoning content visible (`reasoning_content`), but `finish_reason: "length"` at 100 tokens (98 went to reasoning)
- Second call (200 tokens): Timed out at 120s — model too slow on CPU
- Third call (50 tokens): Timed out at 60s

**Conclusion:** 32B Q5_K_M on RTX 4070 4GB works technically but is impractically slow for interactive use. Most computation runs on CPU.

## Recommendation

Use models ≤14B on this hardware for usable speeds. 32B models only for batch/background processing where latency doesn't matter.
