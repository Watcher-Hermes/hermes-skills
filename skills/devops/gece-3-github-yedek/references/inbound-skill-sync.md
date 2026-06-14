# Inbound Skill Sync: GitHub → Local

## Ne işe yarar

GitHub backup reposundaki skill'leri local'e çeker. Outbound diff sync'in
(diff-sync-workflow.md) ters yönü: burada repo'daki yeni skill'ler local'e
kopyalanır. Otomatik cron job ile her gün 20:15'te çalışır.

## Inbound vs Outbound

| Özellik | Outbound (diff-sync-workflow) | Inbound (bu workflow) |
|---------|-------------------------------|----------------------|
| Yön | Local → GitHub | GitHub → Local |
| Ne yapar | Yereldeki eksik skill'leri repo'ya push eder | Repo'daki yeni skill'leri local'e kopyalar |
| Cron | Manuel, gerektikçe | Otomatik, her gün 20:15 |
| Script | Bash/bulunduğu yerde manuel | `sync_missing_skills.py` (kalıcı script) |
| Çalışma modu | LLM-driven (Hermes ajanı) | `no_agent` (direkt script, LLM harcanmaz) |

## Cron Job Yapılandırması

```
Job ID:     cfbe26486805
Name:       GitHub Skill Sync
Schedule:   15 20 * * * (her gün 20:15)
Mode:       no_agent (script stdout'u direkt teslim edilir)
Script:     sync_missing_skills.py  →  ~/.hermes/scripts/sync_missing_skills.py
```

### no_agent Modu

`no_agent=True` ile cron job LLM çağırmaz, sadece script'i çalıştırır ve
stdout'u olduğu gibi teslim eder. Kullanım şartları:
- `prompt` ve `skills` parametreleri IGNORE edilir (script'in kendisi prompt'tur)
- Sadece `script` parametresi kullanılır
- Boş stdout = sessiz çalışma (bildirim gitmez)
- Non-zero exit = hata bildirimi gönderilir

### Script Yolu Kuralı

Cron job script'i **sadece dosya adı** olarak verilir, tam yol değil:
```
# DOĞRU
script: sync_missing_skills.py

# YANLIŞ
script: C:\Users\marko\AppData\Local\hermes\scripts\sync_missing_skills.py
```

Hermes, dosya adını `~/.hermes/scripts/` altında arar.

## Karşılaştırma Algoritması

Path bazında SKILL.md karşılaştırması yapılır — sadece skill adı değil,
kategori + skill adı (örn. `ecc/api-design`) kullanılır. Aynı adda farklı
kategorilerde skill varsa karışmaz.

```python
def get_skill_paths(base_dir):
    """Get set of relative paths (category/skillname) for skills with SKILL.md."""
    paths = set()
    for root, dirs, files in os.walk(str(base_dir)):
        if "SKILL.md" in files:
            rel = os.path.relpath(root, str(base_dir))
            paths.add(rel.replace(os.sep, "/"))
    # Standalone .md files in skills root
    for f in sorted(base_dir.glob("*.md")):
        if f.name not in ("SKILL.md", "README.md"):
            paths.add(f.name)
    return paths
```

Copy işlemi: eksik path'ler için `shutil.copytree` (dizin) veya
`shutil.copy2` (tek dosya) kullanılır.

## MSYS2 / Git Bash Path Tuzağı

Git Bash'in `/tmp` dizini ile Python'un tempdir'i arasında fark vardır.
Git Bash'te `ls /tmp/...` bir dizini gösterirken, Python'da
`os.path.exists("/tmp/...")` False dönebilir.

**Sebep**: Git Bash (MSYS2) `/tmp`'yi kendi sanal dizinine yönlendirir.
Python ise `C:\Users\marko\AppData\Local\Temp`'i kullanır. Aynı yolu
göstermelerine rağmen, işletim sistemi farklı handle'lar atayabilir.

**Çözüm**: Python script'lerinde `tempfile.mkdtemp()` kullan (Python'un
kendi temp yönetimiyle). Script'in içinde clone yapılacaksa `subprocess.run`
ile `git clone` doğrudan Python temp dizinine yapılır.

```python
import tempfile, subprocess
from pathlib import Path

tmp = tempfile.mkdtemp(prefix="hermes-sync-")
try:
    repo_path = Path(tmp) / "repo"
    subprocess.run(["git", "clone", "--depth", "1", REPO_URL, str(repo_path)],
                   capture_output=True, text=True, timeout=120)
    # os.walk(str(repo_path / "skills")) → ÇALIŞIR
finally:
    shutil.rmtree(tmp, ignore_errors=True)
```

## Sync Script Referansı

Script: `sync_missing_skills.py` (`~/.hermes/scripts/`)

İç akış:
1. `tempfile.mkdtemp()` ile geçici dizin oluştur
2. `git clone --depth 1` ile repo'yu klonla
3. `get_skill_paths()` ile local ve repo path'lerini al
4. `repo_paths - local_paths` ile eksikleri bul
5. Her eksik için: `shutil.copytree()` ile kopyala
6. Geçici dizini temizle

## Pitfall'lar

1. **Temp dizin temizliği** — `tempfile.TemporaryDirectory` context manager'ı
   kullanılırsa clone tamamlanmadan temizlenebilir. `mkdtemp()` + manuel
   `shutil.rmtree()` daha güvenilir.

2. **İlk clone uzun sürer** — skills + state.db ~200MB. `--depth 1`
   zorunludur, yoksa timeout riski var. 120s timeout yeterli.

3. **Yeni skill'ler Hermes restart gerektirmez** — Skill'ler dosya sistemi
   üzerinden yüklenir, mevcut oturumda görünür hale gelir. SOUL.md değişikliği
   gerektiren skill güncellemeleri ayrıca restart gerektirmez (SOUL.md her
   mesajda tazelenir).
