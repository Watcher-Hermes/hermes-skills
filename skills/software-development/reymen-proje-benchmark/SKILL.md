---
name: reymen-proje-benchmark
title: R>eYMeN Proje Benchmark
description: "R>eYMeN projesinin memory benchmark sonuclari: 63 dosya, 8989 satir, 0 hata, 12/12 import"
tags: [benchmark, metrics, quality]
audience: maintainer
---

# R>eYMeN Proje Benchmark

## Metrikler (15 Haziran 2026)

| Metrik | Deger |
|--------|-------|
| Python dosyasi | 63 |
| Toplam satir | 8.989 |
| Kod boyutu | 328 KB |
| Derleme hatasi | 0 |
| Derleme suresi | 0.034s |
| Import basarisi | 12/12 |
| CLI --help | 0.066s |
| Skill dosyasi | 423 |
| Env dolu | 9/16 |

## Modul Durumu

| Modul | Satir | Import | Durum |
|-------|-------|--------|-------|
| main.py | 321 | ✅ | ReAct dongusu |
| beyin.py | 212 | ✅ | LM Studio + fallback |
| reyment.py | 935 | ✅ | Profesyonel CLI |
| web_ui.py | 998 | ✅ | Web arayuzu |
| gateway_runner.py | 766 | ✅ | 4 kanal |
| mcp_serve.py | 304 | ✅ | MCP Server |
| kanban_orch.py | 421 | ✅ | Kanban tahtasi |
| batch_runner.py | 215 | ✅ | Toplu islem |
| self_improve.py | 183 | ✅ | Oz gelistirme |
| plugin_loader.py | 106 | ✅ | Plugin sistemi |
| start.py | 497 | ✅ | Orkestrator |

## Karsilastirma (Hermes vs Claude 4.8)

| Kriter | Hermes (ben) | Claude 4.8 |
|--------|-------------|------------|
| Yaklasim | Odakli patch, tek sorun | Butunsel, ozellik+CLI+hata |
| try/except | Sadece ana kodda | Her fonksiyonda |
| Docstring | Atlar | Her yerde |
| CLI | Ayri dosyada | Her modulde |
| Renkli cikti | Yok | Renk sinifi |

## Kazanim

- 63 dosya, 0 hata -> sistem saglikli
- 12/12 import -> moduller arasi baglanti tam
- CLI 0.066s -> hizli baslatma
- Eksik: 7 env anahtari, ACP, plugins/ klasoru bos
