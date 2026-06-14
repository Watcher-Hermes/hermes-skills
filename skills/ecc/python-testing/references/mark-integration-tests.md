# Mark integration tests
@pytest.mark.integration
def test_api_integration():
    response = requests.get("https://api.example.com")
    assert response.status_code == 200