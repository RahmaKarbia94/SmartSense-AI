from datetime import datetime, timedelta

from pydantic import BaseModel, Field, field_validator

TEMPERATURE_MIN = -50.0
TEMPERATURE_MAX = 60.0
HUMIDITY_MIN = 0.0
HUMIDITY_MAX = 100.0
PRESSURE_MIN = 800.0
PRESSURE_MAX = 1100.0


class TelemetryReading(BaseModel):
    device_id: str = Field(min_length=1)
    timestamp: datetime
    temperature: float
    humidity: float
    pressure: float

    @field_validator("timestamp")
    @classmethod
    def timestamp_must_be_utc(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            raise ValueError("timestamp must include timezone info (UTC)")
        if v.utcoffset() != timedelta(0):
            raise ValueError("timestamp must be in UTC")
        return v

    @field_validator("temperature")
    @classmethod
    def temperature_in_range(cls, v: float) -> float:
        if not (TEMPERATURE_MIN <= v <= TEMPERATURE_MAX):
            raise ValueError(
                f"temperature {v} outside reasonable range "
                f"[{TEMPERATURE_MIN}, {TEMPERATURE_MAX}]"
            )
        return v

    @field_validator("humidity")
    @classmethod
    def humidity_in_range(cls, v: float) -> float:
        if not (HUMIDITY_MIN <= v <= HUMIDITY_MAX):
            raise ValueError(
                f"humidity {v} outside reasonable range "
                f"[{HUMIDITY_MIN}, {HUMIDITY_MAX}]"
            )
        return v

    @field_validator("pressure")
    @classmethod
    def pressure_in_range(cls, v: float) -> float:
        if not (PRESSURE_MIN <= v <= PRESSURE_MAX):
            raise ValueError(
                f"pressure {v} outside reasonable range "
                f"[{PRESSURE_MIN}, {PRESSURE_MAX}]"
            )
        return v