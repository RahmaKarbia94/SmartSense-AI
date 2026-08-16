import logging

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

from config import CONTAMINATION, RANDOM_STATE, MIN_SAMPLES_FOR_TRAINING

logger = logging.getLogger(__name__)


class InsufficientDataError(Exception):
    """Raised when there isn't enough data to train a meaningful model."""


class AnomalyDetector:
    """
    Wraps scikit-learn's Isolation Forest for telemetry anomaly detection.

    Isolation Forest is unsupervised: it isolates points by randomly
    partitioning the feature space, and points that are isolated in
    fewer splits are considered more anomalous. No labeled anomaly
    data is required or used.
    """

    def __init__(self):
        self._model = IsolationForest(
            contamination=CONTAMINATION,
            random_state=RANDOM_STATE,
        )
        self._fitted = False

    def fit(self, features: pd.DataFrame) -> None:
        if len(features) < MIN_SAMPLES_FOR_TRAINING:
            raise InsufficientDataError(
                f"Need at least {MIN_SAMPLES_FOR_TRAINING} samples to train, "
                f"got {len(features)}."
            )
        self._model.fit(features)
        self._fitted = True

    def predict(self, features: pd.DataFrame) -> pd.DataFrame:
        """
        Returns a DataFrame indexed like `features`, with columns:
        - is_anomaly: bool
        - anomaly_score: float (higher = more anomalous)
        """
        if not self._fitted:
            raise RuntimeError("Model must be fit before calling predict().")

        raw_predictions = self._model.predict(features)
        raw_scores = self._model.decision_function(features)

        return pd.DataFrame(
            {
                "is_anomaly": raw_predictions == -1,
                # scikit-learn's decision_function is higher = more normal;
                # we invert it so higher = more anomalous, which is more
                # intuitive for downstream consumers.
                "anomaly_score": -raw_scores,
            },
            index=features.index,
        )