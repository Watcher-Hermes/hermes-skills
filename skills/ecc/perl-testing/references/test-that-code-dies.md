# Test that code dies
like(
    dies { divide(10, 0) },
    qr/Division by zero/,
    'dies on division by zero'
);