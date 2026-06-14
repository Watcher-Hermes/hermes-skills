## Fixtures and Setup/Teardown

### Subtest Isolation

```perl
use v5.36;
use Test2::V0;
use File::Temp qw(tempdir);
use Path::Tiny;

subtest 'file processing' => sub {