from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AnomalyResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    device_id: str
    timestamp: datetime
    is_anomaly: bool
    anomaly_score: float