# Use validation set for metric
def metric(example, pred, trace=None):
    return example.answer in pred.answer
```

### 4. Save and Load Optimized Models

```python