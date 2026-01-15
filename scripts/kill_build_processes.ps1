param(
    [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
)

$ErrorActionPreference = 'Continue'
Set-Location $Root

$patterns = @(
    'pyinstaller',
    'PyInstaller',
    'build_windows_release.ps1',
    'Supervertaler.full.spec',
    'Supervertaler.core.spec'
)

$procs = Get-CimInstance Win32_Process |
    Where-Object {
        $_.CommandLine -and ($patterns | Where-Object { $_ -and $_.Length -gt 0 } | ForEach-Object { $_ })
    }

$procs = Get-CimInstance Win32_Process | Where-Object {
    $_.CommandLine -and (
        $_.CommandLine -match 'pyinstaller|PyInstaller|build_windows_release\.ps1|Supervertaler\.full\.spec|Supervertaler\.core\.spec'
    )
}

if (-not $procs) {
    Write-Host 'No matching build processes found.'
    exit 0
}

Write-Host 'Found build-related processes:'
$procs | Select-Object Name, ProcessId, CommandLine | Format-Table -Wrap | Out-String | Write-Host

foreach ($p in $procs) {
    try {
        Stop-Process -Id $p.ProcessId -Force -ErrorAction Stop
        Write-Host ("Stopped PID {0} ({1})" -f $p.ProcessId, $p.Name)
    }
    catch {
        Write-Host ("Failed to stop PID {0}: {1}" -f $p.ProcessId, $_.Exception.Message)
    }
}
