---
name: hibrit-ai-yonlendirme-kurali
title: "Hibrit AI Yönlendirme Kuralı"
description: "Sorgu uzunluğuna ve içeriğine göre Ollama (yerel) veya DeepSeek (uzak) arasında otomatik yönlendirme kuralları."
tags: [routing, model-selection, ollama, deepseek, fallback]
audience: user
related_skills: [hibrit-ai-mimarisi, dolphin-llama3]
---

# Hibrit AI Yönlendirme Kuralı

## Ana Kural

| Koşul | Hedef | Açıklama |
|-------|-------|----------|
| <40 kelime, basit sorgu | **Ollama** (dolphin-llama3) | Hızlı, ücretsiz, offline |
| ≥40 kelime veya "analiz/kod/tasarla" içerir | **DeepSeek** (deepseek-chat) | Yüksek kalite, güçlü analiz |
| DeepSeek bağlantısı koparsa | **Ollama** (otomatik fallback) | Kesintisiz hizmet |

## Tetikleyici Kelimeler (DeepSeek'e yönlendirir)
- `analiz`, `analiz et`
- `kod`, `kodla`, `yaz (kod)`
- `tasarla`, `tasarım`
- Uzun metin (>40 kelime) içeren her sorgu
- Çok adımlı planlama gerektiren işler

## Fallback Mekanizması

```
1. Varsayılan: DeepSeek
2. API hatası / timeout / bağlantı hatası → Ollama
3. Ollama da hata verirse → hata raporla, kullanıcıya bildir
```

## Kullanıcı Deneyimi

Kullanıcı farkına varmaz — geçiş otomatiktir.
Sadece her iki model de çökerse bildirim gönderilir.
