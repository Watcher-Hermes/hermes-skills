# Diff-Based Selective Skill Sync to GitHub

## Ne işe yarar

Full backup yerine sadece **yerelde olup GitHub'da OLMAYAN** skill dosyalarını push eder.
Aynı dosyaları tekrar yollamaz. Özellikle ilk sync veya uzun süredir push yapılmamış
bir repo'yu güncellemek için idealdir.

## Adımlar

### 1. Repo'yu clone'la (shallow, hızlı)

```bash
cd /tmp
git clone --depth 1 https://github.com/asdafgf/hermes-full-backup.git hermes-compare
```

`--depth 1` sadece son commit'i çeker, tüm history'yi indirmez.

### 2. SKILL.md seviyesinde karşılaştır

Dizin seviyesinde değil, **dosya seviyesinde** karşılaştır:

```bash
# Yereldeki tüm SKILL.md'leri bul
find ***REMOVED-BASE64*** -name "SKILL.md" \
  -not -path "*/skills_archive/*" \
  -not -path "*/.curator_backups/*" \
  -not -path "*/.hub/*" > /tmp/local_skills.txt

# Her birinin GitHub'da olup olmadığını kontrol et
while IFS= read -r local_file; do
  rel_path="${local_file#***REMOVED-BASE64***}"
  github_path="/tmp/hermes-compare/skills/$rel_path"
  if [ ! -f "$github_path" ]; then
    echo "EKSIK: $rel_path"
  fi
done < /tmp/local_skills.txt
```

### 3. Sadece eksikleri kopyala

```bash
while IFS= read -r local_file; do
  rel_path="${local_file#***REMOVED-BASE64***}"
  github_path="/tmp/hermes-compare/skills/$rel_path"
  if [ ! -f "$github_path" ]; then
    mkdir -p "$(dirname "$github_path")"
    cp "$local_file" "$github_path"
  fi
done < /tmp/local_skills.txt
```

Aynı işlemi **referans dosyaları** (references/, scripts/, templates/) için de yap.
SKILL.md dışındaki dosyaları `find -type f` ile tara, SKILL.md'yi atla.

### 4. Pitfall: skills/ .gitignore'da olabilir

Repo'nun `.gitignore`'ında `skills/` yazıyorsa `git add` normalde ignore eder.
**Force add yap:**

```bash
git add -f skills/
```

`git status --short` ile stage edilen dosyaları doğrula.

### 5. Commit ve push

```bash
git -c user.name="Hermes Backup" -c user.email="hermes@local" \
  commit -m "skills sync: $(date +%Y-%m-%d) - N yeni/eksik skill dosyasi eklendi"
```

### 6. Auth stratejisi

Direct token URL (`https://user:token@github.com/...`) her zaman çalışmaz —
bazı Git sürümlerinde password authentication hatası verir.

**En güvenilir yol:** `gh` CLI cached credentials'ını kullan:

```bash
# Remote URL'yi token'sız haline getir
git remote set-url origin https://github.com/asdafgf/hermes-full-backup.git
# gh CLI auth çalışıyor mu kontrol et
gh auth status
# Push — gh CLI otomatik auth yapar
git push
```

Eğer `gh` CLI yoksa veya auth yoksa:

```bash
# Strateji 1: SSH
git remote set-url origin git@github.com:asdafgf/hermes-full-backup.git
git push

# Strateji 2: HTTPS + PAT (token URL'de)
git remote set-url origin https://asdafgf:***REMOVED***@github.com/asdafgf/hermes-full-backup.git
GIT_TERMINAL_PROMPT=0 git push
```

## Gerçek Kullanım Örneği (12 Haziran 2026)

- Hedef repo: `asdafgf/hermes-full-backup`
- Eksik bulunan: 268 SKILL.md + 18 referans/script = **286 dosya**
- Çoğu `ecc/` kategorisi (Hermes built-in skill'leri) + custom skill'ler
- Push: `gh` CLI auth ile başarılı
- `.gitignore`'da `skills/` vardı → `git add -f` kullanıldı
- Commit: `7e57f2e`, 70,904 satır eklendi

## Full Backup'tan Farkı

| Özellik | Full Backup (`gece-3-github-yedek`) | Diff Sync (bu workflow) |
|---------|------------------------------------|------------------------|
| Ne yapar | Tümünü push eder | Sadece eksikleri push eder |
| Ne zaman | Cron ile her gece 03:00 | Manuel, ihtiyaç duyuldukça |
| Repo | `hermes-skills` + `obsidian-vault` | `hermes-full-backup` (monorepo) |
| Git işlemi | `git add -A` | `git add -f` (force, .gitignore bypass) |
