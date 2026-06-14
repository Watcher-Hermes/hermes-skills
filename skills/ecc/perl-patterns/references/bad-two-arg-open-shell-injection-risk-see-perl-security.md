# Bad: Two-arg open (shell injection risk, see perl-security)
open FH, $path;            # NEVER do this
open FH, "< $path";        # Still bad — user data in mode string
```

### Path::Tiny for File Operations

```perl
use v5.36;
use Path::Tiny;

my $file = path('config', 'app.json');
my $content = $file->slurp_utf8;
$file->spew_utf8($new_content);