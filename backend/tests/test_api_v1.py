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

    session.add(
        Telemetry(
            device_pk=device.id,
            timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
            temperature=20.0,
            humidity=50.0,
            pressure=1000.0,
        )
    )
    session.add(
        Telemetry(
            device_pk=device.id,
            timestamp=datetime(2026, 1, 2, tzinfo=timezone.utc),
            temperature=25.0,
            humidity=55.0,
            pressure=1010.0,
        )
    )
    session.commit()
    session.close()

    yield TestClient(app)

    app.dependency_overrides.clear()


def test_list_devices(client):
    response = client.get("/api/v1/devices")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["device_id"] == "simulator_001"
    assert "created_at" in data[0]


def test_get_device_success(client):
    response = client.get("/api/v1/devices/simulator_001")
    assert response.status_code == 200
    assert response.json()["device_id"] == "simulator_001"


def test_get_device_not_found(client):
    response = client.get("/api/v1/devices/unknown_device")
    assert response.status_code == 404


def test_get_device_telemetry_newest_first(client):
    response = client.get("/api/v1/devices/simulator_001/telemetry")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["temperature"] == 25.0
    assert data[1]["temperature"] == 20.0


def test_get_device_telemetry_pagination(client):
    response = client.get("/api/v1/devices/simulator_001/telemetry?limit=1&offset=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["temperature"] == 20.0


def test_get_device_telemetry_unknown_device_404(client):
    response = client.get("/api/v1/devices/unknown_device/telemetry")
    assert response.status_code == 404


def test_get_device_telemetry_invalid_limit_422(client):
    response = client.get("/api/v1/devices/simulator_001/telemetry?limit=0")
    assert response.status_code == 422


def test_get_device_telemetry_invalid_offset_422(client):
    response = client.get("/api/v1/devices/simulator_001/telemetry?offset=-1")
    assert response.status_code == 422


def test_latest_telemetry(client):
    response = client.get("/api/v1/telemetry/latest")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["device_id"] == "simulator_001"
    assert data[0]["temperature"] == 25.0