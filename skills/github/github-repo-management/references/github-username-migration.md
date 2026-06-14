# GitHub Username Migration Workflow

Kullanıcı GitHub kullanıcı adını değiştirdiğinde yapılması gerekenler.

## Adımlar

### 1. Kullanıcı adı değişikliği (kullanıcı yapar)
GitHub.com → Settings → Account → Change username

### 2. Kullanıcı adı kuralları
- Sadece alfanumerik karakterler (a-z, 0-9) ve tek tire (`-`)
- Tire ile başlayamaz ve bitemez
- Alt çizgi (`_`), `+` ve diğer özel karakterler YASAK
- GitHub alt çizgiyi tireye çevirir: `Watcher_Hermes` → `Watcher-Hermes`
- Büyük/küçük harf korunur ama URL'ler case-insensitive çalışır

### 3. Kullanıcı adı boşta mı kontrolü
```bash
curl -s -o /dev/null -w "%{http_code}" "https://github.com/istenen-kullanici-adi"
# 404 = boşta, 200 = alınmış
```

### 4. Değişiklik sonrası güncellenmesi gerekenler

| Dosya/Alan | Ne yapılır |
|------------|-----------|
| `git remote set-url origin` | Yeni URL: `https://github.com/yeni-ad/repo.git` |
| `README.md` | Tüm linkleri güncelle |
| `hermes-full-restore.ps1` | `$RepoUrl` değişkenini güncelle |
| `Hermes Memor/MEMORY.md` | Repo linki + gh CLI referansı |
| `Hermes Memor/USER.md` | GitHub kullanıcı adı |
| Skill referansları | `sync_hermes_backup.py`, workflow referansları |
| Hermes memory | `memory(replace)` ile user profile'ı güncelle |

### 5. Push etme

```bash
git remote set-url origin https://github.com/yeni-ad/repo.git
git add -A
git commit -m "kullanici adi guncellendi: eski-ad -> yeni-ad"
git push origin main
```

### 6. Önemli notlar
- Değişiklik GitHub'da 5-30 saniye içinde yayılır
- Eski URL otomatik yönlendirme yapar (redirect)
- `gh auth status` eski kullanıcı adını gösterebilir — sorun değil, token aynı hesap
- Repo visibility (private/public) değişiklikten etkilenmez

## Pitfall — MSYS yol dönüşümü
Git Bash'te `gh api repos/yeni-ad/repo` çalışmaz (MSYS `/`'yi Windows yolu sanar). Kullan:
```bash
gh api repos/yeni-ad/repo
# veya
curl -s -H "Authorization: token $GITHUB_TOKEN" "https://api.github.com/repos/yeni-ad/repo"
```
