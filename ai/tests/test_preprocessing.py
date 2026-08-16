import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import pandas as pd
import pytest

from preprocessing import preprocess


def test_preprocess_selects_only_feature_columns():
    df = pd.DataFrame(
        {
            "device_id": ["simulator_001"] * 3,
            "timestamp": pd.date_range("2026-01-01", periods=3, freq="5s"),
            "temperature": [20.0, 21.0, 22.0],
            "humidity": [50.0, 51.0, 52.0],
            "pressure": [1000.0, 1001.0, 1002.0],
        }
    )
    result = preprocess(df)
    assert list(result.columns) == ["temperature", "humidity", "pressure"]
    assert len(result) == 3


def test_preprocess_drops_missing_values():
    df = pd.DataFrame(
        {
            "temperature": [20.0, np.nan, 22.0],
            "humidity": [50.0, 51.0, 52.0],
            "pressure": [1000.0, 1001.0, 1002.0],
        }
    )
    result = preprocess(df)
    assert len(result) == 2


def test_preprocess_drops_non_numeric_values():
    df = pd.DataFrame(
        {
            "temperature": [20.0, "not_a_number", 22.0],
            "humidity": [50.0, 51.0, 52.0],
            "pressure": [1000.0, 1001.0, 1002.0],
        }
    )
    result = preprocess(df)
    assert len(result) == 2


def test_preprocess_empty_dataframe_returns_empty():
    df = pd.DataFrame(columns=["device_id", "timestamp", "temperature", "humidity", "pressure"])
    result = preprocess(df)
    assert result.empty


def test_preprocess_missing_columns_raises():
    df = pd.DataFrame({"temperature": [20.0]})
    with pytest.raises(ValueError):
        preprocess(df)