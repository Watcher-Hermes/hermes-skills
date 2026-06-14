# Bad: Not using torch.save properly
torch.save(model, "model.pt")  # Saves entire model (fragile, not portable)