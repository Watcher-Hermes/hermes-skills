# Training loop
    for epoch in range(NUM_EPOCHS):
        train_loss = train_epoch(model, optimizer, batch_size)
        val_acc = validate(model)