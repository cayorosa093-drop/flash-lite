"""Orquestração do núcleo usada pela CLI e pela interface."""

from __future__ import annotations

from pathlib import Path

from app.core.models import CleanupCandidate, ProcessInfo, StartupEntry, SystemSnapshot
from app.core.scanner.cleanup import CleanupRuleScanner
from app.core.scanner.processes import ProcessScanner
from app.core.scanner.system import SystemScanner
from app.database.sqlite import LocalDatabase, default_data_dir
from app.platforms.factory import get_platform_backend


class FlashLiteService:
    def __init__(
        self,
        database: LocalDatabase | None = None,
        rules_path: Path | None = None,
    ) -> None:
        self.database = database or LocalDatabase()
        self.system_scanner = SystemScanner()
        self.process_scanner = ProcessScanner()
        self.backend = get_platform_backend()
        self.rules_path = rules_path or Path(__file__).parents[1] / "rules" / "windows" / "cleanup.json"

    def scan_system(self, persist: bool = True) -> SystemSnapshot:
        snapshot = self.system_scanner.scan()
        if persist:
            self.database.record_scan(snapshot)
        return snapshot

    def top_processes(self, limit: int = 10) -> list[ProcessInfo]:
        return self.process_scanner.top_by_memory(limit=limit)

    def startup_entries(self) -> list[StartupEntry]:
        return self.backend.startup_entries()

    def cleanup_preview(self) -> list[CleanupCandidate]:
        scanner = CleanupRuleScanner(self.rules_path, current_platform=self._rule_platform())
        return scanner.scan()

    def _rule_platform(self) -> str:
        return "windows" if self.backend.name == "windows" else self.backend.name

    @property
    def state_dir(self) -> Path:
        return default_data_dir()
