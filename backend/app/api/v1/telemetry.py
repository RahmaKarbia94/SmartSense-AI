from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.telemetry_response import TelemetryResponse
from app.services.telemetry_query_service import get_latest_telemetry

router = APIRouter(prefix="/api/v1/telemetry", tags=["telemetry"])


@router.get("/latest", response_model=list[TelemetryResponse])
def get_latest_telemetry_endpoint(db: Session = Depends(get_db)):
    return get_latest_telemetry(db)