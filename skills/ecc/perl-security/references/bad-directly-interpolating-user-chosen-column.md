# Bad: Directly interpolating user-chosen column
sub bad_order($dbh, $column) {
    $dbh->prepare("SELECT * FROM users ORDER BY $column");  # SQLi!
}
```

### DBIx::Class (ORM Safety)

```perl
use v5.36;