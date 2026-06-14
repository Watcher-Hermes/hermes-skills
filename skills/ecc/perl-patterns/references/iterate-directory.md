# Iterate directory
for my $child (path('src')->children(qr/\.pl$/)) {
    say $child->basename;
}
```