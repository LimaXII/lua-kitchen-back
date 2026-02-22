import uuid
from datetime import date
from pydantic import BaseModel, ConfigDict
from .recipe_ingredient import RecipeIngredientSchema

class RecipeBase(BaseModel):
    name: str
    prepare_mode: str
    prepare_time: int
    score: int = 0
    image_path: str | None = None

class RecipeCreate(RecipeBase):
    ingredients: list[dict] = [] 

class RecipeUpdate(RecipeBase):
    name: str | None = None
    prepare_mode: str | None = None
    prepare_time: int | None = None

class Recipe(RecipeBase):
    id: str
    created_at: date
    updated_at: date

    ingredients: list[RecipeIngredientSchema] = []

    model_config = ConfigDict(from_attributes=True)