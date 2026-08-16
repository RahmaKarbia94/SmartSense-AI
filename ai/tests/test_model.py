import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import pandas as pd
import pytest

from model import AnomalyDetector, InsufficientDataError


def _normal_batch(n=50):
    rng = np.random.default_rng(42)
    return pd.DataFrame(
        {
            "temperature": rng.normal(25, 2, n),
            "humidity": rng.normal(55, 5, n),
            "pressure": rng.normal(1010, 10, n),
        }
    )


def test_insufficient_data_raises():
    detector = AnomalyDetector()
    tiny_batch = _normal_batch(n=5)
    with pytest.raises(InsufficientDataError):
        detector.fit(tiny_batch)


def test_predict_before_fit_raises():
    detector = AnomalyDetector()
    with pytest.raises(RuntimeError):
        detector.predict(_normal_batch())


def test_normal_data_mostly_not_flagged():
    features = _normal_batch(n=100)
    detector = AnomalyDetector()
    detector.fit(features)
    result = detector.predict(features)

    assert set(result.columns) == {"is_anomaly", "anomaly_score"}
    assert len(result) == 100
    # Most of a tightly-clustered normal batch should not be flagged.
    assert result["is_anomaly"].sum() < 20


def test_extreme_outlier_is_flagged():
    features = _normal_batch(n=100)
    detector = AnomalyDetector()
    detector.fit(features)

    outlier = pd.DataFrame(
        {"temperature": [500.0], "humidity": [55.0], "pressure": [1010.0]}
    )
    result = detector.predict(outlier)

    assert result["is_anomaly"].iloc[0] == True
    assert result["anomaly_score"].iloc[0] > 0