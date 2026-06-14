# Or resume the most recent session in the same directory
terminal(command="claude -p 'What did you do last time?' --continue --max-turns 1", workdir="/project", timeout=30)