"""Contrato mínimo compartilhado pelos backends de plataforma."""

from __future__ import annotations

from typing import Protocol

from app.core.models import StartupEntry


class PlatformBackend(Protocol):
    name: str

    def startup_entries(self) -> list[StartupEntry]:
        """Retorna itens de inicialização sem alterá-los."""

