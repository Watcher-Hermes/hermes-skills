# Good: Validate and untaint a file path
sub untaint_filename($input) {
    if ($input =~ m{^([a-zA-Z0-9._-]+)$}) {
        return $1;
    }
    die "Invalid filename: contains unsafe characters\n";
}