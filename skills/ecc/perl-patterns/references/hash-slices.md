# Hash slices
my %subset;
@subset{qw(host port)} = @{$config->{database}}{qw(host port)};