from pathlib import Path

from app.core.models import RiskLevel
from app.core.scanner.cleanup import CleanupRuleScanner


def test_cleanup_rule_finds_only_files_inside_root(tmp_path: Path) -> None:
    cache = tmp_path / "cache"
    cache.mkdir()
    target = cache / "old.tmp"
    target.write_bytes(b"cache")
    (cache / "nested").mkdir()
    (cache / "nested" / "nested.tmp").write_bytes(b"nested")

    rules = tmp_path / "rules.json"
    rules.write_text(
        '{"rules": [{"id": "test-cache", "platforms": ["linux"], '
        f'"category": "Cache", "path": "{cache}", "patterns": ["**/*.tmp"], '
        '"risk": "very_low", "recreatable": true, "automatic_selection": true}]}',
        encoding="utf-8",
    )

    candidates = CleanupRuleScanner(rules, current_platform="linux").scan()

    assert {Path(item.path).name for item in candidates} == {"old.tmp", "nested.tmp"}
    assert all(item.risk == RiskLevel.VERY_LOW for item in candidates)
    assert all(item.selected for item in candidates)

