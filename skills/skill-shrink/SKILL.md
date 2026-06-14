---
name: skill-shrink
title: "Skill Shrink — Şişkin Skill'leri Parçalama"
description: "10KB+ veya 300+ satırlık şişkin skill'leri tespit eder, bölümlerini references/ altına taşır, ana SKILL.md'yi yönlendirici (router) haline getirir."
tags: [skill-audit, optimizasyon, bakim, token-verimliligi]
audience: maintainer
category: devops
related_skills: [skill-benchmark, self-improvement, obsidian-vault-maintenance]
triggers: [skill shrink, skill parcala, siskin skill, token azalt, skill optimize]
version: 1.0.0
---

# Skill Shrink — Şişkin Skill'leri Parçalama Aracı

## Ne İşe Yarar

Büyük skill'ler (10KB+ veya 300+ satır) Hermes'in token limitini gereksiz yere şişirir ve yüklenme süresini artırır. Bu skill, şişkin skill'leri tarar, her `##` bölümünü ayrı bir `references/` dosyasına taşır ve ana SKILL.md'yi hafif bir yönlendiriciye dönüştürür.

## Kullanım

```bash
# Tek bir skill'i küçült
python skill-shrink.py --skill research/research-paper-writing

# Tüm şişkin skill'leri tara (kuru çalıştırma)
python skill-shrink.py --scan

# Tüm şişkin skill'leri küçült
python skill-shrink.py --all
```

## Adımlar

### 1. Şişkin Skill'leri Tara

```python
from pathlib import Path

skills_dir = Path.home() / "AppData/Local/hermes/skills"
SINIR_BYTE = 10 * 1024  # 10 KB
SINIR_SATIR = 300

siskinler = []
for p in skills_dir.rglob("SKILL.md"):
    content = p.read_text(encoding="utf-8", errors="replace")
    satir = len(content.splitlines())
    byte = len(content)
    if byte >= SINIR_BYTE or satir >= SINIR_SATIR:
        siskinler.append((p, byte, satir))
```

### 2. Bölümleri Tespit Et

Skill içindeki `##` ve `###` başlıklarını bul, her bölümün satır aralığını belirle. Frontmatter'ı (--- ... ---) olduğu gibi koru.

### 3. Reference Dosyalarına Taşı

Her bölüm için ayrı bir `.md` dosyası oluştur:

```
skills/X/skill_adi/
├── SKILL.md           ← sadece yönlendirici (~3-5 KB)
├── references/
│   ├── bolum-1-baslik.md
│   ├── bolum-2-baslik.md
│   └── ...
```

### 4. Yeni SKILL.md Oluştur

Reference dosyalarına işaret eden bir router SKILL.md yaz:

```markdown
## 🎯 Aktif Bölümü Seç

| Bölüm | Referans |
|-------|----------|
| Bölüm 1 | `references/bolum-1.md` |
| Bölüm 2 | `references/bolum-2.md` |
```

## Örnek Çıktı

```
BEFORE: research-paper-writing/SKILL.md → 100 KB / 2.379 satır

AFTER:
├── SKILL.md                       → 3 KB (yönlendirici)
├── references/
│   ├── phase-1-literature-review  → 4.3 KB
│   ├── phase-2-experiment-design  → 5.0 KB
│   ├── ... 15 dosya daha

Token kazancı: ~%95
```

## Dikkat Edilmesi Gerekenler

- **Yedek al:** Çalıştırmadan önce `.audience-backup/` veya Git yedeği al
- **İç içe başlıklar:** `###` alt başlıklarını üst başlıktan ayırma, aynı reference dosyasında tut
- **İsimlendirme:** Reference dosya adlarında Türkçe karakter ve boşluk kullanma
- **Doğrulama:** İşlem sonrası `skill_view(name)` ile skill'in hala çalıştığını doğrula
- **Frontmatter koru:** SKILL.md'nin frontmatter'ı (--- ... ---) asla değişmesin

## Hata Yönetimi

- Frontmatter parse edilemezse → skill'i atla ve log'a yaz
- Bölüm bulunamazsa → skill'i atla
- Zaten references/ klasörü varsa → birleştirme yap
