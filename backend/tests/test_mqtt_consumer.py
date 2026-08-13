from unittest.mock import MagicMock

from app.services import mqtt_consumer


def _make_message(payload: bytes, topic: str = "smartsense/devices/simulator_001/telemetry"):
    message = MagicMock()
    message.payload = payload
    message.topic = topic
    return message


def test_on_message_valid_payload_calls_service(monkeypatch):
    received = []
    monkeypatch.setattr(
        mqtt_consumer, "process_telemetry", lambda reading: received.append(reading)
    )

    payload = (
        b'{"device_id": "simulator_001", "timestamp": "2026-08-12T23:00:00+00:00", '
        b'"temperature": 25.34, "humidity": 52.18, "pressure": 1014.27}'
    )
    mqtt_consumer._on_message(MagicMock(), None, _make_message(payload))

    assert len(received) == 1
    assert received[0].device_id == "simulator_001"


def test_on_message_invalid_json_does_not_call_service(monkeypatch):
    received = []
    monkeypatch.setattr(
        mqtt_consumer, "process_telemetry", lambda reading: received.append(reading)
    )

    mqtt_consumer._on_message(MagicMock(), None, _make_message(b"not valid json"))

    assert received == []


def test_on_message_missing_field_does_not_call_service(monkeypatch):
    received = []
    monkeypatch.setattr(
        mqtt_consumer, "process_telemetry", lambda reading: received.append(reading)
    )

    payload = b'{"device_id": "simulator_001", "temperature": 25.34}'
    mqtt_consumer._on_message(MagicMock(), None, _make_message(payload))

    assert received == []