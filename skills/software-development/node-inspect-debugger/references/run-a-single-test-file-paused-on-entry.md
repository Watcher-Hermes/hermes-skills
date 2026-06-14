# Run a single test file paused on entry
node --inspect-brk ./node_modules/vitest/vitest.mjs run --no-file-parallelism src/app/foo.test.tsx
```

In another terminal: `node inspect -p <pid>`, then `sb('src/app/foo.tsx', 42)`, `cont`.

Use `--no-file-parallelism` (vitest) or `--runInBand` (jest) so only one worker exists — debugging a pool is painful.