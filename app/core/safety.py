"""Validações de segurança antes de qualquer operação em arquivos."""

from __future__ import annotations

from pathlib import Path

from app.core.models import CleanupCandidate, RiskLevel

_PROTECTED_PARTS = {
    "windows",
    "system32",
    "winsxs",
    "installer",
    "program files",
    "program files (x86)",
}


class SafetyEngine:
    def validate_candidate(self, candidate: CleanupCandidate) -> tuple[bool, str | None]:
        path = Path(candidate.path)
        root = Path(candidate.root_path)
        try:
            resolved_path = path.resolve(strict=True)
            resolved_root = root.resolve(strict=True)
        except (OSError, RuntimeError):
            return False, "O arquivo não está mais disponível."

        if path.is_symlink():
            return False, "Links simbólicos não entram na limpeza automática."
        if not resolved_path.is_relative_to(resolved_root):
            return False, "O arquivo está fora da pasta aprovada pela regra."
        if any(part.casefold() in _PROTECTED_PARTS for part in resolved_path.parts):
            return False, "O caminho contém uma área protegida do sistema."
        if not resolved_path.is_file():
            return False, "O item não é um arquivo comum."
        if candidate.risk == RiskLevel.HIGH:
            return False, "Itens de alto risco nunca são selecionados automaticamente."
        return True, None

    def approved(self, candidate: CleanupCandidate) -> bool:
        valid, _ = self.validate_candidate(candidate)
        return valid

