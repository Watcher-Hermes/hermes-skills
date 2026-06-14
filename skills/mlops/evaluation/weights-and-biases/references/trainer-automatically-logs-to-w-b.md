# Trainer automatically logs to W&B
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset
)

trainer.train()
```

### PyTorch Lightning

```python
from pytorch_lightning import Trainer
from pytorch_lightning.loggers import WandbLogger
import wandb