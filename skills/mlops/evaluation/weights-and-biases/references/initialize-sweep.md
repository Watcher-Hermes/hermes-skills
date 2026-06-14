# Initialize sweep
sweep_id = wandb.sweep(sweep_config, project="my-project")
```

### Define Training Function

```python
def train():