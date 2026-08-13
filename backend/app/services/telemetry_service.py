import logging

from app.schemas.telemetry import TelemetryReading

logger = logging.getLogger(__name__)


def process_telemetry(reading: TelemetryReading) -> None:
    logger.info(
        "Telemetry received: device=%s temp=%.2f humidity=%.2f pressure=%.2f",
        reading.device_id,
        reading.temperature,
        reading.humidity,
        reading.pressure,
    )