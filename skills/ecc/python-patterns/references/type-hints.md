## Type Hints

### Basic Type Annotations

```python
from typing import Optional, List, Dict, Any

def process_user(
    user_id: str,
    data: Dict[str, Any],
    active: bool = True
) -> Optional[User]:
    """Process a user and return the updated User or None."""
    if not active:
        return None
    return User(user_id, data)
```

### Modern Type Hints (Python 3.9+)

```python