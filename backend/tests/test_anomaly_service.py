from datetime import datetime, timezone

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.session import Base
from app.models.device import Device
from app.models.telemetry import Telemetry
from app.models.anomaly import AnomalyResult
from app.services.anomaly_service import analyze_and_store, get_anomalies


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine)
    session = TestSession()
    yield session
    session.close()


def _seed_readings(db, device_id: str, count: int):
    device = Device(device_id=device_id)
    db.add(device)
    db.flush()

    for i in range(count):
        db.add(
            Telemetry(
                device_pk=device.id,
                timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
                temperature=20.0 + (i % 5),
                humidity=50.0 + (i % 10),
                pressure=1000.0 + (i % 20),
            )
        )
    db.commit()
    return device


def test_analyze_and_store_persists_results(db_session):
    device = _seed_readings(db_session, "simulator_001", count=20)

    analyze_and_store(db_session, device.id, "simulator_001", window=20)

    stored = db_session.query(AnomalyResult).all()
    assert len(stored) == 20


def test_analyze_and_store_insufficient_data_skips_silently(db_session):
    device = _seed_readings(db_session, "simulator_001", count=3)

    analyze_and_store(db_session, device.id, "simulator_001", window=20)

    stored = db_session.query(AnomalyResult).all()
    assert len(stored) == 0


def test_analyze_and_store_skips_already_analyzed(db_session):
    device = _seed_readings(db_session, "simulator_001", count=20)

    analyze_and_store(db_session, device.id, "simulator_001", window=20)
    analyze_and_store(db_session, device.id, "simulator_001", window=20)

    stored = db_session.query(AnomalyResult).all()
    assert len(stored) == 20


def test_get_anomalies_returns_results_for_device(db_session):
    device = _seed_readings(db_session, "simulator_001", count=20)
    analyze_and_store(db_session, device.id, "simulator_001", window=20)

    results = get_anomalies(db_session, "simulator_001")

    assert results is not None
    assert len(results) == 20
    assert all(r.device_id == "simulator_001" for r in results)


def test_get_anomalies_unknown_device_returns_none(db_session):
    results = get_anomalies(db_session, "unknown_device")
    assert results is None
def test_analyze_and_store_handles_db_failure_when_fetching_telemetry(db_session, monkeypatch):
    from app.services import anomaly_service

    def broken_fetch(*args, **kwargs):
        raise Exception("connection refused")

    monkeypatch.setattr(anomaly_service, "get_telemetry_for_device", broken_fetch)

    # Should not raise.
    analyze_and_store(db_session, device_pk=1, device_id="simulator_001", window=20)

def test_save_anomaly_result_handles_concurrent_duplicate_insert(db_session):
    from app.repositories.anomaly_repository import save_anomaly_result

    first = save_anomaly_result(db_session, telemetry_pk=1, is_anomaly=False, anomaly_score=-0.05)
    db_session.commit()
    assert first is not None

    # Simulate a second, concurrent analysis pass landing on the same
    # telemetry row (e.g. two overlapping windows racing each other).
    second = save_anomaly_result(db_session, telemetry_pk=1, is_anomaly=True, anomaly_score=0.5)
    db_session.commit()

    assert second is None
    stored = db_session.query(AnomalyResult).filter_by(telemetry_pk=1).all()
    assert len(stored) == 1
