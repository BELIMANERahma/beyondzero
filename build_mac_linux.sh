#!/bin/bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt pyinstaller
pyinstaller --noconfirm --clean --windowed --name BeyondZero --add-data "assets:assets" --collect-all arabic_reshaper --collect-all bidi main.py
echo "Done: dist/BeyondZero"
