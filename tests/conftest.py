import uuid
import pytest
import requests

from helpers import register_user

BASE_URL = "https://book-club.qa.guru/api/v1"


@pytest.fixture
def unique_user():
    uid = uuid.uuid4().hex[:8]
    return {
        "username": f"testuser_{uid}",
        "password": "TestPassword",
    }


@pytest.fixture
def registered_user(unique_user):
    response = register_user(unique_user)
    assert response.status_code == 201, f"Не удалось зарегистрировать пользователя: {response.text}"
    return unique_user


@pytest.fixture
def api_client():
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})
    return session

@pytest.fixture
def auth_client(registered_user):
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})

    response = session.post(
        f"{BASE_URL}/auth/token/",
        json={
            "username": registered_user["username"],
            "password": registered_user["password"],
        },
    )
    access = response.json()["access"]
    session.headers.update({"Authorization": f"Bearer {access}"})
    return session


@pytest.fixture
def club_data():
    uid = uuid.uuid4().hex[:8]
    return {
        "bookTitle": f"Тестовая книга {uid}",
        "bookAuthors": "Тестовый автор",
        "publicationYear": 2000,
        "description": "Тестовое описание",
        "telegramChatLink": "https://t.me/test",
    }


@pytest.fixture
def created_club(auth_client, club_data):
    response = auth_client.post(f"{BASE_URL}/clubs/", json=club_data)
    assert response.status_code == 201, f"Не удалось создать клуб: {response.status_code} {response.text}"
    club = response.json()
    print(f"\n>>> Создан клуб id={club['id']}")

    yield club

    print()
    print(f">>> Удалён клуб id={club['id']}")
    delete_response = auth_client.delete(f"{BASE_URL}/clubs/{club['id']}/")
    print(f">>> DELETE вернул: {delete_response.status_code} {delete_response.text}")