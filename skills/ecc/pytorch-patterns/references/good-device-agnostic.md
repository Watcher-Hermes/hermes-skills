# Good: Device-agnostic
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = MyModel().to(device)
data = data.to(device)