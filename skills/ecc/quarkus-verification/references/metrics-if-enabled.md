# Metrics (if enabled)
curl http://localhost:8080/q/metrics
```

Expected responses:
```json
{
  "status": "UP",
  "checks": [
    {
      "name": "Database connection",
      "status": "UP"
    }
  ]
}
```