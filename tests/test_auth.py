import pytest

from helpers import check_error_fields, check_status, login_user


def test_login_success(registered_user):
    response = login_user(registered_user["username"], registered_user["password"])

    check_status(response, 200)
    data = response.json()
    assert data.get("access"), f"access пустой или отсутствует: {data}"
    assert data.get("refresh"), f"refresh пустой или отсутствует: {data}"


@pytest.mark.parametrize(
    "field, value",
    [("password", "WrongPassword"), ("username", "wrong_user_xyz")],
    ids=["wrong_password", "wrong_username"],
)
def test_login_invalid_credentials(registered_user, field, value):
    creds = {**registered_user, field: value}

    response = login_user(creds["username"], creds["password"])

    check_status(response, 401)


@pytest.mark.parametrize(
    "empty_fields",
    [["password"], ["username"], ["username", "password"]],
    ids=["empty_password", "empty_username", "both_empty"],
)
def test_login_empty_fields(registered_user, empty_fields):
    creds = {**registered_user, **{field: "" for field in empty_fields}}

    response = login_user(creds["username"], creds["password"])

    check_status(response, 400)
    check_error_fields(response, *empty_fields)
