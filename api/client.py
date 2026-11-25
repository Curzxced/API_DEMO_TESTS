import requests
from config import BASE_URL

class BookingClient:
    def __init__(self, session=None):
        self.session = session or requests.Session()
        self.base_url = BASE_URL

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def auth(self, credentials):
        return self.session.post(f"{self.base_url}/auth", json=credentials)

    def get_booking_ids(self):
        """Получение списка всех ID броней"""
        return self.session.get(f"{self.base_url}/booking")

    def get_booking(self, booking_id):
        """Получение конкретной брони по ID"""
        return self.session.get(f"{self.base_url}/booking/{booking_id}")

    def create_booking(self, payload):
        """Создание новой брони"""
        return self.session.post(f"{self.base_url}/booking", json=payload)

    def update_booking(self, booking_id, payload, token):
        """Обновление брони (требует токен)"""
        # В доке Restful-booker токен передается в cookie, а не в authorization header
        headers = {
            "Cookie": f"token={token}",
            "Accept": "application/json"
        }
        return self.session.put(
            f"{self.base_url}/booking/{booking_id}",
            json=payload,
            headers=headers
        )

    def delete_booking(self, booking_id, token):
        """Удаление брони (требует токен)"""
        headers = {"Cookie": f"token={token}"}
        return self.session.delete(
            f"{self.base_url}/booking/{booking_id}",
            headers=headers
        )