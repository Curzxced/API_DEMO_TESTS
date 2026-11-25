import pytest

@pytest.mark.smoke
def test_auth_success(client, auth_token):
    """Проверяем, что токен успешно получен и он не пустой"""
    assert auth_token is not None
    assert isinstance(auth_token, str)
    assert len(auth_token) > 10

def test_auth_failure(client):
    """Проверяем негативный сценарий авторизации (возврат 200 с Bad credentials)"""
    bad_creds = {"username": "wrong", "password": "wrong"}
    response = client.auth(bad_creds)
    
    assert response.status_code == 200
    assert response.json().get("reason") == "Bad credentials"