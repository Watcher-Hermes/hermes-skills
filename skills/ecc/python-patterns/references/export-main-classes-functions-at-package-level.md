# Export main classes/functions at package level
from mypackage.models import User, Post
from mypackage.utils import format_name

__all__ = ["User", "Post", "format_name"]
```