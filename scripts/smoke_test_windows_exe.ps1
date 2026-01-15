Param(
  [ValidateSet('core','full')]
  [string]$Flavor = 'full',
  [int]$Seconds = 5
)

$ErrorActionPreference = 'Stop'

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot '..')
Set-Location $repoRoot

$distDir = Join-Path $repoRoot ("dist\Supervertaler-$Flavor")
$exePath = Join-Path $distDir 'Supervertaler.exe'

try {
  if (!(Test-Path $exePath)) {
    Write-Host "EXE not built yet: $exePath" -ForegroundColor Yellow
    exit 0
  }

  $fi = Get-Item $exePath
  Write-Host "EXE: $($fi.FullName)"
  Write-Host "Modified: $($fi.LastWriteTime)"
  Write-Host ("SizeMB: {0:N1}" -f ($fi.Length / 1MB))

  $since = Get-Date

  $p = Start-Process -FilePath $exePath -PassThru
  Start-Sleep -Seconds $Seconds

  if ($p.HasExited) {
    Write-Host "Exited quickly. ExitCode=$($p.ExitCode)" -ForegroundColor Yellow
  } else {
    Write-Host "Still running after ${Seconds}s (launch OK). Killing for smoke test..." -ForegroundColor Green
    Stop-Process -Id $p.Id -Force
  }

  Start-Sleep -Seconds 1

  Write-Host "--- Recent crash events (Application log) ---" -ForegroundColor Cyan
  $events = Get-WinEvent -FilterHashtable @{ LogName = 'Application'; StartTime = $since.AddMinutes(-2) } -ErrorAction SilentlyContinue |
    Where-Object {
      $_.Message -like '*Supervertaler.exe*' -and
      $_.ProviderName -in @('Application Error', 'Windows Error Reporting')
    } |
    Select-Object -First 5

  if (-not $events) {
    Write-Host "No crash events found." -ForegroundColor Green
  } else {
    foreach ($e in $events) {
      $msg = $e.Message
      $faultModule = ([regex]::Match($msg, 'Faulting module name:\s*([^\r\n]+)').Groups[1].Value).Trim()
      $exceptionCode = ([regex]::Match($msg, 'Exception code:\s*([^\r\n]+)').Groups[1].Value).Trim()
      if ([string]::IsNullOrWhiteSpace($faultModule)) { $faultModule = '?' }
      if ([string]::IsNullOrWhiteSpace($exceptionCode)) { $exceptionCode = '?' }
      Write-Host ("{0:u} | {1} {2} | module={3} exception={4}" -f $e.TimeCreated, $e.ProviderName, $e.Id, $faultModule, $exceptionCode)
    }
  }

  exit 0
}
catch {
  Write-Host "Smoke test failed: $($_.Exception.Message)" -ForegroundColor Red
  exit 0
}
