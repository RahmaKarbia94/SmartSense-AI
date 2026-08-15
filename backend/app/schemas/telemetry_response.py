from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TelemetryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    device_id: str
    timestamp: datetime
    temperature: float
    humidity: float
    pressure: float