# Bad: Backticks with interpolation
my $output = `ls $user_dir`;   # Shell injection risk
```

Also use `Capture::Tiny` for capturing stdout/stderr from external commands safely.