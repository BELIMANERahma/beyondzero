@echo off
REM Builds BeyondZero.exe (run from this folder). Requires Python 3.9+ with "Add to PATH".
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt pyinstaller
pyinstaller --noconfirm --clean --windowed --name BeyondZero --icon assets\icon.ico ^
  --add-data "assets;assets" --collect-all arabic_reshaper --collect-all bidi main.py
echo.
echo Done: dist\BeyondZero\BeyondZero.exe
echo To make a Setup.exe installer: install Inno Setup, open installer.iss and press Compile.
pause
