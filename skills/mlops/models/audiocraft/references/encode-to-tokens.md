# Encode to tokens
with torch.no_grad():
    encoded = model.encode(wav.unsqueeze(0))
    codes = encoded[0]  # Audio codes