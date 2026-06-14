# Good: Rewrite without nesting
my $good_re = qr/^a+$/;             # Single quantifier
my $good_re2 = qr/^[a-zA-Z]+$/;     # Single quantifier on class