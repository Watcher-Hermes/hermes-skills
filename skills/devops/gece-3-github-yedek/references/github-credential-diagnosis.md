# GitHub Credential Conflict Diagnosis

## Problem: `401 Unauthorized` / `Invalid username or token`

### Symptom
```
fatal: Authentication failed for 'https://github.com/asdafgf/<repo>.git'
fatal: could not read Password for 'https://Eymen2016@github.com': terminal prompts disabled
```

The URL shows a username (`Eymen2016`) that is NOT the intended GitHub account (`asdafgf`).

### Root Cause
Windows Credential Manager has saved credentials for a different GitHub account.
Git uses opportunistic credential matching — when the remote URL doesn't contain
an explicit username in the URL, Git reuses whatever credential the credential
manager returns first.

### Diagnosis Steps

#### Step 1: Check configured credential helper
```bash
git config --global --list | grep credential
```
If output is `credential.helper=manager` or similar, credential manager is active.

#### Step 2: Identify the offending credential
```bash
# Windows Credential Manager
powershell -Command "Get-StoredCredential -Target '*git*' | Format-List Target, UserName, Password"
```

#### Step 3: Check what username is being sent
```bash
GIT_ASKPASS=echo git push origin main 2>&1 | head -5
# Look for "Password for 'https://<USERNAME>@github.com'"
```

### Fix Options

#### Option A: Disable credential helper (fast, per-session)
```bash
git config --global credential.helper ""
```
Then embed credentials directly in the remote URL:
```bash
git remote set-url origin "https://asdafgf:<PAT>@github.com/asdafgf/<repo>.git"
```

#### Option B: Clear Windows Credential Manager
```powershell
# Remove all git credentials
cmdkey /delete:git:https://github.com

# Or via PowerShell
Remove-StoredCredential -Target "git:https://github.com"
```

#### Option C: Use SSH instead (permanent)
```bash
git remote set-url origin git@github.com:asdafgf/<repo>.git
```
Requires SSH key added to GitHub account first.

### Verification
```bash
git remote -v                          # Check URL
GIT_TERMINAL_PROMPT=0 git fetch --dry-run 2>&1  # Test auth without pushing
```

## Obsidian Vault Specific

The `Obsidian Vault` has a remote URL of:
```
https://github.com/asdafgf/obsidian-vault.git
```
No username in URL → Git will try credential manager → gets `Eymen2016` → 401.

### Confirmed Fix for This Setup
```bash
cd "***REMOVED-BASE64*** Vault"
git config --global credential.helper ""
git remote set-url origin "https://asdafgf:<VALID_PAT>@github.com/asdafgf/obsidian-vault.git"
GIT_TERMINAL_PROMPT=0 git push origin main
```
Where `<VALID_PAT>` is a classic PAT with `repo` scope.

## Skills Backup Specific

The `hermes-skills-backup` directory has a remote URL set to SSH:
```
git@github.com:asdafgf/hermes-skills.git
```

### When SSH fails
- Check if SSH key exists: `ls -la ~/.ssh/`
- Check if key is added: `ssh -T git@github.com`
- If key exists but not added: add to GitHub Settings → SSH and GPG keys
- If no key: `ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N "" -C "hermes-backup-cron"`

### Fallback to HTTPS+PAT
```bash
cd /c/Users/marko/hermes-skills-backup
git remote set-url origin "https://asdafgf:<PAT>@github.com/asdafgf/hermes-skills.git"
GIT_TERMINAL_PROMPT=0 git push origin master
```
