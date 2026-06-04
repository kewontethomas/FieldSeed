@echo off
cd /d %~dp0
python -m pip show customtkinter >nul 2>&1
if errorlevel 1 (
    echo Installing FieldSeed desktop UI dependency...
    python -m pip install customtkinter
)
python -m fieldseed app
pause
