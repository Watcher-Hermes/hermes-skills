# In another terminal:
node inspect -p <node pid>
```

Then inside `debug>`:

```
sb('dist/app.js', 220)     # or wherever the suspect render is
cont
```

When it pauses, `repl` → inspect `props`, state refs, `useInput` handler values, etc.

### Debugging a running `hermes --tui`

The TUI spawns Node from the Python CLI. Easiest path:

```bash