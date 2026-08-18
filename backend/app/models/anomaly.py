from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class AnomalyResult(Base):
    __tablename__ = "anomaly_results"

    id = Column(Integer, primary_key=True)
    telemetry_pk = Column(
        Integer, ForeignKey("telemetry.id"), nullable=False, unique=True, index=True
    )
    is_anomaly = Column(Boolean, nullable=False)
    anomaly_score = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    telemetry = relationship("Telemetry")