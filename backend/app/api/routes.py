from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.health_service import get_health_status

router = APIRouter()


@router.get("/")
def read_root() -> dict:
    return {"service": "SmartSense AI Backend", "status": "running"}


@router.get("/health")
def health_check(db: Session = Depends(get_db)) -> dict:
    return get_health_status(db)