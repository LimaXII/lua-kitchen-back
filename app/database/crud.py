from sqlalchemy.orm import Session
from app import models, schemas

def get_or_create_ingredient(db: Session, name: str):
    name_cleaned = name.strip().lower()
    
    ingredient = db.query(models.Ingredient).filter_by(name=name_cleaned).first()
    if not ingredient:
        ingredient = models.Ingredient(name=name_cleaned)
        db.add(ingredient)
        db.commit()
        db.refresh(ingredient)
    return ingredient

def create_recipe(db: Session, recipe_data: schemas.RecipeCreate):
    db_recipe = models.Recipe(
        name=recipe_data.name,
        prepare_mode=recipe_data.prepare_mode,
        prepare_time=recipe_data.prepare_time,
        score=recipe_data.score,
        image_path=recipe_data.image_path,
    )

    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)

    for item in recipe_data.ingredients:
        ing_name = item.get("name") if isinstance(item, dict) else item.name
        ing_qty = item.get("quantity") if isinstance(item, dict) else item.quantity
        
        ingredient = get_or_create_ingredient(db, ing_name)

        db_rel = models.RecipeIngredient(
            recipe_id=db_recipe.id,
            ingredient_id=ingredient.id,
            quantity=ing_qty,
        )
        db.add(db_rel)

    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def list_recipes(db: Session):
    return db.query(models.Recipe).all()

def search_by_ingredient(db: Session, ingredient_name: str):
    return (
        db.query(models.Recipe)
        .join(models.RecipeIngredient)
        .join(models.Ingredient)
        .filter(models.Ingredient.name.contains(ingredient_name.lower()))
        .distinct()
        .all()
    )