import pytest

@pytest.mark.regression
class TestBooking:
    
    def test_get_all_bookings(self, client):
        """Проверяем, что эндпоинт возвращает список ID"""
        response = client.get_booking_ids()
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_create_and_get_booking(self, client, booking_payload, auth_token):
        """Проверяем создание брони и последующее чтение"""
        create_resp = client.create_booking(booking_payload)
        assert create_resp.status_code == 200
        booking_id = create_resp.json()["bookingid"]
        
        get_resp = client.get_booking(booking_id)
        assert get_resp.status_code == 200
        assert get_resp.json()["firstname"] == booking_payload["firstname"]
        
        # Чистим данные вручную, нет фикстуры с teardown
        client.delete_booking(booking_id, auth_token)

    def test_update_booking(self, client, created_booking, booking_payload, auth_token):
        """Проверяем обновление брони (фикстура с teardown)"""
        updated_payload = booking_payload.copy()
        updated_payload["totalprice"] = 999
        
        response = client.update_booking(created_booking, updated_payload, auth_token)
        assert response.status_code == 200
        assert response.json()["totalprice"] == 999
    
    def test_get_nonexistent_booking(self, client):
        """Проверяем, что при запросе несуществующей брони вернется 404"""
        response = client.get_booking(999999)
        assert response.status_code == 404

    @pytest.mark.parametrize("invalid_payload", [
        {},
        {"firstname": "Ivan"}
    ])

    def test_create_booking_negative(self, client, invalid_payload):
        """Проверяем, что сервер не создаст бронь с невалидными данными"""
        response = client.create_booking(invalid_payload)
        assert response.status_code in [400, 500], f"Ожидалась ошибка, но получен {response.status_code}"