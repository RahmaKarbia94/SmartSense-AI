import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import pandas as pd
import pytest

from pipeline import detect_anomalies
from model import InsufficientDataError


def _fake_telemetry(n=50, device_id="simulator_001"):
    rng = np.random.default_rng(42)
    return pd.DataFrame(
        {
            "device_id": [device_id] * n,
            "timestamp": pd.date_range("2026-01-01", periods=n, freq="5s"),
            "temperature": rng.normal(25, 2, n),
            "humidity": rng.normal(55, 5, n),
            "pressure": rng.normal(1010, 10, n),
        }
    )


def test_detect_anomalies_returns_expected_columns():
    with patch("pipeline.load_telemetry", return_value=_fake_telemetry()):
        result = detect_anomalies("simulator_001")

    assert list(result.columns) == ["device_id", "timestamp", "is_anomaly", "anomaly_score"]
    assert len(result) == 50
    assert (result["device_id"] == "simulator_001").all()


def test_detect_anomalies_insufficient_data_raises():
    with patch("pipeline.load_telemetry", return_value=_fake_telemetry(n=3)):
        with pytest.raises(InsufficientDataError):
            detect_anomalies("simulator_001")