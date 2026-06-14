# Hermes Config Repo Remote Migration — 14 June 2026

## Problem

`C:\Users\marko\AppData\Local\hermes\.git` (main Hermes Agent config repo)
had its remote set to `asdafgf/hermes-backup.git` which returned 404
(Repository not found).

This blocked `git push` after new RL system files were added.

## Diagnosis

```bash
cd /c/Users/marko/AppData/Local/hermes
git remote -v
# origin  https://asdafgf:token@github.com/asdafgf/hermes-backup.git  ← 404

git push origin main
# fatal: repository 'https://github.com/asdafgf/hermes-backup.git/' not found
```

Multiple backup repos existed on disk with working remotes:

| Local path | Remote | Status |
|---|---|---|
| `AppData\Local\hermes` | `asdafgf/hermes-backup.git` | ❌ 404 |
| `C:\Users\marko\hermes-backup` | `asdafgf/hermes-full-backup.git` | ✅ Live |
| `C:\Users\marko\hermes-full-backup` | `Watcher-Hermes/hermes-full-backup.git` | ✅ Live |

The `asdafgf/hermes-backup` repo was likely renamed/merged into
`asdafgf/hermes-full-backup` which later moved to `Watcher-Hermes/hermes-full-backup`.

## Fix

```bash
cd /c/Users/marko/AppData/Local/hermes
git remote set-url origin https://github.com/Watcher-Hermes/hermes-full-backup.git
```

Applied to both `AppData\Local\hermes` and `C:\Users\marko\hermes-backup`.

## New Files Added

The RL observation system (`rl_observation/`) was untracked in all repos.
Added 9 files (8 code + .gitignore) with working remote, then pushed:

```bash
cd /c/Users/marko/hermes-backup
cp /c/Users/marko/AppData/Local/hermes/rl_observation/*.py ./
cp /c/Users/marko/AppData/Local/hermes/rl_observation/TALIMAT_KILAVUZU.md ./
git add rl_observation/
git commit -m "feat: RL observation sistemi..."
git push origin main
```

## Principle

The `AppData\Local\hermes` config repo remote MUST point to the active
backup repo. Periodically verify:

```bash
cd /c/Users/marko/AppData/Local/hermes
git ls-remote origin HEAD 2>&1 | head -1
```

If this fails, the remote URL is stale.

## Related

- gece-3-github-yedek pitfall #15 — repo moved/migration for Obsidian vault
- `references/github-username-migration.md` — GitHub username change procedure
