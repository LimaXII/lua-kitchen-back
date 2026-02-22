import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database.init_db import init_db


@pytest.fixture(scope="module")
def client():
    """Test client with in-memory database."""
    init_db()
    yield TestClient(app)


@pytest.fixture
def created_recipe_id(client: TestClient):
    """Create a recipe and return the ID to delete."""
    payload = {
        "name": "Receita para Deletar",
        "prepare_mode": "Teste",
        "prepare_time": 5,
        "ingredients": [{"name": "teste_ing", "quantity": "1"}],
    }
    response = client.post("/recipes", json=payload)
    assert response.status_code == 200
    return response.json()["id"]


def test_delete_recipe_success(client: TestClient, created_recipe_id: str):
    """Delete an existing recipe and verify success."""
    response = client.delete(f"/recipes/{created_recipe_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Receita deletada com sucesso"


def test_delete_recipe_not_found(client: TestClient):
    """Try to delete a non-existent recipe and verify 404."""
    response = client.delete("/recipes/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    assert "não encontrada" in response.json()["detail"].lower()
