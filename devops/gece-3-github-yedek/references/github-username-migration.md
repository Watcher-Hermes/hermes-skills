# GitHub Kullanıcı Adı Değiştirme — Migration Prosedürü

Kullanıcı adı asdafgf → Watcher_Hermes olarak değiştirildiğinde yapılması gerekenler.

## Adımlar

### 1. Kullanıcı Adını GitHub'da Değiştir
- GitHub.com → Settings → Account → Change username
- Yeni adı gir, "Latent-Hermes mevcuttur" onayını gör
- Yeşil "Kullanıcı adımı değiştir" butonuna bas

### 2. Local Git Remote URL'yi Güncelle
```bash
cd /c/Users/marko/hermes-full-backup
git remote set-url origin https://github.com/Watcher_Hermes/hermes-full-backup.git
```

### 3. Repo'daki Tüm Referansları Güncelle
Aşağıdaki dosyalarda eski kullanıcı adını yenisiyle değiştir:

| Dosya | Ne güncellenir |
|-------|----------------|
| `README.md` | Tüm linklerdeki kullanıcı adı |
| `hermes-full-restore.ps1` | `$RepoUrl` ve banner linkleri |
| `Hermes Memor/MEMORY.md` | Repo URL + GitHub CLI notu |
| `Hermes Memor/USER.md` | Kullanıcı profili GitHub alanı |
| `skills/devops/gece-3-github-yedek/SKILL.md` | Auth stratejilerindeki URL'ler |
| `skills/devops/gece-3-github-yedek/scripts/sync_hermes_backup.py` | Clone URL |
| `skills/devops/gece-3-github-yedek/references/diff-sync-workflow.md` | Tüm linkler |
| `skills/devops/gece-3-github-yedek/references/hermes-full-backup-pattern.md` | Tüm linkler |

### 4. GitHub Repo Görünürlüğü
Kullanıcı adı değişince repo private kalır. Kontrol:
```bash
gh repo edit Watcher_Hermes/hermes-full-backup --visibility private --accept-visibility-change-consequences
```

### 5. Commit & Push
```bash
git add -A
git commit -m "kullanici adi guncellendi: eski → yeni"
git push origin main
```

Push başarısız olursa (`Repository not found`), username değişikliği henüz GitHub'da tam yayılmamıştır. Kullanıcıya bildir, birkaç dakika bekle.

### 6. Hermes Memory'yi Güncelle
- `user` store'da GitHub referansını güncelle
- `memory` store'da github ile ilgili entry'leri güncelle
