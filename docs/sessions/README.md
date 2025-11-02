# Chat Sessions & History

This folder contains development session documentation and chat history logs.

## Contents

### 📝 Session Summaries (Markdown)
- `SESSION_SUMMARY_*.md` - Structured summaries of development sessions
- Created manually to document major changes and decisions
- Safe to commit to git

### 💬 Chat History Logs (Text)
- `cursor_chat_history_*.txt` - Complete chat transcripts from Cursor AI sessions
- Contains full conversation history for each day
- **NOT committed to git** (may contain sensitive info)
- Backed up via Macrium and stored here for reference

## File Naming Convention

### Session Summaries
```
SESSION_SUMMARY_YYYY-MM-DD_Description.md
```
Example: `SESSION_SUMMARY_2025-10-29_Afternoon.md`

### Chat History Logs
```
cursor_chat_history_YYYY-MM-DD (MB).txt
```
Example: `cursor_chat_history_2025-11-01 (MB).txt`

## Daily Chat Export Workflow

### ⚡ Quick Method (Recommended - 30 seconds)
**Note:** Cursor's "Copy All" feature doesn't work, and `Ctrl+A` selects editor content. Use manual selection:

1. **In Cursor**: 
   - **Click on any chat message** (the text area, not the input box)
   - **Scroll to top**, click on first message
   - **Scroll to bottom**, hold **Shift** and click on last message
   - Press `Ctrl+C` to copy
   
   📖 **Detailed instructions:** See `CURSOR_CHAT_SELECTION_GUIDE.md`

2. **In PowerShell** (from repo root):
   ```powershell
   .\docs\sessions\save_chat_log.ps1
   ```

3. **Script will**:
   - Detect clipboard content automatically
   - Ask if you want to use it (press Y)
   - Generate filename with today's date
   - Save to `docs/sessions/`
   - Optionally open file for verification

### 📋 Alternative: Manual Paste Mode
If clipboard detection doesn't work:

1. Run the script first: `.\docs\sessions\save_chat_log.ps1`
2. When prompted, paste content directly into PowerShell
3. Script will save automatically

### 📝 Fully Manual Method (Last Resort)
1. Select all chat in Cursor (`Ctrl+A`) and copy (`Ctrl+C`)
2. Create new file: `docs\sessions\cursor_chat_history_YYYY-MM-DD (MB).txt`
3. Paste content and save

### Automation Options
- **Windows Task Scheduler**: Set reminder at end of day
- **Keyboard shortcut**: Create shortcut to save script
- **Cursor extension**: (Future) Potential Cursor extension for auto-export

## Privacy & Git

- ✅ Session summaries (`.md`) - Safe for git (curated content)
- ❌ Chat history logs (`.txt`) - Excluded from git via `.gitignore`

The `.gitignore` file includes:
```
docs/sessions/cursor_chat_history*.txt
docs/sessions/copilot_chat_history*.txt
```

## Backup Recommendations

1. **Include in Macrium Backup:**
   - `C:\Dev\Supervertaler\docs\sessions\`
   - `C:\Dev\Supervertaler_Archive\` (safe deletion archive)

2. **Manual Backup:** Consider periodically backing up to external drive

## Migration Notes

**Legacy Files:**
- Old Copilot chat logs: `copilot_chat_history_*.txt` (GitHub Copilot from VSCode era)
- New Cursor chat logs: `cursor_chat_history_*.txt` (Cursor AI from 2025-11-01+)

Both patterns are gitignored and follow the same naming convention.

---

**Last Updated:** November 1, 2025  
**Status:** ✅ System active for Cursor chat log archiving
