import logging

import pandas as pd
from sqlalchemy import create_engine, text

from config import DATABASE_URL

logger = logging.getLogger(__name__)


def load_telemetry(device_id: str, limit: int = 500) -> pd.DataFrame:
    """
    Load recent telemetry for a single device from PostgreSQL.

    Returns a DataFrame with columns:
    device_id, timestamp, temperature, humidity, pressure

    Ordered oldest -> newest.
    """
    engine = create_engine(DATABASE_URL)

    query = text(
        """
        SELECT d.device_id, t.timestamp, t.temperature, t.humidity, t.pressure
        FROM telemetry t
        JOIN devices d ON t.device_pk = d.id
        WHERE d.device_id = :device_id
        ORDER BY t.timestamp DESC
        LIMIT :limit
        """
    )

    with engine.connect() as conn:
        df = pd.read_sql(query, conn, params={"device_id": device_id, "limit": limit})

    return df.sort_values("timestamp").reset_index(drop=True)