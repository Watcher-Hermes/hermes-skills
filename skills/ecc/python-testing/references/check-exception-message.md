# Check exception message
with pytest.raises(ValueError, match="invalid input"):
    raise ValueError("invalid input provided")