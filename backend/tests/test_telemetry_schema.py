import pytest
from pydantic import ValidationError

from app.schemas.telemetry import TelemetryReading


def test_valid_telemetry():
    reading = TelemetryReading(
        device_id="simulator_001",
        timestamp="2026-08-12T23:00:00+00:00",
        temperature=25.34,
        humidity=52.18,
        pressure=1014.27,
    )
    assert reading.device_id == "simulator_001"
    assert reading.temperature == 25.34


def test_missing_field_raises():
    with pytest.raises(ValidationError):
        TelemetryReading(
            device_id="simulator_001",
            timestamp="2026-08-12T23:00:00+00:00",
            temperature=25.34,
            humidity=52.18,
        )


def test_invalid_type_raises():
    with pytest.raises(ValidationError):
        TelemetryReading(
            device_id="simulator_001",
            timestamp="2026-08-12T23:00:00+00:00",
            temperature="hot",
            humidity=52.18,
            pressure=1014.27,
        )


def test_empty_device_id_raises():
    with pytest.raises(ValidationError):
        TelemetryReading(
            device_id="",
            timestamp="2026-08-12T23:00:00+00:00",
            temperature=25.34,
            humidity=52.18,
            pressure=1014.27,
        )

def test_temperature_out_of_range_raises():
    with pytest.raises(ValidationError):
        TelemetryReading(
            device_id="simulator_001",
            timestamp="2026-08-12T23:00:00+00:00",
            temperature=999.0,
            humidity=52.18,
            pressure=1014.27,
        )


def test_humidity_out_of_range_raises():
    with pytest.raises(ValidationError):
        TelemetryReading(
            device_id="simulator_001",
            timestamp="2026-08-12T23:00:00+00:00",
            temperature=25.34,
            humidity=150.0,
            pressure=1014.27,
        )


def test_pressure_out_of_range_raises():
    with pytest.raises(ValidationError):
        TelemetryReading(
            device_id="simulator_001",
            timestamp="2026-08-12T23:00:00+00:00",
            temperature=25.34,
            humidity=52.18,
            pressure=1.0,
        )


def test_naive_timestamp_raises():
    with pytest.raises(ValidationError):
        TelemetryReading(
            device_id="simulator_001",
            timestamp="2026-08-12T23:00:00",
            temperature=25.34,
            humidity=52.18,
            pressure=1014.27,
        )


def test_non_utc_timezone_raises():
    with pytest.raises(ValidationError):
        TelemetryReading(
            device_id="simulator_001",
            timestamp="2026-08-12T23:00:00+02:00",
            temperature=25.34,
            humidity=52.18,
            pressure=1014.27,
        )        