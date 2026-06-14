# Run sweep
wandb.agent(sweep_id, function=train, count=50)  # Run 50 trials
```

### Sweep Strategies

```python