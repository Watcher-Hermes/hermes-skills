# WRONG: Limits without requests — requests default to limits, over-reserves capacity
resources:
  limits:
    cpu: "2"
    memory: "1Gi"