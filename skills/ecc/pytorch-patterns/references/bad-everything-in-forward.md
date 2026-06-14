# Bad: Everything in forward
class ImageClassifier(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, x):
        x = F.conv2d(x, weight=self.make_weight())  # Creates weight each call!
        return x
```

### Proper Weight Initialization

```python