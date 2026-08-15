import os

from dotenv import load_dotenv

load_dotenv()

APP_ENV = os.getenv("APP_ENV", "development")

DATABASE_URL = os.getenv("DATABASE_URL", "")

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "smartsense/devices/+/telemetry")
MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID", "smartsense_backend_subscriber")