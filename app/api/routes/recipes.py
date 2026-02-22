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
def list_recipes(db: Session = Depends(get_db)):
    return crud.list_recipes(db)

@router.get("/search", response_model=list[schemas.Recipe])
def search_recipes(ingredient: str, db: Session = Depends(get_db)):
    recipes = crud.search_by_ingredient(db, ingredient)
    if not recipes:
        raise HTTPException(status_code=404, detail="Nenhuma receita encontrada com esse ingrediente")
    return recipes