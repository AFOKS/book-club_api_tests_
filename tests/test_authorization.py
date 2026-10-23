import logging
import random

import requests
from jsonschema import validate

from schemas.auth_schema import (
    success_auth,
    unsupported_media_type,
    missing_username_auth,
    missing_password_auth,
    wrong_credentials_auth
)
from schemas.users_schema import success_register_user

logger = logging.getLogger(__name__)


def test_successful_auth(api_url, username, password):
    request_body = {
        "username": username,
        "password": password
    }

    response = requests.post(f"{api_url}/auth/token/", json=request_body)

    logger.info("Status code: %s", response.status_code)
    logger.info("Headers: %s", response.headers)
    logger.info("Body: %s", response.text)

    assert response.status_code == 200

    body = response.json()
    validate(body, schema=success_auth)

    access_token = body["access"]
    refresh_token = body["refresh"]

    assert access_token != refresh_token
    assert len(access_token.split(".")) == 3
    assert len(refresh_token.split(".")) == 3


def test_register_and_auth_new_user(api_url):
    username = f"autotest_{random.randint(1000, 999999)}"
    password = f"TestPass{random.randint(1000, 999999)}!"

    register_body = {
        "username": username,
        "password": password
    }

    register_response = requests.post(f"{api_url}/users/register/", json=register_body)

    logger.info("REGISTER STATUS: %s", register_response.status_code)
    logger.info("REGISTER BODY: %s", register_response.text)

    assert register_response.status_code == 201

    register_data = register_response.json()
    validate(register_data, schema=success_register_user)

    assert register_data["username"] == username
    assert "id" in register_data

    auth_body = {
        "username": username,
        "password": password
    }

    auth_response = requests.post(f"{api_url}/auth/token/", json=auth_body)

    logger.info("AUTH STATUS: %s", auth_response.status_code)
    logger.info("AUTH BODY: %s", auth_response.text)

    assert auth_response.status_code == 200

    auth_data = auth_response.json()
    validate(auth_data, schema=success_auth)

    access_token = auth_data["access"]
    refresh_token = auth_data["refresh"]

    assert access_token != refresh_token
    assert len(access_token.split(".")) == 3
    assert len(refresh_token.split(".")) == 3


def test_wrong_password_auth(api_url, username):
    password = "12345"

    request_body = {
        "username": username,
        "password": password
    }

    response = requests.post(f"{api_url}/auth/token/", json=request_body)

    logger.info("Status code: %s", response.status_code)
    logger.info("Headers: %s", response.headers)
    logger.info("Body: %s", response.text)

    assert response.status_code == 401

    body = response.json()
    validate(body, schema=wrong_credentials_auth)

    assert "detail" in body


def test_missing_password_auth(api_url, username):
    request_body = {
        "username": username
    }

    response = requests.post(f"{api_url}/auth/token/", json=request_body)

    logger.info("Status code: %s", response.status_code)
    logger.info("Headers: %s", response.headers)
    logger.info("Body: %s", response.text)

    assert response.status_code in [400, 401]

    body = response.json()
    validate(body, schema=missing_password_auth)

    assert "password" in body


def test_missing_username_auth(api_url, password):
    request_body = {
        "password": password
    }

    response = requests.post(f"{api_url}/auth/token/", json=request_body)

    logger.info("Status code: %s", response.status_code)
    logger.info("Headers: %s", response.headers)
    logger.info("Body: %s", response.text)

    assert response.status_code in [400, 401]

    body = response.json()
    validate(body, schema=missing_username_auth)

    assert "username" in body


def test_wrong_content_type_auth(api_url, username, password):
    request_body = {
        "username": username,
        "password": password
    }

    headers = {
        "content-type": "image/png"
    }

    response = requests.post(f"{api_url}/auth/token/", headers=headers, json=request_body)

    logger.info("Status code: %s", response.status_code)
    logger.info("Headers: %s", response.headers)
    logger.info("Body: %s", response.text)

    assert response.status_code == 415

    body = response.json()
    validate(body, schema=unsupported_media_type)

    assert "detail" in body