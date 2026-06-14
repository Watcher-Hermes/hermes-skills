# BAD - Routing logic in code instead of markdown tables
if (intent.includes('deploy')) { agent = opsAgent; }
```

Keep routing declarative in `CLAUDE.md` markdown tables. It is inspectable, editable, and debuggable.