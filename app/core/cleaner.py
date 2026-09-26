"""Quarentena reversível para ações explicitamente confirmadas."""

from __future__ import annotations

import json
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path

from app.core.models import CleanupCandidate
from app.core.safety import SafetyEngine


class QuarantineCleaner:
    """Move arquivos aprovados para uma quarentena, nunca os apaga diretamente."""

    def __init__(self, state_dir: Path, safety: SafetyEngine | None = None) -> None:
        self.state_dir = state_dir
        self.quarantine_dir = state_dir / "quarantine"
        self.manifest_path = state_dir / "quarantine.json"
        self.safety = safety or SafetyEngine()
        self.quarantine_dir.mkdir(parents=True, exist_ok=True)

    def clean(self, candidates: list[CleanupCandidate], confirm: bool = False) -> list[dict[str, str]]:
        if not confirm:
            raise ValueError("A limpeza exige confirmação explícita do usuário.")

        manifest = self._read_manifest()
        moved: list[dict[str, str]] = []
        for candidate in candidates:
            if not candidate.selected or not self.safety.approved(candidate):
                continue
            source = Path(candidate.path)
            if not source.exists():
                continue
            token = f"{uuid.uuid4().hex}_{source.name}"
            destination = self.quarantine_dir / token
            try:
                shutil.move(str(source), str(destination))
            except OSError:
                continue
            item = {
                "token": token,
                "original_path": str(source),
                "quarantine_path": str(destination),
                "moved_at": datetime.now(timezone.utc).isoformat(),
            }
            manifest.append(item)
            moved.append(item)
        self._write_manifest(manifest)
        return moved

    def restore(self, token: str) -> bool:
        manifest = self._read_manifest()
        for item in manifest:
            if item.get("token") != token:
                continue
            source = Path(item["quarantine_path"])
            destination = Path(item["original_path"])
            if not source.exists() or destination.exists():
                return False
            destination.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.move(str(source), str(destination))
            except OSError:
                return False
            manifest.remove(item)
            self._write_manifest(manifest)
            return True
        return False

    def _read_manifest(self) -> list[dict[str, str]]:
        if not self.manifest_path.exists():
            return []
        try:
            data = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []
        return data if isinstance(data, list) else []

    def _write_manifest(self, manifest: list[dict[str, str]]) -> None:
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
        )

