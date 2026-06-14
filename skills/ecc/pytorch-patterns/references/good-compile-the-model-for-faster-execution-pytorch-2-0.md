# Good: Compile the model for faster execution (PyTorch 2.0+)
model = MyModel().to(device)
model = torch.compile(model, mode="reduce-overhead")