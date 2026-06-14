---
created: 2026-06-14
status: done
tags: [lm-studio, api, benchmark, kazanim, gpu]
---

# LM Studio API Kullanım Kazanımı

## Sistem
- **LM Studio**: v0.4.16.0
- **GPU**: NVIDIA RTX 4070 Laptop (8GB VRAM)
- **Backend**: llama.cpp CUDA (CUDA 12.2)
- **API Port**: localhost:1234

## Doğrulanmış API Parametreleri

| Parametre | Durum | Açıklama |
|-----------|-------|----------|
| `model` | ✅ Zorunlu | API key alanı, GGUF dosya adı DEĞİL |
| `context_length` | ✅ | 32768 = LLaVA 7B tam kapasite |
| `flash_attention` | ✅ | true/false |
| `echo_load_config` | ✅ | true = config dönüşü görülür |

## REDDEDİLEN Parametreler (bu derlemede)

| Parametre | Hata | Çözüm |
|-----------|------|-------|
| `gpu`, `gpu_layers`, `num_gpu_layers`, `ngl` | Unrecognized key | GUI: Settings > Model Defaults |
| `parallel` | Unrecognized key | Varsayılan n_parallel=4 yeterli |
| `offload_kv_cache_to_gpu` | Unrecognized key | Varsayılan açık |
| `settings` (obje) | Unrecognized key | Düz parametre ver |

## Doğru Çalışan Komut

```bash
curl -s -X POST http://localhost:1234/api/v1/models/load \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llava-v1.6-mistral-7b",
    "context_length": 32768,
    "flash_attention": true,
    "echo_load_config": true
  }'
```

## Model Key'leri

| Model | Key |
|-------|-----|
| Dolphin 8B | `cognitivecomputations.dolphin3.0-llama3.1-8b` |
| LLaVA 7B | `llava-v1.6-mistral-7b` |
| Qwen3 32B | `qwen3-32b-obliterated-i1` |
| Nomic Embed | `text-embedding-nomic-embed-text-v1.5` |

## Varsayılan GPU Ayarları

- CUDA backend: llama.cpp CUDA ✅
- Flash Attention: açık ✅
- KV Cache GPU: açık ✅
- parallel: 4 ✅
- VRAM: ~5.7GB / 8.2GB (LLaVA 7B ile)

## Altın Kural

> GPU offload = GUI'den, context + flash_attention = API'den.
