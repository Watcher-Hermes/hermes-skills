# Create W&B logger
wandb_logger = WandbLogger(
    project="lightning-demo",
    log_model=True  # Log model checkpoints
)