# Bad: No seed control
model = MyModel()  # Different weights every run
```

### 3. Explicit Shape Management

Always document and verify tensor shapes.

```python