---
name: obsidian-vault-maintenance
description: >-
title: "Obsidian Vault Maintenance"
  toplu etiket ekleme, link audit ve doğrulama. 100-1000+ dosyalı vault'lar için
  Python script tabanlı yaklaşım.
version: 2.0.0
author: marko
license: MIT
metadata:
  hermes:
    tags: [obsidian, vault, maintenance, cleanup, audit, links, tags]
category: note-taking
audience: user
tags: [note-taking, obsidian, productivity]
---Obsidian vault'ta toplu bakım — kırık wikilink düzeltme, orphan dosya temizleme,



# Obsidian Vault Maintenance

## Ne Zaman Kullanılır

- Kullanıcı "vault temizle", "kırık linkleri düzelt", "orphan temizle", "etiket ekle" dediğinde
- Yeni bir skill grubu sync edildikten sonra vault'ta dağınıklık oluştuğunda
- Vault audit istenen her durumda
- İlk vault düzenleme operasyonunda

## Genel Yaklaşım

Python script (sistem Python'u ile) → dosyaların fiilen düzenlenmesi. 
Terminal komutlarıyla tek tek düzeltme yapma — Python ile toplu işle.

**Araç zinciri:**
1. `search_files` / `terminal(find/wc)` — durum tespiti
2. Python script yaz + sistem Python ile çalıştır — toplu düzeltme
3. `terminal(mv)` — orphan dosya taşıma
4. Doğrulama scripti — sonuç kontrolü

## Öncelik Kuralı (ÖNEMLİ)

**HER ZAMAN** kırık link kaynağını bulmak için önce `check_links.py` benzeri bir script çalıştır:
```python
import os, re

VAULT = r"C:\Users\marko\OneDrive\Belgeler\Obsidian Vault\Hermes"

# TÜM dosyalar (alt klasör yoluyla birlikte, .md olmadan)
existing = set()
for root, dirs, files in os.walk(VAULT):
    for f in files:
        if f.endswith('.md'):
            rel = os.path.relpath(os.path.join(root, f), VAULT).replace('\\', '/').replace('.md', '')
            existing.add(rel)
            name = f.replace('.md', '')
            existing.add(name)

# TÜM linkler
broken = {}
for root, dirs, files in os.walk(VAULT):
    for f in files:
        if not f.endswith('.md'):
            continue
        path = os.path.join(root, f)
        with open(path, 'r', encoding='utf-8', errors='replace') as fh:
            content = fh.read()
        rel = os.path.relpath(path, VAULT).replace('\\', '/')
        for m in re.finditer(r'\[\[([^\]]+?)\]\]', content):
            target = m.group(1).split('|')[0].strip()
            bare = target.split('#')[0]
            if bare not in existing:
                found = False
                for e in existing:
                    if e.endswith('/' + bare):
                        found = True
                        break
                if not found and not bare.startswith('http'):
                    if rel not in broken:
                        broken[rel] = []
                    broken[rel].append(target)

print(f"Kırık link: {sum(len(v) for v in broken.values())}")
for src, links in sorted(broken.items()):
    for l in links:
        print(f"  {src} -> [[{l}]]")
```

**Hedef:** 0 gerçek kırık link (Rusça/İngilizce dış kaynak notları hariç).

### 1. Vault Durum Tespiti

```python
import re
from pathlib import Path

VAULT = Path(r"C:\Users\marko\OneDrive\Belgeler\Obsidian Vault")

# Tüm .md dosyaları
all_md = list(VAULT.rglob("*.md"))

# Tüm wikilink'leri tara
for md in sorted(all_md):
    content = md.read_text(encoding="utf-8", errors="replace")
    found = re.findall(r'\[\[([^\]|#]+?)(?:[|#][^\]]*)?\]\]', content)
    for link in found:
        # ... target_name = link.split("/")[-1]
        # varsa all_stems'te kontrol
```

### 2. Link Onarımı

**Kırık link türleri ve çözümleri:**

| Tür | Çözüm |
|-----|-------|
| Var olmayan skill notu (vllm, gguf vb.) | `[[link]]` → `\`link\`` |
| Koordinat formatı (`[[500, 375]]`) | `[[500, 375]]` → `` `[500, 375]` `` |
| `skills/XXX` formatı (Obsidian'a skill yazarken oluşur) | `skills/xxx` → `[[xxx]]` regex toplu dönüşümü: `re.sub(r'\[\[skills/([^\]]+?)\]\]', r'[[\1]]', content)` |
| `Hermes/Skills/xxx/yyy` formatı (eski yol) | `re.sub(r'\[\[Hermes/Skills/[^\]]+?\]\]', lambda m: '[[' + m.group(0)[2:-2].split('/')[-1] + ']]', content)` |
| `Hermes/Cron/xxx` formatı | `re.sub(r'\[\[Hermes/Cron/([^\]]+?)\]\]', r'[[\1]]', content)` |
| `Hermes/Skills/MOC - ...` gibi özel isimler | `content.replace('[[Hermes/Skills/MOC - X]]', '[[MOC - X]]')` — elle tek tek |
| Eğitim amaçlı örnekler (`[[wikilinks]]`) | Kod bloğuna çevir |
| Kategori/alt yol linkleri (`windows-automation/vscode-ac`) | Obsidian'da `windows-automation\vscode-ac` dosyasına yönlendir |
| JavaNotes .png360/.webp uzantı hataları | `.png360` → `.png` (gerçek dosya adı) |

**Önemli:** Kırık link sayarken Obsidian'ın otomatik oluşturduğu "Pasted image" referanslarını yanlış sayma. Obsidian görüntü dosyalarını otomatik linkler, onlar kırık değildir.

### 3. Orphan Temizleme

Orphan = hiçbir yerden `[[link]]` almayan dosya.

**Politika (üç aşamalı):**

**Aşama 1 — Beklenen orphan'ları filtrele:**
- `_*_index.md` — index dosyaları beklenen orphan'dır, atla
- `README.md` — MOC başlığı, atla (kendini bağlamaz)
- `Cron.md`, `subprocess-hata-cozme.md` gibi `redirect` içerenler — atla
- `Knowledge/Skills-legacy/*` — arşiv altındaki dosyalar beklenir, atla

**Aşama 2 — Gerçek orphan'ları MOC ile bağla:**
- Knowledge klasörü → `Knowledge/README.md` MOC oluştur, tüm notları alfabetik listele
- JavaNotes gibi ayrı klasörler → `KlasorAdi/README.md` MOC oluştur
- Skills/ kökündeki anlamlı dosyalar (Hibrit AI, Dolphin vb.) → `_Skills_index.md`'ye link ekle

**Aşama 3 — Eski/Skills-root legacy taşıma:**
- Skills/ kökündeki `DESCRIPTION.md`, `SKILL.md`, `README.md` gibi Hermes repo'dan kalan dosyalar → `Knowledge/Skills-legacy/` altına taşı
- `<50` satırlık taslak/boş skill şablonları → aynı arşive taşı
- Anlamlı içerikli dosyalar (Hibrit AI Mimarisi, dolphin-llama3, self-improvement vb.) → olduğu yerde kal, _Skills_index'e ekle

**MOC oluşturma şablonu:**
```markdown
## Kategori Adı (alfabetik)

### A
- [[path/to/NotAdı|NotAdı]]
- [[path/to/DigerNot|DiğerNot]]

### B
- [[path/to/BaskaNot|BaşkaNot]]
```

**Orphan tespit scripti:**
```python
all_links = set()
for md in all_md:
    content = md.read_text(encoding="utf-8", errors="replace")
    found = re.findall(r'\[\[([^\]|#]+?)(?:[|#][^\]]*)?\]\]', content)
    for link in found:
        all_links.add(link.split("/")[-1])

orphans = []
for md in all_md:
    stem = md.stem
    if stem.startswith('_'): continue  # index dosyaları
    if stem in ('daily', 'tasks', 'kanban'): continue  # Obsidian özel
    if stem not in all_links:
        orphans.append(md)
```

### 4. Toplu Etiket Ekleme

Frontmatter'a `tags:` alanı ekle. Etiket politikası:

```
#hermes            → kök Hermes notları
#hermes #skill     → skill notları
#hermes #knowledge → Knowledge/ altı (taşınmış notlar)
#hermes #skill #kategori → kategori bazlı
```

Dotayı direkt `write_file` ile baştan yaz. `patch` riskli çünkü önceki içerik tutarsız olabilir.

### 5. Doğrulama

Düzeltme bittikten sonra aynı script 2 kere daha çalıştırılır:
- Kalan kırık link sayısını raporla
- Kalan orphan sayısını raporla
- Toplam dosya sayısını raporla

Kalan 0-5 kırık link (eğitim amaçlı örnekler hariç) kabul edilebilir.

## Pitfalls

0. **ÖNCE regex taraması — replace için tam formatı doğrula:** Kırık link düzeltirken `[[hedef|görünen]]` formatını `[[hedef]]` ararken kaçırma. `re.findall(r'\\[\\[([^\\]|]+?)(?:[|#][^\\]]*)?\\]\\]', content)` ile tarama yaptığında formattan `|görünen` kısmı ayrışır, ama sonra Python `str.replace('[[hedef]]', ...)` ile düzeltme yaparken `[[hedef|görünen]]` eşleşmez. **Çözüm:** replace yapmadan önce content içinde tam string'i (pipe dahil) kontrol et:
   `if '[[hedef|görünen]]' in content:` — varsa o haliyle replace et.

0. **Büyük vault tarama performansı (1000+ dosya):** Ana vault 1456 dosya, Hermes/ 304 dosya iken tek bir `os.walk` + tüm dosyaları `read_text()` ile tarama 3-5 saniye sürer. Script'i yazarken:
   - `os.walk`'ı 1 kere çalıştır, `existing` set'ini oluştur, sonra 2. turda her dosyayı oku
   - Regex derlemesini loop dışında yap: `pattern = re.compile(r'\\[\\[([^\\]]+?)\\]\\]')`
   - `.gitignore`, `.obsidian/` ve `node_modules/` altını atla
   - İki vault'u (ana + Hermes/) ayrı ayrı tara, aynı script içinde iki tarama çalıştır

0. **Ana vault + Hermes alt vault çapraz linkleri:** Ana vault (`JavaNotes/`) Hermes/ altındaki sayfalara link verirse, Ana vault taraması Hermes/ dosyalarını `existing` set'ine katmazsa kırık sayar. **Çözüm:** Her iki vault'un dosyalarını da `existing` set'ine ekle, link kaynağına bakmaksızın her vault'taki tüm linkleri kontrol et.

1. **`_README` gibi özel isimli dosyalar:** Hermes GitHub repo'sundan kalan `[[_README|açıklama]]` linkleri vault'ta `_README.md` olmadığı için her zaman kırıktır. Bunları inlint code'a (`\`_README\``) çevir. Ama `_software-development_index` gibi gerçek index dosyalarına yapılan linkleri KARIŞTIRMA — onlar vault'ta var.

2. **Windows'ta `\` vs `/` yolları:** Obsidian wikilink'leri `/` kullanır (`windows-automation/vscode-ac`), ama filesystem `\` bekler. Link çözümlemede her iki formata da bak.
2. **re.sub group reference hatası:** Python 3.14'te `re.sub(r'...', r'`\1, \2`', ...)` backtick içindeki `\1` çalışmaz. Lambda fonksiyon kullan.
3. **Obsidian'in otomatik resim linkleri:** `[[Pasted image 2023...]]` gibi linkler gerçekte `.png` dosyalarıdır, Obsidian vault assets klasöründe durur. Kırık link sayma bunları yanlış pozitif olarak raporlayabilir — kontrol et.
4. **Skill notlarının orphan görünmesi:** Bir skill notu kendi kategorisi dışında hiçbir yerde referans alınmamış olabilir. Bu durumda `_category_index.md`'ye ekleyerek düzelt.
5. **Python 3.14 ile re.sub:** Backreference içeren stringlerde backtick karakter sorunu yaratır. Her zaman lambda fonksiyon kullan:
   ```python
   content = re.sub(r'\[\[(\d+),\s*(\d+)\]\]', 
                    lambda m: f'`[{m.group(1)}, {m.group(2)}]`', 
                    content)
   ```
7. **`skills/XXX` formatında linkler:** Obsidian'a skill notları yazılırken `skills/XXX` formatında linkler oluşabilir (`[[skills/hermes-agent]]`). Bunları topluca `[[XXX]]`'e çevir:
   ```python
   content = re.sub(r'\[\[skills/([^\]]+?)\]\]', r'[[\1]]', content)
   ```
   Bu regex **en son** uygulanmalı — önce diğer tüm düzeltmeler yapılmalı.

8. **Redirect notları oluştur:** Eski isimle var olmayan ama eski linklerin yöneldiği sayfalar için (Cron, gece-gelistirme, MOC - Windows Otomasyon, subprocess-hata-cozme) kısa redirect notları oluştur. İçinde sadece `➡️ [[hedef]]` yazsın.

9. **execute_code içinde write_file sınırı:** `execute_code` tool call limitine (50) takılabilir. Çok sayıda dosya düzeltilecekse direkt `open(path, 'w').write(content)` kullan — tool call limitini harcamaz. `from hermes_tools import write_file` import etme, direkt Python file I/O yap.

10. **Kontrol scriptinde alt klasör eşleme:** Sadece `stem` ile eşleme yapma — `Hermes/skills/autonomous-ai-agents/_autonomous-ai-agents_index`'e link `[[autonomous-ai-agents/_autonomous-ai-agents_index]]` şeklinde olabilir. `existing` set'ine tüm `relpath`'leri koy ve `endswith('/' + target)` ile kontrol et.
7. **Hermes/Knowledge klasörü:** `Hermes/Knowledge/` yoksa `mkdir -p` ile oluştur. Dosya taşıma için `terminal(mv)` kullan.

## Referans Dosyaları

- `references/vault-bulk-fix-example.md` — 709 dosyalı vault'ta opsiyon D uygulamasının tam kaynak kodu
- `references/bulk-link-fix-strategy.md` — link düzeltme stratejisi: 4 fazlı yaklaşım, regex sırası, redirect notları oluşturma
- `references/vault-verify-example.md` — nihai doğrulama scripti
- `references/orphan-moc-strategy.md` — 139 orphan'ı MOC + arşiv + redirect ile çözme stratejisi (gerçek veriler, Python kodları, kategorizasyon tablosu)

## Script Dosyaları

- `scripts/check_links_v2.py` — gelişmiş link kırığı tarama scripti (alt klasör eşlemesi destekler). Kullanım: `python scripts/check_links_v2.py [vault_yolu]`

## İlgili Referanslar

Aktif bağlantı (yeni bağlantılar ekleme) için `obsidian` skill'indeki
`references/vault-relationship-linking.md` dosyasına bak — MOC
oluşturma, kategori ötesi bağlantı ve üç katmanlı bağlantı mimarisini
anlatır. Bu skill kırık link **onarımına** odaklanırken, o reference
yeni bağlantı **kurulumuna** odaklanır.
