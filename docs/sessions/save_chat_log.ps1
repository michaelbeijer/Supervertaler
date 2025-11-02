# Save Cursor Chat Log Script
# Usage: 
#   1. In Cursor: Select chat messages manually, then Ctrl+C (copy)
#   2. Run this script - it will detect clipboard automatically
#   3. Or run script first, then paste when prompted

$ErrorActionPreference = "Stop"

# Get paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent (Split-Path -Parent $ScriptDir)
$SessionsDir = Join-Path $RepoRoot "docs\sessions"

# Ensure sessions directory exists
if (-not (Test-Path $SessionsDir)) {
    New-Item -ItemType Directory -Path $SessionsDir -Force | Out-Null
    Write-Host "[OK] Created sessions directory: $SessionsDir" -ForegroundColor Green
}

# Generate filename with today's date
$DateString = Get-Date -Format "yyyy-MM-dd"
$Filename = "cursor_chat_history_$DateString (MB).txt"
$FilePath = Join-Path $SessionsDir $Filename

# Check if file already exists
if (Test-Path $FilePath) {
    Write-Host ""
    Write-Host "[!] File already exists: $Filename" -ForegroundColor Yellow
    $Choice = Read-Host "Overwrite? (Y/N)"
    if ($Choice -ne "Y" -and $Choice -ne "y") {
        Write-Host "[X] Operation cancelled." -ForegroundColor Yellow
        exit 0
    }
}

Write-Host ""
Write-Host "Cursor Chat Log Saver" -ForegroundColor Cyan
Write-Host ("=" * 50) -ForegroundColor Gray

# Try to get from clipboard first (preferred method)
$ChatContent = $null
try {
    $ClipboardContent = Get-Clipboard -Raw -ErrorAction SilentlyContinue
    if ($ClipboardContent -and $ClipboardContent.Trim().Length -gt 50) {
        # Validate clipboard content - reject if it looks like error output
        $IsErrorOutput = $ClipboardContent -match "(ParseException|CategoryInfo|MissingArgument|Unexpected token|At line \d+)" -or 
                         $ClipboardContent -match "PowerShell Extension" -or
                         $ClipboardContent -match "Copyright.*Microsoft"
        
        if ($IsErrorOutput) {
            Write-Host ""
            Write-Host "[!] Clipboard contains PowerShell error output, not chat content." -ForegroundColor Yellow
            Write-Host "   Please copy your CHAT messages from Cursor instead." -ForegroundColor Yellow
            Write-Host ""
            $ClipboardContent = $null  # Clear it so we go to alternative method
        } else {
            $Preview = $ClipboardContent.Substring(0, [Math]::Min(150, $ClipboardContent.Length))
            Write-Host ""
            Write-Host "[OK] Found content in clipboard!" -ForegroundColor Green
            Write-Host "   Preview: $Preview..." -ForegroundColor Gray
            Write-Host "   Size: $($ClipboardContent.Length) characters" -ForegroundColor Gray
            Write-Host ""
            $UseClipboard = Read-Host "Use clipboard content? (Y/N, default: Y)"
            if ($UseClipboard -eq "" -or $UseClipboard -eq "Y" -or $UseClipboard -eq "y") {
                $ChatContent = $ClipboardContent
            }
        }
    } else {
        Write-Host ""
        Write-Host "[!] Clipboard is empty or too short." -ForegroundColor Yellow
        Write-Host "   Please copy chat content from Cursor first." -ForegroundColor Yellow
    }
} catch {
    Write-Host ""
    Write-Host "[!] Could not read from clipboard: $_" -ForegroundColor Yellow
}

# If no clipboard content, use file-based paste method
if ([string]::IsNullOrWhiteSpace($ChatContent)) {
    Write-Host ""
    Write-Host "Alternative Method: File Paste" -ForegroundColor Cyan
    Write-Host "   Creating temporary file for you to paste into..." -ForegroundColor Gray
    
    $TempFile = Join-Path $env:TEMP "cursor_chat_paste_$DateString.txt"
    
    # Create instruction file
    $Instructions = @"
Please follow these steps:
1. This Notepad window will open
2. Go to Cursor and select all chat (Ctrl+A)
3. Copy it (Ctrl+C)
4. Paste into this Notepad window (Ctrl+V)
5. Save (Ctrl+S) and close Notepad
6. Come back here and press Enter

File location: $TempFile
"@
    
    Write-Host $Instructions -ForegroundColor White
    
    # Create empty file and open in Notepad
    "" | Out-File -FilePath $TempFile -Encoding UTF8
    
    try {
        Start-Process notepad.exe -ArgumentList $TempFile -Wait
        Write-Host ""
        Write-Host "[OK] Notepad closed. Reading file..." -ForegroundColor Green
        
        if (Test-Path $TempFile) {
            $ChatContent = Get-Content -Path $TempFile -Raw -Encoding UTF8
            Remove-Item $TempFile -ErrorAction SilentlyContinue
        }
        
        if ([string]::IsNullOrWhiteSpace($ChatContent)) {
            Write-Host "[X] No content found in file. Exiting." -ForegroundColor Red
            exit 1
        }
    } catch {
        Write-Host "[X] Error with file method: $_" -ForegroundColor Red
        Write-Host ""
        Write-Host "Please use manual method:" -ForegroundColor Yellow
        Write-Host "   1. Create: $FilePath" -ForegroundColor Gray
        Write-Host "   2. Paste chat content and save" -ForegroundColor Gray
        exit 1
    }
}

# Validate content
if ([string]::IsNullOrWhiteSpace($ChatContent)) {
    Write-Host "[X] No content provided. Exiting." -ForegroundColor Red
    exit 1
}

# Add header with metadata
$Header = @"
========================================
Cursor Chat Log - $DateString
Saved: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
========================================

"@

$FullContent = $Header + $ChatContent

# Save to file
try {
    $FullContent | Out-File -FilePath $FilePath -Encoding UTF8
    $FileSize = (Get-Item $FilePath).Length
    $FileSizeKB = [math]::Round($FileSize / 1KB, 2)
    
    Write-Host ""
    Write-Host "[OK] Chat log saved successfully!" -ForegroundColor Green
    Write-Host "   File: $FilePath" -ForegroundColor Cyan
    Write-Host "   Size: $FileSizeKB KB" -ForegroundColor Cyan
    
    # Ask if user wants to open the file
    Write-Host ""
    $OpenFile = Read-Host "Open file for verification? (Y/N)"
    if ($OpenFile -eq "Y" -or $OpenFile -eq "y") {
        Start-Process notepad.exe -ArgumentList $FilePath
    }
    
    Write-Host ""
    Write-Host "[OK] Done! Chat log archived." -ForegroundColor Green
    
} catch {
    Write-Host ""
    Write-Host "[X] Error saving file: $_" -ForegroundColor Red
    exit 1
}
