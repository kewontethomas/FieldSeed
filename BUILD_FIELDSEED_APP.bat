@echo off
setlocal
cd /d "%~dp0"

echo Installing build dependency...
python -m pip install pyinstaller customtkinter

echo Building FieldSeed desktop app with icon...
python -m PyInstaller ^
  --noconfirm ^
  --onedir ^
  --windowed ^
  --name FieldSeed ^
  --icon assets\fieldseed.ico ^
  --add-data "assets;assets" ^
  --add-data "data;data" ^
  -m fieldseed app

echo.
echo Build complete.
echo Open: dist\FieldSeed\FieldSeed.exe
pause
