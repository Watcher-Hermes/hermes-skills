# Good: Encode for URL context
sub safe_url_param($value) {
    return uri_escape_utf8($value);
}