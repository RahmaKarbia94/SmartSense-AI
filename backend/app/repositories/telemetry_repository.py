from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.device import Device
from app.models.telemetry import Telemetry
from app.schemas.telemetry import TelemetryReading
def get_telemetry_for_device(db: Session, device_pk: int, limit: int, offset: int):
    return (
        db.query(Telemetry)
        .filter(Telemetry.device_pk == device_pk)
        .order_by(Telemetry.timestamp.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


def get_latest_telemetry_per_device(db: Session):
    latest_per_device = (
        db.query(
            Telemetry.device_pk,
            func.max(Telemetry.timestamp).label("max_timestamp"),
        )
        .group_by(Telemetry.device_pk)
        .subquery()
    )

    return (
        db.query(Telemetry, Device.device_id)
        .join(Device, Telemetry.device_pk == Device.id)
        .join(
            latest_per_device,
            (Telemetry.device_pk == latest_per_device.c.device_pk)
            & (Telemetry.timestamp == latest_per_device.c.max_timestamp),
        )
        .all()
    )


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