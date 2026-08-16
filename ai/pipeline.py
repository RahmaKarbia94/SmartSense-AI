import logging

import pandas as pd

from data_loader import load_telemetry
from preprocessing import preprocess
from model import AnomalyDetector

logger = logging.getLogger(__name__)

RESULT_COLUMNS = ["device_id", "timestamp", "is_anomaly", "anomaly_score"]


def detect_anomalies(device_id: str, limit: int = 500) -> pd.DataFrame:
    """
    End-to-end anomaly detection for one device's recent telemetry.

    telemetry (PostgreSQL) -> preprocessing -> model -> anomaly result

    Returns a DataFrame with: device_id, timestamp, is_anomaly, anomaly_score.
    Trains a fresh Isolation Forest on the loaded batch each call — see
    ai/README.md for why, and its limitations.
    """
    raw = load_telemetry(device_id, limit=limit)
    features = preprocess(raw)

    detector = AnomalyDetector()
    detector.fit(features)
    predictions = detector.predict(features)

    result = raw.loc[features.index, ["device_id", "timestamp"]].join(predictions)
    return result[RESULT_COLUMNS].reset_index(drop=True)