# Python 3.9+ - Use built-in types
def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}