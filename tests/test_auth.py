from helpers import login_user


def test_login_success(registered_user):
    response = login_user(registered_user["username"], registered_user["password"])

    assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. Тело: {response.text}"

    data = response.json()
    assert "access" in data, f"Нет ключа access в ответе: {data}"
    assert "refresh" in data, f"Нет ключа refresh в ответе: {data}"
    assert isinstance(data["access"], str) and data["access"], "access пустой"


def test_login_wrong_password(registered_user):
    response = login_user(registered_user["username"], "WrongPassword")

    assert response.status_code == 401, f"Ожидали 401, получили {response.status_code}. Тело: {response.text}"


def test_login_wrong_username(registered_user):
    response = login_user("wrong_user_xyz", registered_user["password"])

    assert response.status_code == 401, f"Ожидали 401, получили {response.status_code}. Тело: {response.text}"


def test_login_empty_password(registered_user):
    response = login_user(registered_user["username"], "")

    assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}. Тело: {response.text}"
    errors = response.json()
    assert "password" in errors, f"Ожидали ошибку: {errors}"


def test_login_empty_username(registered_user):
    response = login_user("", registered_user["password"])

    assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}. Тело: {response.text}"
    errors = response.json()
    assert "username" in errors, f"Ожидали ошибку: {errors}"


def test_login_both_fields_empty():
    response = login_user("", "")

    assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}. Тело: {response.text}"
    errors = response.json()
    assert "username" in errors
    assert "password" in errors