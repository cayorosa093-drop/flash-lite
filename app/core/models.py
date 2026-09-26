"""Modelos compartilhados pelo núcleo e pelos backends."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


class RiskLevel(StrEnum):
    """Nível de risco de uma ação de limpeza."""

    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    @property
    def label(self) -> str:
        return {
            RiskLevel.VERY_LOW: "Muito baixo",
            RiskLevel.LOW: "Baixo",
            RiskLevel.MEDIUM: "Revisar",
            RiskLevel.HIGH: "Não recomendado",
        }[self]


@dataclass(frozen=True)
class SystemSnapshot:
    platform: str
    distribution: str | None
    cpu_percent: float
    cpu_count: int
    memory_total_bytes: int
    memory_available_bytes: int
    memory_used_bytes: int
    memory_percent: float
    disk_total_bytes: int
    disk_free_bytes: int
    disk_used_bytes: int
    disk_free_percent: float
    collected_at: str

    @property
    def health_score(self) -> int:
        """Estimativa simples e explicável; não substitui um diagnóstico completo."""

        score = 100
        if self.memory_percent >= 90:
            score -= 25
        elif self.memory_percent >= 80:
            score -= 15
        elif self.memory_percent >= 70:
            score -= 7

        if self.disk_free_percent < 5:
            score -= 30
        elif self.disk_free_percent < 10:
            score -= 20
        elif self.disk_free_percent < 15:
            score -= 10

        if self.cpu_percent >= 95:
            score -= 10
        return max(0, min(100, score))

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["health_score"] = self.health_score
        return result


@dataclass(frozen=True)
class ProcessInfo:
    pid: int
    name: str
    memory_bytes: int
    cpu_percent: float
    status: str
    username: str | None = None

    @property
    def memory_mb(self) -> float:
        return self.memory_bytes / (1024 * 1024)

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["memory_mb"] = round(self.memory_mb, 2)
        return result


@dataclass(frozen=True)
class StartupEntry:
    id: str
    name: str
    source: str
    command: str
    enabled: bool = True
    reversible: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CleanupCandidate:
    rule_id: str
    category: str
    path: str
    root_path: str
    size_bytes: int
    risk: RiskLevel
    explanation: str
    recreatable: bool
    selected: bool
    can_restore: bool = True
    blocked_reason: str | None = None

    @property
    def size_mb(self) -> float:
        return self.size_bytes / (1024 * 1024)

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["risk"] = self.risk.value
        result["size_mb"] = round(self.size_mb, 2)
        return result

