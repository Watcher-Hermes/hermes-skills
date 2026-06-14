<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://hermes-agent.nousresearch.com/img/hermes-og-image-blue.png">
    <source media="(prefers-color-scheme: light)" srcset="https://hermes-agent.nousresearch.com/img/hermes-og-image-blue.png">
    <img src="https://hermes-agent.nousresearch.com/img/hermes-og-image-blue.png" alt="Hermes Agent" width="600">
  </picture>
</p>

<p align="center">
  <b>1,038</b> modüler skill · <b>4,476</b> reference dosyası · <b>0</b> şişkin
  <br>
  <sub>Router+Reference mimarisi · Her skill ≤ 4 KB</sub>
</p>

<p align="center">
  <a href="#-i̇statistikler"><img src="https://img.shields.io/badge/skills-1,038-6366f1?style=flat-square&labelColor=1e1b4b" alt="skills"></a>
  <a href="#-kategori-yapısı"><img src="https://img.shields.io/badge/references-4,476-8b5cf6?style=flat-square&labelColor=1e1b4b" alt="references"></a>
  <a href="#-kategori-yapısı"><img src="https://img.shields.io/badge/categories-530-a855f7?style=flat-square&labelColor=1e1b4b" alt="categories"></a>
  <a href="#-hızlı-başlangıç"><img src="https://img.shields.io/badge/bloat-0-success?style=flat-square&labelColor=1e1b4b" alt="bloat"></a>
</p>

---

## 📊 İstatistikler

| Metrik | Değer |
|--------|------:|
| **SKILL.md** | **1,038** |
| **Reference dosyası** | **4,476** |
| **Kategori** | **530** |
| **Şişkin skill (10KB+)** | **0** |
| Audience: `user` | 695 |
| Audience: `contributor` | 288 |
| Audience: `maintainer` | 51 |

---

## 📂 Kategori Yapısı

```
skills/
├── ecc/                  262   Kod geliştirme pattern'leri
├── windows-automation/   43    Windows otomasyon
├── software-development/ 34    Geliştirme araçları
├── mlops/                26    Model yönetimi, inference
├── productivity/         26    PDF, OCR, kamera, klavye
├── autonomous-ai-agents/ 23    Otonom ajan döngüleri
├── creative/             22    ASCII art, diyagram, video
├── user-preferences/     17    Profil ve model ayarları
├── devops/               13    Backup, cron, migration
├── note-taking/          12    Obsidian, Notion
├── security/             10    Pentest, tersine mühendislik
├── media/                 8    YouTube, Spotify, GIF
├── research/              8    Arxiv, paper, polymarket
├── gaming/                6    Oyun otomasyonu
├── github/                6    PR, issue, repo yönetimi
├── apple/                 5    macOS, iOS, iMessage
├── data-science/          3    Jupyter, HuggingFace
├── windows-system-auto./  2    Kamera, güvenlik izleme
└── …                    500+  Tek konulu özel skill'ler
```

---

## 🏗 Skill Yapısı

Her skill **Router+Reference** mimarisiyle oluşturulmuştur:

```
skills/kategori/skill-adi/
├── SKILL.md              Router — yalnızca yönlendirme (≤ 4 KB)
├── references/           Detaylı belgeler
│   ├── ornek-referans.md
│   └── …                 
├── templates/            Şablon dosyaları
├── scripts/              Yardımcı script'ler
└── assets/               Görseller
```

### Zorunlu Frontmatter

```yaml
---
name: skill-adi
title: "Skill Başlığı"
description: "Use when <tetikleyici>. <kısa açıklama>."
version: 1.0.0
audience: user|contributor|maintainer
tags: [kategori, alt-kategori]
---
```

### Audience Kategorileri

| Tür | Sayı | Kapsam |
|-----|-----:|--------|
| **USER** | 695 | Günlük kullanım — AI araçları, otomasyon, media, creative |
| **CONTRIBUTOR** | 288 | Kod geliştirme — pattern'ler, framework'ler, testing |
| **MAINTAINER** | 51 | Sistem bakımı — devops, audit, cron, backup |

---

## 🚀 Hızlı Başlangıç

```bash
# Hermes Agent ile bir skill'i yükle
skill_view(name='skill-adi')

# Tüm skill'leri listele
skills_list()

# Kategoriye göre filtrele
skills_list(category='windows-automation')
```

---

## 🔗 Bağlantılı Repolar

| Repo | Açıklama |
|------|----------|
| [hermes-mouse](https://github.com/Watcher-Hermes/hermes-mouse) | Windows fare/klavye otomasyon script'i |
| [obsidian-vault](https://github.com/Watcher-Hermes/obsidian-vault) | Obsidian vault yedekleri |
| [hermes-memory-backup](https://github.com/Watcher-Hermes/hermes-memory-backup) | Memory yedekleri |

