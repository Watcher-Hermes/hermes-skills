# Test that code lives
ok(lives { divide(10, 2) }, 'division succeeds') or note($@);