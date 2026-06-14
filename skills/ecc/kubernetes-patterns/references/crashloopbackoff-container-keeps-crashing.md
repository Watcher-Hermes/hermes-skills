# CrashLoopBackOff: container keeps crashing
kubectl logs <pod-name> --previous -n my-namespace  # Check crash logs
kubectl describe pod <pod-name> -n my-namespace     # Check exit code & OOMKilled