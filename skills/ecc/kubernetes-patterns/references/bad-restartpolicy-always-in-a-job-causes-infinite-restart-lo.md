# BAD: restartPolicy: Always in a Job (causes infinite restart loop)
spec:
  restartPolicy: Always   # Use OnFailure or Never for Jobs
```

---