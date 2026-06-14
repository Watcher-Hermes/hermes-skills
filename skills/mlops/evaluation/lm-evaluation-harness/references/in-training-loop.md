# In training loop
if step % eval_interval == 0:
    model.save_pretrained(f"checkpoints/step-{step}")