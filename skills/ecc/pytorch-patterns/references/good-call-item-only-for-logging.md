# Good: Call .item() only for logging
loss = criterion(output, target)
loss.backward()
print(f"Loss: {loss.item():.4f}")  # .item() after backward is fine