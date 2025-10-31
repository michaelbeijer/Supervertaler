# Safe Archive Script
# Archives files instead of deleting them permanently
# Usage: .\safe_archive.ps1 -Path "path\to\file.txt" -Reason "Why archiving"

param(
    [Parameter(Mandatory=$true)]
    [string]$Path,
    
    [Parameter(Mandatory=$false)]
    [string]$Reason = "Manual archive"
)

$ErrorActionPreference = "Stop"

# Archive location OUTSIDE the workspace
$ArchiveRoot = "C:\Dev\Supervertaler_Archive"

# Create archive folder if it doesn't exist
if (-not (Test-Path $ArchiveRoot)) {
    New-Item -ItemType Directory -Path $ArchiveRoot | Out-Null
    Write-Host "Created archive directory: $ArchiveRoot" -ForegroundColor Green
}

# Get current date for organization
$DateFolder = Get-Date -Format "yyyy-MM"
$ArchiveDate = "$ArchiveRoot\$DateFolder"

if (-not (Test-Path $ArchiveDate)) {
    New-Item -ItemType Directory -Path $ArchiveDate | Out-Null
}

# Resolve full path
$FullPath = Resolve-Path $Path -ErrorAction SilentlyContinue
if (-not $FullPath) {
    Write-Error "File not found: $Path"
    exit 1
}

# Get file info
$Item = Get-Item $FullPath

# Create timestamped archive name
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$ArchiveName = "$($Item.BaseName)_$Timestamp$($Item.Extension)"
$ArchivePath = Join-Path $ArchiveDate $ArchiveName

# Create metadata file
$MetadataPath = "$ArchivePath.meta.txt"
$Metadata = @"
Archive Metadata
================
Original Path: $($Item.FullName)
Archived On: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Reason: $Reason
File Size: $($Item.Length) bytes
Original Modified: $($Item.LastWriteTime)

You can restore this file by copying it back to its original location.
"@

# Archive the file
try {
    Copy-Item -Path $Item.FullName -Destination $ArchivePath -Force
    $Metadata | Out-File -FilePath $MetadataPath -Encoding UTF8
    
    Write-Host ""
    Write-Host "✓ File archived successfully!" -ForegroundColor Green
    Write-Host "  Original: $($Item.FullName)" -ForegroundColor Cyan
    Write-Host "  Archive:  $ArchivePath" -ForegroundColor Yellow
    Write-Host "  Metadata: $MetadataPath" -ForegroundColor Gray
    Write-Host "  Reason:   $Reason" -ForegroundColor Gray
    
    # Now delete the original
    Remove-Item -Path $Item.FullName -Force
    Write-Host ""
    Write-Host "✓ Original file removed from workspace" -ForegroundColor Green
    
} catch {
    Write-Error "Failed to archive file: $_"
    exit 1
}

Write-Host ""
Write-Host "Archive location: $ArchiveRoot" -ForegroundColor Magenta
