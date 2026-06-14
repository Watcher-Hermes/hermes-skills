# BAD - API keys in agent files or CLAUDE.md
Your OpenAI API key is sk-xxxxxxxx
```

Use environment variables or a `.env` file loaded by scripts. Agents reference `process.env.API_KEY`.

### External Database for Simple State

```markdown