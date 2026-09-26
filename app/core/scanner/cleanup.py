"""Scanner orientado por regras para gerar prévias de limpeza."""

from __future__ import annotations

import json
import os
import platform
import re
from pathlib import Path
from typing import Any

from app.core.models import CleanupCandidate, RiskLevel

_WINDOWS_ENV = re.compile(r"%([^%]+)%")


def expand_path(value: str) -> Path:
    """Expande variáveis Unix e Windows sem executar nenhum comando."""

    expanded = os.path.expandvars(os.path.expanduser(value))

    def replace_windows_var(match: re.Match[str]) -> str:
        return os.environ.get(match.group(1), match.group(0))

    expanded = _WINDOWS_ENV.sub(replace_windows_var, expanded)
    return Path(expanded)


class CleanupRuleScanner:
    def __init__(self, rules_path: Path, current_platform: str | None = None) -> None:
        self.rules_path = rules_path
        self.current_platform = (current_platform or platform.system()).lower()

    def _load_rules(self) -> list[dict[str, Any]]:
        document = json.loads(self.rules_path.read_text(encoding="utf-8"))
        rules = document.get("rules", [])
        if not isinstance(rules, list):
            raise ValueError("O arquivo de regras precisa conter uma lista em 'rules'.")
        return [rule for rule in rules if isinstance(rule, dict)]

    def scan(self, max_files_per_rule: int = 2_000) -> list[CleanupCandidate]:
        candidates: list[CleanupCandidate] = []
        for rule in self._load_rules():
            platforms = {str(item).lower() for item in rule.get("platforms", [])}
            if platforms and self.current_platform not in platforms:
                continue

            root = expand_path(str(rule.get("path", "")))
            if not root.exists() or not root.is_dir():
                continue

            try:
                risk = RiskLevel(str(rule.get("risk", RiskLevel.HIGH)))
            except ValueError:
                # Uma regra inválida não pode virar uma ação de limpeza por
                # acidente; ela é ignorada até ser corrigida/revisada.
                continue
            patterns = rule.get("patterns", ["*"])
            if not isinstance(patterns, list):
                continue

            seen: set[Path] = set()
            for pattern in patterns:
                for path in root.glob(str(pattern)):
                    if len(seen) >= max_files_per_rule:
                        break
                    try:
                        resolved = path.resolve(strict=True)
                        if resolved in seen or path.is_symlink() or not path.is_file():
                            continue
                        if not resolved.is_relative_to(root.resolve()):
                            continue
                        size = path.stat().st_size
                    except (OSError, RuntimeError, ValueError):
                        continue

                    seen.add(resolved)
                    candidates.append(
                        CleanupCandidate(
                            rule_id=str(rule.get("id", "unknown")),
                            category=str(rule.get("category", "Item analisado")),
                            path=str(resolved),
                            root_path=str(root.resolve()),
                            size_bytes=size,
                            risk=risk,
                            explanation=str(
                                rule.get(
                                    "explanation",
                                    "Este item foi encontrado por uma regra conhecida.",
                                )
                            ),
                            recreatable=bool(rule.get("recreatable", False)),
                            selected=bool(rule.get("automatic_selection", False))
                            and risk in {RiskLevel.VERY_LOW, RiskLevel.LOW},
                        )
                    )
        return candidates
