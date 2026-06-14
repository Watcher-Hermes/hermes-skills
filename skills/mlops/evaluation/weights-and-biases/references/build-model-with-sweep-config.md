# Build model with sweep config
    model = build_model(wandb.config)
    optimizer = get_optimizer(optimizer_name, lr)