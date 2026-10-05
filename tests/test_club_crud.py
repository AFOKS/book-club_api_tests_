from tests.conftest import BASE_URL


def test_create_club_success(created_club, club_data):
    assert created_club["bookTitle"] == club_data["bookTitle"]
    assert created_club["bookAuthors"] == club_data["bookAuthors"]
    assert created_club["publicationYear"] == club_data["publicationYear"]
    assert created_club["description"] == club_data["description"]
    assert created_club["telegramChatLink"] == club_data["telegramChatLink"]
    assert "id" in created_club


def test_create_club_missing_title(auth_client, club_data):
    bad_data = club_data.copy()
    bad_data.pop("bookTitle")

    response = auth_client.post(f"{BASE_URL}/clubs/", json=bad_data)

    assert response.status_code == 400
    assert "bookTitle" in response.json()


def test_create_club_duplicate_title(auth_client, created_club, club_data):
    response = auth_client.post(f"{BASE_URL}/clubs/", json=club_data)

    assert response.status_code == 400
    assert "bookTitle" in response.json()


def test_get_club_by_id(auth_client, created_club):
    response = auth_client.get(f"{BASE_URL}/clubs/{created_club['id']}/")

    assert response.status_code == 200
    data = response.json()
    print()
    print(f"Получен:{data}")
    assert data["id"] == created_club["id"]
    assert data["bookTitle"] == created_club["bookTitle"]


def test_get_club_not_found(auth_client):
    response = auth_client.get(f"{BASE_URL}/clubs/99999999/")

    assert response.status_code == 404


def test_update_club_title(auth_client, created_club):
    new_title = "Новое название"
    response = auth_client.patch(
        f"{BASE_URL}/clubs/{created_club['id']}/",
        json={"bookTitle": new_title},
    )

    print()
    print(f"Получен:{response.text}")
    assert response.status_code == 200
    assert response.json()["bookTitle"] == new_title


def test_delete_club(auth_client, created_club):
    club_id = created_club["id"]

    response = auth_client.delete(f"{BASE_URL}/clubs/{club_id}/")
    assert response.status_code == 204

    check = auth_client.get(f"{BASE_URL}/clubs/{club_id}/")
    assert check.status_code == 404


def test_create_club_without_auth(api_client, club_data):
    response = api_client.post(f"{BASE_URL}/clubs/", json=club_data)

    assert response.status_code == 401


def test_update_club_without_auth(api_client, created_club):
    response = api_client.patch(f"{BASE_URL}/clubs/{created_club['id']}/", json={"bookTitle": "X"})

    assert response.status_code == 401


def test_delete_club_without_auth(api_client, created_club):
    response = api_client.delete(f"{BASE_URL}/clubs/{created_club['id']}/")

    print()
    print(f"Получен:{response.text}")
    assert response.status_code == 401