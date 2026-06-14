## Taint Mode

Perl's taint mode (`-T`) tracks data from external sources and prevents it from being used in unsafe operations without explicit validation.

### Enabling Taint Mode

```perl
#!/usr/bin/perl -T
use v5.36;