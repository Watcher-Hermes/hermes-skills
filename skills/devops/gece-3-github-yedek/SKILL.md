---

name: gece-3-github-yedek
description: >-
  Her gece saat 03:00'te tüm Hermes skill'lerini ve Obsidian vault
  klasörünü GitHub'a yedekler. Skills reposu yoksa MCP GitHub ile
  oluşturur, varsa push eder. Obsidian vault zaten GitHub'a bağlıdır.
  Sonuç Telegram'a bildirilir. Auth sorunları için çoklu strateji
  kullanır: SSH, HTTPS+PAT, MCP GitHub.
version: 2.2.0
author: hermes-agent
license: MIT
metadata:
  hermes:
    tags: [yedek, github, nightly, backup, cron, skills, obsidian]
audience: maintainer
related_skills:
      - obsidian-vault-kurallari
      - tam-sistem-yetkisi
      - nightly-self-improvement
      - env-kayit-kurallari
      - github-auth
---

# Gece 3 Github Yedek

Bu skill modüler bir yönlendiricidir. İhtiyacınız olan bölümü seçin ve ilgili reference dosyasını yükleyin.

## 📂 Bölümler

| Bölüm | Reference Dosyası |
|-------|------------------|
| Amaç | `references/ama.md` |
| Cron Job | `references/cron-job.md` |
| ÖN KOŞUL: PAT Scope Doğrulama | `references/n-ko-ul-pat-scope-do-rulama.md` |
| PAT fine-grained token IÇIN: Repository access → All repositories → Read and Write | `references/pat-fine-grained-token-i-in-repository-access-all-repositori.md` |
| Auth Stratejileri (öncelik sırasıyla) | `references/auth-stratejileri-ncelik-s-ras-yla.md` |
| Obsidian vault git config'den PAT'ı ayıkla | `references/obsidian-vault-git-config-den-pat-ay-kla.md` |
| gh CLI (keyring'de kendi OAuth token'ı var) | `references/gh-cli-keyring-de-kendi-oauth-token-var.md` |
| MCP GitHub üzerinden doğrudan dosya push | `references/mcp-github-zerinden-do-rudan-dosya-push.md` |
| Adımlar (cron tarafından otomatik çalıştırılır) | `references/ad-mlar-cron-taraf-ndan-otomatik-al-t-r-l-r.md` |
| SSH test | `references/ssh-test.md` |
| PAT test — önce /user ile ana hesap kontrolü | `references/pat-test-nce-user-ile-ana-hesap-kontrol.md` |
| Izleyici-Hermes kullanıcısı kontrolü (asdafgf yeniden adlandırıldı) | `references/izleyici-hermes-kullan-c-s-kontrol-asdafgf-yeniden-adland-r-.md` |
| Git credential helper'ı devre dışı bırak (Eymen2016 çakışması önlemi) | `references/git-credential-helper-devre-d-b-rak-eymen2016-ak-mas-nlemi.md` |
| Backup klasörü oluştur (yoksa) | `references/backup-klas-r-olu-tur-yoksa.md` |
| Skills'i kopyala | `references/skills-i-kopyala.md` |
| Git repo oluştur/yönet | `references/git-repo-olu-tur-y-net.md` |
| Eğer .git yoksa init et | `references/e-er-git-yoksa-init-et.md` |
| Push dene — SSH önce | `references/push-dene-ssh-nce.md` |
| SSH başarısızsa HTTPS+PAT dene | `references/ssh-ba-ar-s-zsa-https-pat-dene.md` |
| Önce JavaNotes submodule'ünü işle | `references/nce-javanotes-submodule-n-i-le.md` |
| Ana repo | `references/ana-repo.md` |
| Branch adını belirle | `references/branch-ad-n-belirle.md` |
| Push dene | `references/push-dene.md` |
| Başarısızsa PAT dene | `references/ba-ar-s-zsa-pat-dene.md` |
| Python betiği ile Telegram bildirimi | `references/python-beti-i-ile-telegram-bildirimi.md` |
| Pitfall'lar | `references/pitfall-lar.md` |
| Başarı Kriterleri | `references/ba-ar-kriterleri.md` |
| Referans Dosyaları | `references/referans-dosyalar.md` |
| Bakım | `references/bak-m.md` |

## Kullanım

1. İhtiyacın olan bölümü belirle
2. `skill_view(name="...", file_path="references/...")` ile yükle
