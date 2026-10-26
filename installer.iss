; Inno Setup script - creates Output\BeyondZero_Setup.exe (download Inno Setup from jrsoftware.org)
[Setup]
AppName=Beyond Zero - ما وراء الصفر
AppVersion=1.0
DefaultDirName={autopf}\BeyondZero
DefaultGroupName=Beyond Zero
OutputBaseFilename=BeyondZero_Setup
SetupIconFile=assets\icon.ico
PrivilegesRequired=lowest
Compression=lzma
SolidCompression=yes
[Files]
Source: "dist\BeyondZero\*"; DestDir: "{app}"; Flags: recursesubdirs
[Icons]
Name: "{group}\Beyond Zero"; Filename: "{app}\BeyondZero.exe"
Name: "{autodesktop}\Beyond Zero"; Filename: "{app}\BeyondZero.exe"; Tasks: desktopicon
[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"
[Run]
Filename: "{app}\BeyondZero.exe"; Description: "Launch the game"; Flags: postinstall nowait
