# ServiceAccount with token disabled — safest default
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-app-sa
  namespace: my-namespace
automountServiceAccountToken: false   # No K8s API token injected into pods
```

```yaml