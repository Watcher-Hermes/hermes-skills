# Bad: Mutable default arguments
def append_to(item, items=[]):
    items.append(item)
    return items