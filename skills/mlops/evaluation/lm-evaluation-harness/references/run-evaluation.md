# Run evaluation
    os.system(f"./eval_checkpoint.sh checkpoints step-{step}")
```

Or use PyTorch Lightning callbacks:

```python
from pytorch_lightning import Callback

class EvalHarnessCallback(Callback):
    def on_validation_epoch_end(self, trainer, pl_module):
        step = trainer.global_step
        checkpoint_path = f"checkpoints/step-{step}"