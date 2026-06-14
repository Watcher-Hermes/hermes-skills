# Bad: Slow defaults
dataloader = DataLoader(dataset, batch_size=32)  # num_workers=0, no pin_memory
```

### Custom Collate for Variable-Length Data

```python