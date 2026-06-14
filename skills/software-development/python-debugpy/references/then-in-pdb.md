# then in pdb:
(Pdb) pp d
(Pdb) pp list(d.keys())
(Pdb) w                # how did we get here
```

**"This test passes in isolation but fails in the suite."**
```bash
scripts/run_tests.sh tests/the_test.py --pdb -p no:xdist