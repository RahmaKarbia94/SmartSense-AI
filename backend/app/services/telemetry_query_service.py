from sqlalchemy.orm import Session

from app.repositories.device_repository import get_device_by_device_id
from app.repositories.telemetry_repository import (
    get_telemetry_for_device,
    get_latest_telemetry_per_device,
)
from app.schemas.telemetry_response import TelemetryResponse


def get_device_telemetry(
    db: Session, device_id: str, limit: int, offset: int
) -> list[TelemetryResponse] | None:
    device = get_device_by_device_id(db, device_id)
    if device is None:
        return None

    readings = get_telemetry_for_device(db, device.id, limit, offset)
    return [
        TelemetryResponse(
            id=r.id,
            device_id=device_id,
            timestamp=r.timestamp,
            temperature=r.temperature,
            humidity=r.humidity,
            pressure=r.pressure,
        )
        for r in readings
    ]


def get_latest_telemetry(db: Session) -> list[TelemetryResponse]:
    rows = get_latest_telemetry_per_device(db)
    return [
        TelemetryResponse(
            id=telemetry.id,
            device_id=device_id_str,
            timestamp=telemetry.timestamp,
            temperature=telemetry.temperature,
            humidity=telemetry.humidity,
            pressure=telemetry.pressure,
        )
        for telemetry, device_id_str in rows
    ]