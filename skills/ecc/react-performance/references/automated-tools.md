## Automated Tools

Many of these rules are now automated:

- **Next.js 13.5+ Optimize Package Imports** — barrel import optimization
- **React Compiler** (RFC, in canary) — auto-memoization
- **Turbopack** — faster builds, better tree-shaking
- **Bundle Analyzer** (`@next/bundle-analyzer`) — visualize first-load JS

When the project ships React Compiler, demote `rerender-*` manual memoization rules to "review-only" — the compiler handles them. Manual `useMemo`/`useCallback` becomes unnecessary noise.