# Bad: String form — shell injection!
sub bad_search($pattern) {
    system("grep -r '$pattern' /var/log/app/");  # If $pattern = "'; rm -rf / #"
}