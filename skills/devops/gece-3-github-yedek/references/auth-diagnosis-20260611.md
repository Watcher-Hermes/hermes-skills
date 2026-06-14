# Auth Diagnosis — 2026-06-11 Nightly Backup

## Problem

Gece yedek cron job'u GitHub'a push edemedi. Sebepler:
- Repo'lar GitHub'da mevcut değildi (`hermes-skills`, `obsidian-vault`)
- Fine-grained PAT repo oluşturamıyor
- Classic PAT expired
- SSH key GitHub'a ekli değil

## Auth Test Sonuçları

### 1. SSH
`~/.ssh/id_ed25519` var ama GitHub hesabına (asdafgf) eklenmemiş.
**Çözüm**: GitHub → Settings → SSH and GPG keys → New SSH key.

### 2. Classic PAT
40 karakter, `ghp_` ile başlıyor, .env'de mevcut ama expired/revoked.
**Çözüm**: GitHub → Settings → Developer settings → Tokens (classic) → yeni token, `repo` scope'u işaretle.

### 3. Fine-Grained PAT
`gh` CLI ile çalışır, repo listeleme yapar, /user 200 verir. Ama repo oluşturamaz.
**Çözüm**: Ya classic PAT kullan, ya GitHub'da manuel repo oluştur.

## Repo Durumu (GitHub)

asdafgf hesabındaki mevcut repo'lar:
- `wifi-ag-tarayici` (public) — ADMIN
- `hermes-gemini-copilot` (public) — ADMIN
- `runners-journey` (public) — ADMIN

Eksik repo'lar:
- `hermes-skills` — GitHub'da 404
- `obsidian-vault` — GitHub'da 404

## Çözüm Yolu

1. GitHub.com'da manuel repo oluştur
2. Push et
3. Yeni classic PAT oluştur ve .env'ye yaz
