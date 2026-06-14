# GitHub Token Auth Diagnosis

## Token Prefix Quick Guide

| Prefix | Type | Capabilities |
|--------|------|-------------|
| `ghp_` | Classic PAT | Full `repo` scope = create + write + read. Best for automation. |
| `github_pat_` | Fine-grained PAT | Scoped to specific repos/permissions. May authenticate but have zero write access. |
| `gho_` | OAuth token | App-scoped. Rarely used directly. |
| `ghs_` | Server token | GitHub app installation. |

## Two-Tier Auth Diagnostic

Fine-grained PATs (`github_pat_`) can authenticate the user but still fail on repo operations. Run this check:

```bash
TOKEN="the-token-here"

# Tier 1 — /user endpoint (basic auth check)
HTTP_AUTH=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token $TOKEN" \
  "https://api.github.com/user")

# Tier 2 — /user/repos endpoint (repo access check)
HTTP_REPOS=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token $TOKEN" \
  "https://api.github.com/user/repos?per_page=1")

# Interpret
if [ "$HTTP_AUTH" = "200" ]; then
  echo "✓ Token authenticates"
  if [ "$HTTP_REPOS" = "200" ]; then
    echo "✓ Token has repo read access"
    echo "  (check write separately with PUT test)"
  elif [ "$HTTP_REPOS" = "403" ]; then
    echo "✗ Token is read-only on repos (403)"
    echo "  -> Use classic PAT or fix fine-grained PAT permissions"
  elif [ "$HTTP_REPOS" = "401" ]; then
    echo "✗ Token has NO repo access (401)"
    echo "  -> Fine-grained PAT created without selecting any repos"
  fi
else
  echo "✗ Token does not authenticate"
fi
```

## Write Permission Test

```bash
# Quick write check via API
TOKEN="..."
RESULT=$(curl -s -X PUT \
  -H "Authorization: token $TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/contents/test-write-perm.txt" \
  -d '{"message":"perm check","content":"dGVzdA==","branch":"main"}')

if echo "$RESULT" | grep -q '"content"'; then
  echo "✓ Token has WRITE access"
  # Clean up test file
  curl -s -X DELETE -H "Authorization: token $TOKEN" \
    "https://api.github.com/repos/$OWNER/$REPO/contents/test-write-perm.txt" \
    -d '{"message":"cleanup","branch":"main"}' > /dev/null
elif echo "$RESULT" | grep -q "Resource not accessible"; then
  echo "✗ Token is READ-ONLY — classic PAT (ghp_) with repo scope required"
elif echo "$RESULT" | grep -q "Bad credentials"; then
  echo "✗ Token has no access to this repo at all"
elif echo "$RESULT" | grep -q "Not Found"; then
  echo "✗ Repo not found or token has no access to it"
fi
```

## Fix Strategies

### If token is fine-grained (github_pat_) and read-only:
- **Option A:** Create classic PAT at https://github.com/settings/tokens/new with `repo` scope
- **Option B:** Edit the fine-grained PAT at Settings > Developer settings > Fine-grained PATs, add "Contents: write" + "Administration: write" permissions for each target repo
- **Option C:** Push to an existing repo that the token CAN write to (monorepo workaround)

### If token is classic (ghp_) but fails:
- Token may have expired — regenerate
- Token may not have `repo` scope checked — create new one
- GitHub Push Protection may be blocking — clean token references from files

## gh auth token Masking

`gh auth token` returns a MASKED version of the token (e.g., `github...sbFX` at 13 chars), NOT the full token. This means:

- You CANNOT extract the actual token from `gh auth token` for use in API calls
- You CAN use `gh` CLI commands directly (they work with the stored token)
- For custom API calls, use the token value directly (from user or .env) rather than `gh auth token`
