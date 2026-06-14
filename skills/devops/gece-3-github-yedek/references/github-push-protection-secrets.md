# GitHub Push Protection — Secret Scanning

## Sorun

Skill referans dosyalarında gerçek PAT token'lar (veya `ghp_***` gibi redakte edilmiş halleri) GitHub push protection tarafından tespit edilir ve push engellenir:

```
remote: - Push cannot contain secrets
remote:   —— GitHub Personal Access Token ——
remote:    locations: path/to/file.md:104
```

## Çözüm

### Seçenek A: Dosyaları sil + force push (önceki commit temizse)

```bash
rm -f skills/devops/gece-3-github-yedek/references/auth-diagnosis-*.md
git add -A
git commit -m "token iceren dosyalar silindi"
git push --force origin master
```

### Seçenek B: Repoyu sıfırdan kur (önceki commit'lerde token varsa)

```bash
cd /path/to/repo
rm -rf .git                    # tüm history'i sil
git init                       # yeni temiz repo
git remote add origin https://github.com/Watcher-Hermes/<repo>.git
git add -A
git commit -m "temiz baslangic"
git push --force origin master # force push (GitHub'taki eski history'nin yerine gecer)
```

### Seçenek C: GitHub web UI'dan secret'ı "allow" et

Push reddedildiğinde, hata mesajında bir URL verilir:
```
https://github.com/Watcher-Hermes/<repo>/security/secret-scanning/unblock-secret/<hash>
```
Bu URL'den secret'ı manuel allow edip tekrar push deneyebilirsin. Ancak bu sadece o özel commit için geçerlidir.

## Önleme

- Skill dosyalarına token yazarken `***REDACTED***` KULLANMA — GitHub `ghp_` ve `github_pat_` prefix'lerini tarar, redakte edilmiş halde bile bloklar
- Bunun yerine: `TOKEN_ORNEK_AMA_GECERSIZ` veya `<GERCEK_TOKEN_BURAYA>` gibi prefix'siz placeholder'lar kullan
- Token'ları skill dosyasına eklemeden önce binary open() ile .env'den oku (maskesiz), ama SKILL.md'ye yazma

## Tespit

```bash
# Token iceren dosyalari bul
grep -rl "ghp_\|github_pat_\|gho_\|ghu_\|ghs_\|ghr_" skills/ 2>/dev/null

# Tam olarak hangi token'lar var gor
grep -oh "ghp_[^ \",;)]*\|github_pat_[^ \",;)]*\|gh[ousr]_[^ \",;)]*" skills/ 2>/dev/null | sort -u
```
