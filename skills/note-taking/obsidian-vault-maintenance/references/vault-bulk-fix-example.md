# 709-dosyalı Obsidian Vault Toplu Bakım (Opsiyon D)

Bu oturumda uygulanan tam senaryo: kırık link düzeltme + orphan temizleme + toplu etiket ekleme.

## Özet

| Ölçüm | Önce | Sonra |
|-------|------|-------|
| Kırık link | ~160 (gerçek) | 4 (eğitim amaçlı) |
| Orphan dosya | 55 | 0 |
| Etiketsiz not | 233 | 0 |
| Dosya sayısı | 709 | 710 |

## Ana Script (vault_fix_all_d.py)

Üç adımı tek seferde yapan Python script:

1. **Skill haritası oluştur:** Hermes/Skills/ altındaki tüm dosyaları tara, dosya adı → tam yol eşlemesi
2. **Kırık linkleri bul ve düzelt:** Her .md dosyasındaki `[[link]]`'leri skill haritasına göre çöz, bulunamayanları inline code yap
3. **Orphan tespit:** Hiçbir yerden link almayan dosyaları bul, Knowledge/ altına taşı
4. **Etiket ekle:** Frontmatter kontrol et, yoksa kategori bazlı etiket ekle

### Önemli script teknikleri

**re.sub'da backreference + backtick:**
```python
# YANLIŞ — Python 3.14'te hata verir:
# content = re.sub(r'\[\['(\d+),\s*(\d+)\]\]', r'`[\1, \2]`', content)

# DOĞRU — lambda fonksiyon kullan:
content = re.sub(r'\[\[(\d+),\s*(\d+)\]\]', 
                 lambda m: f'`[{m.group(1)}, {m.group(2)}]`', 
                 content)
```

**Windows path'leriyle çalışma:**
```python
# Obsidian wikilink formatı: windows-automation/vscode-ac
# Filesystem formatı: windows-automation\vscode-ac.md
# Çözüm: önce /'yi \'ye çevir
parts = link_clean.split("/")
target_name = parts[-1]

# Tam path kontrolü
base_path = link_clean.replace("/", "\\")
full_path = VAULT / "Hermes" / "Skills" / f"{base_path}.md"
```

**Orphan tespit — tüm linkleri topla, sonra dosyaları eşle:**
```python
all_links = set()
for md in all_md:
    content = md.read_text(encoding="utf-8")
    found = re.findall(r'\[\[([^\]|#]+?)(?:[|#][^\]]*)?\]\]', content)
    for link in found:
        all_links.add(link.split("/")[-1])

orphans = [md for md in all_md if md.stem not in all_links]
```

## Doğrulama Scripti (vault_verify.py)

Son durumu kontrol eden bağımsız script:
- Toplam .md sayısı
- Kırık wikilink detayları (dosya bazında)
- Kalan orphan sayısı
- Hermes/ altı dosya sayısı

## Referans

Scriptlerin kaynağı (eğer silinmemişse):
- `C:\Users\marko\AppData\Local\hermes\scripts\vault_fix_all_d.py`
- `C:\Users\marko\AppData\Local\hermes\scripts\vault_verify.py`
- `C:\Users\marko\AppData\Local\hermes\scripts\vault_fix_remaining.py`
