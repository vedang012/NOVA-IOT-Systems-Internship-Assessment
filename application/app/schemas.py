from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class DeviceBase(BaseModel):
    device_id: str
    name: Optional[str] = None
    location: Optional[str] = None

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ReadingBase(BaseModel):
    device_id: str
    temperature: float
    humidity: float
    co2: int
    timestamp: datetime

class ReadingCreate(ReadingBase):
    pass

class Reading(ReadingBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
