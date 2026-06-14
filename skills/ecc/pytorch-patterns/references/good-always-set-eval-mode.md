# Good: Always set eval mode
model.eval()
with torch.no_grad():
    output = model(val_data)