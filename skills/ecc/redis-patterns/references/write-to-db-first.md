# Write to DB first
    db.execute("UPDATE products SET ... WHERE id = %s", product_id)