import json
from unittest.mock import MagicMock

import paho.mqtt.client as mqtt
import mqtt_client


def test_publish_reading_success():
    client = MagicMock()
    client.publish.return_value.rc = mqtt.MQTT_ERR_SUCCESS

    reading = {"device_id": "simulator_001", "temperature": 25.0}
    mqtt_client.publish_reading(client, reading)

    client.publish.assert_called_once()
    args, kwargs = client.publish.call_args
    assert args[0] == mqtt_client.MQTT_TOPIC
    assert json.loads(args[1]) == reading
    assert kwargs["qos"] == mqtt_client.QOS_LEVEL


def test_publish_reading_failure_logs_error(caplog):
    client = MagicMock()
    client.publish.return_value.rc = mqtt.MQTT_ERR_NO_CONN

    with caplog.at_level("ERROR"):
        mqtt_client.publish_reading(client, {"device_id": "simulator_001"})

    assert "Failed to publish telemetry" in caplog.text


def test_publish_reading_serialization_error(caplog):
    client = MagicMock()

    with caplog.at_level("ERROR"):
        mqtt_client.publish_reading(client, {"bad": object()})

    client.publish.assert_not_called()
    assert "Failed to serialize telemetry" in caplog.text