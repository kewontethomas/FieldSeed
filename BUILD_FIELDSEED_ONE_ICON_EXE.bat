@echo off
setlocal
cd /d "%~dp0"
echo ==========================================
echo Building FieldSeed Desktop one-icon app
echo ==========================================
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller
python -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --windowed ^
  --onefile ^
  --name FieldSeed ^
  --icon assets\fieldseed.ico ^
  --collect-all customtkinter ^
  --add-data "tools;tools" ^
  launch_fieldseed.py

echo.
echo Build complete.
echo Your app should be here:
echo dist\FieldSeed.exe
echo.
pause
