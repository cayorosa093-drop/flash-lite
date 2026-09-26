"""Coleta de métricas básicas sem alterar o sistema."""

from __future__ import annotations

import datetime as dt
import os
import platform
import shutil

import psutil

from app.core.models import SystemSnapshot


def _distribution_name() -> str | None:
    if platform.system() != "Linux":
        return None
    try:
        return platform.freedesktop_os_release().get("PRETTY_NAME")
    except (AttributeError, OSError):
        return None


class SystemScanner:
    """Scanner básico usado pelo dashboard inicial."""

    def scan(self) -> SystemSnapshot:
        memory = psutil.virtual_memory()
        disk = shutil.disk_usage(os.path.abspath(os.sep))
        disk_free_percent = (disk.free / disk.total * 100) if disk.total else 0.0

        return SystemSnapshot(
            platform=platform.system(),
            distribution=_distribution_name(),
            cpu_percent=psutil.cpu_percent(interval=0.15),
            cpu_count=psutil.cpu_count(logical=True) or 1,
            memory_total_bytes=memory.total,
            memory_available_bytes=memory.available,
            memory_used_bytes=memory.used,
            memory_percent=memory.percent,
            disk_total_bytes=disk.total,
            disk_free_bytes=disk.free,
            disk_used_bytes=disk.used,
            disk_free_percent=disk_free_percent,
            collected_at=dt.datetime.now(dt.timezone.utc).isoformat(),
        )

