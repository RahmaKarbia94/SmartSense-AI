from unittest.mock import MagicMock

from app.services.health_service import get_health_status


def test_health_status_ok_when_db_reachable():
    db = MagicMock()
    db.execute.return_value = None

    result = get_health_status(db)

    assert result == {"status": "ok", "database": "connected"}


def test_health_status_degraded_when_db_unreachable():
    db = MagicMock()
    db.execute.side_effect = Exception("connection refused")

    result = get_health_status(db)

    assert result == {"status": "degraded", "database": "unreachable"}