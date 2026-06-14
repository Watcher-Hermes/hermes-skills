# Fine-Grained PAT Diagnosis

## Problem: PAT authenticates but cannot push or create repos

### Symptom
```
# PAT passes user auth test
curl -H "Authorization: token github_pat_..." https://api.github.com/user
# → HTTP 200, shows user "asdafgf"

# BUT fails on repo operations
curl -H "Authorization: token github_pat_..." https://api.github.com/user/repos
# → HTTP 401 {"message":"Bad credentials"}

curl -H "Authorization: token github_pat_..." https://api.github.com/repos/asdafgf/obsidian-vault
# → HTTP 401 {"message":"Bad credentials"}

# git push fails
git push origin main
# → fatal: Repository not found
```

### Root Cause
The PAT is a **fine-grained token** (not classic). Fine-grained tokens have these restrictions:

1. **Scope-limited to specific repos** — Only repos explicitly selected in the token settings are accessible. All others return `Repository not found`.
2. **No `repo` scope** — Fine-grained tokens don't use scopes like `repo`. Instead they use per-repo permissions (Read/Write/Admin).
3. **Expired tokens** — Fine-grained tokens can expire silently. `/user` may still return 200 even for expired tokens for a grace period.
4. **Deleted repos** — If a repo was deleted on GitHub, the remote URL still points to it. Git returns `Repository not found` even with a valid token.

### Diagnosis Steps

#### Step 1: Check token type
```bash
# Check if token is fine-grained (starts with github_pat_)
echo "$TOKEN" | head -c 15
# github_pat_...  → fine-grained
# ghp_...         → classic (but maybe expired)
```

#### Step 2: List accessible repos
```python
import urllib.request, json

req = urllib.request.Request("https://api.github.com/user/repos?per_page=100&type=all")
req.add_header("Authorization", f"token {TOKEN}")
try:
    resp = urllib.request.urlopen(req)
    repos = json.loads(resp.read())
    print(f"Accessible repos ({len(repos)}):")
    for r in repos:
        print(f"  {r['full_name']} (private={r['private']})")
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()}")
    print("→ Token has NO repo access. This is a restricted classic or fine-grained token.")
```

#### Step 3: Check repo existence
```bash
# Check if repo actually exists on GitHub
curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: token $TOKEN" \
  https://api.github.com/repos/asdafgf/obsidian-vault
# 200 = exists and accessible
# 401/403 = exists but token can't see it (fine-grained restriction)
# 404 = repo doesn't exist
```

#### Step 4: Check scopes header
```bash
curl -s -D - -o /dev/null \
  -H "Authorization: token $TOKEN" \
  https://api.github.com/user | grep -i X-OAuth-Scopes
# X-OAuth-Scopes: repo, workflow  → full access (classic)
# X-OAuth-Scopes: none or empty   → fine-grained or restricted
```

### Fix

#### Fix A: Upgrade to classic PAT (recommended)
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Create new token with scopes: `repo`, `workflow`
3. Set no expiration (or 1 year)
4. Update `.env`: `GITHUB_TOKEN=<new_token>`

#### Fix B: Add repos to existing fine-grained PAT
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens
2. Select the token → Repository access → "All repositories" or add the missing ones
3. Set repository permissions → Contents: Read and write

#### Fix C: Recreate deleted repos on GitHub
If repo was deleted (e.g., `obsidian-vault`):
1. Create new empty repo on GitHub manually (web interface)
2. Or use PAT with `repo` scope via REST API
3. Then push from local:

```bash
cd "***REMOVED-BASE64*** Vault"
git remote set-url origin "https://asdafgf:<CLASSIC_PAT>@github.com/asdafgf/obsidian-vault.git"
git push -u origin main
```

### Hermes-Specific Notes
- The embedded PAT `***GITHUB_PAT_REMOVED***` is a **fine-grained token** with access to 3 repos only:
  - `asdafgf/hermes-gemini-copilot`
  - `asdafgf/runners-journey`
  - `asdafgf/wifi-ag-tarayici`
- `obsidian-vault` repo was deleted from GitHub (returns 404)
- `hermes-skills` repo was never created on GitHub
- SSH key exists at `~/.ssh/id_ed25519.pub` but is not added to GitHub account
