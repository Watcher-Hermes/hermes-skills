# --- Port-forward for local debugging ---
kubectl port-forward pod/<pod-name> 8080:8080 -n my-namespace
kubectl port-forward svc/my-app 8080:80 -n my-namespace