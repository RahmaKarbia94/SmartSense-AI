import random
from datetime import datetime, timezone

from config import (
    DEVICE_ID,
    TEMPERATURE_MIN,
    TEMPERATURE_MAX,
    HUMIDITY_MIN,
    HUMIDITY_MAX,
    PRESSURE_MIN,
    PRESSURE_MAX,
)


def generate_reading():
    temperature = round(
        random.uniform(TEMPERATURE_MIN, TEMPERATURE_MAX), 2
    )

    humidity = round(
        random.uniform(HUMIDITY_MIN, HUMIDITY_MAX), 2
    )

    pressure = round(
    random.uniform(PRESSURE_MIN, PRESSURE_MAX), 2
)

    return {
        "device_id": DEVICE_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure,
    }