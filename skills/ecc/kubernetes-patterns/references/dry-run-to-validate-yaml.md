# --- Dry-run to validate YAML ---
kubectl apply -f deployment.yaml --dry-run=client
kubectl apply -f deployment.yaml --dry-run=server   # Validates against live cluster
```

### Diagnosing Common Errors

```bash