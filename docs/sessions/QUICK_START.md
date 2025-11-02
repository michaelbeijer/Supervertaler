# Quick Start: Saving Cursor Chat Logs

## 🎯 Daily Workflow (30 seconds)

### Option 1: PowerShell Script (Easiest)
```powershell
# 1. In Cursor: Select chat messages manually (see guide below)
# 2. Copy selection (Ctrl+C)
# 3. In PowerShell (from repo root):
.\docs\sessions\save_chat_log.ps1
# 4. Press Y when asked about clipboard → Done!
```

**⚠️ Important:** Cursor's `Ctrl+A` selects editor content, not chat!  
**✅ Use:** Click on chat message → Scroll top → Shift+Click bottom → Ctrl+C  
📖 **Full guide:** `docs/sessions/CURSOR_CHAT_SELECTION_GUIDE.md`

### Option 2: Manual (If script doesn't work)
```powershell
# 1. Copy chat from Cursor
# 2. Create file: docs\sessions\cursor_chat_history_YYYY-MM-DD (MB).txt
# 3. Paste and save
```

## ⚡ Keyboard Shortcut Setup (Windows)

Create a shortcut for even faster access:

1. **Right-click** `save_chat_log.ps1` → **Create Shortcut**
2. **Right-click shortcut** → **Properties**
3. Set **Shortcut key**: `Ctrl+Alt+S` (or your preference)
4. **Run**: Minimized
5. Now just press `Ctrl+Alt+S` after copying chat!

## 📅 Windows Task Scheduler Reminder

Set up a daily reminder at 5 PM:

```powershell
# Run this once to create the reminder:
$Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -WindowStyle Hidden -Command `"Write-Host 'Remember to save today'\''s Cursor chat log! Press Ctrl+Alt+S after copying.'; Start-Sleep -Seconds 10`""
$Trigger = New-ScheduledTaskTrigger -Daily -At 5:00PM
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "Cursor Chat Log Reminder" -Action $Action -Trigger $Trigger -Settings $Settings -Description "Daily reminder to save Cursor chat logs"
```

## 🔍 Verify Saved Logs

Check `docs/sessions/` folder:
- Files should be named: `cursor_chat_history_YYYY-MM-DD (MB).txt`
- Files are automatically gitignored (won't be committed)
- Backup via Macrium includes this folder

## ❓ Troubleshooting

**Script won't run?**
- Right-click PowerShell → "Run as Administrator"
- Or: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**Clipboard not working?**
- Use manual paste method (Option 2 above)
- Or paste content when script prompts

**File already exists?**
- Script will ask if you want to overwrite
- Or manually rename existing file

---

**Goal:** Never lose a day's conversation with Cursor! 📚

