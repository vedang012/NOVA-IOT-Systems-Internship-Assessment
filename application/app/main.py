import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# Parse CORS_ORIGINS from environment variable. 
# Example value: "http://localhost:3000,http://localhost:5173"
cors_origins_str = os.getenv("CORS_ORIGINS", "")
origins = [origin.strip() for origin in cors_origins_str.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Accept"],
)


# Connect routers
app.include_router(health.router)
app.include_router(devices.router)
app.include_router(readings.router)
