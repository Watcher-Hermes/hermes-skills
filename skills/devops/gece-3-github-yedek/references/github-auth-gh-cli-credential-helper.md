# gh CLI Credential Helper — GitHub Auth Stratejisi

## Ne Zaman Kullanılır

- SSH key GitHub'a eklenmemişse (Permission denied publickey)
- `.env`'deki GITHUB_TOKEN placeholder/truncated ise (`***REMOVED***...0qyk`, 13 karakter)
- PAT push protection tarafından bloklanıyorsa
- Windows credential manager çakışması varsa

## Nasıl Çalışır

GitHub CLI (`gh`) Windows'ta **keyring** üzerinden token yönetir. `gh auth login` ile giriş yapıldığında token Windows Credential Manager'a kaydedilir. Git, `credential.helper = !gh auth git-credential` sayesinde bu token'ı otomatik kullanır.

**Avantajları:**
- `.env` dosyasına bağımlı değildir — env_watcher.py truncation'ından etkilenmez
- Token güvenli şekilde keyring'de saklanır
- `repo` scope'u ile gelir (classic PAT)
- Herhangi bir credential helper çakışmasını bypass eder

## Kullanım

```bash
# Durum kontrolü
gh auth status

# Remote URL'de PAT olmamalı
git remote set-url origin https://github.com/OWNER/REPO.git

# Push
GIT_TERMINAL_PROMPT=0 git push origin main
```

## Tanı

```bash
# gh CLI kurulu mu?
gh --version

# Oturum açık mı?
gh auth status 2>&1 | grep "Logged in"

# Hangi scope'lar var?
gh auth status 2>&1 | grep "Token scopes"
```

## 2026-06-13 Oturum Notları

Bu oturumda:
- SSH: `Permission denied (publickey)` — key GitHub'a eklenmemiş
- PAT: `.env`'de `GITHUB_TOKEN=***REMOVED***...0qyk` (truncated, 13 chars) — push 401
- `gh auth status`: `✓ Logged in to github.com account asdafgf` — **çalıştı**
- Push başarılı: `***REMOVED***...KxUM` → `Watcher-Hermes/obsidian-vault.git`
- Repo taşınmış: `asdafgf/obsidian-vault` → `Watcher-Hermes/obsidian-vault`
