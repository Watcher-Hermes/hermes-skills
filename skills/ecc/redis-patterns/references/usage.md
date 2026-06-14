# Usage
token = acquire_lock("order:payment:123")
if token:
    try:
        process_payment()
    finally:
        release_lock("order:payment:123", token)
```

> For multi-node setups use the `redlock-py` library which implements the full Redlock algorithm.