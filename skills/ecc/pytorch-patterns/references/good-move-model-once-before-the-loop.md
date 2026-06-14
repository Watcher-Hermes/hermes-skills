# Good: Move model once before the loop
model = model.to(device)
for data, target in dataloader:
    data, target = data.to(device), target.to(device)