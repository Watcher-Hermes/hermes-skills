# Bad: O(n²) due to string immutability
result = ""
for item in items:
    result += str(item)