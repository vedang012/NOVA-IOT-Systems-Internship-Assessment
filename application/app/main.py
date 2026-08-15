from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import engine
from . import models
from .routers import health, devices, readings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure that the models are created in the database on startup.
    # In a robust production environment, use a tool like Alembic for migrations instead.
    models.Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Nova IoT API",
    description="Minimal FastAPI backend for IoT metrics",
    version="0.1.0",
    lifespan=lifespan
)


# Connect routers
app.include_router(health.router)
app.include_router(devices.router)
app.include_router(readings.router)
