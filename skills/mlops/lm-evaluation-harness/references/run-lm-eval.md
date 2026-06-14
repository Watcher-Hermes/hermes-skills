# Run lm-eval
        os.system(f"lm_eval --model hf --model_args pretrained={checkpoint_path} ...")
```

**Step 4: Plot learning curves**

```python
import json
import matplotlib.pyplot as plt