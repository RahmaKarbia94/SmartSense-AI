from sqlalchemy.orm import Session

from app.models.device import Device


def get_or_create_device(db: Session, device_id: str) -> Device:
    device = db.query(Device).filter(Device.device_id == device_id).first()
    if device is not None:
        return device

    device = Device(device_id=device_id)
    db.add(device)
    db.flush()
    return device

def list_devices(db: Session):
    return db.query(Device).order_by(Device.device_id).all()


def get_device_by_device_id(db: Session, device_id: str):
    return db.query(Device).filter(Device.device_id == device_id).first()