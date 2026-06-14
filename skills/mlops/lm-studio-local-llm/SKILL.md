---
name: lm-studio-local-llm
title: "LM Studio API ile Model Yükleme"
description: "LM Studio v0.4.16.0 REST API ile model yükleme, GPU offload (GUI), context ve flash_attention ayarları. Doğrulanmış curl komutları."
version: 2.0.0
platforms: [windows]
audience: user
tags: [lm-studio, api, model-load, gpu, cuda, gguf, local-llm]
---

# LM Studio API ile Model Yükleme

## API ile Model Yükleme

**LM Studio v0.4.16.0** — API kabul edilen parametreler:

| Parametre | Değer | Durum |
|-----------|-------|--------|
| `model` | Model key (zorunlu) | ✅ |
| `context_length` | 8192, 32768 (max) | ✅ |
| `flash_attention` | true/false | ✅ |
| `echo_load_config` | true (config dönüşü) | ✅ |
| `gpu`, `parallel`, `offload_kv_cache_to_gpu` | — | ❌ Bu derlemede tanınmaz |

```bash
# Dogru komut — context tam kapasite
curl -s -X POST http://localhost:1234/api/v1/models/load \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llava-v1.6-mistral-7b",
    "context_length": 32768,
    "flash_attention": true,
    "echo_load_config": true
  }'
```

## Önemli Notlar

- `context_length: 32768` = modelin tam kapasitesi (LLaVA 7B, n_ctx_train=32768). 8192 verirsen `"n_ctx_seq (8192) < n_ctx_train (32768)"` uyarısı alırsın
- `gpu` parametresi bu derlemede yok. **GPU offload ayarı sadece GUI'den yapılır:** Settings > Model Defaults > GPU Offload slider
- `parallel` ve `offload_kv_cache_to_gpu` API'de yok ama gerek yok — varsayılan olarak `n_parallel=4` ve KV cache otomatik yönetilir
- `echo_load_config: true` eklenirse yanıtta `load_config` altında nihai konfigürasyon görünür

## Model Key'leri

```bash
curl -s http://localhost:1234/api/v1/models/ | python3 -c "import sys,json; [print(m['key']) for m in json.load(sys.stdin)['models']]"
```

| Model | Key |
|-------|-----|
| Dolphin 8B | `cognitivecomputations.dolphin3.0-llama3.1-8b` |
| LLaVA 7B | `llava-v1.6-mistral-7b` |
| Qwen3 32B | `qwen3-32b-obliterated-i1` |
| Nomic Embed | `text-embedding-nomic-embed-text-v1.5` |

## GPU Durumu

```
GPU: NVIDIA RTX 4070 Laptop (8GB VRAM)
Backend: llama.cpp CUDA
VRAM kullanimi: ~5.7GB / 8.2GB (LLaVA 7B ile)
```

Doğrulama: `nvidia-smi` veya `curl -s http://localhost:1234/api/v1/models/`

## Kazanım

Bu öğrenimle elde edilenler:
1. LM Studio REST API'si (v0.4.16.0) sadece `model`, `context_length`, `flash_attention`, `echo_load_config` parametrelerini kabul eder
2. GPU offload API'den yapılamaz, GUI'den yapılır
3. Model key = API'deki `key` alanı, GGUF dosya adı değil
4. `echo_load_config: true` ile yüklenen config görülebilir
5. Varsayılan GPU ayarları: CUDA, flash_attention açık, KV cache GPU'da, parallel=4
