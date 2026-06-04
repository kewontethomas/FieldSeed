$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Exe = Join-Path $Root "dist\FieldSeed.exe"
$Icon = Join-Path $Root "assets\fieldseed.ico"
if (!(Test-Path $Exe)) {
    Write-Host "FieldSeed.exe not found. Run BUILD_FIELDSEED_ONE_ICON_EXE.bat first."
    exit 1
}
$Desktop = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $Desktop "FieldSeed.lnk"
$Shell = New-Object -ComObject WScript.Shell
$Shortcut = $Shell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $Exe
$Shortcut.WorkingDirectory = Split-Path $Exe
$Shortcut.IconLocation = $Icon
$Shortcut.Description = "FieldSeed Desktop Cockpit"
$Shortcut.Save()
Write-Host "Created desktop shortcut: $ShortcutPath"
