from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.session import Base, get_db
from app.main import app
from app.models.device import Device
from app.models.telemetry import Telemetry
from app.services.anomaly_service import analyze_and_store


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    session = TestingSessionLocal()
    device = Device(device_id="simulator_001")
    session.add(device)
    session.flush()

    for i in range(20):
        session.add(
            Telemetry(
                device_pk=device.id,
                timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
                temperature=20.0 + (i % 5),
                humidity=50.0 + (i % 10),
                pressure=1000.0 + (i % 20),
            )
        )
    session.commit()

    analyze_and_store(session, device.id, "simulator_001", window=20)
    session.close()

    yield TestClient(app)

    app.dependency_overrides.clear()


def test_get_anomalies_success(client):
    response = client.get("/api/v1/devices/simulator_001/anomalies")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 20
    assert set(data[0].keys()) == {"device_id", "timestamp", "is_anomaly", "anomaly_score"}


def test_get_anomalies_unknown_device_404(client):
    response = client.get("/api/v1/devices/unknown_device/anomalies")
    assert response.status_code == 404