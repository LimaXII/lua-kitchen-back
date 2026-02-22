import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database.init_db import init_db


@pytest.fixture(scope="module")
def client():
    """Client test with in-memory database."""
    init_db()
    yield TestClient(app)


def test_create_recipe(client: TestClient):
    """Send POST to create a recipe and verify 200 response."""
    payload = {
        "name": "Bolo de Chocolate",
        "prepare_mode": "Misture os ingredientes e asse por 40 min",
        "prepare_time": 45,
        "score": 5,
        "image_path": None,
        "ingredients": [
            {"name": "farinha", "quantity": "2 xícaras"},
            {"name": "chocolate", "quantity": "200g"},
        ],
    }
    response = client.post("/recipes", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Bolo de Chocolate"
    assert data["prepare_time"] == 45
    assert "id" in data
    assert len(data["ingredients"]) == 2


def test_create_recipe_minimal(client: TestClient):
    """Create recipe with minimal fields (no ingredients)."""
    payload = {
        "name": "Ovo Cozido",
        "prepare_mode": "Ferva água e coloque o ovo por 10 min",
        "prepare_time": 10,
        "ingredients": [],
    }
    response = client.post("/recipes", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Ovo Cozido"
    assert data["ingredients"] == []
