import logging
import uuid

import pytest

from client import ApiClient
from helpers import check_status, login_user, register_user

log = logging.getLogger(__name__)


def _unique_user() -> dict:
    return {
        "username": f"testuser_{uuid.uuid4().hex[:8]}",
        "password": "TestPassword",
    }


@pytest.fixture
def unique_user():
    return _unique_user()


@pytest.fixture
def registered_user(unique_user):
    check_status(register_user(unique_user), 201)
    return unique_user


@pytest.fixture
def api_client():
    return ApiClient()


@pytest.fixture
def make_auth_client():
    """Фабрика: каждый вызов регистрирует нового пользователя и возвращает авторизованного клиента."""

    def _make() -> ApiClient:
        user = _unique_user()
        check_status(register_user(user), 201)
        response = login_user(user["username"], user["password"])
        check_status(response, 200)

        client = ApiClient()
        client.headers["Authorization"] = f"Bearer {response.json()['access']}"
        return client

    return _make


@pytest.fixture
def auth_client(make_auth_client):
    return make_auth_client()


@pytest.fixture
def club_data():
    return {
        "bookTitle": f"Тестовая книга {uuid.uuid4().hex[:8]}",
        "bookAuthors": "Тестовый автор",
        "publicationYear": 2000,
        "description": "Тестовое описание",
        "telegramChatLink": "https://t.me/test",
    }


@pytest.fixture
def club_factory(auth_client):
    """Создаёт клубы с уникальными названиями и удаляет их после теста."""
    created = []

    def _create(**overrides) -> dict:
        data = {
            "bookTitle": f"Тестовая книга {uuid.uuid4().hex[:8]}",
            "bookAuthors": "Тестовый автор",
            "publicationYear": 2000,
            "description": "Тестовое описание",
            "telegramChatLink": "https://t.me/test",
            **overrides,
        }
        response = auth_client.post("/clubs/", json=data)
        check_status(response, 201)
        club = response.json()
        created.append(club["id"])
        return club

    yield _create

    for club_id in created:
        response = auth_client.delete(f"/clubs/{club_id}/")
        # 404 — нормально: тест мог удалить клуб сам
        if response.status_code not in (204, 404):
            log.warning("Не удалось удалить клуб %s: %s %s", club_id, response.status_code, response.text)


@pytest.fixture
def created_club(club_factory, club_data):
    return club_factory(**club_data)
