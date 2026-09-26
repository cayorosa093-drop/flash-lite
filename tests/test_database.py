from pathlib import Path

from app.database.sqlite import LocalDatabase
from app.core.scanner.system import SystemScanner


def test_database_records_scan(tmp_path: Path) -> None:
    database = LocalDatabase(tmp_path / "flash-lite.db")
    snapshot = SystemScanner().scan()

    scan_id = database.record_scan(snapshot)

    assert scan_id > 0
    scans = database.recent_scans()
    assert scans[0]["health_score"] == snapshot.health_score

