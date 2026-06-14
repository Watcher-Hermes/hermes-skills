# Detect flaky tests (repeat each 5 times)
pip install pytest-repeat
pytest tests/test_login.py --count=5 -v
```