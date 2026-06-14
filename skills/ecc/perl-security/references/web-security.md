## Web Security

### XSS Prevention

```perl
use v5.36;
use HTML::Entities qw(encode_entities);
use URI::Escape qw(uri_escape_utf8);