# Git File Operations Guide

## Critical: Preventing Data Loss When Moving/Renaming Files

### The Problem

When files are moved or renamed using standard file system commands (e.g., PowerShell's `Move-Item` or `Rename-Item`), Git initially sees these operations as:
- **Deleted files** in the old location
- **Untracked files** in the new location

If you commit and push in this state, **the files will be deleted from GitHub** and their history lost.

### The Solution

Always use Git's native commands for file operations, or immediately stage changes after using file system commands.

---

## Method 1: Use Git Commands (RECOMMENDED)

### Moving Files

```powershell
# DON'T use:
Move-Item source.py destination/

# DO use:
git mv source.py destination/
```

### Renaming Files

```powershell
# DON'T use:
Rename-Item old_name.py new_name.py

# DO use:
git mv old_name.py new_name.py
```

### Moving Entire Directories

```powershell
# DON'T use:
Move-Item old_folder/ new_location/

# DO use:
git mv old_folder new_location/old_folder
```

**Advantages of `git mv`:**
- ✅ Immediately tracked as a rename/move
- ✅ Automatically staged for commit
- ✅ Preserves file history
- ✅ No risk of accidental deletion

---

## Method 2: Safety Net (If File System Commands Were Used)

If you or an AI assistant already moved files using `Move-Item` or `Rename-Item`:

### Step 1: Stage All Changes
```powershell
git add -A
```

This tells Git to stage everything, allowing it to detect renames.

### Step 2: Verify Git Detected the Renames
```powershell
git status
```

**Look for this (GOOD):**
```
renamed:    old_path/file.py -> new_path/file.py
```

**NOT this (BAD):**
```
deleted:    old_path/file.py
Untracked files:
    new_path/file.py
```

If you see "deleted:" and "Untracked files:", Git didn't detect the rename. Run `git add -A` again.

### Step 3: Commit Only After Verification
```powershell
git commit -m "Reorganize file structure"
git push
```

---

## Workflow Checklist

Before syncing to GitHub after file operations:

- [ ] Run `git status` to check current state
- [ ] Verify files show as `renamed:` not `deleted:`
- [ ] If files show as deleted, run `git add -A`
- [ ] Run `git status` again to verify
- [ ] Only then commit and push

---

## Why This Matters

**Without proper handling:**
- ❌ Files appear deleted from GitHub
- ❌ File history is lost
- ❌ Contributors lose access to the files
- ❌ Previous commits may reference missing files

**With proper handling:**
- ✅ Full file history preserved
- ✅ Git blame still works
- ✅ Commits remain intact
- ✅ Clean repository structure

---

## Quick Reference Commands

| Operation | Command | Auto-Staged? |
|-----------|---------|--------------|
| Move file | `git mv old_path new_path` | Yes ✅ |
| Rename file | `git mv old_name new_name` | Yes ✅ |
| Move directory | `git mv old_dir new_dir` | Yes ✅ |
| Stage after filesystem ops | `git add -A` | Yes ✅ |
| Check status | `git status` | N/A |

---

## Real-World Example

### ❌ Wrong Way (Causes Data Loss)
```powershell
Move-Item docs/ .dev/docs/
git commit -m "Move docs"  # Files show as DELETED!
git push                    # Files removed from GitHub!
```

### ✅ Right Way (Preserves Everything)
```powershell
git mv docs .dev/docs
git status                  # Verify shows "renamed:"
git commit -m "Move docs to .dev/"
git push                    # Files safely moved on GitHub
```

### ✅ Alternative (Recovery Method)
```powershell
Move-Item docs/ .dev/docs/  # Oops, used filesystem command
git status                  # Shows "deleted:" - STOP!
git add -A                  # Stage everything
git status                  # Now shows "renamed:" - SAFE!
git commit -m "Move docs to .dev/"
git push
```

---

## For AI Assistants Working in This Repository

**When asked to move or rename files:**

1. **ALWAYS use `git mv` commands** instead of `Move-Item` or `Rename-Item`
2. **IMMEDIATELY run `git status`** after operations to verify
3. **CHECK for `renamed:` status** - if you see `deleted:`, run `git add -A`
4. **ALERT the user** if anything looks suspicious before they sync

---

## Additional Resources

- [Git Documentation: git-mv](https://git-scm.com/docs/git-mv)
- [Git Documentation: Detecting Renames](https://git-scm.com/docs/git-diff#Documentation/git-diff.txt--M)

---

**Last Updated:** October 10, 2025  
**Related to:** Repository reorganization, version renumbering, file structure cleanup
