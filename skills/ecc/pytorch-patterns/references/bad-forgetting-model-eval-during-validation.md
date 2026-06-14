# Bad: Forgetting model.eval() during validation
model.train()
with torch.no_grad():
    output = model(val_data)  # Dropout still active! BatchNorm uses batch stats!