## Core Workload Patterns

### Deployment — Production Template

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  namespace: my-namespace
  labels:
    app: my-app
    version: "1.0.0"
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1          # Allow 1 extra pod during update
      maxUnavailable: 0    # Never reduce below desired count
  template:
    metadata:
      labels:
        app: my-app
        version: "1.0.0"
    spec: