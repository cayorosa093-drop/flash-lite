"""Leitura de aplicativos autostart no padrão XDG."""

from __future__ import annotations

import os
from pathlib import Path

from app.core.models import StartupEntry


class LinuxBackend:
    name = "linux"

    def startup_entries(self) -> list[StartupEntry]:
        directories = [
            Path.home() / ".config" / "autostart",
            Path("/etc/xdg/autostart"),
        ]
        entries: list[StartupEntry] = []
        seen: set[str] = set()
        for directory in directories:
            if not directory.is_dir():
                continue
            for desktop_file in sorted(directory.glob("*.desktop")):
                if desktop_file.name in seen:
                    continue
                seen.add(desktop_file.name)
                values = self._read_desktop_file(desktop_file)
                if values.get("Hidden", "false").lower() == "true":
                    continue
                entries.append(
                    StartupEntry(
                        id=f"xdg:{desktop_file}",
                        name=values.get("Name", desktop_file.stem),
                        source=str(desktop_file),
                        command=values.get("Exec", ""),
                        enabled=True,
                    )
                )
        return entries

    @staticmethod
    def _read_desktop_file(path: Path) -> dict[str, str]:
        values: dict[str, str] = {}
        try:
            for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
                if "=" not in line or line.startswith("#"):
                    continue
                key, value = line.split("=", 1)
                values[key.strip()] = value.strip()
        except OSError:
            pass
        return values

