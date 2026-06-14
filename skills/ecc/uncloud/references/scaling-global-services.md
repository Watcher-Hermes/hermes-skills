## Scaling & Global Services

```bash
uc scale web 5    # 5 replicas (spread across machines)
uc scale web 1    # Scale down
```

```yaml
services:
  caddy:
    deploy:
      mode: global   # One container on every machine
```

---