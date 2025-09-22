from __future__ import annotations
from fastapi import FastAPI
from .routes import health, inference, memory, experience


def create_app() -> FastAPI:
    app = FastAPI(title="GPT_5 Child API")
    app.include_router(health.router, prefix="/health", tags=["health"])
    app.include_router(memory.router, prefix="/memory", tags=["memory"])
    app.include_router(experience.router, prefix="/exp", tags=["experience"])
    app.include_router(inference.router, prefix="/inference", tags=["inference"])
    return app

