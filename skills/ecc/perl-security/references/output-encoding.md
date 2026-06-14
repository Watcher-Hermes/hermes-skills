## Output Encoding

Always encode output for its context: `HTML::Entities::encode_entities()` for HTML, `URI::Escape::uri_escape_utf8()` for URLs, `JSON::MaybeXS::encode_json()` for JSON.