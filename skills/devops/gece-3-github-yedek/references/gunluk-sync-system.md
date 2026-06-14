# Günlük Sync + Haftalık Bakım Sistemi (2026-06-13)

## Günlük no_agent Sync (21:00)

**Cron job:** `gunluk-backup-sync` (job_id: 86ef5e46f92e)
**Script:** `scripts/sync_hermes_backup.py`
**Schedule:** `0 21 * * *` (her gün 21:00)
**no_agent:** true

### Yaptıkları:
1. `%USERPROFILE%\hermes-backup` repo'sunu clone/pull eder
2. **Skills diff:** Hermes'teki skills/ ile GitHub'daki skills/ arasında SHA256 manifest karşılaştırması yapar
   - Sadece eklenen/değişen dosyaları kopyalar (tamamen sil+tekrar kopyala)
   - `.bundled_manifest`, `.usage.json` gibi iç dosyaları atlar
3. **Memory sync:** `memories/MEMORY.md` ve `memories/USER.md` dosyalarını `Hermes Memor/` klasörüne kopyalar
4. **state.db:** Boyut/mtime değişimini kontrol eder
   - 1MB+ fark veya son 1 saatte değişiklik varsa zip'ler
   - 55MB parçalara böler (GitHub limiti)
5. Değişiklik varsa `git add + commit + push` yapar
6. **Sessiz:** Değişiklik yoksa hiçbir çıktı vermez

### Log:
`%HERMES_HOME%\logs\backup-sync.log`

## Haftalık LLM Bakım (Çarşamba)

**Cron job:** `haftalik-bakim-carsamba` (job_id: 066c3c1ed9e3)
**Schedule:** `0 */4 * * 3` (Çarşamba günü 4 saatte bir)
**Skills:** obsidian-vault-path-fix, tam-sistem-yetkisi

### Startup Trigger:
`scripts/haftalik-bakim-startup.bat` → Windows Startup klasörüne kopyalanır.
- Bilgisayar açılınca gün kontrolü yapar
- Çarşamba ise `%HERMES_HOME%\haftalik-bakim.flag` dosyası oluşturur
- Gateway çalışmıyorsa başlatır
- Flag, cron job tarafından okunur ve silinir

### LLM Bakımı Yaptıkları (flag varsa):
1. GitHub'daki skills/ ile karşılaştırma (silinmiş/sahipsiz skill'ler)
2. config.yaml güncellik kontrolü
3. Genel durum raporu

### Flag mekanizması:
- Flag yoksa cron job sessizce biter (LLM harcamaz)
- Startup .bat sadece Çarşamba günü flag oluşturur
- Cron job `0 */4 * * 3` ile günde 6 kez dener (00, 04, 08, 12, 16, 20)
- İlk flag bulan cron bakımı yapıp flag'i siler

## Cron Job Özeti

| Job ID | Adı | Schedule | Tip | Ne yapar |
|--------|-----|----------|-----|----------|
| 6b3a7cd39da0 | gece-3-github-yedek | 40 20 * * * | LLM | Obsidian vault push |
| 86ef5e46f92e | gunluk-backup-sync | 0 21 * * * | no_agent | skills+memory+state.db diff→push |
| 066c3c1ed9e3 | haftalik-bakim-carsamba | 0 */4 * * 3 | LLM | Skill temizlik + config kontrol |
