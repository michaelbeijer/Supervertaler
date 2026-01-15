param(
    [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path,
    [string[]]$KeepZips = @(
        'Supervertaler-v1.9.104-Windows-CORE.zip',
        'Supervertaler-v1.9.104-Windows-FULL.zip'
    )
)

$ErrorActionPreference = 'Stop'
Set-Location $Root

function Write-Section([string]$Title) {
    Write-Host ''
    Write-Host ('=== ' + $Title + ' ===')
}

$distPath = Join-Path $Root 'dist'
$buildPath = Join-Path $Root 'build'

Write-Section 'BEFORE'
if (Test-Path $distPath) {
    Write-Host 'dist folders:'
    Get-ChildItem $distPath -Directory | Select-Object Name, LastWriteTime | Sort-Object Name | Format-Table | Out-String | Write-Host

    Write-Host 'dist zip files:'
    Get-ChildItem $distPath -File -Filter '*.zip' | Select-Object Name, LastWriteTime, Length | Sort-Object LastWriteTime -Descending | Format-Table | Out-String | Write-Host
}
else {
    Write-Host 'dist/ does not exist'
}

Write-Host ("build/ exists: {0}" -f (Test-Path $buildPath))

$toDeleteZips = @()
if (Test-Path $distPath) {
    $toDeleteZips = Get-ChildItem $distPath -File -Filter '*.zip' | Where-Object { $KeepZips -notcontains $_.Name }
}

Write-Section 'DELETING'
$legacyDist = Join-Path $distPath 'Supervertaler'
if (Test-Path $legacyDist) {
    Write-Host 'Removing dist\\Supervertaler (legacy single build)'
    Remove-Item $legacyDist -Recurse -Force
}

if (Test-Path $buildPath) {
    Write-Host 'Removing build\\ (PyInstaller work dir)'
    Remove-Item $buildPath -Recurse -Force
}

foreach ($z in $toDeleteZips) {
    Write-Host ('Removing dist\\' + $z.Name)
    Remove-Item $z.FullName -Force
}

Write-Section 'AFTER'
if (Test-Path $distPath) {
    Write-Host 'dist folders:'
    Get-ChildItem $distPath -Directory | Select-Object Name, LastWriteTime | Sort-Object Name | Format-Table | Out-String | Write-Host

    Write-Host 'dist zip files:'
    Get-ChildItem $distPath -File -Filter '*.zip' | Select-Object Name, LastWriteTime, Length | Sort-Object LastWriteTime -Descending | Format-Table | Out-String | Write-Host
}
else {
    Write-Host 'dist/ does not exist'
}

Write-Host ("build/ exists: {0}" -f (Test-Path $buildPath))
