# Or use Artifacts (recommended)
artifact = wandb.Artifact('model', type='model')
artifact.add_file('checkpoint.pth')
wandb.log_artifact(artifact)
```