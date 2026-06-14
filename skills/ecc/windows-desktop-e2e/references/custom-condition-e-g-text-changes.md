# Custom condition (e.g. text changes)
page.wait_until(lambda: page.get_text(page.by_id("lblStatus")) == "Ready")
```

**Never use `time.sleep()` as primary synchronization** — use `wait()` or `wait_until()`.