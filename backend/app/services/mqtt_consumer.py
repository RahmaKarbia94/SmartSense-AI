import json
import logging

import paho.mqtt.client as mqtt
from pydantic import ValidationError

from app.config import MQTT_HOST, MQTT_PORT, MQTT_CLIENT_ID, MQTT_TOPIC
from app.schemas.telemetry import TelemetryReading
from app.services.telemetry_service import process_telemetry

logger = logging.getLogger(__name__)


def _on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        logger.info("MQTT consumer connected to %s:%s", MQTT_HOST, MQTT_PORT)
        client.subscribe(MQTT_TOPIC)
        logger.info("Subscribed to topic: %s", MQTT_TOPIC)
    else:
        logger.error("MQTT consumer connection failed: %s", reason_code)


def _on_disconnect(client, userdata, disconnect_flags, reason_code, properties=None):
    if reason_code == 0:
        logger.info("MQTT consumer disconnected")
    else:
        logger.warning("MQTT consumer unexpected disconnect (%s) - attempting reconnect...", reason_code)


def _on_message(client, userdata, message):
    try:
        raw = message.payload.decode("utf-8")
    except UnicodeDecodeError as e:
        logger.error("Failed to decode MQTT payload: %s", e)
        return

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        logger.error("Invalid JSON on topic %s: %s", message.topic, e)
        return

    if not isinstance(data, dict):
        logger.error(
            "Telemetry payload on topic %s is not a JSON object: %s",
            message.topic, type(data).__name__,
        )
        return

    try:
        reading = TelemetryReading(**data)
    except ValidationError as e:
        logger.error("Invalid telemetry payload on topic %s: %s", message.topic, e)
        return
    
    process_telemetry(reading)


def create_consumer() -> mqtt.Client:
    client = mqtt.Client(
        client_id=MQTT_CLIENT_ID,
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    )
    client.on_connect = _on_connect
    client.on_disconnect = _on_disconnect
    client.on_message = _on_message
    client.reconnect_delay_set(min_delay=1, max_delay=30)

    client.connect(MQTT_HOST, MQTT_PORT)
    client.loop_start()
    return client


def stop_consumer(client: mqtt.Client) -> None:
    client.loop_stop()
    client.disconnect()