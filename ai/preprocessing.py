import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

FEATURE_COLUMNS = ["temperature", "humidity", "pressure"]


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare telemetry for the anomaly detection model.

    - Selects temperature, humidity, pressure.
    - Drops rows with missing or non-finite values.
    - Returns a DataFrame with only the feature columns, ready for
      the model. The original row index is preserved so results can
      be mapped back to their source rows (device_id, timestamp) by
      the caller.
    """
    if df.empty:
        return df[FEATURE_COLUMNS] if all(c in df.columns for c in FEATURE_COLUMNS) else pd.DataFrame(columns=FEATURE_COLUMNS)

    missing_columns = [c for c in FEATURE_COLUMNS if c not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    features = df[FEATURE_COLUMNS].copy()

    for col in FEATURE_COLUMNS:
        features[col] = pd.to_numeric(features[col], errors="coerce")

    valid_mask = np.isfinite(features).all(axis=1)
    dropped = (~valid_mask).sum()
    if dropped > 0:
        logger.warning("Dropped %d row(s) with missing/invalid values", dropped)

    return features[valid_mask]