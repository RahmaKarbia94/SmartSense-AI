import logging

from sqlalchemy import text
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def get_health_status(db: Session) -> dict:
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        logger.error("Health check failed: database unreachable: %s", e)
        return {"status": "degraded", "database": "unreachable"}