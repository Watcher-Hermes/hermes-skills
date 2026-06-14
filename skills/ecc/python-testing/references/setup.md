# Setup
    db = Database(":memory:")
    db.create_tables()
    db.insert_test_data()

    yield db  # Provide to test