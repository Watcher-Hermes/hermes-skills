# Bad: In-place operations breaking autograd
x = F.relu(x, inplace=True)  # Can break gradient computation
x += residual                  # In-place add breaks autograd graph