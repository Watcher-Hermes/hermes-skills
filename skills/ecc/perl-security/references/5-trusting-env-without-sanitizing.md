# 5. Trusting $ENV without sanitizing
my $path = $ENV{UPLOAD_DIR};             # Could be manipulated
system("ls $path");                      # Double vulnerability