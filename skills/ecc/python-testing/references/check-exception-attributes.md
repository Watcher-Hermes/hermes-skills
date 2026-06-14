# Check exception attributes
with pytest.raises(ValueError) as exc_info:
    raise ValueError("error message")
assert str(exc_info.value) == "error message"
```