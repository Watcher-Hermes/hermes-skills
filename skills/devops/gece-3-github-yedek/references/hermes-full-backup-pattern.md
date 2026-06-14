# Hermes Full Backup & Restore Pattern

## Genel Bakış

Gece yedeği skills + Obsidian vault'u ayrı repolara yedeklerken, **full backup** tüm Hermes ortamını (state.db dahil) tek bir repoda toplar.

**Full backup repo**: `https://github.com/asdafgf/hermes-full-backup`

## Full Backup İçeriği

| Öğe | Kaynak | Not |
|-----|--------|-----|
| `skills/` | `~/.hermes/skills/` | Tüm skill kategorileri |
| `hermes-state-part001.zip` | `state.db` | 240MB → 55MB zip part |
| `hermes-state-part002.zip` | `state.db-wal + state.db-shm` | ~50MB zip part |
| `hermes-full-restore.ps1` | PowerShell restore script | Tek tuş kurulum + güncelleme |
| `hermes-config-template.yaml` | config template | API anahtarları maskelenmiş |
| `README.md` | Kullanım talimatları | |

## state.db Yedekleme (SQLite, 240MB+)

state.db sürekli büyür ve değişir. GitHub'a push için:

```python
import zipfile, os

hermes_dir = r"C:\Users\marko\AppData\Local\hermes"
output = r"/tmp/hermes-state-backup.zip"

files = [
    os.path.join(hermes_dir, "state.db"),
    os.path.join(hermes_dir, "state.db-wal"),
    os.path.join(hermes_dir, "state.db-shm")
]

with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for f in files:
        if os.path.exists(f):
            zf.write(f, os.path.basename(f))
```

### 100MB GitHub Limitini Aşma

GitHub dosya limiti 100MB. 240MB state.db → zip ~105MB → hala limit üstü.
Çözüm: 55MB chunk'lara böl:

```python
chunk_size = 55 * 1024 * 1024  # 55MB
with open(zip_path, 'rb') as f:
    data = f.read()

offset = 0
part = 1
while offset < len(data):
    chunk = data[offset:offset + chunk_size]
    part_file = f"hermes-state-part{part:03d}.zip"
    with open(part_file, 'wb') as pf:
        pf.write(chunk)
    offset += chunk_size
    part += 1
```

Restore scriptinde parçalar birleştirilir:
```powershell
$stream = [System.IO.File]::OpenWrite($mergedZip)
foreach ($part in @($part1, $part2)) {
    $partData = [System.IO.File]::ReadAllBytes($part)
    $stream.Write($partData, 0, $partData.Length)
}
$stream.Close()
Expand-Archive -Path $mergedZip -DestinationPath $extractDir -Force
```

## GitHub Push Protection (Skills İçin Kritik)

Skill dosyaları token referansları içerebilir (`github_pat_...`, `ghp_...`).
GitHub Push Protection bu push'ları engeller.

### Çözüm: Token'ları Temizle + Amend

```bash
# 1. Token'ları placeholder ile değiştir
python3 << 'PYEOF'
import re, os
for root, dirs, files in os.walk('./skills/'):
    for fname in files:
        path = os.path.join(root, fname)
        try:
            with open(path, 'r') as f:
                content = f.read()
            new = re.sub(r'github_pat_[a-zA-Z0-9_]+', '[GIZLI-TOKEN]', content)
            new = re.sub(r'ghp_[a-zA-Z0-9]+', '[GIZLI-TOKEN]', new)
            if new != content:
                with open(path, 'w') as f:
                    f.write(new)
        except:
            pass
PYEOF

# 2. Amend + force push
git add -A
git commit --amend -m "Same message (secrets cleaned)"
git push origin main --force
```

### Alternatif: Unblock URL

GitHub hata mesajında şu formatta URL verir:
```
https://github.com/owner/repo/security/secret-scanning/unblock-secret/<id>
```
Kullanıcı bu linke tıklayıp "Allow secret" derse push geçer. Ancak skills sık güncelleniyorsa token referanslarını temizlemek daha kalıcı çözümdür.

## Restore Scripti (hermes-full-restore.ps1)

Yeni bilgisayarda:

```powershell
# İlk kurulum
git clone https://github.com/asdafgf/hermes-full-backup.git %USERPROFILE%\hermes-backup
powershell -ExecutionPolicy Bypass -File %USERPROFILE%\hermes-backup\hermes-full-restore.ps1

# Güncelleme
powershell -ExecutionPolicy Bypass -File %USERPROFILE%\hermes-backup\hermes-full-restore.ps1 -Update
```

Script şunları yapar:
1. `git pull` ile en son sürümü çeker
2. Hermes'i durdurur (varsa)
3. Skills'i kopyalar (eski skills `.old` yedeklenir)
4. state.db parçalarını birleştirip açar
5. Config template'ini oluşturur (yoksa)
6. `.env` eksikse uyarır

## PAT Türü Karşılaştırması (Güncel)

| İşlem | Classic PAT (`ghp_`) | Fine-Grained PAT (`github_pat_`) |
|-------|---------------------|----------------------------------|
| Repo oluşturma | ✅ `repo` scope ile | ❌ "Repository creation" yetkisi gerek |
| Push | ✅ Her repo'ya | ✅ Sadece yetkilendirilmiş repo'lar |
| Large file (>50MB) | ⚠️ Uyarı verir ama geçer | ⚠️ Aynı |
| `gh auth token` | Tam token döner | **Maskelenmiş** döner (~13 haneli) |

**Kritik**: Fine-grained PAT ile `gh auth token` komutu maskelenmiş token döndürür.
Bunu git remote URL'sinde kullanmak hata verir. Her zaman ham token'ı kullan.
