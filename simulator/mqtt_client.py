import json
import paho.mqtt.client as mqtt

from config import BROKER_HOST, BROKER_PORT, MQTT_CLIENT_ID, MQTT_TOPIC


def create_client() -> mqtt.Client:
    client = mqtt.Client(
        client_id=MQTT_CLIENT_ID,
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    )
    client.connect(BROKER_HOST, BROKER_PORT)
    return client


def publish_reading(client: mqtt.Client, reading: dict) -> None:
    payload = json.dumps(reading)
    client.publish(MQTT_TOPIC, payload)