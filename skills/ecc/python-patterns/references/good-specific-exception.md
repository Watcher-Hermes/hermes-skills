# Good: Specific exception
try:
    risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
```

__Remember__: Python code should be readable, explicit, and follow the principle of least surprise. When in doubt, prioritize clarity over cleverness.