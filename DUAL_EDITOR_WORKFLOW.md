# Dual Editor Workflow - VS Code & Cursor

**Date**: October 30, 2025  
**Context**: Working safely with both VS Code and Cursor on the same Supervertaler repo

---

## Summary

You can work on the Supervertaler project in **both VS Code and Cursor** interchangeably without issues. Cursor has already configured your repo for this.

---

## Configuration Files Added

### `.editorconfig`
- **Purpose**: Standardizes formatting rules across both editors
- **Settings**:
  - UTF-8 encoding for all files
  - LF (Unix) line endings (except Windows scripts)
  - 4-space indentation
  - Automatic final newline
  - CRLF only for `.bat` and `.ps1` files

### `.gitattributes`
- **Purpose**: Normalizes line endings in Git repository
- **Settings**:
  - Auto-detects text vs. binary files
  - Enforces LF line endings in repo (prevents CRLF noise)
  - Binary file preservation for images, PDFs, ZIP files

**Result**: No more "file changed on disk" conflicts from line-ending diffs

---

## Safe Workflow

### Before Switching Editors

Always follow this sequence:

```
VS Code session complete
    ↓
git add .
git commit -m "descriptive message"
git push
    ↓
Switch to Cursor (or vice versa)
    ↓
git pull
Start editing
    ↓
git add .
git commit -m "descriptive message"
git push
    ↓
Back to VS Code
git pull
```

### Key Rules

1. **Pull before you start** - Always `git pull` when switching editors
2. **Push when done** - Commit and push before switching
3. **Avoid concurrent edits** - Don't have both editors open on the same file
4. **No file-changed prompts** - If you get "file changed on disk" warnings, one editor is lagging

---

## Common Scenarios

### Scenario 1: VS Code → Cursor Same Day

```powershell
# In VS Code
git add .
git commit -m "feat: add feature X"
git push

# Close VS Code
# Open Cursor

# In Cursor
git pull  # ← IMPORTANT
# Now you see all VS Code changes
# Edit code...
git add .
git commit -m "fix: improve feature X"
git push
```

### Scenario 2: Cursor → VS Code Next Morning

```powershell
# Cursor session from yesterday was pushed
# Open VS Code

# In VS Code
git pull  # ← IMPORTANT - gets Cursor changes from yesterday
# See all Cursor edits from yesterday
# Continue working...
```

### Scenario 3: Non-Fast-Forward Error

If you forgot to pull and get this error:
```
! [rejected] main -> main (non-fast-forward)
error: failed to push some refs to 'origin/main'
```

**Resolution**:
```powershell
git fetch origin
git rebase origin/main
# or
git pull --rebase
git push
```

---

## Configuration Verification

### Check `.editorconfig` Applied
```powershell
# Open any Python file in both editors
# Should see:
# - 4-space indentation
# - LF line endings (status bar: "LF" not "CRLF")
# - UTF-8 encoding
```

### Check `.gitattributes` Applied
```powershell
# Image files should be marked as binary
git ls-files --stage | grep -E "\.(png|jpg|gif)"
# Should show: 160000 or binary marker
```

---

## Line Ending Detection

### VS Code
- Status bar (bottom right) shows **"CRLF"** or **"LF"**
- `.editorconfig` forces **"LF"** for Python files
- `.gitattributes` normalizes on push

### Cursor
- Should respect `.editorconfig` automatically
- If not, go to Settings and set End of Line to `\n` (LF)

---

## Troubleshooting

### "File was modified on disk" prompt

**Cause**: One editor edited the file, other editor is out of sync

**Solution**:
```powershell
# In the editor showing the prompt
# Click "Revert" or "Reload"
git pull  # Make sure you have latest
```

### Different formatting between edits

**Cause**: Editors have different formatter settings

**Solution**:
```powershell
# Verify both use same formatter:
# VS Code: Install Pylance + Python extension
# Cursor: Should auto-detect .editorconfig
# Both should use black/flake8 if configured
```

### Line ending diff noise

**Cause**: Mixing CRLF and LF

**Solution**: 
```powershell
# Normalize to LF (should be automatic now)
git config core.autocrlf input  # On Windows
git add -A
git commit -m "normalize line endings"
git push
```

---

## Best Practices

✅ **DO**:
- Pull before starting
- Push before switching
- Use meaningful commit messages
- Keep sessions in different branches if working in parallel
- Let .editorconfig handle formatting

❌ **DON'T**:
- Edit the same file in both editors simultaneously
- Skip `git pull` when switching editors
- Force push (unless you really know why)
- Commit large generated files or `.vscode/` settings

---

## Performance & Watchers

### File Watchers
- VS Code watches for file changes
- Cursor watches for file changes
- Don't run both with active file watchers on the same file at once
- This is only a problem if you have a watcher running the same process (e.g., pytest --watch)

### Python Interpreters
- Use the **same Python venv/interpreter** in both editors
- If different, you might see different dependency resolutions
- Recommended: Set Python interpreter path explicitly in both

---

## Git Best Practices Summary

| Action | Command | When |
|--------|---------|------|
| Start session | `git pull` | Before any editing |
| Save work | `git add .` `git commit -m "..."` | After feature/fix |
| Publish | `git push` | Before switching editors |
| Update | `git pull` | After switching editors |
| Branch for experiments | `git checkout -b feature/name` | Parallel work |
| Merge back | `git merge feature/name` | Ready to integrate |

---

## Example Timeline

```
Monday 9 AM - VS Code
├─ git pull
├─ Edit Supervertaler_Qt.py
├─ git add .
├─ git commit -m "feat: improve UI layout"
├─ git push ← Ready to switch
└─ Close VS Code

Monday 2 PM - Cursor
├─ git pull ← Get Monday 9 AM changes
├─ Edit modules/translation_results_panel.py
├─ git add .
├─ git commit -m "fix: font size handling"
├─ git push ← Ready to switch
└─ Close Cursor

Tuesday 9 AM - VS Code
├─ git pull ← Get Monday 2 PM changes from Cursor
├─ See the font size fix
├─ Continue work...
```

---

## References

- **EditorConfig**: https://editorconfig.org/
- **Git Attributes**: https://git-scm.com/docs/gitattributes
- **VS Code + EditorConfig**: Requires "EditorConfig for VS Code" extension (usually pre-installed)
- **Cursor + EditorConfig**: Built-in support

---

## Quick Checklist Before Using Cursor

- [x] `.editorconfig` exists and is committed
- [x] `.gitattributes` exists and is committed
- [x] `git push` completed in VS Code
- [x] Cursor has same Python interpreter configured
- [x] `.editorconfig` extension installed in Cursor (if needed)
- [x] Both editors use LF line endings (not CRLF)

You're all set! 🚀
