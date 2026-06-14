# Bad: Manual argument unpacking
sub connect_db {
    my ($host, $port, $timeout) = @_;
    $port    //= 5432;
    $timeout //= 30;