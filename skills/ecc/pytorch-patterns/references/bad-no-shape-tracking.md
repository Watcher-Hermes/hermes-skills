# Bad: No shape tracking
def forward(self, x):
    x = self.conv1(x)
    x = self.pool(x)
    x = x.view(x.size(0), -1)  # What size is this?
    return self.fc(x)           # Will this even work?
```