# 5. Global variables as configuration
our $TIMEOUT = 30;                       # Bad: mutable global
use constant TIMEOUT => 30;              # Better: constant