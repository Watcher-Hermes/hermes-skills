# Log metrics
        wandb.log({
            "train/loss": train_loss,
            "val/accuracy": val_acc
        })