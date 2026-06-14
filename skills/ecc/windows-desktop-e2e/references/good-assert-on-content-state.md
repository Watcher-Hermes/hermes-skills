# GOOD: assert on content / state
assert page.get_text(page.by_id("lblStatus")) == "Logged in"
assert page.by_id("btnLogout").is_enabled()
```

```python