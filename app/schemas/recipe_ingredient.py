from pydantic import BaseModel, ConfigDict
from .ingredient import Ingredient


class RecipeIngredientCreate(BaseModel):
    """Item de ingrediente ao criar/editar receita: nome e quantidade (opcional)."""
    name: str
    quantity: str | None = None


class RecipeIngredientSchema(BaseModel):
    ingredient: Ingredient
    quantity: str | None = None

    model_config = ConfigDict(from_attributes=True)