# Browse and Restore Archived Files
# Lists archived files and helps restore them

param(
    [Parameter(Mandatory=$false)]
    [string]$Month = (Get-Date -Format "yyyy-MM"),
    
    [Parameter(Mandatory=$false)]
    [string]$SearchPattern = "*"
)

$ArchiveRoot = "C:\Dev\Supervertaler_Archive"
$MonthPath = Join-Path $ArchiveRoot $Month

if (-not (Test-Path $MonthPath)) {
    Write-Host "No archives found for $Month" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Available months:" -ForegroundColor Cyan
    Get-ChildItem $ArchiveRoot -Directory | ForEach-Object { Write-Host "  - $($_.Name)" }
    exit 0
}

Write-Host ""
Write-Host "=== Archived Files for $Month ===" -ForegroundColor Cyan
Write-Host ""

# Get all archived files (not metadata)
$ArchivedFiles = Get-ChildItem $MonthPath -Filter $SearchPattern | Where-Object { -not $_.Name.EndsWith('.meta.txt') }

if ($ArchivedFiles.Count -eq 0) {
    Write-Host "No archived files found matching: $SearchPattern" -ForegroundColor Yellow
    exit 0
}

$Index = 1
$FileList = @()

foreach ($File in $ArchivedFiles) {
    $MetaFile = "$($File.FullName).meta.txt"
    
    Write-Host "[$Index] $($File.Name)" -ForegroundColor Yellow
    
    if (Test-Path $MetaFile) {
        $MetaContent = Get-Content $MetaFile -Raw
        if ($MetaContent -match 'Original Path: (.+)') {
            Write-Host "    Original: $($Matches[1])" -ForegroundColor Gray
        }
        if ($MetaContent -match 'Archived On: (.+)') {
            Write-Host "    Archived: $($Matches[1])" -ForegroundColor Gray
        }
        if ($MetaContent -match 'Reason: (.+)') {
            Write-Host "    Reason:   $($Matches[1])" -ForegroundColor Gray
        }
    }
    
    $FileList += $File
    $Index++
    Write-Host ""
}

Write-Host "=== Options ===" -ForegroundColor Cyan
Write-Host "[Number] - View file content"
Write-Host "[R Number] - Restore file to original location"
Write-Host "[Q] - Quit"
Write-Host ""

$Choice = Read-Host "Enter your choice"

if ($Choice -match '^R\s*(\d+)$') {
    $FileIndex = [int]$Matches[1] - 1
    if ($FileIndex -ge 0 -and $FileIndex -lt $FileList.Count) {
        $SelectedFile = $FileList[$FileIndex]
        $MetaFile = "$($SelectedFile.FullName).meta.txt"
        
        if (Test-Path $MetaFile) {
            $MetaContent = Get-Content $MetaFile -Raw
            if ($MetaContent -match 'Original Path: (.+)') {
                $OriginalPath = $Matches[1].Trim()
                
                Write-Host ""
                Write-Host "Restoring:" -ForegroundColor Cyan
                Write-Host "  From: $($SelectedFile.FullName)" -ForegroundColor Yellow
                Write-Host "  To:   $OriginalPath" -ForegroundColor Green
                
                $Confirm = Read-Host "Proceed? (Y/N)"
                if ($Confirm -eq 'Y' -or $Confirm -eq 'y') {
                    # Create directory if needed
                    $ParentDir = Split-Path $OriginalPath -Parent
                    if (-not (Test-Path $ParentDir)) {
                        New-Item -ItemType Directory -Path $ParentDir -Force | Out-Null
                    }
                    
                    Copy-Item -Path $SelectedFile.FullName -Destination $OriginalPath -Force
                    Write-Host ""
                    Write-Host "✓ File restored successfully!" -ForegroundColor Green
                }
            }
        }
    }
} elseif ($Choice -match '^\d+$') {
    $FileIndex = [int]$Choice - 1
    if ($FileIndex -ge 0 -and $FileIndex -lt $FileList.Count) {
        $SelectedFile = $FileList[$FileIndex]
        Write-Host ""
        Write-Host "=== File Content ===" -ForegroundColor Cyan
        Write-Host ""
        Get-Content $SelectedFile.FullName
    }
}
