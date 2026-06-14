# Bad: Only saving model weights (can't resume training)
torch.save(model.state_dict(), "model.pt")
```