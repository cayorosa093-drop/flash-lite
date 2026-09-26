"""Banco local pequeno para histórico e auditoria."""

from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from typing import Any


def default_data_dir() -> Path:
    candidates: list[Path] = []
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home()))
        candidates.append(base / "Flash-Lite")
    else:
        candidates.append(
            Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
            / "flash-lite"
        )

    # Ambientes empacotados, sandboxes e execuções de desenvolvimento podem
    # deixar a pasta de dados do usuário indisponível. O fallback continua
    # sendo local, explícito e ignorado pelo controle de versão.
    candidates.append(Path.cwd() / "flash-lite-data")
    for candidate in candidates:
        try:
            candidate.mkdir(parents=True, exist_ok=True)
            return candidate
        except OSError:
            continue
    raise OSError("Não foi possível criar uma pasta local para os dados do Flash-Lite.")


class LocalDatabase:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or (default_data_dir() / "flash-lite.db")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS scans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    collected_at TEXT NOT NULL,
                    health_score INTEGER NOT NULL,
                    payload TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    action_type TEXT NOT NULL,
                    payload TEXT NOT NULL
                );
                """
            )

    def record_scan(self, snapshot: Any) -> int:
        payload = snapshot.to_dict()
        with self._connect() as connection:
            cursor = connection.execute(
                "INSERT INTO scans (collected_at, health_score, payload) VALUES (?, ?, ?)",
                (snapshot.collected_at, snapshot.health_score, json.dumps(payload)),
            )
            return int(cursor.lastrowid)

    def record_action(self, action_type: str, payload: dict[str, Any]) -> int:
        with self._connect() as connection:
            cursor = connection.execute(
                "INSERT INTO actions (action_type, payload) VALUES (?, ?)",
                (action_type, json.dumps(payload, ensure_ascii=False)),
            )
            return int(cursor.lastrowid)

    def recent_scans(self, limit: int = 10) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM scans ORDER BY id DESC LIMIT ?", (max(1, limit),)
            ).fetchall()
        return [dict(row) for row in rows]
