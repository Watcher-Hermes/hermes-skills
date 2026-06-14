# 4. Disabling strict refs
no strict 'refs';                        # Almost always wrong
${"My::Package::$var"} = $value;         # Use a hash instead