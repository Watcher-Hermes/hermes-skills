# Good: Using context managers
def process_file(path: str) -> str:
    with open(path, 'r') as f:
        return f.read()