import logging
import random

import requests
from jsonschema import validate

from helpers import create_club
from schemas.club_schema import success_create_club

logger = logging.getLogger(__name__)


def test_success_create_club(api_url, auth_headers, club_body):
    response = create_club(api_url, auth_headers, club_body)

    logger.info("Status code: %s", response.status_code)
    logger.info("Headers: %s", response.headers)
    logger.info("Body: %s", response.text)

    assert response.status_code == 201

    body = response.json()
    validate(body, schema=success_create_club)

    assert body["bookTitle"] == club_body["bookTitle"]
    assert body["bookAuthors"] == club_body["bookAuthors"]
    assert body["publicationYear"] == club_body["publicationYear"]
    assert body["description"] == club_body["description"]
    assert body["telegramChatLink"] == club_body["telegramChatLink"]
    assert body["reviews"] == [] or len(body["reviews"]) == 0

    club_id = body["id"]

    delete_response = requests.delete(f"{api_url}/clubs/{club_id}/", headers=auth_headers)
    assert delete_response.status_code == 204


def test_get_created_club(api_url, auth_headers, club_body):
    create_response = create_club(api_url, auth_headers, club_body)
    assert create_response.status_code == 201

    created_body = create_response.json()
    club_id = created_body["id"]

    get_response = requests.get(f"{api_url}/clubs/{club_id}/", headers=auth_headers)

    logger.info("Status code: %s", get_response.status_code)
    logger.info("Headers: %s", get_response.headers)
    logger.info("Body: %s", get_response.text)

    assert get_response.status_code == 200

    get_body = get_response.json()
    assert get_body["id"] == club_id
    assert get_body["bookTitle"] == club_body["bookTitle"]
    assert get_body["bookAuthors"] == club_body["bookAuthors"]

    requests.delete(f"{api_url}/clubs/{club_id}/", headers=auth_headers)


def test_update_club(api_url, auth_headers, club_body):
    create_response = create_club(api_url, auth_headers, club_body)
    assert create_response.status_code == 201

    club_id = create_response.json()["id"]

    update_body = {
        "bookTitle": f"Updated Title {random.randint(1000, 999999)}",
        "bookAuthors": "Updated Author",
        "publicationYear": 2025,
        "description": "Updated description",
        "telegramChatLink": "https://t.me/qa.guru"
    }

    update_response = requests.patch(
        f"{api_url}/clubs/{club_id}/",
        headers=auth_headers,
        json=update_body
    )

    logger.info("Status code: %s", update_response.status_code)
    logger.info("Headers: %s", update_response.headers)
    logger.info("Body: %s", update_response.text)

    assert update_response.status_code in [200, 204]

    get_response = requests.get(f"{api_url}/clubs/{club_id}/", headers=auth_headers)
    assert get_response.status_code == 200

    print(update_response.text)

    body = get_response.json()
    assert body["bookTitle"] == update_body["bookTitle"]
    assert body["bookAuthors"] == "Updated Author"
    assert body["publicationYear"] == update_body["publicationYear"]
    assert body["description"] == "Updated description"

    requests.delete(f"{api_url}/clubs/{club_id}/", headers=auth_headers)


def test_delete_club(api_url, auth_headers, club_body):
    create_response = create_club(api_url, auth_headers, club_body)
    assert create_response.status_code == 201

    club_id = create_response.json()["id"]

    delete_response = requests.delete(f"{api_url}/clubs/{club_id}/", headers=auth_headers)

    logger.info("Status code: %s", delete_response.status_code)
    logger.info("Headers: %s", delete_response.headers)
    logger.info("Body: %s", delete_response.text)

    assert delete_response.status_code == 204

    get_response = requests.get(f"{api_url}/clubs/{club_id}/", headers=auth_headers)
    assert get_response.status_code in [404, 410]