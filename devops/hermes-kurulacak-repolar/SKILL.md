---
name: hermes-kurulacak-repolar
description: >-
  Hermes Agent kurulumu için gerekli GitHub repolarının listesi ve
  sıralı kurulum talimatları. Watcher-Hermes/hermes-full-backup
  reposundaki KURULACAK_REPOLAR.md dosyasını referans alır.
version: 1.0.0
author: hermes-agent
license: MIT
metadata:
  hermes:
    tags: [kurulum, github, repo, setup, migration]
    related_skills:
      - hermes-migration-restore
      - github-repo-management
---

# Hermes Kurulacak GitHub Repoları

## Amaç

Hermes Agent yeni bir bilgisayara kurulurken hangi GitHub repolarının
banklone edilmesi gerektiğini ve hangi sırayla kurulacağını tanımlar.

## Repo Listesi

| Sıra | Repo | URL | Durum |
|------|------|-----|:----:|
| 1 | hermes-full-backup | https://github.com/Watcher-Hermes/hermes-full-backup | ❌ Bulunamadı |
| 2 | hermes-gemini-copilot | https://github.com/Izleyici-Hermes/hermes-gemini-copilot | ✅ |
| 3 | ai-engineering-from-scratch-zh | https://github.com/fancyboi999/ai-engineering-from-scratch-zh | ✅ 489 skill |
| 4 | kali-pentest | https://github.com/x-glacier/kali-pentest | ✅ 269 araç |
| 5 | wifi-ag-tarayici | https://github.com/Izleyici-Hermes/wifi-ag-tarayici | ✅ |
| 6 | runners-journey | https://github.com/Izleyici-Hermes/runners-journey | ✅ |
| 7 | hermes-studio | https://github.com/EKKOLearnAI/hermes-studio | ✅ 7.890★ Web dashboard |
| 8 | share-skill | https://github.com/Noshkoto/hermes-share-skill | ✅ Session export skill |
| 9 | paper-deep-reader | https://github.com/kingmt123/paper-deep-reader | ✅ Akademik makale okuma |
| 10 | hersona | https://github.com/shiro-0x/hersona | ✅ 6 adet kişilik şablonu |

## Kaynak Dosya

Detaylı açıklamalar ve kurulum komutları:

```
C:\Users\marko\hermes-backup\KURULACAK_REPOLAR.md
```

Bu dosya `Watcher-Hermes/hermes-full-backup` reposunda version
control altındadır. Güncellemek için:

```bash
cd /c/Users/marko/hermes-backup
# KURULACAK_REPOLAR.md düzenle
git add KURULACAK_REPOLAR.md
git commit -m "Repo listesi güncellendi"
git push origin main
```

## Toplu Klonlama

Tüm repoları tek seferde indirmek için:

```bash
mkdir -p ~/hermes-repos && cd ~/hermes-repos
git clone https://github.com/Watcher-Hermes/hermes-full-backup.git || echo "NOT: repo bulunamadi, manuel olustur"
git clone https://github.com/asdafgf/hermes-gemini-copilot.git
git clone https://github.com/fancyboi999/ai-engineering-from-scratch-zh.git
git clone https://github.com/x-glacier/kali-pentest.git
git clone https://github.com/asdafgf/wifi-ag-tarayici.git
git clone https://github.com/asdafgf/runners-journey.git
echo "Tüm repolar indirildi."
```

## Kurulum Notları

### Hermes Studio (hermes-web-ui)
```bash
npm install -g hermes-web-ui      # 59 package, ~10sn
hermes-web-ui start               # localhost:8648
```
- Port: 8648
- Log: ~/.hermes-web-ui/server.log
- MCP server otomatik eklenir (72 MCP tool)
- Uninstall: `npm uninstall -g hermes-web-ui`

## Pitfall

- `Watcher-Hermes/hermes-full-backup` repo'su GitHub'da bulunamadi (404). Ya silinmis ya da hic olusturulmamis. Yedekleme icin `C:\Users\marko\hermes-skills-backup\` klasoru lokal yedek olarak kullaniliyor. GitHub'a push icin yeni repo olusturulmasi gerekiyor (PAT fine-grained oldugu icin REST API ile olusturulamadi).

## Yeni Repo Ekleme

Yeni bir GitHub reposu Hermes kurulumuna eklendiğinde:

1. `KURULACAK_REPOLAR.md` dosyasına ekle (sıraya uygun)
2. Bu skill'i güncelle: `skill_manage(action='patch')`
3. Obsidian notunu güncelle: `Hermes/Hermes-Kurulacak-Repolar.md`
4. GitHub'a push et
