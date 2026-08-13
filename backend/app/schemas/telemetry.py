from datetime import datetime

from pydantic import BaseModel, Field


class TelemetryReading(BaseModel):
    device_id: str = Field(min_length=1)
    timestamp: datetime
    temperature: float
    humidity: float
    pressure: float