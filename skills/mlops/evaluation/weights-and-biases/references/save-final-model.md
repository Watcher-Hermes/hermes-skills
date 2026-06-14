# Save final model
artifact = wandb.Artifact('final-model', type='model')
artifact.add_file('model.pth')
wandb.log_artifact(artifact)