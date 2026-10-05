import requests

BASE_URL = "https://book-club.qa.guru/api/v1"


def register_user(user_data):
    return requests.post(f"{BASE_URL}/users/register/", json=user_data)


def login_user(username, password):
    return requests.post(f"{BASE_URL}/auth/token/", json={"username": username, "password": password})