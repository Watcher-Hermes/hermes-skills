# Load
loaded_qa = dspy.ChainOfThought("question -> answer")
loaded_qa.load("models/qa_v1.json")
```

### 5. Monitor and Debug

```python