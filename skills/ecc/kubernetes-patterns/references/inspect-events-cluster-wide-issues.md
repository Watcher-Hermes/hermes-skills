# --- Inspect events (cluster-wide issues) ---
kubectl get events -n my-namespace --sort-by='.lastTimestamp'