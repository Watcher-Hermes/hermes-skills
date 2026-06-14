# Backup İnfrastrüktür Durumu — 2026-06-14

## Gözlem

Bu tarihte `asdafgf` GitHub kullanıcısı API'dan 404 dönüyor.
Kullanıcı adı `Izleyici-Hermes` olarak değiştirilmiş (hafızada kayıtlı).
`Watcher-Hermes` organizasyonu çalışıyor (Obsidian vault push'u başarılı).

## Skills Backup Repo

| Özellik | Durum |
|---------|-------|
| Local repo | `/c/Users/marko/hermes-skills-backup/` — commit'li, branch = master |
| Remote | `https://github.com/asdafgf/hermes-skills.git` — 404 (eski kullanıcı adı) |
| Düzeltme | Remote URL `Izleyici-Hermes` olarak güncellenmeli |

## Öneri

Skills backup repo'sunun remote URL'i güncellenmeli:
1. `cd /c/Users/marko/hermes-skills-backup`
2. `git remote set-url origin https://github.com/Izleyici-Hermes/hermes-skills.git`
3. `GIT_TERMINAL_PROMPT=0 git push origin master`
| Branch | main |
| Son push | Başarılı (`0170b5a`) — MEMORY/USER backup dosyaları dahil |

## Alınan Yedek Dosyaları

Obsidian vault `08-Backup/` klasöründe:
- `MEMORY-yedek-2026-06-14.md` — Hermes MEMORY.md içeriği (76 satır, ~10KB)
- `USER-yedek-2026-06-14.md` — Hermes USER.md içeriği (8 satır, ~1.3KB)

## Öneri

Skills backup repo'su `Watcher-Hermes` org'una taşınmalı:
1. GitHub'da `Watcher-Hermes/hermes-skills-backup` repo'su oluştur
2. `cd /c/Users/marko/hermes-skills-backup && git remote set-url origin https://github.com/Watcher-Hermes/hermes-skills-backup.git`
3. `git push -u origin master`
4. Skill'deki auth stratejilerini Watcher-Hermes org'una güncelle
