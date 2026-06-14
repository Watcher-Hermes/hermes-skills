# Values are base64-encoded (NOT encrypted — use Sealed Secrets or ESO for real encryption)
data:
  db-password: czNjcjN0  # base64 of 's3cr3t'
```

> **Important:** Raw Kubernetes Secrets are only base64-encoded, not encrypted at rest unless your cluster has encryption configured. Use [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets) or [External Secrets Operator](https://external-secrets.io) for production.

---