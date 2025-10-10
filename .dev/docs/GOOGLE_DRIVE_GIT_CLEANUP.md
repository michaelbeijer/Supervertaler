# Google Drive + Git: Desktop.ini Cleanup Guide

## The Problem

Google Drive automatically creates `desktop.ini` files in folders to store folder customization settings (icons, views, etc.). When your Git repository is stored in Google Drive, these files get created inside the `.git/refs/` directory, breaking Git's internal reference system.

**Symptoms:**
```
warning: ignoring broken ref refs/desktop.ini
warning: ignoring broken ref refs/heads/desktop.ini
warning: ignoring broken ref refs/remotes/desktop.ini
warning: ignoring broken ref refs/remotes/origin/desktop.ini
warning: ignoring broken ref refs/tags/desktop.ini
```

---

## Quick Fix (Run When Warnings Appear)

Run this PowerShell script to clean up all `desktop.ini` files from the `.git` directory:

```powershell
# Navigate to repository root
cd "C:\Users\mbeijer\My Drive\Software\Python\Supervertaler"

# Remove all desktop.ini files from .git directory
Get-ChildItem -Path .git -Filter desktop.ini -Recurse -Force | Remove-Item -Force

# Verify they're gone
git status
```

---

## Automated Cleanup Script

Save this as `cleanup_desktop_ini.ps1` in your repository root:

```powershell
# cleanup_desktop_ini.ps1
# Removes Google Drive's desktop.ini files from .git directory

$repoPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$gitPath = Join-Path $repoPath ".git"

Write-Host "Cleaning up desktop.ini files from .git directory..." -ForegroundColor Yellow

$desktopIniFiles = Get-ChildItem -Path $gitPath -Filter "desktop.ini" -Recurse -Force -ErrorAction SilentlyContinue

if ($desktopIniFiles) {
    $count = ($desktopIniFiles | Measure-Object).Count
    Write-Host "Found $count desktop.ini file(s). Removing..." -ForegroundColor Cyan
    
    $desktopIniFiles | ForEach-Object {
        Write-Host "  Removing: $($_.FullName)" -ForegroundColor Gray
        Remove-Item $_.FullName -Force
    }
    
    Write-Host "✓ Cleanup complete!" -ForegroundColor Green
} else {
    Write-Host "✓ No desktop.ini files found in .git directory" -ForegroundColor Green
}
```

**Usage:**
```powershell
.\cleanup_desktop_ini.ps1
```

---

## Prevention Strategy

Unfortunately, you **cannot completely prevent** Google Drive from creating `desktop.ini` files. However, you can minimize the issue:

### Option 1: Run Cleanup Before Git Operations
Always run the cleanup script before committing or pushing:
```powershell
.\cleanup_desktop_ini.ps1
git status
git commit -m "Your commit message"
git push
```

### Option 2: Add to Your Workflow
Create a combined script that cleans and commits:

```powershell
# git_safe_commit.ps1
.\cleanup_desktop_ini.ps1
git add -A
git status
# Then manually commit and push
```

### Option 3: Move Repository Out of Google Drive (Not Recommended)
If the issue becomes too problematic, consider:
- Moving the repository to a local folder (e.g., `C:\Git\Supervertaler`)
- Using GitHub as your primary sync/backup
- Only syncing specific files to Google Drive if needed

---

## Why `.gitignore` Doesn't Help

You might notice `desktop.ini` is already in your `.gitignore` file. This prevents `desktop.ini` files in your **working directory** from being tracked, but:

❌ `.gitignore` does **NOT** affect the `.git` directory itself  
❌ Google Drive creates these files directly in `.git/refs/`  
❌ Git's internal directory is not subject to `.gitignore` rules

---

## Long-term Solution

**Best Practice:** Keep your Git repositories outside of Google Drive sync folders.

**Alternative Workflows:**
1. **Primary:** Git repository in local folder (e.g., `C:\Users\mbeijer\Documents\Git\Supervertaler`)
2. **Backup:** GitHub serves as your cloud backup
3. **Optional:** Manually copy specific files to Google Drive for sharing (not the whole repo)

---

## Quick Reference

| When | Command |
|------|---------|
| Before committing | `.\cleanup_desktop_ini.ps1` |
| If you see warnings | `Get-ChildItem -Path .git -Filter desktop.ini -Recurse -Force \| Remove-Item -Force` |
| Check for files | `Get-ChildItem -Path .git -Filter desktop.ini -Recurse -Force` |

---

**Last Updated:** October 10, 2025  
**Related Issue:** Google Drive folder sync conflicts with Git internal structure
