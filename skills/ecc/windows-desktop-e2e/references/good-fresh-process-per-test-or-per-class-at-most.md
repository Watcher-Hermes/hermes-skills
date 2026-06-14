# GOOD: fresh process per test (or per class at most)
@pytest.fixture(scope="function")
def app(): ...
```