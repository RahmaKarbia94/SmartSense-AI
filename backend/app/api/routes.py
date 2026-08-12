from fastapi import APIRouter

from app.services.health_service import get_health_status

router = APIRouter()


@router.get("/")
def read_root() -> dict:
    return {"service": "SmartSense AI Backend", "status": "running"}


@router.get("/health")
def health_check() -> dict:
    return get_health_status()