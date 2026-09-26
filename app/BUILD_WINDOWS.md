# Gerar o instalador Windows

O projeto possui dois artefatos de distribuição:

- `dist/Flash-Lite/Flash-Lite.exe`: aplicativo portátil com as dependências empacotadas;
- `installer-output/Flash-Lite-Setup.exe`: instalador completo para o usuário final.

O build precisa ser executado em Windows. O PyInstaller empacota dependências para o sistema em que é executado e não gera corretamente um executável Windows a partir do Linux.

## Pré-requisitos da máquina de build

Instale:

1. Python 3.12 ou superior, preferencialmente 3.12;
2. Inno Setup 6, caso também queira gerar o instalador;
3. este projeto completo.

O usuário final não precisará instalar Python, `psutil` ou `PySide6`: essas dependências são incluídas no aplicativo pelo PyInstaller.

## Build automático

Abra o Prompt de Comando na raiz do projeto e execute:

```bat
app\build_windows.bat
```

O script irá:

1. criar o ambiente `.venv-build`;
2. instalar `psutil`, `PySide6` e PyInstaller;
3. empacotar o `main.py` e as regras de limpeza;
4. gerar `app\dist\Flash-Lite\Flash-Lite.exe`;
5. gerar `app\installer-output\Flash-Lite-Setup.exe` se o Inno Setup estiver instalado.

## Build manual

```bat
py -3 -m venv app\.venv-build
call app\.venv-build\Scripts\activate.bat
python -m pip install -r app\requirements-windows.txt
python -m PyInstaller app\Flash-Lite.spec --noconfirm --clean --distpath app\dist --workpath app\build
```

Para gerar o instalador depois do build:

```bat
ISCC app\installer\Flash-Lite.iss
```

## Resultado

O `Flash-Lite-Setup.exe` instala o aplicativo em `Program Files`, cria atalhos no menu Iniciar e na área de trabalho e oferece a execução ao final da instalação. O banco local, a quarentena e as configurações continuam sendo gravados na pasta de dados do usuário, não dentro de `Program Files`.
