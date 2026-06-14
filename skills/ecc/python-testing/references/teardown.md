# Teardown
    db.close()

def test_database_query(database):
    """Test database operations."""
    result = database.query("SELECT * FROM users")
    assert len(result) > 0
```

### Fixture Scopes

```python