# --- Pod status and logs ---
kubectl get pods -n my-namespace
kubectl get pods -n my-namespace -o wide          # Show node assignment
kubectl describe pod <pod-name> -n my-namespace   # Events and state details
kubectl logs <pod-name> -n my-namespace           # Current logs
kubectl logs <pod-name> -n my-namespace --previous  # Logs from crashed container
kubectl logs <pod-name> -n my-namespace -c <container>  # Multi-container pod