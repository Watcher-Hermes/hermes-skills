# Inspect trace
for call in dspy.settings.trace:
    print(f"Prompt: {call['prompt']}")
    print(f"Response: {call['response']}")
```