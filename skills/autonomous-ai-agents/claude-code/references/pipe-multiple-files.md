# Pipe multiple files
terminal(command="cat src/*.py | claude -p 'Find all TODO comments' --max-turns 1", timeout=60)