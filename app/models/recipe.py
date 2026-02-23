import uuid
from datetime import date
from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.orm import relationship
from app.database.session import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    prepare_mode = Column(String, nullable=False)
    prepare_time = Column(Integer, nullable=False)
    score = Column(Integer, default=0)
    image_path = Column(String, nullable=True)
    times_made = Column(Integer, default=0)

    created_at = Column(Date, default=date.today)
    updated_at = Column(Date, default=date.today)

    ingredients = relationship(
        "RecipeIngredient",
        back_populates="recipe",
        cascade="all, delete"
    )