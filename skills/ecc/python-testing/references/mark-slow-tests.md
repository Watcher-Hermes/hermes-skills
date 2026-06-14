# Mark slow tests
@pytest.mark.slow
def test_slow_operation():
    time.sleep(5)