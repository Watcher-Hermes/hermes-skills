# Good: Trade compute for memory
from torch.utils.checkpoint import checkpoint

class LargeModel(nn.Module):
    def forward(self, x: torch.Tensor) -> torch.Tensor: