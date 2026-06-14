# Increase memory limits, check for memory leaks
kubectl describe pod <pod-name> -n my-namespace | grep -A5 "Last State"
```

---