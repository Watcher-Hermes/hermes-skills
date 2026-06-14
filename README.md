# Hermes Skills Kütüphanesi

Hermes Agent için **1.038 modüler skill** içeren ana kütüphane. Router+Reference yapısıyla sıfır şişkinlik — her skill en fazla 3-4 KB.

## İstatistikler

| Metrik | Değer |
|--------|-------|
| Toplam SKILL.md | **1.038** |
| Reference dosyası | **4.476** |
| Kategori | **530** |
| Şişkin skill | **0** |
| Audience: USER | 695 |
| Audience: CONTRIBUTOR | 288 |
| Audience: MAINTAINER | 51 |

## Kategori Yapısı

```
skills/
├── ecc/              (262) — Kod geliştirme pattern'leri
├── windows-automation/ (43) — Windows otomasyon skill'leri
├── software-development/ (34) — Geliştirme araçları
├── mlops/             (26) — Model yönetimi, inference, benchmark
├── productivity/      (26) — PDF, OCR, kamera, clipboard
├── autonomous-ai-agents/ (23) — Otonom ajan döngüleri
├── creative/          (22) — ASCII art, diyagram, video, müzik
├── user-preferences/  (17) — Kullanıcı profili ve model ayarları
├── devops/            (13) — Backup, cron, kanban, migration
├── note-taking/       (12) — Obsidian, Notion entegrasyonu
├── security/          (10) — Pentest, tersine mühendislik
├── media/              (8) — YouTube, Spotify, GIF
├── research/           (8) — Arxiv, paper, polymarket
├── gaming/             (6) — Oyun otomasyonu
├── github/             (6) — PR, issue, repo yönetimi
├── apple/              (5) — macOS, iOS, iMessage
├── data-science/       (3) — Jupyter, HuggingFace
├── windows-system-automation/ (2) — Kamera, güvenlik izleme
├── ...               (500+) — Her biri tek konulu özel skill
```

## Skill Yapısı

Her skill `SKILL.md` (Router) + `references/` (detaylar) formatındadır:

```
skills/kategori/skill-adi/
├── SKILL.md                  ← Router (≤ 4 KB)
├── references/               ← Detaylı referanslar
│   ├── calisma-prensipleri.md
│   ├── element-ve-workflow.md
│   └── test-ve-tuzaklar.md
├── templates/                ← Şablon dosyaları
├── scripts/                  ← Yardımcı script'ler
└── assets/                   ← Görseller
```

## Zorunlu Frontmatter

```yaml
---
name: skill-adi
title: "Skill Başlığı"
description: "Use when <trigger>. <kısa açıklama>."
version: 1.0.0
audience: user|contributor|maintainer
tags: [kategori, alt-kategori]
---
```

## Audience Kategorileri

| Tür | Sayı | Kapsam |
|-----|------|--------|
| **USER** | 695 | Günlük kullanım — AI/ML araçları, windows otomasyon, media, creative |
| **CONTRIBUTOR** | 288 | Kod geliştirme — pattern'ler, framework'ler, testing, scaffold |
| **MAINTAINER** | 51 | Sistem bakımı — devops, audit, cron, backup, cleanup |

## Bağlantılı Repolar

| Repo | Açıklama |
|------|----------|
| [hermes-mouse](https://github.com/Watcher-Hermes/hermes-mouse) | Windows fare/klavye otomasyon script'i |
| [obsidian-vault](https://github.com/Watcher-Hermes/obsidian-vault) | Obsidian vault yedekleri |
| [hermes-memory-backup](https://github.com/Watcher-Hermes/hermes-memory-backup) | Memory yedekleri |


## Lisans

MIT — her skill kendi SKILL.md frontmatter'ında lisans bilgisi taşır.
