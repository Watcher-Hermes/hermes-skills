# Orphan → MOC Stratejisi

Bu reference, 139 orphan dosyanın çözümü için kullanılan stratejiyi belgeler.

## Durum
- 782 .md dosyalı vault
- 139 orphan (hiçbir yerden [[link]] almayan)
- Hedef: **53** orphan (beklenen: MOC'ler, redirect'ler, arşiv)

## Kategorizasyon

| Kategori | Sayı | Çözüm |
|----------|------|-------|
| Knowledge/* | 29 | MOC (README.md) oluştur → alfabetik bağlantı |
| Skills/ kökü | 36 | 7 anlamlı dosya → _Skills_index'e ekle; 50 taslak → Knowledge/Skills-legacy/ arşivi |
| JavaNotes/notes | 47 | MOC (README.md) oluştur → alfabetik bağlantı (384 not bağlandı) |
| Cron.md / subprocess-hata-cozme.md | 2 | Redirect notlarına çevir |

## MOC Oluşturma (Map of Content)

```python
import re
from pathlib import Path

VAULT = Path(r"C:\Users\marko\OneDrive\Belgeler\Obsidian Vault")
klasor = VAULT / "Hermes/Knowledge"  # veya "JavaNotes/notes"

files = sorted([f.name for f in klasor.glob("*.md") if f.stem != 'README'])

moc = ["# MOC Başlığı", "", "## Kategori", ""]
cats = {}
for fname in files:
    stem = fname.replace('.md', '')
    prefix = stem[0].upper()
    cats.setdefault(prefix, []).append(stem)

for prefix in sorted(cats):
    moc.append(f"### {prefix}")
    for name in sorted(cats[prefix]):
        rel = f"Hermes/Knowledge/{name}"  # İlgili yola göre ayarla
        moc.append(f"- [[{rel}|{name}]]")
    moc.append("")

(klasor / "README.md").write_text('\n'.join(moc), encoding='utf-8')
```

## Redirect Notu Şablonu

```markdown
[[hedef_not]]

> Eski konum — yeni not için bağlantıya tıkla.

---
*Redirect — eski konum*
```

## Arşiv Taşıma

```python
src = VAULT / "Hermes/Skills"
dst = VAULT / "Hermes/Knowledge/Skills-legacy"
dst.mkdir(parents=True, exist_ok=True)

for fname in skill_root_taslaklari:
    content = f"> Eski Hermes skill taslağı — artık kullanılmıyor.\n\n{src.joinpath(fname).read_text()}"
    dst.joinpath(fname).write_text(content, encoding='utf-8')
    src.joinpath(fname).unlink()
```

## Doğrulama

Orphan düzeltme sonrası nihai tarama:

```python
orphans = []
for md in all_md:
    stem = md.stem
    if stem.startswith('_'): continue
    if stem in ('daily', 'tasks', 'kanban'): continue
    if stem not in all_links:
        orphans.append(md)
```

Kalan orphan'lar şunlardan oluşmalı:
1. MOC README.md'leri — başkalarını bağlar, kendini bağlatmaz
2. Redirect notları — yönlendirme içerir, link almaz
3. Arşiv dosyaları — Knowledge/Skills-legacy/ altı, bilinçli olarak izole
