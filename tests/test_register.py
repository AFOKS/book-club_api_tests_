import pytest

from helpers import check_error_fields, check_status, register_user


def test_register_user_success(unique_user):
    response = register_user(unique_user)

    check_status(response, 201)
    data = response.json()
    assert data["username"] == unique_user["username"]
    assert "id" in data
    assert "password" not in data


def test_register_duplicate_username(registered_user):
    response = register_user(registered_user)

    check_status(response, 400)
    check_error_fields(response, "username")


@pytest.mark.parametrize("missing_field", ["username", "password"])
def test_register_missing_field(unique_user, missing_field):
    user_data = {k: v for k, v in unique_user.items() if k != missing_field}

    response = register_user(user_data)

    check_status(response, 400)
    check_error_fields(response, missing_field)
