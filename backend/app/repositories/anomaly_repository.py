from sqlalchemy.orm import Session

from app.models.anomaly import AnomalyResult


def save_anomaly_result(
    db: Session, telemetry_pk: int, is_anomaly: bool, anomaly_score: float
) -> AnomalyResult:
    result = AnomalyResult(
        telemetry_pk=telemetry_pk,
        is_anomaly=is_anomaly,
        anomaly_score=anomaly_score,
    )
    db.add(result)
    db.flush()
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