import pytest
from fastapi.testclient import TestClient

from main import create_app


@pytest.fixture
def client(database_path):
    with TestClient(create_app(database_path)) as test_client:
        yield test_client


def test_create_and_list_review(client):
    assert client.get("/reviews").json() == []
    response = client.post(
        "/reviews",
        json={"author": "  Настя  ", "text": " Круто, класс! "},
    )
    assert response.status_code == 201
    review = response.json()
    assert review == {"id": 1, "author": "Настя", "text": "Круто, класс!"}
    response = client.get("/reviews")
    assert response.status_code == 200
    assert response.json() == [review]
    assert client.get("/docs").status_code == 200


@pytest.mark.parametrize(
    ("payload", "field"),
    [
        ({"author": "   ", "text": "Текст"}, "author"),
        ({"author": "Автор", "text": " \t "}, "text"),
        ({"author": "Автор", "text": "x" * 1001}, "text"),
        ({"author": "Автор"}, "text"),
        ({"text": "Текст"}, "author"),
    ],
)
def test_invalid_review_is_rejected(client, payload, field):
    response = client.post("/reviews", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", field]
    assert client.get("/reviews").json() == []


def test_filter_get_and_delete_review(client):
    first = client.post(
        "/reviews",
        json={"author": "Настя", "text": "Круто!"},
    ).json()
    second = client.post(
        "/reviews",
        json={"author": "Миша", "text": "Класс!"},
    ).json()

    assert client.get("/reviews?author=Настя").json() == [first]
    assert client.get("/reviews?author=Неизвестный").json() == []
    assert client.get(f"/reviews/{first['id']}").json() == first

    response = client.delete(f"/reviews/{first['id']}")
    assert response.status_code == 204
    assert response.content == b""
    assert client.get("/reviews").json() == [second]


def test_missing_review_returns_404(client):
    response = client.get("/reviews/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Отзыв не найден"}

    response = client.delete("/reviews/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Отзыв не найден"}


def test_database_survives_application_restart(database_path):
    with TestClient(create_app(database_path)) as first_client:
        review = first_client.post(
            "/reviews",
            json={"author": "Настя", "text": "Круто, класс!"},
        ).json()

    with TestClient(create_app(database_path)) as second_client:
        assert second_client.get("/reviews").json() == [review]
