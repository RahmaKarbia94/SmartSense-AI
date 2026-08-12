import importlib
import config


def test_defaults(monkeypatch):
    for var in ("MQTT_HOST", "MQTT_PORT", "MQTT_TOPIC", "DEVICE_ID", "SENSOR_INTERVAL"):
        monkeypatch.delenv(var, raising=False)

    importlib.reload(config)

    assert config.MQTT_HOST == "localhost"
    assert config.MQTT_PORT == 1883
    assert config.DEVICE_ID == "simulator_001"
    assert config.MQTT_TOPIC == "smartsense/devices/simulator_001/telemetry"
    assert config.SENSOR_INTERVAL == 5


def test_env_override(monkeypatch):
    monkeypatch.setenv("MQTT_HOST", "192.168.1.50")
    monkeypatch.setenv("MQTT_PORT", "8883")
    monkeypatch.setenv("SENSOR_INTERVAL", "10")

    importlib.reload(config)

    assert config.MQTT_HOST == "192.168.1.50"
    assert config.MQTT_PORT == 8883
    assert config.SENSOR_INTERVAL == 10