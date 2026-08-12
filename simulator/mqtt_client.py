import json
import logging

import paho.mqtt.client as mqtt

from config import MQTT_HOST, MQTT_PORT, MQTT_CLIENT_ID, MQTT_TOPIC

logger = logging.getLogger(__name__)

QOS_LEVEL = 1  # at-least-once delivery


def _on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        logger.info("Connected to MQTT broker at %s:%s", MQTT_HOST, MQTT_PORT)
    else:
        logger.error("MQTT connection failed: %s", reason_code)


def _on_disconnect(client, userdata, disconnect_flags, reason_code, properties=None):
    if reason_code == 0:
        logger.info("Disconnected from MQTT broker")
    else:
        logger.warning("Unexpected MQTT disconnect (%s) — attempting reconnect...", reason_code)


def create_client() -> mqtt.Client:
    client = mqtt.Client(
        client_id=MQTT_CLIENT_ID,
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    )
    client.on_connect = _on_connect
    client.on_disconnect = _on_disconnect
    client.reconnect_delay_set(min_delay=1, max_delay=30)

    client.connect(MQTT_HOST, MQTT_PORT)
    client.loop_start()
    return client


def publish_reading(client: mqtt.Client, reading: dict) -> None:
    try:
        payload = json.dumps(reading)
    except (TypeError, ValueError) as e:
        logger.error("Failed to serialize telemetry to JSON: %s", e)
        return

    result = client.publish(MQTT_TOPIC, payload, qos=QOS_LEVEL)
    if result.rc != mqtt.MQTT_ERR_SUCCESS:
        logger.error("Failed to publish telemetry (rc=%s)", result.rc)

    else:
        logger.info("Published telemetry to %s", MQTT_TOPIC)


def stop_client(client: mqtt.Client) -> None:
    client.loop_stop()
    client.disconnect()