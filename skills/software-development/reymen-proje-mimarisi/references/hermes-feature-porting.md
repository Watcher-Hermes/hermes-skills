# Hermes Feature Porting — R>eYMeN'e Ekleme Deseni

Hermes Agent'dan R>eYMeN'e ozellik eklerken izlenecek adimlar.

## Porting Siralamasi
1. **Buyuk ozellikler** once: CLI, Web, MCP, Provider, Plugin
2. **Mevcut kodu guncelle**: mevcut modulleri iyilestir
3. **Test + kurulum**: test_suite.py, setup_keys.py
4. **Runtime + context**: ajan runtime, trajectory compressor

## Her Modul Icin Standart

| Bilesen | Gerekli |
|---------|---------|
| Docstring | Dosya basi + her fonksiyon |
| try/except | Her dis baglantili islemde |
| CLI | En az --help, argparse |
| __main__ | Test blogu |
| Hata mesaji | Anlamli, ne yapilmasi gerektigini soyleyen |

## Mevcut Providerlar (23 adet)
Yerel: lmstudio, ollama, vllm, xinference, litellm
Bulut: deepseek, openai, anthropic, groq, together, mistral, cohere, perplexity, fireworks, openrouter, google, azure, huggingface, nvidia, alibaba, moonshot, zhipu, anyscale

## R>eYMeN'e Ozgu Olmali
- Direkt Hermes kopyasi degil, R>eYMeN kimligine uygun
- Turkce hata mesajlari
- Basit, hafif, Windows odakli
