from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.anomaly import AnomalyResult


def save_anomaly_result(
    db: Session, telemetry_pk: int, is_anomaly: bool, anomaly_score: float
) -> AnomalyResult | None:
    """
    Inserts an anomaly result, tolerating a concurrent insert for the
    same telemetry_pk (e.g. two overlapping analysis windows racing
    each other). Uses a SAVEPOINT so only this row's failed insert is
    rolled back, not the whole in-progress transaction/batch.

    Returns the created row, or None if another insert for the same
    telemetry_pk won the race.
    """
    result = AnomalyResult(
        telemetry_pk=telemetry_pk,
        is_anomaly=is_anomaly,
        anomaly_score=anomaly_score,
    )
    try:
        with db.begin_nested():
            db.add(result)
            db.flush()
    except IntegrityError:
        return None
    return result

def get_anomalies_for_device(db: Session, device_pk: int):
    from app.models.telemetry import Telemetry

    return (
        db.query(AnomalyResult, Telemetry.timestamp)
        .join(Telemetry, AnomalyResult.telemetry_pk == Telemetry.id)
        .filter(Telemetry.device_pk == device_pk)
        .order_by(Telemetry.timestamp.desc())
        .all()
    )
def get_already_analyzed_telemetry_ids(db: Session, telemetry_ids: list[int]) -> set[int]:
    if not telemetry_ids:
        return set()

    rows = (
        db.query(AnomalyResult.telemetry_pk)
        .filter(AnomalyResult.telemetry_pk.in_(telemetry_ids))
        .all()
    )
    return {row[0] for row in rows}