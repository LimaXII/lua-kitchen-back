from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import recipes, health

app = FastAPI(title="Recipes API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router)
app.include_router(recipes.router)