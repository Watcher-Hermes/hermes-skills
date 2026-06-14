# Good: Encode for JSON context
use JSON::MaybeXS qw(encode_json);
sub safe_json($data) {
    return encode_json($data);  # Handles escaping
}