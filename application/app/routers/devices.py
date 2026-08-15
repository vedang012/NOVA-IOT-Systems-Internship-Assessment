from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..security import get_api_key

router = APIRouter(
    prefix="/api/devices", 
    tags=["devices"],
    dependencies=[Depends(get_api_key)]
)

@router.get("", response_model=List[schemas.Device])
def get_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Return all registered devices.
    """
    devices = db.query(models.Device).offset(skip).limit(limit).all()
    return devices
