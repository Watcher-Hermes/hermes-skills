# Token Scanning Prevention — GitHub Push Protection

## Problem

GitHub's secret scanning push protection, commit geçmişinde herhangi bir PAT/token varsa tüm branch push'unu engeller. *Sonraki commit'te token'ı silsen bile ilk commit hala geçmişte olduğu için push reddedilir.*

## Tespit

GitHub push sırasında şu hata:
```
remote: - GITHUB PUSH PROTECTION
remote:     - Push cannot contain secrets
remote:
remote:       —— GitHub Personal Access Token ——————
remote:        locations:
remote:          - commit: <sha>
remote:            path: <file>:<line>
```

## Anlık Çözüm: Squash + Force Push

Token içeren commit(ler)i squash et ki token hiç GitHub'a ulaşmasın:

```bash
cd /c/Users/marko/hermes-full-backup

# Kaç commit olduğunu görmek için
git log --oneline -5

# Token içeren commit dahil tümünü squash et
git reset --soft HEAD~N    # N = token içeren commit sayısı
git commit -m "mesaj"
git push --force origin main
```

Uyarı: `--force` sadece tek kişilik veya izole branch'lerde kullan.

## Kritik: Kısmi/Truncated Token'lar DAHİ Tetikler

GitHub'ın secret scanner'ı **token prefix'lerini** arar — tam token olması gerekmez.
Şu örneklerin TÜMÜ push protection'ı tetikler:

```
***REMOVED***...KxUM             ← kırpılmış, ama `ghp_` prefix'i yeterli
github...eT6B             ← kırpılmış, ama `github_pat_` ima ediyor
github_pat_...            ← kırpılmış, en tehlikelisi
```

**YANLIŞ inanç**: "Token'ı kırparsam (son karakterleri `...` yaparsam) güvende olurum."
**GERÇEK**: GitHub scanner'ı `ghp_` veya `github_pat_` prefix'ini gördüğü an bloklar.

### Güvenli Yöntem — Token'dan Eser Bırakma

Sadece kırpmak yetmez. Dosyayı tamamen yeniden yaz:

```bash
# 1. Eski dosyayı sil
rm references/auth-diagnosis-20260611.md

# 2. Baştan yaz — hiçbir token prefix'i, hiçbir kırpılmış versiyon yok
#    "ghp_" kelimesi bile geçmemeli
```

Veya token türünü metin olarak anlat, örnek gösterme:
```
YANLIŞ: Classic PAT (`***REMOVED***...KxUM`)
DOĞRU: Classic PAT (40 karakter, `ghp_` ile başlıyor, expired)
```

NOT: `ghp_` veya `github_pat_` prefix'lerini örnek olarak göstermek bile GitHub scanner'ı tarafından yakalanabilir. En güvenlisi: "Classic PAT" veya "Fine-grained PAT" diyerek geç, hiç prefix gösterme.

## Önleyici: Push Öncesi Tarama

Push öncesi referans dosyalarında PAT pattern'lerini tara:

```bash
grep -rn "ghp_\\|github_pat_\\|gho_\\|ghu_\\|ghs_\\|ghr_" skills/devops/gece-3-github-yedek/references/
# Çıktı varsa → push BLOCKLANIR. Dosyayı COMPLETELY rewrite et.
```

Varsa: **patch ile düzeltme yapma!** Dosyayı baştan yaz — tek bir `ghp_` veya `github_pat_` prefix'i kalmamalı.

## Kalıcı Çözüm

Aşağıdaki dosyalarda PAT token'ları bulunabilir. Push öncesi kontrol et:

- `references/auth-diagnosis-*.md`
- `references/fine-grained-pat-diagnosis.md`
- `references/github-credential-diagnosis.md`

## .gitignore Skills Dışlaması

hermes-full-backup gibi skill yedekleme repolarında .gitignore içinde `skills/` varsa git add skills/ sessizce başarısız olur:
```
The following paths are ignored by one of your .gitignore files:
skills
```

Çözüm: `.gitignore`'dan `skills/` satırını kaldır veya `# Skills - tracked for backup` yorumuyla değiştir.

## Referans Yazım Kuralı

Referans dosyalarında asla ham PAT yazma, asla kırpılmış token prefix'i (`ghp_...`, `github_pat_...`) kullanma.
Bunun yerine token türünü metin olarak anlat:

- YANLIŞ: `***REMOVED***...KxUM`
- YANLIŞ: `github_pat_...`
- DOĞRU: "Classic PAT (40 karakter, expired)"
- DOĞRU: "Fine-grained PAT (3 repo yetkisi)"
