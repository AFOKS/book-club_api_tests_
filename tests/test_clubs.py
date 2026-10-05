from jsonschema import validate

from helpers import check_status
from schemas.schema import CLUBS_LIST_SCHEMA


def test_get_clubs_has_results(api_client, created_club):
    response = api_client.get("/clubs/")

    check_status(response, 200)
    data = response.json()
    assert isinstance(data["results"], list)
    assert data["results"], "Список результатов пуст"
    assert data["count"] > 0


def test_get_clubs_matches_schema(api_client, created_club):
    response = api_client.get("/clubs/")

    check_status(response, 200)
    validate(instance=response.json(), schema=CLUBS_LIST_SCHEMA)


def test_get_clubs_real_content(api_client, created_club):
    response = api_client.get("/clubs/")

    check_status(response, 200)
    for club in response.json()["results"]:
        assert club["bookTitle"].strip(), f"bookTitle пустой у клуба {club.get('id')}"
        assert club["bookAuthors"].strip(), f"bookAuthors пустой у клуба {club.get('id')}"
        assert isinstance(club["publicationYear"], int), f"publicationYear не int у клуба {club.get('id')}"


def test_search_finds_created_club(api_client, created_club):
    response = api_client.get("/clubs/", params={"search": created_club["bookTitle"]})

    check_status(response, 200)
    results = response.json()["results"]
    ids = [club["id"] for club in results]
    assert created_club["id"] in ids, (
        f"Клуб {created_club['id']} ('{created_club['bookTitle']}') не найден в результатах поиска: {ids}"
    )


def test_search_results_match_query(api_client, created_club):
    query = created_club["bookTitle"]

    response = api_client.get("/clubs/", params={"search": query})

    check_status(response, 200)
    for club in response.json()["results"]:
        assert query.lower() in club["bookTitle"].lower(), (
            f"'{club['bookTitle']}' не содержит поисковый запрос '{query}'"
        )


def test_get_clubs_page_size(api_client, club_factory):
    club_factory()
    club_factory()

    response = api_client.get("/clubs/", params={"page": 1, "page_size": 2})

    check_status(response, 200)
    data = response.json()
    assert data["count"] >= 2
    assert len(data["results"]) == 2
