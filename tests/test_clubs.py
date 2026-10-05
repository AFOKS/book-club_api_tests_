import pytest
import requests
from jsonschema import validate

from schemas.schema import CLUBS_LIST_SCHEMA

BASE_URL = "https://book-club.qa.guru/api/v1/clubs/"


def test_get_clubs_has_results():
    response = requests.get(BASE_URL)

    assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

    data = response.json()
    assert isinstance(data["results"], list)
    assert data["results"], "Список результатов пуст"
    assert data["count"] > 0


def test_get_clubs_matches_schema():
    response = requests.get(BASE_URL)

    assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

    data = response.json()
    validate(instance=data, schema=CLUBS_LIST_SCHEMA)


def test_get_clubs_real_content():
    response = requests.get(BASE_URL)

    assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

    first_club = response.json()["results"][0]
    assert first_club["bookTitle"].strip(), "bookTitle пустой"
    assert first_club["bookAuthors"].strip(), "bookAuthors пустой"
    assert isinstance(first_club["publicationYear"], int)


def test_search_returns_matching_book():
    response = requests.get(BASE_URL, params={'search': 'Тестовая книга'})

    assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

    data = response.json()
    assert data["results"], "Список результатов пуст"

    book_title = data["results"][0]["bookTitle"]
    assert 'Тестовая книга' in book_title, f"Ожидалось, что '{book_title}' содержит 'Тестовая книга'"


def test_search_clubs():
    first_response = requests.get(BASE_URL)

    assert first_response.status_code == 200, f"Ожидался 200, получен {first_response.status_code}"

    search_item = first_response.json()["results"][0]["bookTitle"]

    response = requests.get(BASE_URL, params={"search": search_item})

    assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

    data = response.json()
    assert data["count"] >= 1, "Ожидался хотя бы 1 результат"
    assert search_item in data["results"][0]["bookTitle"]


def test_get_clubs_page_size():
    response = requests.get(BASE_URL, params={"page": 1, "page_size": 2})

    assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

    data = response.json()
    if data["count"] < 2:
        pytest.skip("В базе меньше 2 клубов — тест пагинации пропущен")

    assert len(data["results"]) == 2