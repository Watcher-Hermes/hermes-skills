# Bad: Using .item() before backward
loss = criterion(output, target).item()  # Detaches from graph!
loss.backward()  # Error: can't backprop through .item()