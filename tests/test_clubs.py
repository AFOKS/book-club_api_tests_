import logging

import requests
from jsonschema import validate

from schemas.clubs_schema import clubs_schema

logger = logging.getLogger(__name__)


# Проверяем получение списка клубов без параметров
def test_get_clubs_default(api_url):
    response = requests.get(f"{api_url}/clubs/")
    body = response.json()

    logger.info("Status code: %s", response.status_code)
    logger.info("Headers: %s", response.headers)
    logger.info("Body: %s", response.text)

    assert response.status_code == 200
    validate(instance=body, schema=clubs_schema)

    assert "results" in body
    assert isinstance(body["results"], list)
    assert len(body["results"]) > 0


# Проверяем поиск клубов по параметру search
def test_get_clubs_search(api_url):
    params = {"search": "book"}
    response = requests.get(f"{api_url}/clubs/", params=params)
    body = response.json()

    logger.info("Status code: %s", response.status_code)
    logger.info("Headers: %s", response.headers)
    logger.info("Body: %s", response.text)

    assert response.status_code == 200
    validate(instance=body, schema=clubs_schema)

    assert "results" in body
    assert isinstance(body["results"], list)


# Проверяем, что можно запросить вторую страницу
def test_get_clubs_page_2(api_url):
    params = {"page": 2}
    response = requests.get(f"{api_url}/clubs/", params=params)
    body = response.json()

    logger.info("Status code: %s", response.status_code)
    logger.info("Headers: %s", response.headers)
    logger.info("Body: %s", response.text)

    assert response.status_code == 200
    validate(instance=body, schema=clubs_schema)

    assert "results" in body
    assert isinstance(body["results"], list)


# Проверяем, что page_size=1 ограничивает количество клубов в ответе
def test_get_clubs_page_size_1(api_url):
    params = {"page_size": 1}
    response = requests.get(f"{api_url}/clubs/", params=params)
    body = response.json()

    logger.info("Status code: %s", response.status_code)
    logger.info("Headers: %s", response.headers)
    logger.info("Body: %s", response.text)

    assert response.status_code == 200
    validate(instance=body, schema=clubs_schema)

    assert "results" in body
    assert isinstance(body["results"], list)
    assert len(body["results"]) <= 1


# Проверяем структуру полей у первого клуба
def test_get_first_club_fields(api_url):
    response = requests.get(f"{api_url}/clubs/")
    body = response.json()

    logger.info("Status code: %s", response.status_code)
    logger.info("Headers: %s", response.headers)
    logger.info("Body: %s", response.text)

    assert response.status_code == 200
    validate(instance=body, schema=clubs_schema)

    first_club = body["results"][0]

    assert isinstance(first_club["id"], int)
    assert isinstance(first_club["bookTitle"], str)
    assert isinstance(first_club["bookAuthors"], str)
    assert isinstance(first_club["publicationYear"], int)
    assert isinstance(first_club["telegramChatLink"], str)


# Проверяем поле members у первого клуба
def test_first_club_members_are_list_of_ints(api_url):
    response = requests.get(f"{api_url}/clubs/")
    body = response.json()

    logger.info("Status code: %s", response.status_code)
    logger.info("Headers: %s", response.headers)
    logger.info("Body: %s", response.text)

    assert response.status_code == 200
    validate(instance=body, schema=clubs_schema)

    first_club = body["results"][0]

    assert isinstance(first_club["members"], list)
    for member in first_club["members"]:
        assert isinstance(member, int)


# Проверяем, что id клубов в results не повторяются
def test_clubs_ids_are_unique(api_url):
    response = requests.get(f"{api_url}/clubs/")
    body = response.json()

    logger.info("Status code: %s", response.status_code)
    logger.info("Headers: %s", response.headers)
    logger.info("Body: %s", response.text)

    assert response.status_code == 200
    validate(instance=body, schema=clubs_schema)

    club_ids = [club["id"] for club in body["results"]]

    assert len(club_ids) == len(set(club_ids))