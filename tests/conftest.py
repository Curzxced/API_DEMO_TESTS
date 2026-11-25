import pytest
from api.client import BookingClient
from config import AUTH_CREDENTIALS

@pytest.fixture(scope="session")
def client():
    """
    Создаем один клиент на всю сессию тестов.
    Благодаря __enter__ и __exit__ в классе, сессия закроется автоматически в конце.
    """
    with BookingClient() as c:
        yield c

@pytest.fixture(scope="session")
def auth_token(client):
    """
    Получаем токен один раз перед всеми тестами.
    Чтобы не логиниться перед каждым тестом и не нагружать сервер.
    ИИ сначала предложил делать логин перед каждым тестом, но так прогон будет медленный
    Так как токен в restful-booker не имеет короткой жизни, было вынесено на уровень сессии.
    """
    response = client.auth(AUTH_CREDENTIALS)
    assert response.status_code == 200, f"Не удалось авторизоваться. Ответ: {response.text}"
    return response.json()["token"]