from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.api.deps import get_db
from app.database import crud

router = APIRouter(prefix="/recipes", tags=["Recipes"])

@router.post("", response_model=schemas.Recipe)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    return crud.create_recipe(db, recipe)

@router.get("", response_model=list[schemas.Recipe])
def list_recipes(
    order_by_times_made: bool = False,
    db: Session = Depends(get_db),
):
    return crud.list_recipes(db, order_by_times_made=order_by_times_made)

@router.get("/search", response_model=list[schemas.Recipe])
def search_recipes(ingredient: str, db: Session = Depends(get_db)):
    recipes = crud.search_by_ingredient(db, ingredient)
    if not recipes:
        raise HTTPException(status_code=404, detail="No recipes found with this ingredient")
    return recipes

@router.get("/{recipe_id}", response_model=schemas.Recipe)
def get_recipe_by_uuid(recipe_id: str, db: Session = Depends(get_db)):
    recipe = crud.get_recipe_by_id(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.patch("/{recipe_id}/increment-times-made", response_model=schemas.Recipe)
def increment_recipe_times_made(recipe_id: str, db: Session = Depends(get_db)):
    recipe = crud.increment_times_made(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.delete("/{recipe_id}")
def delete_recipe(recipe_id: str, db: Session = Depends(get_db)):
    if not crud.delete_recipe(db, recipe_id):
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"message": "Recipe deleted successfully"}