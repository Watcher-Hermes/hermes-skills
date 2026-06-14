# paused. Now:
repl
> myVariable
> Object.keys(this)
```

**"What's the call path into this function?"**
```
debug> sb('suspectFn')
debug> cont