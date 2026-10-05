from helpers import register_user


def test_register_user_success(unique_user):
    response = register_user(unique_user)

    print()
    print(f"Статус: {response.status_code}")
    print(f"Тело: {response.text}")

    assert response.status_code == 201, f"Ожидали 201, получили {response.status_code}. Тело: {response.text}"
    data = response.json()
    assert data["username"] == unique_user["username"]
    assert "id" in data
    assert "password" not in data


def test_register_duplicate_username(unique_user):
    first = register_user(unique_user)
    assert first.status_code == 201

    response = register_user(unique_user)

    assert response.status_code == 400
    assert "username" in response.json()


def test_register_missing_password(unique_user):
    user_data = unique_user.copy()
    user_data.pop("password")

    response = register_user(user_data)

    assert response.status_code == 400
    assert "password" in response.json()


def test_register_missing_username(unique_user):
    user_data = unique_user.copy()
    user_data.pop("username")

    response = register_user(user_data)

    assert response.status_code == 400
    assert "username" in response.json()