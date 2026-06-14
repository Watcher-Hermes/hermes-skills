# Android Project Git Push Patterns

## .gitignore for Android Projects

The default Android `.gitignore` must exclude build intermediates (nested `**/build`), not just root `/build`:

```gitignore
*.iml
.gradle
**/build
local.properties
release.keystore
*.keystore
*.jks
*.apk
*.aab
nul
.idea/
.DS_Store
```

Key differences from default:
- `**/build` (not `/build`) — covers `app/build/`, `app/build/intermediates/`, etc.
- `release.keystore` + `*.keystore` + `*.jks` — sensitive signing keys
- `nul` — Windows artifact from redirected output

## Push Flow

```bash
# 1. Write .gitignore first
cat > .gitignore << 'EOF'
*.iml
.gradle
**/build
local.properties
release.keystore
*.keystore
*.jks
*.apk
*.aab
.idea/
.DS_Store
EOF

# 2. Init and add
git init
git add -A
git commit -m "Initial commit - Android app"

# 3. Create repo (may fail with fine-grained PAT)
gh repo create owner/RepoName --private --source=. --remote=origin --push

# 4. Fallback — push to existing monorepo if repo creation fails
git remote add origin https://github.com/owner/existing-repo.git
git push origin main
```

## Common Pitfalls

- **`nul` file on Windows** — Delete before `git add`: `rm -f nul`
- **`/build` vs `**/build`** — Gradle creates `app/build/` (nested), not just `build/` (root). Use `**/build`.
- **release.keystore in repo** — Always exclude. This is your app signing key.
- **`.idea/` exclusion** — Prevents IDE config from leaking into repo.
