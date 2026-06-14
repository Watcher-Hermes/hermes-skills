# Save model
torch.save(model.state_dict(), "model.pth")
wandb.save("model.pth")  # Upload to W&B

wandb.finish()
```