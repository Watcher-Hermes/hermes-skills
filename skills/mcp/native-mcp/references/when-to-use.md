## When to Use

Use this whenever you want to:
- Connect to MCP servers and use their tools from within Hermes Agent
- Add external capabilities (filesystem access, GitHub, databases, APIs) via MCP
- Run local stdio-based MCP servers (npx, uvx, or any command)
- Connect to remote HTTP/StreamableHTTP MCP servers
- Have MCP tools auto-discovered and available in every conversation
- Bridge Hermes with Obsidian vaults — see `references/obsidian-mcp.md` for a real-world setup using the `obsidian-pkm` npm package (20 tools for vault read/write/search/link analysis)

For ad-hoc, one-off MCP tool calls from the terminal without configuring anything, see the `mcporter` skill instead.