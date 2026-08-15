from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.device import DeviceResponse
from app.schemas.telemetry_response import TelemetryResponse
from app.services.device_service import get_all_devices, get_device
from app.services.telemetry_query_service import get_device_telemetry

router = APIRouter(prefix="/api/v1/devices", tags=["devices"])


@router.get("", response_model=list[DeviceResponse])
def list_devices_endpoint(db: Session = Depends(get_db)):
    return get_all_devices(db)


@router.get("/{device_id}", response_model=DeviceResponse)
def get_device_endpoint(device_id: str, db: Session = Depends(get_db)):
    device = get_device(db, device_id)
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.get("/{device_id}/telemetry", response_model=list[TelemetryResponse])
def get_device_telemetry_endpoint(
    device_id: str,
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    readings = get_device_telemetry(db, device_id, limit, offset)
    if readings is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return readings