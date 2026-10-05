import pytest

from helpers import check_error_fields, check_status


def test_create_club_success(created_club, club_data):
    for field in ("bookTitle", "bookAuthors", "publicationYear", "description", "telegramChatLink"):
        assert created_club[field] == club_data[field], f"Поле {field} не совпало"
    assert "id" in created_club


def test_create_club_missing_title(auth_client, club_data):
    bad_data = {k: v for k, v in club_data.items() if k != "bookTitle"}

    response = auth_client.post("/clubs/", json=bad_data)

    check_status(response, 400)
    check_error_fields(response, "bookTitle")


def test_create_club_duplicate_title(auth_client, created_club, club_data):
    response = auth_client.post("/clubs/", json=club_data)

    check_status(response, 400)
    check_error_fields(response, "bookTitle")


def test_get_club_by_id(auth_client, created_club):
    response = auth_client.get(f"/clubs/{created_club['id']}/")

    check_status(response, 200)
    data = response.json()
    assert data["id"] == created_club["id"]
    assert data["bookTitle"] == created_club["bookTitle"]


def test_get_club_not_found(auth_client):
    response = auth_client.get("/clubs/99999999/")

    check_status(response, 404)


def test_update_club_title(auth_client, created_club):
    new_title = "Новое название"

    response = auth_client.patch(f"/clubs/{created_club['id']}/", json={"bookTitle": new_title})

    check_status(response, 200)
    assert response.json()["bookTitle"] == new_title


def test_delete_club(auth_client, created_club):
    club_id = created_club["id"]

    check_status(auth_client.delete(f"/clubs/{club_id}/"), 204)
    check_status(auth_client.get(f"/clubs/{club_id}/"), 404)


def test_create_club_without_auth(api_client, club_data):
    response = api_client.post("/clubs/", json=club_data)

    check_status(response, 401)


@pytest.mark.parametrize("method", ["patch", "delete"])
def test_modify_club_without_auth(api_client, created_club, method):
    body = {"bookTitle": "X"} if method == "patch" else None

    response = api_client.request(method, f"/clubs/{created_club['id']}/", json=body)

    check_status(response, 401)
