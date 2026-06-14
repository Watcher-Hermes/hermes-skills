# Good: Encode output for HTML context
sub safe_html($user_input) {
    return encode_entities($user_input);
}