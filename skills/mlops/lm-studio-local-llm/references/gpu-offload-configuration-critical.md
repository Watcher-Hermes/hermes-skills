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