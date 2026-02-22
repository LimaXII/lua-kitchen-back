import pytest

from app.database.session import SessionLocal
from app.database.init_db import init_db
from app.database import crud
from app import schemas, models


@pytest.fixture(scope="module")
def db_session():
    """Database session with test data."""
    init_db()
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def sample_recipe(db_session):
    """Create a sample recipe for tests."""
    recipe_data = schemas.RecipeCreate(
        name="Panqueca Americana",
        prepare_mode="Misture e frite",
        prepare_time=15,
        score=4,
        ingredients=[
            {"name": "leite", "quantity": "1 xícara"},
            {"name": "ovo", "quantity": "2 unidades"},
        ],
    )
    return crud.create_recipe(db_session, recipe_data)


def test_select_recipes(db_session, sample_recipe):
    """SELECT on the recipes table."""
    recipes = crud.list_recipes(db_session)
    assert len(recipes) >= 1
    names = [r.name for r in recipes]
    assert "Panqueca Americana" in names


def test_select_ingredients(db_session, sample_recipe):
    """SELECT on the ingredients table."""

    ingredients = db_session.query(models.Ingredient).all()
    assert len(ingredients) >= 2
    names = [i.name for i in ingredients]
    assert "leite" in names
    assert "ovo" in names


def test_select_recipe_ingredients(db_session, sample_recipe):
    """SELECT on the recipe_ingredients table (N:N relationship)."""

    rels = db_session.query(models.RecipeIngredient).all()
    assert len(rels) >= 2
    for rel in rels:
        assert rel.recipe_id is not None
        assert rel.ingredient_id is not None
        assert rel.quantity is not None or rel.quantity is None


def test_all_three_tables_populated(db_session, sample_recipe):
    """Ensure that the three tables have data after creating a recipe."""

    recipes_count = db_session.query(models.Recipe).count()
    ingredients_count = db_session.query(models.Ingredient).count()
    recipe_ingredients_count = db_session.query(models.RecipeIngredient).count()

    assert recipes_count >= 1
    assert ingredients_count >= 2
    assert recipe_ingredients_count >= 2
