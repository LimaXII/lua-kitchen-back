import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.orm import relationship
from app.database.session import Base


def _utc_now():
    return datetime.now(timezone.utc)


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    prepare_mode = Column(String, nullable=False)
    prepare_time = Column(Integer, nullable=False)
    score = Column(Integer, default=0)
    image_base64 = Column(Text, nullable=True)
    times_made = Column(Integer, default=0)

    created_at = Column(DateTime, default=_utc_now)
    updated_at = Column(DateTime, default=_utc_now, onupdate=_utc_now)

    ingredients = relationship(
        "RecipeIngredient",
        back_populates="recipe",
        cascade="all, delete"
    )