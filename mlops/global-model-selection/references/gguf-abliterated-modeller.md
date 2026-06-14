# GGUF / Abliterated Yerel Model Alternatifleri

Benchmark'taki API modellerinin Ollama/LM Studio'da çalışan GGUF alternatifleri.

## Abliterated (Sansürsüz) Modeller

| Model | GGUF Linki | Boyut | Quant |
|-------|-----------|-------|-------|
| Qwen3-32B | `mradermacher/Qwen3-32B-abliterated-GGUF` | ~17 GB | IQ4_XS (default) |
| Qwen3-32B (Q4) | `mradermacher/Qwen3-32B-abliterated-GGUF:Q4_K_M` | ~20 GB | Q4_K_M |
| Qwen3-32B (i1) | `mradermacher/Qwen3-32B-abliterated-i1-GGUF` | ~17 GB | IQ4_XS |
| Kaynak ST | `roslein/Qwen3-32B-abliterated` | 65.5 GB | safetensors (14 dosya) |

## Ollama'ya Çekme

```bash
ollama pull hf.co/mradermacher/Qwen3-32B-abliterated-GGUF
# veya Q4_K_M
ollama pull hf.co/mradermacher/Qwen3-32B-abliterated-GGUF:Q4_K_M
```

## LM Studio'ya Yükleme

1. GGUF'u indir → `curl -L -o qwen3-32b-ab.Q4_K_M.gguf https://huggingface.co/mradermacher/Qwen3-32B-abliterated-GGUF/resolve/main/Qwen3-32B-abliterated.Q4_K_M.gguf`
2. `%USERPROFILE%\.lmstudio\models\` klasörüne kopyala
3. LM Studio'yu yeniden başlat

## Benchmark Karşılıkları

| API Modeli | Yerel GGUF Alternatifi | Performans Tahmini |
|-----------|----------------------|-------------------|
| Qwen Plus (3206 Elo) | qwen3:32b (abliterated) | ~%75-85 |
| DeepSeek V4-Pro | deepseek-r1:32b / qwen3:32b | ~%60-70 |
| Gemini 3.1 Pro | gemma3:27b | ~%55-65 |
