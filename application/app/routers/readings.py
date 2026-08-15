from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/readings", tags=["readings"])

@router.post("", response_model=schemas.Reading, status_code=status.HTTP_201_CREATED)
def create_reading(reading: schemas.ReadingCreate, db: Session = Depends(get_db)):
    """
    Save a new sensor reading. Auto-creates a minimal device entry if the device_id does not exist.
    """
    device = db.query(models.Device).filter(models.Device.device_id == reading.device_id).first()
    if not device:
        # Create a new minimal device record based on device_id to satisfy foreign key constraint
        device = models.Device(device_id=reading.device_id, name="Auto-registered", location="Unknown")
        db.add(device)
        db.flush()

    db_reading = models.Reading(**reading.model_dump())
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    return db_reading

@router.get("", response_model=List[schemas.Reading])
def get_readings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Return stored sensor readings.
    """
    readings = db.query(models.Reading).offset(skip).limit(limit).all()
    return readings
