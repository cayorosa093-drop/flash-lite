@echo off
setlocal EnableExtensions

rem Build do instalador Windows do Flash-Lite.
rem Este arquivo deve ser executado em um computador Windows.

set "APP_DIR=%~dp0"
set "PROJECT_DIR=%APP_DIR%.."
set "VENV_DIR=%APP_DIR%.venv-build"

if not exist "%PROJECT_DIR%\main.py" (
    echo ERRO: main.py nao foi encontrado em "%PROJECT_DIR%".
    exit /b 1
)

where py >nul 2>nul
if errorlevel 1 (
    echo ERRO: instale o Python 3.12+ pelo site https://www.python.org/downloads/windows/
    exit /b 1
)

py -3 -m venv "%VENV_DIR%"
if errorlevel 1 (
    echo ERRO: Python 3.12 ou superior nao esta instalado.
    echo Instale o Python 3.12+ e marque a opcao de adicionar o Python ao PATH.
    exit /b 1
)

call "%VENV_DIR%\Scripts\activate.bat"
python -m pip install --upgrade pip
if errorlevel 1 exit /b 1

python -m pip install -r "%APP_DIR%requirements-windows.txt"
if errorlevel 1 exit /b 1

cd /d "%PROJECT_DIR%"
python -m PyInstaller "%APP_DIR%Flash-Lite.spec" --noconfirm --clean --distpath "%APP_DIR%dist" --workpath "%APP_DIR%build"
if errorlevel 1 exit /b 1

set "ISCC_EXE="
where ISCC >nul 2>nul
if not errorlevel 1 set "ISCC_EXE=ISCC"
if not defined ISCC_EXE if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" set "ISCC_EXE=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if not defined ISCC_EXE if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" set "ISCC_EXE=%ProgramFiles%\Inno Setup 6\ISCC.exe"

if not defined ISCC_EXE (
    echo.
    echo Aplicativo criado em:
    echo   %APP_DIR%dist\Flash-Lite\Flash-Lite.exe
    echo.
    echo Inno Setup nao foi encontrado. Instale-o para gerar o instalador .exe:
    echo   https://jrsoftware.org/isinfo.php
    exit /b 0
)

"%ISCC_EXE%" "%APP_DIR%installer\Flash-Lite.iss"
if errorlevel 1 exit /b 1

echo.
echo Instalador criado em:
echo   %APP_DIR%installer-output\Flash-Lite-Setup.exe
exit /b 0
