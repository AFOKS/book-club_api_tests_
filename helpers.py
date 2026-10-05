import requests

from config import BASE_URL, TIMEOUT


def register_user(user_data):
    return requests.post(f"{BASE_URL}/users/register/", json=user_data, timeout=TIMEOUT)


def login_user(username, password):
    return requests.post(
        f"{BASE_URL}/auth/token/",
        json={"username": username, "password": password},
        timeout=TIMEOUT,
    )


def check_status(response, expected: int) -> None:
    assert response.status_code == expected, (
        f"{response.request.method} {response.request.url}: "
        f"ожидали {expected}, получили {response.status_code}. Тело: {response.text}"
    )


def check_error_fields(response, *fields: str) -> None:
    """Проверяет, что в теле ответа есть ошибки по указанным полям."""
    errors = response.json()
    for field in fields:
        assert field in errors, f"Нет ошибки по полю '{field}': {errors}"
