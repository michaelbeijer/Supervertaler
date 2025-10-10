# cleanup_desktop_ini.ps1
# Removes Google Drive's desktop.ini files from .git directory
# Run this before git operations to avoid "ignoring broken ref" warnings

$repoPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$gitPath = Join-Path $repoPath ".git"

Write-Host "Cleaning up desktop.ini files from .git directory..." -ForegroundColor Yellow

$desktopIniFiles = Get-ChildItem -Path $gitPath -Filter "desktop.ini" -Recurse -Force -ErrorAction SilentlyContinue

if ($desktopIniFiles) {
    $count = ($desktopIniFiles | Measure-Object).Count
    Write-Host "Found $count desktop.ini file(s). Removing..." -ForegroundColor Cyan
    
    $desktopIniFiles | ForEach-Object {
        Write-Host "  Removing: $($_.FullName)" -ForegroundColor Gray
        Remove-Item $_.FullName -Force
    }
    
    Write-Host "✓ Cleanup complete!" -ForegroundColor Green
} else {
    Write-Host "✓ No desktop.ini files found in .git directory" -ForegroundColor Green
}

Write-Host "`nYou can now safely run git commands." -ForegroundColor White
