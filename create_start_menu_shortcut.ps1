# Create Windows Start Menu shortcut for Supervertaler
# Run this script ONCE after extracting the ZIP

$ErrorActionPreference = 'Stop'

Write-Host "Creating Start Menu shortcut for Supervertaler..." -ForegroundColor Cyan

# Get the directory where this script is located (should be the Supervertaler folder)
$SupervertalerDir = $PSScriptRoot
$ExePath = Join-Path $SupervertalerDir "Supervertaler.exe"

# Verify EXE exists
if (!(Test-Path $ExePath)) {
    Write-Host "ERROR: Supervertaler.exe not found in $SupervertalerDir" -ForegroundColor Red
    Write-Host "Make sure you're running this script from the extracted Supervertaler folder." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
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

Write-Host "✓ Start Menu shortcut created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "You can now find 'Supervertaler' in your Start Menu." -ForegroundColor Cyan
Write-Host "You can also pin it to the taskbar by right-clicking the shortcut." -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to close"
