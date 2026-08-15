import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.api.v1.devices import router as devices_router
from app.api.v1.telemetry import router as telemetry_router
from app.services.mqtt_consumer import create_consumer, stop_consumer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("SmartSense AI backend starting up...")
    mqtt_client = create_consumer()
    app.state.mqtt_client = mqtt_client

    yield

    logger.info("SmartSense AI backend shutting down...")
    stop_consumer(mqtt_client)


app = FastAPI(title="SmartSense AI Backend", lifespan=lifespan)
app.include_router(router)
app.include_router(devices_router)
app.include_router(telemetry_router)