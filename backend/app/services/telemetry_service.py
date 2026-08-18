import logging
import threading

from app.db.session import SessionLocal
from app.repositories.device_repository import get_or_create_device
from app.repositories.telemetry_repository import insert_telemetry
from app.schemas.telemetry import TelemetryReading
from app.services.anomaly_service import analyze_and_store

logger = logging.getLogger(__name__)


def _run_anomaly_analysis(device_pk: int, device_id: str) -> None:
    """Runs in a background thread with its own DB session."""
    db = SessionLocal()
    try:
        analyze_and_store(db, device_pk, device_id)
    finally:
        db.close()


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
        device_pk, device_id = device.id, reading.device_id
    except Exception as e:
        db.rollback()
        logger.error("Database error while storing telemetry for device=%s: %s", reading.device_id, e)
        return
    finally:
        db.close()

    threading.Thread(
        target=_run_anomaly_analysis,
        args=(device_pk, device_id),
        daemon=True,
    ).start()