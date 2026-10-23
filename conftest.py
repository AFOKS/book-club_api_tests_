import logging
import random

import pytest
import requests

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

API_URL = "https://book-club.qa.guru/api/v1"


@pytest.fixture
def api_url():
    return API_URL


@pytest.fixture
def username():
    return "Petrov"


@pytest.fixture
def password():
    return "1234567890"


@pytest.fixture
def access_token(api_url, username, password):
    response = requests.post(
        f"{api_url}/auth/token/",
        json={
            "username": username,
            "password": password
        }
    )
    assert response.status_code == 200
    return response.json()["access"]


@pytest.fixture
def auth_headers(access_token):
    return {
        "Authorization": f"Bearer {access_token}"
    }


@pytest.fixture
def club_body():
    return {
        "bookTitle": f"Random book {random.randint(1000, 999999)}",
        "bookAuthors": "Random Author",
        "publicationYear": 2024,
        "description": "Random description",
        "telegramChatLink": "https://t.me/qa.guru"
    }