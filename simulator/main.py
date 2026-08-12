import time
import json

from config import SENSOR_INTERVAL
from sensor import generate_reading
from mqtt_client import create_client, publish_reading


def main():
    print("SmartSense AI - Virtual IoT Device")
    print("Starting sensor simulation...\n")

    try:
        client = create_client()
    except (ConnectionRefusedError, OSError) as e:
        print(f"Failed to connect to MQTT broker: {e}")
        return

    try:
        while True:
            reading = generate_reading()
            print(json.dumps(reading, indent=2))
            publish_reading(client, reading)
            time.sleep(SENSOR_INTERVAL)
    except KeyboardInterrupt:
        print("\nStopping simulator...")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()