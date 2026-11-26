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
    ИИ предложил делать логин перед каждым тестом, но так прогон будет медленный
    Так как токен в restful-booker не имеет короткой жизни, было вынесено на уровень сессии.
    """
    response = client.auth(AUTH_CREDENTIALS)
    assert response.status_code == 200, f"Не удалось авторизоваться. Ответ: {response.text}"
    return response.json()["token"]

@pytest.fixture
def booking_payload():
    """
    Дефолтный пейлоад для создания брони.
    Возвращает словарь, который тесты могут менять как захотят.
    """
    return {
        "firstname": "Ivan",
        "lastname": "Petrov",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-01-01",
            "checkout": "2025-01-07"
        },
        "additionalneeds": "Breakfast"
    }

@pytest.fixture
def created_booking(client, booking_payload, auth_token):
    """
    Фикстура создаст бронь перед тестом и удалит после.
    Так тесты не засоряют общую базу тестовыми данными.
    """
    # Создаем
    response = client.create_booking(booking_payload)
    assert response.status_code == 200, "Не удалось создать тестовую бронь"
    booking_id = response.json()["bookingid"]
    
    # Отдаем ID в тест
    yield booking_id
    
    # Уборка выполнится автоматически после теста
    client.delete_booking(booking_id, auth_token)