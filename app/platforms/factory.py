"""Seleção do backend sem espalhar verificações de sistema pelo app."""

from __future__ import annotations

import platform

from app.platforms.base import PlatformBackend


def get_platform_backend() -> PlatformBackend:
    system = platform.system()
    if system == "Windows":
        from app.platforms.windows.backend import WindowsBackend

        return WindowsBackend()
    if system == "Linux":
        from app.platforms.linux.backend import LinuxBackend

        return LinuxBackend()

    from app.platforms.generic.backend import GenericBackend

    return GenericBackend()

