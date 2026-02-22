from fastapi import FastAPI

from app.api.routes import recipes, health

app = FastAPI(title="Recipes API")

# Routers
app.include_router(health.router)
app.include_router(recipes.router)