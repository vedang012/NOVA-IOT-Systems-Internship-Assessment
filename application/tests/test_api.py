import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
import uuid

# Use in-memory SQLite for testing to avoid needing a real database running
from sqlalchemy.pool import StaticPool
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# We must mock get_db before importing main for it to apply on router endpoints? No, dependency overrides can happen after
from app.main import app
from app.database import get_db, Base
from app import models

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "API is running"}

def test_create_reading():
    device_id = f"TEST-ROOM-{uuid.uuid4().hex[:4]}"
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    read_data = {
        "device_id": device_id,
        "temperature": 23.8,
        "humidity": 87.4,
        "co2": 1180,
        "timestamp": now
    }
    response = client.post("/api/readings", json=read_data)
    assert response.status_code == 201
    data = response.json()
    assert data["device_id"] == device_id
    assert data["temperature"] == 23.8
    assert data["humidity"] == 87.4
    assert data["co2"] == 1180
    assert "id" in data

def test_get_devices():
    response = client.get("/api/devices")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_readings():
    response = client.get("/api/readings")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "temperature" in data[0]
