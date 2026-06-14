# Apply ResourceQuota to limit namespace consumption
kubectl apply -f - <<EOF
apiVersion: v1
kind: ResourceQuota
metadata:
  name: my-namespace-quota
  namespace: my-namespace
spec:
  hard:
    requests.cpu: "4"
    requests.memory: 4Gi
    limits.cpu: "8"
    limits.memory: 8Gi
    pods: "20"
EOF
```

---