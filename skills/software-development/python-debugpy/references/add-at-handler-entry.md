# Add at handler entry
import remote_pdb; remote_pdb.set_trace(host="127.0.0.1", port=4444)
```
Trigger the handler. `nc 127.0.0.1 4444`, then `w` to see the suspended frame, `!import asyncio; asyncio.all_tasks()` to see what else is pending.

**"Post-mortem on a crash in an Ink child process / subprocess."**
```bash
PYTHONFAULTHANDLER=1 python -m pdb -c continue path/to/entrypoint.py