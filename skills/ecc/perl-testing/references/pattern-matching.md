# Pattern matching
like($error, qr/not found/i, 'error mentions not found');
unlike($output, qr/password/, 'output hides password');