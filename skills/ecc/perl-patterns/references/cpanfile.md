# cpanfile
requires 'Moo', '>= 2.005';
requires 'Path::Tiny';
requires 'JSON::MaybeXS';
requires 'Try::Tiny';

on test => sub {
    requires 'Test2::V0';
    requires 'Test::MockModule';
};
```