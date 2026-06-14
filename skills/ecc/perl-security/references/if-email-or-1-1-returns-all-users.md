# If $email = "' OR 1=1 --", returns all users
    $sth->execute;
    return $sth->fetchrow_hashref;
}
```

### Dynamic Column Allowlists

```perl
use v5.36;