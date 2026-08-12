import time
import json
import logging

from config import SENSOR_INTERVAL
from sensor import generate_reading
from mqtt_client import create_client, publish_reading, stop_client

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def main():
    logger.info("SmartSense AI - Virtual IoT Device")
    logger.info("Starting sensor simulation...")

    try:
        client = create_client()
    except (ConnectionRefusedError, OSError) as e:
        logger.error("Failed to connect to MQTT broker: %s", e)
        return

    try:
        while True:
            reading = generate_reading()
            print(json.dumps(reading, indent=2))
            publish_reading(client, reading)
            time.sleep(SENSOR_INTERVAL)
    except KeyboardInterrupt:
        logger.info("Stopping simulator...")
    finally:
        stop_client(client)
        logger.info("Simulator shut down cleanly.")


if __name__ == "__main__":
    main()