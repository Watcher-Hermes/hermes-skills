## Recipe 4: Post-mortem on any exception

```python
import pdb, sys
try:
    run_the_thing()
except Exception:
    pdb.post_mortem(sys.exc_info()[2])
```

Or wrap a whole script:

```bash
python -m pdb -c continue script.py