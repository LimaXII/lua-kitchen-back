from datetime import datetime, timezone
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
        image_base64=recipe_data.image_base64,
        times_made=0,
    )

    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)

    for item in recipe_data.ingredients:
        ing_name = item.get("name") if isinstance(item, dict) else item.name
        ing_qty = item.get("quantity") if isinstance(item, dict) else item.quantity

        ingredient = get_or_create_ingredient(db, ing_name)

        quantity_lower = ing_qty.strip().lower() if (ing_qty and str(ing_qty).strip()) else None
        db_rel = models.RecipeIngredient(
            recipe_id=db_recipe.id,
            ingredient_id=ingredient.id,
            quantity=quantity_lower,
        )
        db.add(db_rel)

    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def get_recipe_by_id(db: Session, recipe_id: str):
    return db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()


def list_recipes(db: Session, order_by_times_made: bool = False):
    q = db.query(models.Recipe)
    if order_by_times_made:
        q = q.order_by(models.Recipe.times_made.desc())
    return q.all()


def increment_times_made(db: Session, recipe_id: str):
    recipe = get_recipe_by_id(db, recipe_id)
    if not recipe:
        return None
    recipe.times_made = (recipe.times_made or 0) + 1
    recipe.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(recipe)
    return recipe

def search_by_ingredient(db: Session, ingredient_name: str):
    return (
        db.query(models.Recipe)
        .join(models.RecipeIngredient)
        .join(models.Ingredient)
        .filter(models.Ingredient.name.contains(ingredient_name.lower()))
        .distinct()
        .all()
    )


def delete_recipe(db: Session, recipe_id: str):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        return False
    db.delete(recipe)
    db.commit()
    return True