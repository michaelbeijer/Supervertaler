# Supervertaler v2.4.1 Complete Build Script
# Run this script to build the complete distribution package

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Supervertaler v2.4.1 Build Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Clean
Write-Host "[1/5] Cleaning build environment..." -ForegroundColor Yellow
Remove-Item -Path "dist" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "build" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "Supervertaler_v2.4.1_Windows.zip" -Force -ErrorAction SilentlyContinue
Write-Host "      ✅ Cleaned" -ForegroundColor Green
Write-Host ""

# Step 2: Build with PyInstaller
Write-Host "[2/5] Building with PyInstaller (60-90 seconds)..." -ForegroundColor Yellow
$buildOutput = pyinstaller Supervertaler.spec --noconfirm 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "      ✅ Build complete" -ForegroundColor Green
} else {
    Write-Host "      ❌ Build failed!" -ForegroundColor Red
    Write-Host $buildOutput
    exit 1
}
Write-Host ""

# Step 3: Post-build (copy files to root)
Write-Host "[3/5] Running post-build script..." -ForegroundColor Yellow
python post_build.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "      ✅ Files copied to root" -ForegroundColor Green
} else {
    Write-Host "      ❌ Post-build failed!" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 4: Create ZIP
Write-Host "[4/5] Creating release ZIP..." -ForegroundColor Yellow
Compress-Archive -Path "dist\Supervertaler_v2.4.1" -DestinationPath "Supervertaler_v2.4.1_Windows.zip" -Force
Write-Host "      ✅ ZIP created" -ForegroundColor Green
Write-Host ""

# Step 5: Summary
Write-Host "[5/5] Build Summary" -ForegroundColor Yellow
Write-Host ""
$zipInfo = Get-Item "Supervertaler_v2.4.1_Windows.zip"
$zipSizeMB = [math]::Round($zipInfo.Length / 1MB, 2)
Write-Host "  📦 Package: Supervertaler_v2.4.1_Windows.zip" -ForegroundColor Cyan
Write-Host "  📏 Size: $zipSizeMB MB" -ForegroundColor Cyan
Write-Host "  📁 Location: $($zipInfo.FullName)" -ForegroundColor Cyan
Write-Host ""

Write-Host "ROOT folder contents:" -ForegroundColor Yellow
Get-ChildItem "dist\Supervertaler_v2.4.1" -Exclude "_internal" | ForEach-Object {
    if ($_.PSIsContainer) {
        Write-Host "  📁 $($_.Name)/" -ForegroundColor Green
    } else {
        Write-Host "  📄 $($_.Name)" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ✅ BUILD SUCCESSFUL!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Test the executable: dist\Supervertaler_v2.4.1\Supervertaler.exe"
Write-Host "  2. Upload ZIP to GitHub: Supervertaler_v2.4.1_Windows.zip"
Write-Host "  3. See: docs\GITHUB_RELEASE_v2.4.1_INSTRUCTIONS.md"
Write-Host ""
