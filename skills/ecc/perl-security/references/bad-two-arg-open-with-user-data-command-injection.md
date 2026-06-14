# Bad: Two-arg open with user data (command injection)
sub bad_read($path) {
    open my $fh, $path;        # If $path = "|rm -rf /", runs command!
    open my $fh, "< $path";   # Shell metacharacter injection
}
```

### TOCTOU Prevention and Path Traversal

```perl
use v5.36;
use Fcntl qw(:DEFAULT :flock);
use File::Spec;
use Cwd qw(realpath);