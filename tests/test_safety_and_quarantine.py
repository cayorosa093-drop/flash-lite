from pathlib import Path

import pytest

from app.core.cleaner import QuarantineCleaner
from app.core.models import CleanupCandidate, RiskLevel
from app.core.safety import SafetyEngine


def _candidate(path: Path, root: Path, selected: bool = True) -> CleanupCandidate:
    return CleanupCandidate(
        rule_id="test",
        category="Teste",
        path=str(path),
        root_path=str(root),
        size_bytes=path.stat().st_size,
        risk=RiskLevel.VERY_LOW,
        explanation="Arquivo recriável de teste.",
        recreatable=True,
        selected=selected,
    )


def test_quarantine_requires_explicit_confirmation(tmp_path: Path) -> None:
    root = tmp_path / "cache"
    root.mkdir()
    file_path = root / "item.tmp"
    file_path.write_text("temporary", encoding="utf-8")
    cleaner = QuarantineCleaner(tmp_path / "state")

    with pytest.raises(ValueError):
        cleaner.clean([_candidate(file_path, root)])


def test_quarantine_can_restore_file(tmp_path: Path) -> None:
    root = tmp_path / "cache"
    root.mkdir()
    file_path = root / "item.tmp"
    file_path.write_text("temporary", encoding="utf-8")
    cleaner = QuarantineCleaner(tmp_path / "state")

    moved = cleaner.clean([_candidate(file_path, root)], confirm=True)

    assert len(moved) == 1
    assert not file_path.exists()
    assert cleaner.restore(moved[0]["token"])
    assert file_path.read_text(encoding="utf-8") == "temporary"


def test_safety_rejects_protected_path(tmp_path: Path) -> None:
    root = tmp_path / "Windows"
    root.mkdir()
    file_path = root / "system.dll"
    file_path.write_text("protected", encoding="utf-8")

    valid, reason = SafetyEngine().validate_candidate(_candidate(file_path, root))

    assert not valid
    assert reason is not None

