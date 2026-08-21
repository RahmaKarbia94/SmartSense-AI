import logging

import pandas as pd
from sqlalchemy.orm import Session

from preprocessing import preprocess
from model import AnomalyDetector, InsufficientDataError

from app.repositories.telemetry_repository import get_telemetry_for_device
from app.repositories.anomaly_repository import (
    save_anomaly_result,
    get_already_analyzed_telemetry_ids,
    get_anomalies_for_device,
)
from app.repositories.device_repository import get_device_by_device_id
from app.schemas.anomaly import AnomalyResultResponse

logger = logging.getLogger(__name__)


def get_anomalies(db: Session, device_id: str) -> list[AnomalyResultResponse] | None:
    device = get_device_by_device_id(db, device_id)
    if device is None:
        return None

    rows = get_anomalies_for_device(db, device.id)
    return [
        AnomalyResultResponse(
            device_id=device_id,
            timestamp=timestamp,
            is_anomaly=result.is_anomaly,
            anomaly_score=result.anomaly_score,
        )
        for result, timestamp in rows
    ]


def analyze_and_store(db: Session, device_pk: int, device_id: str, window: int = 100) -> None:
    """
    Re-analyze a device's recent telemetry window for anomalies and
    persist the results. Trains a fresh model on the window each call
    (see ai/README.md for why, and its limitations).
    """
    try:
        readings = get_telemetry_for_device(db, device_pk, limit=window, offset=0)
    except Exception as e:
        logger.error(
            "Failed to fetch telemetry for anomaly analysis, device=%s: %s",
            device_id, e,
        )
        return

    if not readings:
        return

    raw = pd.DataFrame(
        [
            {
                "id": r.id,
                "temperature": r.temperature,
                "humidity": r.humidity,
                "pressure": r.pressure,
            }
            for r in readings
        ]
    )

    features = preprocess(raw)

    try:
        detector = AnomalyDetector()
        detector.fit(features)
        predictions = detector.predict(features)
    except InsufficientDataError as e:
        logger.info(
            "Skipping anomaly analysis for device=%s: %s", device_id, e
        )
        return
    except Exception as e:
        logger.error(
            "Anomaly analysis failed for device=%s: %s", device_id, e
        )
        return

    telemetry_ids = raw.loc[features.index, "id"]
    already_analyzed = get_already_analyzed_telemetry_ids(
        db, telemetry_ids.tolist()
    )

    new_count = 0
    try:
        for idx in features.index:
            tid = int(telemetry_ids.loc[idx])
            if tid in already_analyzed:
                continue
            saved = save_anomaly_result(
                db,
                telemetry_pk=tid,
                is_anomaly=bool(predictions.loc[idx, "is_anomaly"]),
                anomaly_score=float(predictions.loc[idx, "anomaly_score"]),
            )
            if saved is not None:
                new_count += 1
        db.commit()
        logger.info(
            "Stored %d new anomaly result(s) for device=%s (%d already analyzed, skipped)",
            new_count, device_id, len(features) - new_count,
        )
    except Exception as e:
        db.rollback()
        logger.error(
            "Failed to persist anomaly results for device=%s: %s", device_id, e
        )