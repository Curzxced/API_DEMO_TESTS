import os

BASE_URL = os.getenv("BASE_URL", "https://restful-booker.herokuapp.com")
AUTH_CREDENTIALS = {
    "username": os.getenv("API_USER", "admin"),
    "password": os.getenv("API_PASS", "password123")
}