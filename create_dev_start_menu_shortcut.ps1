# Create Windows Start Menu shortcut for Supervertaler (Developer Version)
# This creates a shortcut to run.cmd for running from source

$ErrorActionPreference = 'Stop'

Write-Host "Creating Start Menu shortcut for Supervertaler (Dev)..." -ForegroundColor Cyan

# Get the directory where this script is located
$SupervertalerDir = $PSScriptRoot
$RunCmdPath = Join-Path $SupervertalerDir "run.cmd"
$IconPath = Join-Path $SupervertalerDir "assets\icon.ico"

# Verify run.cmd exists
if (!(Test-Path $RunCmdPath)) {
    Write-Host ""
    Write-Host "ERROR: run.cmd not found in $SupervertalerDir" -ForegroundColor Red
    Write-Host "Make sure you're running this script from the Supervertaler source directory." -ForegroundColor Yellow
    Write-Host ""
    $null = Read-Host "Press Enter to exit"
    exit 1
}

# Create shortcut in Start Menu
$StartMenuPath = [Environment]::GetFolderPath("StartMenu")
$ShortcutPath = Join-Path $StartMenuPath "Programs\Supervertaler (Dev).lnk"

$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $RunCmdPath
$Shortcut.WorkingDirectory = $SupervertalerDir
$Shortcut.Description = "Supervertaler - AI Translation Tool (Dev Build)"

# Use icon if available, otherwise default CMD icon
if (Test-Path $IconPath) {
    $Shortcut.IconLocation = $IconPath
    Write-Host "Using custom icon: $IconPath" -ForegroundColor Gray
} else {
    Write-Host "Icon not found, using default CMD icon" -ForegroundColor Gray
}

$Shortcut.Save()

Write-Host ""
Write-Host "SUCCESS: Start Menu shortcut created!" -ForegroundColor Green
Write-Host ""
Write-Host "Shortcut name: 'Supervertaler (Dev)'" -ForegroundColor Cyan
Write-Host "Shortcut location: $ShortcutPath" -ForegroundColor Gray
Write-Host ""
Write-Host "You can now find 'Supervertaler (Dev)' in your Start Menu." -ForegroundColor Cyan
Write-Host "You can also pin it to the taskbar by right-clicking the shortcut." -ForegroundColor Cyan
Write-Host ""
$null = Read-Host "Press Enter to close"
