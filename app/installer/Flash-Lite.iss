#define AppName "Flash-Lite"
#define AppVersion "0.1.0"
#define AppPublisher "Flash-Lite"
#define AppExeName "Flash-Lite.exe"

[Setup]
AppId={{B2D6FE7A-3D8F-4C47-9E5B-6E1D68E7B6A5}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={autopf}\Flash-Lite
DefaultGroupName={#AppName}
OutputDir=..\installer-output
OutputBaseFilename=Flash-Lite-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\{#AppExeName}

[Files]
Source: "..\dist\Flash-Lite\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na area de trabalho"; GroupDescription: "Atalhos:"

[Run]
Filename: "{app}\{#AppExeName}"; Description: "Executar o Flash-Lite"; Flags: nowait postinstall skipifsilent
