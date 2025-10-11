# Migration Script: Suffix-based to Parallel Folder Structure
# Migrates from user data/*_private folders to user data_private/ structure
# Git-aware: properly handles tracked vs untracked files

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "Supervertaler: Private Data Migration Script" -ForegroundColor Cyan
Write-Host "Suffix-based → Parallel Folder Structure" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Get script directory (should be .dev folder)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptDir

# Verify we're in the right location
if (-not (Test-Path "$repoRoot\.supervertaler.local")) {
    Write-Host "ERROR: .supervertaler.local not found!" -ForegroundColor Red
    Write-Host "This script should only be run by developers with dev mode enabled." -ForegroundColor Red
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host "✓ Dev mode detected (.supervertaler.local found)" -ForegroundColor Green
Write-Host ""

# Define source and destination paths
$userDataDir = Join-Path $repoRoot "user data"
$privateDataDir = Join-Path $repoRoot "user data_private"

# Folders to migrate
$foldersToMigrate = @(
    "System_prompts_private",
    "Custom_instructions_private",
    "Projects_private",
    "TMs_private",
    "Glossaries_private",
    "Segmentation_rules_private",
    "Non-translatables (NTs)_private"
)

# Check what exists
Write-Host "Scanning for existing private folders..." -ForegroundColor Cyan
$foldersFound = @()
foreach ($folder in $foldersToMigrate) {
    $sourcePath = Join-Path $userDataDir $folder
    if (Test-Path $sourcePath) {
        $itemCount = (Get-ChildItem -Path $sourcePath -File -Recurse -ErrorAction SilentlyContinue | Measure-Object).Count
        if ($itemCount -gt 0) {
            $folderInfo = New-Object PSObject -Property @{
                Name = $folder
                Path = $sourcePath
                Items = $itemCount
            }
            $foldersFound += $folderInfo
            Write-Host "  ✓ Found: $folder ($itemCount files)" -ForegroundColor Yellow
        }
    }
}

if ($foldersFound.Count -eq 0) {
    Write-Host ""
    Write-Host "No private folders with content found. Migration not needed." -ForegroundColor Green
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 0
}

Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "Migration Plan:" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
foreach ($folder in $foldersFound) {
    $baseName = $folder.Name -replace '_private$', ''
    Write-Host "  $($folder.Name) → user data_private\$baseName" -ForegroundColor White
    Write-Host "    ($($folder.Items) files)" -ForegroundColor Gray
}
Write-Host ""

# Confirm
Write-Host "This will:" -ForegroundColor Yellow
Write-Host "  1. Create new user data_private/ folder structure" -ForegroundColor White
Write-Host "  2. MOVE all private files to new locations" -ForegroundColor White
Write-Host "  3. Remove old empty *_private folders" -ForegroundColor White
Write-Host "  4. Update git to track the changes" -ForegroundColor White
Write-Host ""
Write-Host "Your data will be preserved safely!" -ForegroundColor Green
Write-Host ""
$confirm = Read-Host "Proceed with migration? (yes/no)"

if ($confirm -ne "yes") {
    Write-Host "Migration cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Starting migration..." -ForegroundColor Cyan
Write-Host ""

# Create new directory structure
Write-Host "[1/4] Creating new directory structure..." -ForegroundColor Cyan
if (-not (Test-Path $privateDataDir)) {
    New-Item -ItemType Directory -Path $privateDataDir -Force | Out-Null
    Write-Host "  ✓ Created: user data_private\" -ForegroundColor Green
}

$migratedCount = 0
$errorCount = 0

# Migrate each folder
Write-Host ""
Write-Host "[2/4] Migrating files..." -ForegroundColor Cyan
foreach ($folder in $foldersFound) {
    $sourcePath = $folder.Path
    $baseName = $folder.Name -replace '_private$', ''
    $destPath = Join-Path $privateDataDir $baseName
    
    Write-Host "  Processing: $baseName..." -ForegroundColor White
    
    try {
        # Create destination folder
        if (-not (Test-Path $destPath)) {
            New-Item -ItemType Directory -Path $destPath -Force | Out-Null
        }
        
        # Move all files
        $files = Get-ChildItem -Path $sourcePath -File -Recurse -ErrorAction SilentlyContinue
        foreach ($file in $files) {
            $relativePath = $file.FullName.Substring($sourcePath.Length + 1)
            $destFile = Join-Path $destPath $relativePath
            $destFileDir = Split-Path -Parent $destFile
            
            # Create subdirectories if needed
            if (-not (Test-Path $destFileDir)) {
                New-Item -ItemType Directory -Path $destFileDir -Force | Out-Null
            }
            
            # Move file
            Move-Item -Path $file.FullName -Destination $destFile -Force
            $migratedCount++
        }
        
        Write-Host "    ✓ Migrated $($files.Count) files" -ForegroundColor Green
        
    } catch {
        Write-Host "    ✗ Error: $_" -ForegroundColor Red
        $errorCount++
    }
}

# Remove old empty folders
Write-Host ""
Write-Host "[3/4] Cleaning up old folder structure..." -ForegroundColor Cyan
foreach ($folder in $foldersFound) {
    $sourcePath = $folder.Path
    
    # Check if folder is now empty
    $remaining = Get-ChildItem -Path $sourcePath -File -Recurse -ErrorAction SilentlyContinue
    if ($remaining.Count -eq 0) {
        Remove-Item -Path $sourcePath -Recurse -Force
        Write-Host "  ✓ Removed empty folder: $($folder.Name)" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ Folder not empty (skipped): $($folder.Name)" -ForegroundColor Yellow
    }
}

# Git operations
Write-Host ""
Write-Host "[4/4] Updating git..." -ForegroundColor Cyan

# Check if we're in a git repo
$isGitRepo = Test-Path (Join-Path $repoRoot ".git")

if ($isGitRepo) {
    Push-Location $repoRoot
    
    try {
        # Stage the new private data folder (will be ignored by .gitignore)
        Write-Host "  · Staging changes..." -ForegroundColor White
        
        # The old *_private folders should already be in .gitignore
        # The new user data_private/ is also in .gitignore
        # So this won't actually commit private data, just records the structure change
        
        git add -A 2>&1 | Out-Null
        
        Write-Host "  ✓ Git updated (private data still excluded by .gitignore)" -ForegroundColor Green
        
    } catch {
        Write-Host "  ⚠ Git update had issues: $_" -ForegroundColor Yellow
    }
    
    Pop-Location
} else {
    Write-Host "  ℹ Not a git repository - skipping git operations" -ForegroundColor Gray
}

# Summary
Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "Migration Complete!" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  ✓ Migrated: $migratedCount files" -ForegroundColor Green
if ($errorCount -gt 0) {
    Write-Host "  ✗ Errors: $errorCount" -ForegroundColor Red
}
Write-Host ""
Write-Host "Your private data is now in:" -ForegroundColor White
Write-Host "  user data_private\" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Test both programs to ensure everything works" -ForegroundColor White
Write-Host "  2. Verify .gitignore excludes user data_private/" -ForegroundColor White
Write-Host "  3. Commit the structural changes (not the private data)" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
