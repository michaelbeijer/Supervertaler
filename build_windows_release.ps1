Param(
  [switch]$Clean,
  [switch]$CoreOnly,
  [switch]$FullOnly
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

function Build-One($flavor, $venvDir, $specPath, $zipSuffix, $extras) {
  $version = Get-Version

  $basePython = $null
  if (Test-Path .\.venv\Scripts\python.exe) {
    $basePython = Resolve-Path .\.venv\Scripts\python.exe
  } else {
    $basePython = (Get-Command python).Source
  }

  if ($Clean -and (Test-Path $venvDir)) {
    Remove-Item -Recurse -Force $venvDir
  }

  Ensure-Venv $venvDir $basePython
  $py = Resolve-Path (Join-Path $venvDir 'Scripts\python.exe')

  Install-Build-Tooling $py

  # Install Supervertaler into this build venv
  if ([string]::IsNullOrWhiteSpace($extras)) {
    & $py -m pip install -q -e .
  } else {
    & $py -m pip install -q -e ('.' + $extras)
  }

  # Clean build outputs per flavor (avoid dist folder collisions)
  if ($Clean) {
    if (Test-Path build) { Remove-Item -Recurse -Force build }
    # NOTE: do NOT delete dist/ entirely because we may be building multiple flavors.
  }

  # Ensure the output folder isn't locked by a running EXE from a previous build.
  # This is a common cause of WinError 5 during PyInstaller's COLLECT clean step.
  $distDir = if ($flavor -eq 'core') { 'dist\Supervertaler-core' } else { 'dist\Supervertaler-full' }
  Get-Process Supervertaler -ErrorAction SilentlyContinue | Stop-Process -Force
  if (Test-Path $distDir) {
    Remove-Item -Recurse -Force $distDir
  }

  Write-Host "=== Building $flavor EXE via $specPath ===" -ForegroundColor Cyan
  & $py -m PyInstaller --noconfirm --clean $specPath

  $zipPath = "dist\Supervertaler-v$version-Windows-$zipSuffix.zip"

  Write-Host "=== Zipping $flavor to $zipPath ===" -ForegroundColor Cyan
  & $py .\create_release_zip.py --dist-dir $distDir --output-zip $zipPath --flavor $flavor
}

$version = Get-Version
Write-Host ("Supervertaler version: v$version") -ForegroundColor Green

# Default behavior: build both
$buildCore = $true
$buildFull = $true
if ($CoreOnly) { $buildFull = $false }
if ($FullOnly) { $buildCore = $false }

if ($buildCore) {
  Build-One -flavor 'core' -venvDir '.venv-build-core' -specPath '.\Supervertaler.core.spec' -zipSuffix 'CORE' -extras ''
}

if ($buildFull) {
  Build-One -flavor 'full' -venvDir '.venv-build-full' -specPath '.\Supervertaler.full.spec' -zipSuffix 'FULL' -extras '[supermemory,local-whisper]'
}

Write-Host "DONE. Release assets are in dist\\" -ForegroundColor Green
