# Good: Enforce timeout on untrusted patterns
use POSIX qw(alarm);
sub safe_match($string, $pattern, $timeout = 2) {
    my $matched;
    eval {
        local $SIG{ALRM} = sub { die "Regex timeout\n" };
        alarm($timeout);
        $matched = $string =~ $pattern;
        alarm(0);
    };
    alarm(0);
    die $@ if $@;
    return $matched;
}
```