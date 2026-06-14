# Bad: Blocklist — always incomplete
sub bad_validate($input) {
    die "Invalid" if $input =~ /[<>"';&|]/;  # Misses encoded attacks
    return $input;
}
```

### Length Constraints

```perl
use v5.36;

sub validate_comment($text) {
    die "Comment is required\n"        unless length($text) > 0;
    die "Comment exceeds 10000 chars\n" if length($text) > 10_000;
    return $text;
}
```