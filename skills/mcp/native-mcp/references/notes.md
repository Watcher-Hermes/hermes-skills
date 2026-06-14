## Notes

- MCP tools are called synchronously from the agent's perspective but run asynchronously on a dedicated background event loop
- Tool results are returned as JSON with either `{"result": "..."}` or `{"error": "..."}`
- The native MCP client is independent of `mcporter` -- you can use both simultaneously
- Server connections are persistent and shared across all conversations in the same agent process
- Adding or removing servers requires restarting the agent (no hot-reload currently)