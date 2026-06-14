# Deep comparison
is_deeply(
    $got,
    { name => 'Alice', roles => ['admin'] },
    'returns expected structure'
);