# Good: Slurpy parameter for variable args
sub log_message($level, @details) {
    say "[$level] " . join(' ', @details);
}