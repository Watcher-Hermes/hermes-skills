## Mocking

### Test::MockModule

```perl
use v5.36;
use Test2::V0;
use Test::MockModule;

subtest 'mock external API' => sub {
    my $mock = Test::MockModule->new('MyApp::API');