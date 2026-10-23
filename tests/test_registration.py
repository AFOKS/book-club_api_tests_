import logging
import random

import requests
from jsonschema import validate

from schemas.users_schema import (
    success_register_user,
    register_user_bad_request,
    register_user_duplicate_username,
    register_user_missing_password,
    register_user_missing_username
)

logger = logging.getLogger(__name__)


def test_successful_registration(api_url):
    username = f"autotest_user_{random.randint(1000, 999999)}"
    password = f"TestPass{random.randint(1000, 999999)}!"

    request_body = {
        "username": username,
        "password": password
    }

    response = requests.post(f"{api_url}/users/register/", json=request_body)

    logger.info("Status code: %s", response.status_code)
    logger.info("Headers: %s", response.headers)
    logger.info("Body: %s", response.text)

    assert response.status_code == 201

    body = response.json()
    validate(body, schema=success_register_user)

    assert body["username"] == username
    assert "id" in body
    assert "password" not in body


def test_register_duplicate_username(api_url):
    username = f"autotest_user_{random.randint(1000, 999999)}"
    password = f"TestPass{random.randint(1000, 999999)}!"

    request_body = {
        "username": username,
        "password": password
    }

    first_response = requests.post(f"{api_url}/users/register/", json=request_body)
    assert first_response.status_code == 201

    second_response = requests.post(f"{api_url}/users/register/", json=request_body)

    logger.info("Status code: %s", second_response.status_code)
    logger.info("Headers: %s", second_response.headers)
    logger.info("Body: %s", second_response.text)

    assert second_response.status_code == 400

    body = second_response.json()
    validate(body, schema=register_user_duplicate_username)

    assert "username" in body


def test_register_missing_password(api_url):
    username = f"autotest_user_{random.randint(1000, 999999)}"

    request_body = {
        "username": username
    }

    response = requests.post(f"{api_url}/users/register/", json=request_body)

    logger.info("Status code: %s", response.status_code)
    logger.info("Headers: %s", response.headers)
    logger.info("Body: %s", response.text)

    assert response.status_code == 400

    body = response.json()
    validate(body, schema=register_user_missing_password)

    assert "password" in body


def test_register_missing_username(api_url):
    password = "Tes*******345!"

    request_body = {
        "password": password
    }

    response = requests.post(f"{api_url}/users/register/", json=request_body)

    logger.info("Status code: %s", response.status_code)
    logger.info("Headers: %s", response.headers)
    logger.info("Body: %s", response.text)

    assert response.status_code == 400

    body = response.json()
    validate(body, schema=register_user_missing_username)

    assert "username" in body


def test_register_empty_username_and_password(api_url):
    request_body = {
        "username": "",
        "password": ""
    }

    response = requests.post(f"{api_url}/users/register/", json=request_body)

    logger.info("Status code: %s", response.status_code)
    logger.info("Headers: %s", response.headers)
    logger.info("Body: %s", response.text)

    assert response.status_code == 400

    body = response.json()
    validate(body, schema=register_user_bad_request)

    assert "username" in body
    assert "password" in body