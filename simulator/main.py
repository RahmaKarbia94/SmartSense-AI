import paho.mqtt.client as mqttgit rev-parse --show-toplevel
import time
import json

from config import SENSOR_INTERVAL
from sensor import generate_reading


def main():
    print("SmartSense AI - Virtual IoT Device")
    print("Starting sensor simulation...\n")

    while True:
        reading = generate_reading()

        print(json.dumps(reading, indent=2))

        time.sleep(SENSOR_INTERVAL)


if __name__ == "__main__":
    main()