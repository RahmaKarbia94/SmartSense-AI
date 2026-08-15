from sqlalchemy.orm import Session

from app.models.telemetry import Telemetry
from app.schemas.telemetry import TelemetryReading


def insert_telemetry(db: Session, reading: TelemetryReading, device_pk: int) -> Telemetry:
    telemetry = Telemetry(
        device_pk=device_pk,
        timestamp=reading.timestamp,
        temperature=reading.temperature,
        humidity=reading.humidity,
        pressure=reading.pressure,
    )
    db.add(telemetry)
    db.flush()
    return telemetry