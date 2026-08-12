import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("SmartSense AI backend starting up...")
    yield
    logger.info("SmartSense AI backend shutting down...")


app = FastAPI(title="SmartSense AI Backend", lifespan=lifespan)
app.include_router(router)