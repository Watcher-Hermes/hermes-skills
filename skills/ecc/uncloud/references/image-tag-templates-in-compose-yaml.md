## Image Tag Templates (in compose.yaml)

```yaml
image: myapp:{{gitdate "20060102"}}.{{gitsha 7}}
image: myapp:{{gitsha 7}}.${GITHUB_RUN_ID:-local}
```

| Function | Output |
|----------|--------|
| `{{gitsha N}}` | First N chars of commit SHA |
| `{{gitdate "format"}}` | Git commit date in Go format |
| `{{date "format"}}` | Current date |

---