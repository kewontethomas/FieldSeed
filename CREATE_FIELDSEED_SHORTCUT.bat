@echo off
setlocal
cd /d "%~dp0"

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
 "$WshShell = New-Object -comObject WScript.Shell; ^
  $Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\FieldSeed.lnk'); ^
  $Shortcut.TargetPath = '%CD%\START_FIELDSEED.bat'; ^
  $Shortcut.WorkingDirectory = '%CD%'; ^
  $Shortcut.IconLocation = '%CD%\assets\fieldseed.ico'; ^
  $Shortcut.Save()"

echo FieldSeed desktop shortcut created.
pause
