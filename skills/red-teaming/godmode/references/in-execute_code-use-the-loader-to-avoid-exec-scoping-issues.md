# In execute_code — use the loader to avoid exec-scoping issues:
import os
exec(open(os.path.expanduser(
    os.path.join(os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes")), "skills/red-teaming/godmode/scripts/load_godmode.py")
)).read())