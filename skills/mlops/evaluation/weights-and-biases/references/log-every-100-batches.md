# Log every 100 batches
        if batch_idx % 100 == 0:
            wandb.log({
                "loss": loss.item(),
                "epoch": epoch,
                "batch": batch_idx
            })