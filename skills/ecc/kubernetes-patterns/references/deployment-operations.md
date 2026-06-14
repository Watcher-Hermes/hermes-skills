# --- Deployment operations ---
kubectl rollout status deployment/my-app -n my-namespace
kubectl rollout history deployment/my-app -n my-namespace
kubectl rollout undo deployment/my-app -n my-namespace      # Rollback
kubectl rollout undo deployment/my-app --to-revision=2 -n my-namespace