# 2. Indirect object syntax (ambiguous parsing)
my $obj = new Foo(bar => 1);            # Bad
my $obj = Foo->new(bar => 1);           # Good