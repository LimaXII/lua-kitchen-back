from pydantic import BaseModel
from .ingredient import Ingredient

class RecipeIngredientSchema(BaseModel):
    ingredient: Ingredient
    quantity: str | None = None

    class Config:
        from_attributes = True