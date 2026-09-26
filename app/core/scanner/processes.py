"""Leitura dos processos em execução."""

from __future__ import annotations

import psutil

from app.core.models import ProcessInfo


class ProcessScanner:
    def top_by_memory(self, limit: int = 10) -> list[ProcessInfo]:
        processes: list[ProcessInfo] = []
        for process in psutil.process_iter(["pid", "name", "status", "username"]):
            try:
                info = process.info
                memory_bytes = process.memory_info().rss
                processes.append(
                    ProcessInfo(
                        pid=int(info.get("pid") or process.pid),
                        name=str(info.get("name") or "Processo desconhecido"),
                        memory_bytes=memory_bytes,
                        cpu_percent=process.cpu_percent(interval=None),
                        status=str(info.get("status") or "unknown"),
                        username=info.get("username"),
                    )
                )
            except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
                continue

        processes.sort(key=lambda item: item.memory_bytes, reverse=True)
        return processes[: max(0, limit)]

