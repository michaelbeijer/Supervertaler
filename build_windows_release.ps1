Param(
  [switch]$Clean
)

$ErrorActionPreference = 'Stop'

Set-Location $PSScriptRoot

function Get-Version {
  $content = Get-Content -Raw -Encoding UTF8 .\Supervertaler.py
  $m = [regex]::Match($content, '__version__\s*=\s*["\'']([^"\'']+)["\'']')
  if ($m.Success) { return $m.Groups[1].Value }
  return 'unknown'
}

function Ensure-Venv($path, $basePython) {
  if (!(Test-Path $path)) {
    & $basePython -m venv $path
  }
}

function Install-Build-Tooling($py) {
  & $py -m pip install -q -U pip setuptools wheel
  & $py -m pip install -q -U pyinstaller
}

$version = Get-Version
Write-Host ("Supervertaler version: v$version") -ForegroundColor Green

# Find base Python
$basePython = $null
if (Test-Path .\.venv\Scripts\python.exe) {
  $basePython = Resolve-Path .\.venv\Scripts\python.exe
} else {
  $basePython = (Get-Command python).Source
}

$venvDir = '.venv-build'

if ($Clean -and (Test-Path $venvDir)) {
  Write-Host "Cleaning build venv..." -ForegroundColor Yellow
  Remove-Item -Recurse -Force $venvDir
}

Ensure-Venv $venvDir $basePython
$py = Resolve-Path (Join-Path $venvDir 'Scripts\python.exe')

Install-Build-Tooling $py

# Install Supervertaler (core only - no local-whisper to avoid PyTorch/PyInstaller conflicts)
# Voice commands still work via OpenAI Whisper API
Write-Host "Installing Supervertaler with all dependencies..." -ForegroundColor Cyan
& $py -m pip install -q -e "."

# Clean build outputs
if ($Clean) {
  if (Test-Path build) { Remove-Item -Recurse -Force build }
}

# Ensure the output folder isn't locked by a running EXE from a previous build
$distDir = 'dist\Supervertaler'
Get-Process Supervertaler -ErrorAction SilentlyContinue | Stop-Process -Force
if (Test-Path $distDir) {
  Remove-Item -Recurse -Force $distDir
}

Write-Host "=== Building Supervertaler EXE via Supervertaler.spec ===" -ForegroundColor Cyan
& $py -m PyInstaller --noconfirm --clean .\Supervertaler.spec

# Copy user_data directly next to the EXE (not inside _internal/)
# This makes dictionaries, prompts, and settings easily accessible to users.
Write-Host "=== Copying user_data to $distDir ===" -ForegroundColor Cyan
$userDataSrc = "user_data"
$userDataDest = Join-Path $distDir "user_data"
if (Test-Path $userDataDest) { Remove-Item -Recurse -Force $userDataDest }

# Create user_data structure with only the files we want to ship
New-Item -ItemType Directory -Path $userDataDest -Force | Out-Null

# Copy dictionaries (Hunspell files)
if (Test-Path "$userDataSrc\dictionaries") {
  Copy-Item -Recurse "$userDataSrc\dictionaries" "$userDataDest\dictionaries"
  Write-Host "  - Copied dictionaries"
}

# Copy Prompt_Library (default prompts)
if (Test-Path "$userDataSrc\Prompt_Library") {
  Copy-Item -Recurse "$userDataSrc\Prompt_Library" "$userDataDest\Prompt_Library"
  Write-Host "  - Copied Prompt_Library"
}

# Copy Translation_Resources
if (Test-Path "$userDataSrc\Translation_Resources") {
  Copy-Item -Recurse "$userDataSrc\Translation_Resources" "$userDataDest\Translation_Resources"
  Write-Host "  - Copied Translation_Resources"
}

# Copy voice_scripts
if (Test-Path "$userDataSrc\voice_scripts") {
  Copy-Item -Recurse "$userDataSrc\voice_scripts" "$userDataDest\voice_scripts"
  Write-Host "  - Copied voice_scripts"
}

# Copy individual files
@("shortcuts.json", "voice_commands.json", "translation_memory.db") | ForEach-Object {
  if (Test-Path "$userDataSrc\$_") {
    Copy-Item "$userDataSrc\$_" "$userDataDest\$_"
    Write-Host "  - Copied $_"
  }
}

$zipPath = "dist\Supervertaler-v$version-Windows.zip"

Write-Host "=== Zipping to $zipPath ===" -ForegroundColor Cyan
& $py .\create_release_zip.py --dist-dir $distDir --output-zip $zipPath --flavor unified

Write-Host "DONE. Release asset: $zipPath" -ForegroundColor Green
