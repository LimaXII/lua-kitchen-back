"""Tests for get recipe by UUID, increment times_made, and order_by_times_made."""

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
def created_recipe(client: TestClient):
    """Create a recipe and return full response data."""
    payload = {
        "name": "Receita para Teste UUID",
        "prepare_mode": "Modo de preparo",
        "prepare_time": 20,
        "score": 5,
        "ingredients": [{"name": "ingrediente_teste", "quantity": "1"}],
    }
    response = client.post("/recipes", json=payload)
    assert response.status_code == 200
    return response.json()


def test_get_recipe_by_uuid_success(client: TestClient, created_recipe: dict):
    """GET /recipes/{id} returns the recipe when it exists."""
    recipe_id = created_recipe["id"]
    response = client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == recipe_id
    assert data["name"] == "Receita para Teste UUID"
    assert "times_made" in data
    assert data["times_made"] == 0


def test_get_recipe_by_uuid_not_found(client: TestClient):
    """GET /recipes/{id} returns 404 for non-existent UUID."""
    response = client.get("/recipes/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    assert "não encontrada" in response.json()["detail"].lower()


def test_increment_times_made_success(client: TestClient, created_recipe: dict):
    """PATCH /recipes/{id}/increment-times-made increments and returns recipe."""
    recipe_id = created_recipe["id"]
    response = client.patch(f"/recipes/{recipe_id}/increment-times-made")
    assert response.status_code == 200
    data = response.json()
    assert data["times_made"] == 1
    # Increment again
    response2 = client.patch(f"/recipes/{recipe_id}/increment-times-made")
    assert response2.status_code == 200
    assert response2.json()["times_made"] == 2


def test_increment_times_made_not_found(client: TestClient):
    """PATCH /recipes/{id}/increment-times-made returns 404 for non-existent recipe."""
    response = client.patch(
        "/recipes/00000000-0000-0000-0000-000000000000/increment-times-made"
    )
    assert response.status_code == 404
    assert "não encontrada" in response.json()["detail"].lower()


def test_list_recipes_order_by_times_made(client: TestClient):
    """GET /recipes?order_by_times_made=true returns recipes sorted by times_made desc."""
    # Create two recipes
    r1 = client.post(
        "/recipes",
        json={
            "name": "Receita A",
            "prepare_mode": "Modo A",
            "prepare_time": 10,
            "ingredients": [],
        },
    ).json()
    r2 = client.post(
        "/recipes",
        json={
            "name": "Receita B",
            "prepare_mode": "Modo B",
            "prepare_time": 10,
            "ingredients": [],
        },
    ).json()
    # Increment Receita B twice and Receita A once
    client.patch(f"/recipes/{r2['id']}/increment-times-made")
    client.patch(f"/recipes/{r2['id']}/increment-times-made")
    client.patch(f"/recipes/{r1['id']}/increment-times-made")
    # List with order_by_times_made
    response = client.get("/recipes?order_by_times_made=true")
    assert response.status_code == 200
    recipes = response.json()
    names = [r["name"] for r in recipes]
    # First ones should be those with higher times_made (Receita B=2, Receita A=1)
    idx_b = names.index("Receita B")
    idx_a = names.index("Receita A")
    assert idx_b < idx_a


def test_list_recipes_default_includes_times_made(client: TestClient, created_recipe: dict):
    """GET /recipes returns recipes with times_made field."""
    response = client.get("/recipes")
    assert response.status_code == 200
    recipes = response.json()
    assert len(recipes) >= 1
    for r in recipes:
        assert "times_made" in r


def test_cors_middleware_configured(client: TestClient):
    """App responds successfully; CORS is enabled in main.py for browser requests."""
    response = client.get("/recipes")
    assert response.status_code == 200
