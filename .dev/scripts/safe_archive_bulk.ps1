# Archive Multiple Files or Folders
# Archives multiple files/folders instead of deleting them
# Usage: .\safe_archive_bulk.ps1 -Paths @("file1.txt", "file2.txt") -Reason "Cleanup"

param(
    [Parameter(Mandatory=$true)]
    [string[]]$Paths,
    
    [Parameter(Mandatory=$false)]
    [string]$Reason = "Bulk archive"
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "=== Safe Archive (Bulk Mode) ===" -ForegroundColor Cyan
Write-Host "Reason: $Reason" -ForegroundColor Gray
Write-Host ""

$SuccessCount = 0
$FailCount = 0

foreach ($Path in $Paths) {
    try {
        & "$PSScriptRoot\safe_archive.ps1" -Path $Path -Reason $Reason
        $SuccessCount++
    } catch {
        Write-Host "✗ Failed to archive: $Path" -ForegroundColor Red
        Write-Host "  Error: $_" -ForegroundColor Red
        $FailCount++
    }
    Write-Host ""
    Write-Host "---"
    Write-Host ""
}

Write-Host ""
Write-Host "=== Summary ===" -ForegroundColor Cyan
Write-Host "Successfully archived: $SuccessCount" -ForegroundColor Green
if ($FailCount -gt 0) {
    Write-Host "Failed: $FailCount" -ForegroundColor Red
}
