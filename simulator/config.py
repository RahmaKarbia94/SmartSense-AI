import os

DEVICE_ID = os.getenv("DEVICE_ID", "simulator_001")
SENSOR_INTERVAL = int(os.getenv("SENSOR_INTERVAL", "5"))

TEMPERATURE_MIN = 18.0
TEMPERATURE_MAX = 35.0
HUMIDITY_MIN = 30.0
HUMIDITY_MAX = 80.0
PRESSURE_MIN = 950.0
PRESSURE_MAX = 1050.0

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", f"smartsense/devices/{DEVICE_ID}/telemetry")
MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID", f"{DEVICE_ID}_publisher")