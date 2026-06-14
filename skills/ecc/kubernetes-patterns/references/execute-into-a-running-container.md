# --- Execute into a running container ---
kubectl exec -it <pod-name> -n my-namespace -- sh
kubectl exec -it <pod-name> -n my-namespace -- bash