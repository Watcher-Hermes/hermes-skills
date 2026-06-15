---
name: reymen-proje-mimarisi
title: R>eYMeN Proje Mimarisi
description: R>eYMeN otonom ReAct ajaninin mimarisi, dosya yapisi ve entegrasyon noktalari
tags: [hermes, reymen, react, architecture]
audience: maintainer
---

# R>eYMeN Proje Mimarisi

61 Python dosyasi, 423 skill, 4 entegre modul.

## Kritik Noktalar
- .env → 16 degisken, cift yonlu senkronizasyon
- FileLock → JSON yazma yarisi korumasi
- Fallback zinciri → otomatik provider siralamasi
- Tekrar korumasi → ayni eylem 2. kez loop keser
- **init siralamasi**: `self.learning` gibi attribute'ler once tanimlanmali, sonra kullanilmali. Aksi halde AttributeError.
- **Side-by-side mimari**: R>eYMeN ve Hermes Agent ic ice gecmez, yan yana calisir. Her bilesen kendine ozgu (kendi CLI, kendi motor, kendi dashboard).

## Batch Runner Deseni
`batch_runner.py` — paralel toplu gorev isleme:
- `SonucYoneticisi`: thread-safe, checkpoint'li, JSONL cikti
- `paralel_calistir()`: threading.Queue ile thread havuzu
- `gorev_isle()`: AIAgentOrchestrator cagrisi
- `hedefleri_yukle()`: .txt / .jsonl parser
- CLI: --dosya, --hedefler, --paralel, --cikti, --sessiz

## Kod Kalitesi (Claude 4.8 karsilastirmasi)
- Her fonksiyonda try/except
- Her fonksiyonda docstring
- Renkli terminal ciktisi (Renk sinifi)
- Her modulde CLI (argparse + --help)
- Butunsel: ozellik + test + dokumantasyon bir arada

## Calistirma
```
reyemen.bat start | agent | doctor | hermes ...
```

## Referanslar
- `references/hermes-feature-porting.md` — Hermes'ten ozellik ekleme deseni
