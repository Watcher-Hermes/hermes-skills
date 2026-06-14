## Security

### Environment Variable Filtering

For stdio servers, Hermes does NOT pass your full shell environment to MCP subprocesses. Only safe baseline variables are inherited:

- `PATH`, `HOME`, `USER`, `LANG`, `LC_ALL`, `TERM`, `SHELL`, `TMPDIR`
- Any `XDG_*` variables

All other environment variables (API keys, tokens, secrets) are excluded unless you explicitly add them via the `env` config key. This prevents accidental credential leakage to untrusted MCP servers.

```yaml
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env: