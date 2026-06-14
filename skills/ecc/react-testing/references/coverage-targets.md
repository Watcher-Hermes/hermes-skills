## Coverage Targets

| Layer | Target |
|---|---|
| Pure utilities | >=90% |
| Custom hooks | >=85% |
| Presentational components | >=80% — behavior, not lines |
| Container components | >=70% — golden paths + error states |
| Pages | E2E covered separately; smoke test minimum |

Configure via `vitest.config.ts` / `jest.config.js`:

```ts
// vitest.config.ts
test: {
  coverage: {
    provider: "v8",
    reporter: ["text", "html", "lcov"],
    thresholds: {
      lines: 80,
      functions: 80,
      branches: 70,
      statements: 80,
    },
  },
}
```