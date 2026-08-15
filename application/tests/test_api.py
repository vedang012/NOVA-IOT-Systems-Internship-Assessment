import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
import uuid

# Mock environment variables BEFORE any application imports
os.environ["API_KEY"] = "super-secret-test-key"
os.environ["CORS_ORIGINS"] = "http://localhost:3000"

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

valid_headers = {"X-API-Key": "super-secret-test-key"}
invalid_headers = {"X-API-Key": "wrong-key"}

def test_health():
    response = client.get("/health")
    # Health endpoint should not require an API key
    assert response.status_code == 200

def test_unauthenticated_requests():
    # Attempting to access protected endpoints without API key
    assert client.get("/api/devices").status_code == 401
    assert client.get("/api/readings").status_code == 401
    assert client.post("/api/readings", json={}).status_code == 401

def test_invalid_api_key_requests():
    # Attempting to access protected endpoints with a bad API key
    assert client.get("/api/devices", headers=invalid_headers).status_code == 401
    assert client.get("/api/readings", headers=invalid_headers).status_code == 401

def test_create_reading_authenticated():
    device_id = f"TEST-ROOM-{uuid.uuid4().hex[:4]}"
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    read_data = {
        "device_id": device_id,
        "temperature": 23.8,
        "humidity": 87.4,
        "co2": 1180,
        "timestamp": now
    }
    response = client.post("/api/readings", json=read_data, headers=valid_headers)
    assert response.status_code == 201

def test_get_devices_authenticated():
    response = client.get("/api/devices", headers=valid_headers)
    assert response.status_code == 200

def test_get_readings_authenticated():
    response = client.get("/api/readings", headers=valid_headers)
    assert response.status_code == 200
