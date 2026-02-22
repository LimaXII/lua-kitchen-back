"""Test create recipe API. Caution: This test will modify the main database.
In case you need to run this script only, use this command:
poetry run pytest tests/test_create_recipe_api.py -v
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database.init_db import init_db


@pytest.fixture(scope="module")
def client():
    init_db()
    yield TestClient(app)


def test_create_recipe_via_api(client: TestClient):
    """Create a recipe by sending POST to /recipes."""
    response = client.post(
        "/recipes",
        json={
            "name": "Cachorro quente com pimentão",
            "prepare_mode": "Grelhe a salsicha, refogue o pimentão e monte no pão",
            "prepare_time": 15,
            "score": 4,
            "ingredients": [
                {"name": "salsicha", "quantity": "2 unidades"},
                {"name": "pimentão", "quantity": "1/2 unidade"},
                {"name": "pão de hot dog", "quantity": "1 unidade"},
            ],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Cachorro quente com pimentão"
    assert data["prepare_time"] == 15
    assert "id" in data
    assert len(data["ingredients"]) == 3
