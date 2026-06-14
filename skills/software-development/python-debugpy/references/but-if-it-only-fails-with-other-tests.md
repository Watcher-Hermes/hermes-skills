# But if it only fails WITH other tests:
source .venv/bin/activate
python -m pytest tests/ -x --pdb -p no:xdist