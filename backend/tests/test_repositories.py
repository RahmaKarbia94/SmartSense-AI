import pytest
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import Base
from app.models.device import Device
from app.models.telemetry import Telemetry
from app.repositories.device_repository import get_or_create_device
from app.repositories.telemetry_repository import insert_telemetry
from app.schemas.telemetry import TelemetryReading


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine)
    session = TestSession()
    yield session
    session.close()


def test_get_or_create_device_creates_new(db_session):
    device = get_or_create_device(db_session, "simulator_001")
    assert device.id is not None
    assert device.device_id == "simulator_001"


def test_get_or_create_device_returns_existing(db_session):
    first = get_or_create_device(db_session, "simulator_001")
    db_session.commit()

    second = get_or_create_device(db_session, "simulator_001")

    assert first.id == second.id
    assert db_session.query(Device).count() == 1


def test_insert_telemetry_stores_correct_values(db_session):
    device = get_or_create_device(db_session, "simulator_001")
    db_session.commit()

    reading = TelemetryReading(
        device_id="simulator_001",
        timestamp=datetime.now(timezone.utc),
        temperature=25.34,
        humidity=52.18,
        pressure=1014.27,
    )
    insert_telemetry(db_session, reading, device_pk=device.id)
    db_session.commit()

    stored = db_session.query(Telemetry).first()
    assert stored.device_pk == device.id
    assert stored.temperature == 25.34
    assert stored.humidity == 52.18
    assert stored.pressure == 1014.27


def test_multiple_readings_same_device_single_device_row(db_session):
    device = get_or_create_device(db_session, "simulator_001")
    db_session.commit()

    for _ in range(3):
        reading = TelemetryReading(
            device_id="simulator_001",
            timestamp=datetime.now(timezone.utc),
            temperature=20.0,
            humidity=50.0,
            pressure=1000.0,
        )
        insert_telemetry(db_session, reading, device_pk=device.id)
    db_session.commit()

    assert db_session.query(Device).count() == 1
    assert db_session.query(Telemetry).count() == 3