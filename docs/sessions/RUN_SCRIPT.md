# How to Run the Chat Log Script

## Quick Method

### Step 1: Open PowerShell
- Press **Windows Key**, type `powershell`, press **Enter**
- OR: Right-click **Start button** → **Windows PowerShell** or **Terminal**

### Step 2: Navigate to Repository
```powershell
cd C:\Dev\Supervertaler
```

### Step 3: Run Script
```powershell
.\docs\sessions\save_chat_log.ps1
```

---

## Alternative: File Explorer Method

1. Open **File Explorer**
2. Navigate to: `C:\Dev\Supervertaler`
3. In the address bar, type: `powershell` and press **Enter**
   - This opens PowerShell in that folder
4. Run:
   ```powershell
   .\docs\sessions\save_chat_log.ps1
   ```

---

## If You Get an Error: "Execution Policy"

If PowerShell says:
```
.\save_chat_log.ps1 : File cannot be loaded because running scripts is disabled
```

**Fix it (run once):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try running the script again.

**What this does:** Allows you to run local PowerShell scripts (safe)

---

## Visual Guide

```
1. Windows Key → Type "powershell" → Enter
   
   ┌─────────────────────────────┐
   │ Windows PowerShell          │
   │ PS C:\Users\YourName>       │
   │                             │
   └─────────────────────────────┘

2. Type: cd C:\Dev\Supervertaler
   
   ┌─────────────────────────────┐
   │ Windows PowerShell          │
   │ PS C:\Dev\Supervertaler>    │
   │                             │
   └─────────────────────────────┘

3. Type: .\docs\sessions\save_chat_log.ps1
   
   ┌─────────────────────────────┐
   │ Windows PowerShell          │
   │ PS C:\Dev\Supervertaler>    │
   │ .\docs\sessions\save_chat_log.ps1
   │                             │
   │ 📋 Cursor Chat Log Saver    │
   │ ✅ Found content in clipboard!
   │ ...
   └─────────────────────────────┘
```

---

## Troubleshooting

### "Cannot find path"
- Make sure you're in `C:\Dev\Supervertaler` folder
- Check the path exists: `dir docs\sessions\save_chat_log.ps1`

### "Permission denied"
- Run PowerShell as Administrator:
  - Right-click PowerShell → "Run as Administrator"
  - Then navigate and run script

### "Script won't execute"
- Run the ExecutionPolicy command above
- Or right-click script → "Run with PowerShell"

---

## Quick Copy-Paste

Copy this entire block into PowerShell:
```powershell
cd C:\Dev\Supervertaler
.\docs\sessions\save_chat_log.ps1
```

---

**That's it!** The script will guide you through the rest. 🚀

