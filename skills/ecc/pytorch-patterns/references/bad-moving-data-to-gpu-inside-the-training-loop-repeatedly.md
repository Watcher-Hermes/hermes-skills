# Bad: Moving data to GPU inside the training loop repeatedly
for data, target in dataloader:
    model = model.cuda()  # Moves model EVERY iteration!