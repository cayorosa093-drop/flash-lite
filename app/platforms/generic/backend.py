"""Backend neutro e somente leitura."""

from __future__ import annotations

from app.core.models import StartupEntry


class GenericBackend:
    name = "generic"

    def startup_entries(self) -> list[StartupEntry]:
        return []

