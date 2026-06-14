# Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()