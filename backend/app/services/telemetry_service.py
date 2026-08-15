import logging

from sqlalchemy.exc import SQLAlchemyError

from app.db.session import SessionLocal
from app.repositories.device_repository import get_or_create_device
from app.repositories.telemetry_repository import insert_telemetry
from app.schemas.telemetry import TelemetryReading

logger = logging.getLogger(__name__)


def process_telemetry(reading: TelemetryReading) -> None:
    db = SessionLocal()
    try:
        device = get_or_create_device(db, reading.device_id)
        insert_telemetry(db, reading, device_pk=device.id)
        db.commit()
        logger.info(
            "Stored telemetry: device=%s temp=%.2f humidity=%.2f pressure=%.2f",
            reading.device_id,
            reading.temperature,
            reading.humidity,
            reading.pressure,
        )
    except Exception as e:
        db.rollback()
        logger.error("Database error while storing telemetry for device=%s: %s", reading.device_id, e)
    finally:
        db.close()