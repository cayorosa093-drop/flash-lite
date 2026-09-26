"""Leitura dos itens Run do Registro do Windows."""

from __future__ import annotations

from app.core.models import StartupEntry


class WindowsBackend:
    name = "windows"

    def startup_entries(self) -> list[StartupEntry]:
        try:
            import winreg
        except ImportError:
            return []

        entries: list[StartupEntry] = []
        locations = [
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", "HKCU"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run", "HKLM"),
        ]
        for hive, path, label in locations:
            try:
                with winreg.OpenKey(hive, path) as key:
                    index = 0
                    while True:
                        try:
                            name, command, _ = winreg.EnumValue(key, index)
                        except OSError:
                            break
                        entries.append(
                            StartupEntry(
                                id=f"{label}:{name}",
                                name=name,
                                source=f"{label}\\{path}",
                                command=str(command),
                            )
                        )
                        index += 1
            except OSError:
                continue
        return entries

