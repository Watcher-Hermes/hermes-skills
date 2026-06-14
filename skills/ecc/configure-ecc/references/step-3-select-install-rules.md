## Step 3: Select & Install Rules

Use `AskUserQuestion` with `multiSelect: true`:

```
Question: "Which rule sets do you want to install?"
Options:
  - "Common rules (Recommended)" — "Language-agnostic principles: coding style, git workflow, testing, security, etc. (8 files)"
  - "TypeScript/JavaScript" — "TS/JS patterns, hooks, testing with Playwright (5 files)"
  - "Python" — "Python patterns, pytest, black/ruff formatting (5 files)"
  - "Go" — "Go patterns, table-driven tests, gofmt/staticcheck (5 files)"
```

Execute installation:
```bash