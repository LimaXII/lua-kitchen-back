from pydantic import BaseModel, ConfigDict
from .ingredient import Ingredient

class RecipeIngredientSchema(BaseModel):
    ingredient: Ingredient
    quantity: str | None = None

    model_config = ConfigDict(from_attributes=True)