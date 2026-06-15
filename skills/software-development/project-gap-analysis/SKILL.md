---
name: project-gap-analysis
title: "Proje Eksiklik Analizi"
description: >-
  Analyze a project by examining its file structure, code, configs, and
  environment — then compare against a target system to identify gaps
  systematically. Output: prioritized action plan with categories.
version: 1.0.0
tags: [planning, analysis, project, audit, migration]
platforms: [windows]
audience: contributor
---

# Proje Eksiklik Analizi

## Ne Zaman Kullanılır

- Kullanıcı bir projeyi inceleyip eksiklerini sormak istediğinde
- Bir projeyi başka bir sisteme (Hermes Agent, referans proje) benzetmek gerektiğinde
- Kullanıcı "bunun eksikleri neler" veya "tamamlanınca nasıl olur" dediğinde
- Mevcut bir projeyi yükseltmek/port etmek için plan yapılırken

## Adım Adım

### Adım 1: Proje Yapısını Çıkar

Önce projenin fiziksel dosya yapısını tam olarak al:

```bash
# Klasör yapısı (derinlemesine)
ls -laR "PROJE_YOLU/" 2>&1

# Sadece .py dosyaları (boyutlarıyla)
ls -la "PROJE_YOLU/"*.py 2>&1
```

**ÖNEMLİ — Çift iç içe geçme kontrolü:** ZIP'ten çıkarılan projelerde sık görülür.
`C:\proje\proje\` şeklinde gereksiz bir katman varsa, doğru yapı `C:\proje\` olmalıdır.
Kontrol et:

```bash
ls -la "C:\proje\" 2>&1
# Eğer içinde sadece 1 klasör varsa ve adı projeyle aynıysa → çift iç içe geçmiş
```

**ZIP içeriğini kontrol et:** Projede `.zip` dosyası varsa içinde ne olduğuna bak:

```bash
unzip -l "dosya.zip" 2>&1
```

### Adım 2: Kilit Dosyaları Oku

Her projede mutlaka okunması gerekenler:
- `README.md` — proje ne işe yarar, sürüm geçmişi
- Ana giriş dosyası (`main.py`, `app.py`, `cli.py`)
- Config/ayar dosyaları (`.env`, `config.yaml`, `config.json`)
- Bağımlılıklar (`requirements.txt`, `pyproject.toml`)
- Proje talimatı (`CLAUDE.md`, `PROJE_REHBERI.md`, `AGENTS.md`)
- Kimlik/ajan dosyası (`SOUL.md`, kullanıcı varsa)

Her dosyayı `read_file()` ile oku, içeriğini anla.

### Adım 3: Karşılaştırma Yap

**ÖNCE ŞUNU NETLEŞTİR: Aynı sistemi mi karşılaştırıyoruz?**
Kullanıcı "şunu şuna benzet" dediğinde, ikisinin aynı yazılım mı yoksa farklı projeler mi olduğunu kontrol et:

- Aynı kaynaktan türemiş (fork/kopya) mı?
- İsim benzer ama kod tabanı farklı mı? (ör: R>eYMeN ≠ Nous Hermes Agent)
- Biri diğerinin etrafına yazılmış yardımcı araçlar mı?
- Bunu netleştirmezsen yanlış karşılaştırma yaparsın.

Kategorileri netleştirdikten sonra hedef sistem (ör: Hermes Agent) ile mevcut projeyi şu başlıklarda karşılaştır:

| Kategori | Neye Bak |
|----------|----------|
| **Çalıştırma** | LLM provider, API anahtarları, bağımlılıklar kurulu mu? |
| **Konfigürasyon** | .env var mı? Config dolu mu? |
| **CLI** | Komut satırı arayüzü var mı? Kaç alt komut? |
| **Provider** | Kaç LLM destekleniyor? Fallback var mı? |
| **Gateway** | Telegram, Discord, Web, SMS — hangi kanallar var? |
| **MCP** | Model Context Protocol desteği var mı? |
| **Skill/Beceri** | Kaç beceri var? Kategorize edilmiş mi? FTS5 indeksli mi? |
| **Hafıza** | Kalıcı/vektörel/oturum hafızası dolu mu? |
| **Güvenlik** | HITL, PII filtresi, circuit breaker, rate limit? |
| **Plugin** | Dışarıdan eklenti yükleme var mı? |
| **Test** | Test dosyası, CI/CD var mı? |

Detaylı karşılaştırma şablonu → [references/3-system-comparison.md](references/3-system-comparison.md)

### Adım 4: Eksikleri Kategorize Et

Her eksik için öncelik seviyesi ata:

| Öncelik | Anlamı |
|---------|--------|
| **[KRITIK]** | Proje çalışmaz, hemen düzeltilmeli |
| **[BUYUK]** | Önemli özellik eksik, çalışmayı etkiler |
| **[ORTA]** | İyileştirme, olmazsa olmaz değil |
| **[KUCUK]** | Bonus özellik, sonra eklenebilir |

### Adım 5: Rapor Dosyası Oluştur

Masaüstüne `eksiklikler.txt` olarak yaz. İçinde:

```
═══════════════════════════════════════════
EKSİKLİKLER — TAM LİSTE (TARIH)
═══════════════════════════════════════════

A. BASLIK 1 — Alt Başlık
───────────────────────────────

[KRITIK] A1. madde
   - detay
   - detay
   - Cozum: ne yapılmalı

[BUYUK] A2. madde
   ...

B. BASLIK 2
...

───────────────────────────────
YAPILACAKLAR SIRALAMASI
───────────────────────────────

ONCELIK 1 (Hemen):
  1. ...
ONCELIK 2 (1-2 gun):
  4. ...
ONCELIK 3 (1 hafta):
  7. ...
```

Rapor yolunu `C:\Users\marko\OneDrive\Desktop\eksiklikler.txt` olarak kullan (OneDrive masaüstü, asla `Desktop` kısayolu değil).

### Adım 6: Özeti Kullanıcıya Sun

Özet olarak şunları söyle:
- Kaç eksik bulundu (her kategoride)
- En kritik 2-3 madde
- En kısa yol (alternatif varsa)
- "Ne zaman dönersen başlarız"

## Pitfalls

1. **Yüzeysel analiz** — Sadece dosya isimlerine bakıp geçme. Her kilit dosyayı oku.
2. **Önceliksiz liste** — 25 maddeyi önceliksiz sıralarsan kullanıcı nereden başlayacağını bilemez. Her zaman KRITIK > BUYUK > ORTA > KUCUK sırala.
3. **Alternatif yolu atlama** — Bazen en kısa çözüm mevcut sistemi değiştirmek değil, başka bir sistemi adapte etmektir. Bunu da belirt.
4. **OneDrive masaüstü yolu** — Doğru yol: `C:\Users\marko\OneDrive\Desktop\`, asla `C:\Users\marko\Desktop\` kullanma.
