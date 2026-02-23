from datetime import datetime
from pydantic import BaseModel, ConfigDict
from .recipe_ingredient import RecipeIngredientCreate, RecipeIngredientSchema


class RecipeCreate(BaseModel):
    name: str
    prepare_mode: str
    prepare_time: int
    score: int = 0
    ingredients: list[RecipeIngredientCreate]  # nome + quantidade (opcional) de cada um
    image_base64: str | None = None


class RecipeBase(BaseModel):
    name: str
    prepare_mode: str
    prepare_time: int
    score: int = 0
    image_base64: str | None = None
    times_made: int = 0


class Recipe(RecipeBase):
    id: str
    created_at: datetime
    updated_at: datetime

    ingredients: list[RecipeIngredientSchema] = []

    model_config = ConfigDict(from_attributes=True)


class RecipeUpdate(RecipeBase):
    name: str | None = None
    prepare_mode: str | None = None
    prepare_time: int | None = None