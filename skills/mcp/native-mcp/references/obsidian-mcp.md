# Obsidian MCP Server (obsidian-pkm)

Real-world setup: connect Obsidian vault to Hermes via `obsidian-pkm` npm package.

## Config (in `~/.hermes/config.yaml`)

```yaml
mcp_servers:
  obsidian:
    command: "npx"
    args: ["-y", "obsidian-pkm"]
    env:
      VAULT_PATH: "C:/Users/marko/OneDrive/Belgeler/Obsidian Vault"
      VAULT_PKM_VAULT_NAME: "Obsidian Vault"
```

**Key env vars:**
- `VAULT_PATH` — **required.** Absolute path to the Obsidian vault directory.
- `VAULT_PKM_VAULT_NAME` — optional. Overrides the vault name used for `obsidian://` URIs; defaults to the basename of VAULT_PATH.
- `VAULT_PKM_OPENAI_KEY` — optional. Enables semantic search (OpenAI embeddings). Without it, full-text search still works but conceptual search is disabled.

## Verification

```bash
# Quick health check
npx -y obsidian-pkm doctor

# With vault path set
VAULT_PATH="C:/Users/marko/OneDrive/Belgeler/Obsidian Vault" npx -y obsidian-pkm doctor
```

Expected output:
```
  ✓ Node.js v24+ (required: >= 20)
  ✓ VAULT_PATH: C:/Users/marko/...
  ✓ Vault is a directory
  ✓ better-sqlite3 loaded
  ✓ sqlite-vec loaded
  ⚠ Templates missing (optional — create 05-Templates/ folder)
  ⚠ OpenAI key missing (semantic search disabled, full-text works)
```

## Tools Provided (20 total)

| Prefix | Tool | Purpose |
|--------|------|---------|
| `mcp_obsidian_` | `vault_write` | Create notes from templates |
| | `vault_read` | Read note contents |
| | `vault_edit` | Surgical string replacement |
| | `vault_search` | Full-text keyword search |
| | `vault_list` | List files and folders |
| | `vault_move` | Move/rename with wikilink update |
| | `vault_links` | Wikilink analysis |
| | `vault_tags` | Tag discovery with counts |
| | `vault_recent` | Recently modified files |
| | `vault_activity` | Cross-conversation session log |
| | +10 more (semantic search, graph, templates, etc.) |

## Pitfalls

1. **Hermes restarts required after config change** — `mcp_servers` hot-reload is NOT supported yet.
2. **`npx` first-run delay** — The first `npx -y obsidian-pkm` downloads and compiles native deps (30-60s). Subsequent runs are instant. Set a high `connect_timeout` (120s+) in the server config.
3. **Environment filtering** — Hermes strips most env vars from MCP subprocesses. `VAULT_PATH` must be set explicitly in the `env:` block, not relied on from shell context.
4. **`doctor` failure without VAULT_PATH** — When run from terminal without the env var, it defaults to `$HOME/Documents/PKM` which may not exist. Always pass the env var when testing.
