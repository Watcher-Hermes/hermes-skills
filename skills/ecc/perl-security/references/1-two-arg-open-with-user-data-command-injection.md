# 1. Two-arg open with user data (command injection)
open my $fh, $user_input;               # CRITICAL vulnerability