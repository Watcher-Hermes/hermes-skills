# Exception testing (preferred approach)
with pytest.raises(ValueError):
    raise ValueError("error message")