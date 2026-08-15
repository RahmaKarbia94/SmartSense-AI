from sqlalchemy.orm import Session

from app.repositories.device_repository import list_devices, get_device_by_device_id
from app.schemas.device import DeviceResponse


def get_all_devices(db: Session) -> list[DeviceResponse]:
    devices = list_devices(db)
    return [DeviceResponse.model_validate(d) for d in devices]


def get_device(db: Session, device_id: str) -> DeviceResponse | None:
    device = get_device_by_device_id(db, device_id)
    if device is None:
        return None
    return DeviceResponse.model_validate(device)