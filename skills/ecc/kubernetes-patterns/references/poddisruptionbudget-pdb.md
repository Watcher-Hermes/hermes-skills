## PodDisruptionBudget (PDB)

Prevent too many pods going down during node drains or rolling updates:

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: my-app-pdb
  namespace: my-namespace
spec:
  minAvailable: 2           # OR use maxUnavailable: 1
  selector:
    matchLabels:
      app: my-app
```

---