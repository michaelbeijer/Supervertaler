# Create Windows Start Menu shortcut for Supervertaler
# Run this script ONCE after extracting the ZIP

$ErrorActionPreference = 'Stop'

Write-Host "Creating Start Menu shortcut for Supervertaler..." -ForegroundColor Cyan

# Get the directory where this script is located
$SupervertalerDir = $PSScriptRoot
$ExePath = Join-Path $SupervertalerDir "Supervertaler.exe"

# Check if running from source (no EXE) or from distributed build
if (!(Test-Path $ExePath)) {
    Write-Host ""
    Write-Host "INFO: This script is for the distributed Windows build only." -ForegroundColor Yellow
    Write-Host "Supervertaler.exe not found in: $SupervertalerDir" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "If you're running from source code, you don't need this script." -ForegroundColor Cyan
    Write-Host "For end users: Extract the Supervertaler ZIP first, then run this script." -ForegroundColor Cyan
    Write-Host ""
    $null = Read-Host "Press Enter to exit"
    exit 0
}

# Create shortcut in Start Menu
$StartMenuPath = [Environment]::GetFolderPath("StartMenu")
$ShortcutPath = Join-Path $StartMenuPath "Programs\Supervertaler.lnk"

$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $ExePath
$Shortcut.WorkingDirectory = $SupervertalerDir
$Shortcut.Description = "Supervertaler - AI-powered translation workbench"

# Use the EXE's embedded icon
$Shortcut.IconLocation = "$ExePath,0"

$Shortcut.Save()

Write-Host ""
Write-Host "SUCCESS: Start Menu shortcut created!" -ForegroundColor Green
Write-Host ""
Write-Host "You can now find 'Supervertaler' in your Start Menu." -ForegroundColor Cyan
Write-Host "You can also pin it to the taskbar by right-clicking the shortcut." -ForegroundColor Cyan
Write-Host ""
$null = Read-Host "Press Enter to close"
