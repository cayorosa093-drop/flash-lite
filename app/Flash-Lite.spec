# -*- mode: python ; coding: utf-8 -*-
"""Build one-folder do Flash-Lite para Windows."""

from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files


APP_DIR = Path(SPECPATH)
PROJECT_DIR = APP_DIR.parent

datas = [
    (str(APP_DIR / "rules"), "app/rules"),
]
datas += collect_data_files("PySide6")

a = Analysis(
    [str(PROJECT_DIR / "main.py")],
    pathex=[str(PROJECT_DIR)],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    name="Flash-Lite",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    exclude_binaries=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="Flash-Lite",
)
