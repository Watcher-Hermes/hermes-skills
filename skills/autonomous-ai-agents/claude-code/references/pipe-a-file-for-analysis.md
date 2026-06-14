# Pipe a file for analysis
terminal(command="cat src/auth.py | claude -p 'Review this code for bugs' --max-turns 1", timeout=60)