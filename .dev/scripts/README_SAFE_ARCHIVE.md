# Safe Archive System

## Purpose
**NEVER DELETE FILES PERMANENTLY** - Always archive them first so they can be recovered.

## Archive Location
All archived files are stored **OUTSIDE the workspace** at:
```
C:\Dev\Supervertaler_Archive\
```

Files are organized by month (YYYY-MM) and include:
- The original file with a timestamp
- A `.meta.txt` file with metadata (original path, reason, date, etc.)

## Usage

### Archive a Single File
```powershell
.\safe_archive.ps1 -Path "path\to\file.txt" -Reason "Cleanup old logs"
```

### Archive Multiple Files
```powershell
.\safe_archive_bulk.ps1 -Paths @("file1.txt", "file2.txt", "folder\*") -Reason "Project reorganization"
```

### From Any Location
```powershell
# Add to your PowerShell profile or use full path
C:\Dev\Supervertaler\.dev\scripts\safe_archive.ps1 -Path "myfile.txt" -Reason "Testing"
```

## Examples

### Archive old chat histories
```powershell
.\safe_archive_bulk.ps1 -Paths @(
    "docs\sessions\old_session.txt",
    "copilot_chat_history_*.txt"
) -Reason "Moving to new storage location"
```

### Archive before cleanup
```powershell
# Before deleting anything, archive it first
.\safe_archive.ps1 -Path "temp_file.py" -Reason "No longer needed"
```

## Benefits
1. ✅ **Recovery Safety** - Can always recover archived files
2. ✅ **Full Metadata** - Know why, when, and from where files were archived
3. ✅ **Outside Workspace** - Won't clutter your git repo
4. ✅ **Organized by Date** - Easy to find recent archives
5. ✅ **Backup-Friendly** - Archive folder can be included in backups

## Important Notes
- Archive location is **NOT** in your git repository
- Include `C:\Dev\Supervertaler_Archive` in your Macrium backups!
- Files are copied first, then deleted (safe operation)
- Each archived file gets a unique timestamp to prevent overwrites

## Copilot Instructions
**For GitHub Copilot:**
- Before deleting ANY file, ALWAYS use `safe_archive.ps1` first
- Use `safe_archive_bulk.ps1` for multiple files
- Never use direct `Remove-Item` or `rm` commands on user files
- Always provide a clear `-Reason` parameter

## Recovery

### Easy Way (Interactive)
```powershell
.\browse_archives.ps1
```
This will:
- Show all archived files for the current month
- Let you view file contents
- Restore files to their original location with one command

### Manual Way
1. Go to `C:\Dev\Supervertaler_Archive\YYYY-MM\`
2. Check the `.meta.txt` file to see the original location
3. Copy the archived file back to its original location
4. Remove the timestamp from the filename if desired

### Browse Specific Month
```powershell
.\browse_archives.ps1 -Month "2025-10"
```

### Search for Specific Files
```powershell
.\browse_archives.ps1 -SearchPattern "*chat*"
```
