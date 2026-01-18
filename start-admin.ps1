# Start Beijerterm Admin Panel in Development Mode
# Double-click this file to start the admin panel at http://localhost:5000

Write-Host "🌐 Starting Beijerterm Admin Panel..." -ForegroundColor Cyan
Write-Host ""

Set-Location "$PSScriptRoot\beijerterm\admin"

try {
    python start_dev.py
} catch {
    Write-Host "❌ Error starting admin panel: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}
