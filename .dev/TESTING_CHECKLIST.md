# Testing Checklist: Parallel Folder Structure Implementation

## Pre-Migration Tests

### ✅ Backup Current State
- [ ] Export current chat history (just in case!)
- [ ] Create git commit of current state
- [ ] Note down what files exist in `*_private` folders

## Migration Process

### ✅ Run Migration Script
```powershell
cd .dev
.\migrate_to_parallel_structure.ps1
```

**Expected Results:**
- ✓ Script detects `.supervertaler.local` file
- ✓ Lists all `*_private` folders with file counts
- ✓ Creates new `user data_private/` structure
- ✓ Moves all private files to new locations
- ✓ Removes old empty `*_private` folders
- ✓ Updates git staging

**After Migration, Verify:**
- [ ] All files moved successfully (check migration summary)
- [ ] Old `*_private` folders are gone
- [ ] New `user data_private/` exists with correct subfolders
- [ ] Private files are in correct new locations

## CLASSIC Version (v2.4.3) Testing

### ✅ User Mode Testing (Without .supervertaler.local)

**Setup:**
1. [ ] Rename `.supervertaler.local` to `.supervertaler.local.backup`
2. [ ] Launch `Supervertaler_v2.4.3-CLASSIC.py`

**UI Verification:**
- [ ] No "🔒 DEV MODE" banner visible
- [ ] No private checkboxes visible anywhere
- [ ] Clean, simple interface

**Prompt Library Tests:**
- [ ] Can see public System Prompts
- [ ] Can save new System Prompt (should go to `user data/System_prompts/`)
- [ ] Can load System Prompt
- [ ] Can delete System Prompt
- [ ] No [Private] prefixes visible

**Project Library Tests:**
- [ ] Can see public Projects
- [ ] Can save new Project (should go to `user data/Projects/`)
- [ ] Can load Project
- [ ] Can delete Project
- [ ] No [Private] prefixes visible

**File System Verification:**
- [ ] New prompts saved to: `user data/System_prompts/`
- [ ] New projects saved to: `user data/Projects/`
- [ ] Private folders NOT accessed

### ✅ Dev Mode Testing (With .supervertaler.local)

**Setup:**
1. [ ] Rename `.supervertaler.local.backup` back to `.supervertaler.local`
2. [ ] Launch `Supervertaler_v2.4.3-CLASSIC.py`

**UI Verification:**
- [ ] "🔒 DEV MODE - All data saved to private folders" banner visible (red background)
- [ ] No private checkboxes visible (auto-routing, not UI-based)
- [ ] Same clean interface as user mode

**Prompt Library Tests:**
- [ ] Can see private System Prompts (from `user data_private/System_prompts/`)
- [ ] Can save new System Prompt (should go to `user data_private/System_prompts/`)
- [ ] Can load System Prompt
- [ ] Can delete System Prompt
- [ ] Prompts show WITHOUT [Private] prefix (clean names)

**Project Library Tests:**
- [ ] Can see private Projects (from `user data_private/Projects/`)
- [ ] Can save new Project (should go to `user data_private/Projects/`)
- [ ] Can load Project with all settings restored
- [ ] Can delete Project
- [ ] Projects show WITHOUT [Private] prefix (clean names)

**File System Verification:**
- [ ] New prompts saved to: `user data_private/System_prompts/`
- [ ] New projects saved to: `user data_private/Projects/`
- [ ] Public folders (`user data/`) NOT accessed

**Migration Verification:**
- [ ] Old private prompts accessible (migrated from `System_prompts_private/`)
- [ ] Old private projects accessible (migrated from `Projects_private/`)
- [ ] All migrated files load correctly

## CAT Version (v3.1.0-beta) Testing

### ✅ User Mode Testing (Without .supervertaler.local)

**Setup:**
1. [ ] Ensure `.supervertaler.local` is not present
2. [ ] Launch `Supervertaler_v3.1.0-beta_CAT.py`

**UI Verification:**
- [ ] No "🔒 DEV MODE" banner visible
- [ ] Prompt Library shows public prompts only
- [ ] No "Import as private?" dialogs

**Prompt Library Tests:**
- [ ] Can see public System Prompts and Custom Instructions
- [ ] Can import prompt (no private option shown)
- [ ] Can create new prompt
- [ ] Can load and apply prompts
- [ ] Prompts saved to `user data/System_prompts/` or `user data/Custom_instructions/`

**Translation Tests:**
- [ ] Can import DOCX
- [ ] Can translate segments
- [ ] Can save project
- [ ] Can export files

**File System Verification:**
- [ ] Prompts saved to: `user data/System_prompts/`
- [ ] Instructions saved to: `user data/Custom_instructions/`
- [ ] Projects, TMs, etc. in `user data/` subfolders

### ✅ Dev Mode Testing (With .supervertaler.local)

**Setup:**
1. [ ] Ensure `.supervertaler.local` exists
2. [ ] Launch `Supervertaler_v3.1.0-beta_CAT.py`

**UI Verification:**
- [ ] "🔒 DEV MODE - All data saved to private folders" banner visible (red background)
- [ ] Prompt Library shows private prompts
- [ ] No "Import as private?" dialogs (auto-routes)

**Prompt Library Tests:**
- [ ] Can see private System Prompts and Custom Instructions
- [ ] Can import prompt (automatically goes to private folder)
- [ ] Can create new prompt
- [ ] Can load and apply prompts
- [ ] Prompts saved to `user data_private/System_prompts/` or `user data_private/Custom_instructions/`

**Translation Tests:**
- [ ] Can import DOCX
- [ ] Can translate segments
- [ ] Can save project
- [ ] Can export files
- [ ] All operations work identically to user mode

**File System Verification:**
- [ ] Prompts saved to: `user data_private/System_prompts/`
- [ ] Instructions saved to: `user data_private/Custom_instructions/`
- [ ] Projects, TMs, etc. in `user data_private/` subfolders

**Migration Verification:**
- [ ] Old private prompts/instructions accessible
- [ ] All migrated files load correctly

## Git Integration Testing

### ✅ Git Status Verification

```powershell
git status
```

**Expected:**
- [ ] `user data_private/` shown as untracked (because of .gitignore)
- [ ] Changes to `.gitignore` shown
- [ ] Changes to `.py` files shown
- [ ] Old `*_private/` folders NOT shown (removed)

### ✅ Gitignore Verification

```powershell
git check-ignore -v "user data_private/test.txt"
```

**Expected:**
- [ ] Shows that `user data_private/` is ignored
- [ ] Points to `.gitignore` rule

### ✅ Commit Structure Changes

```powershell
git add .gitignore
git add Supervertaler_v2.4.3-CLASSIC.py
git add Supervertaler_v3.1.0-beta_CAT.py
git add .dev/
git commit -m "Refactor: Parallel folder structure for private data

- Changed from suffix-based (*_private) to parallel structure
- user data/ for public, user data_private/ for dev mode
- Simplified .gitignore (7 lines → 1 line)
- Removed all private UI elements
- Added dev mode status banners
- Auto-routing based on .supervertaler.local flag"
```

**Verify:**
- [ ] Commit includes code changes
- [ ] Commit includes .gitignore update
- [ ] Commit includes migration script
- [ ] Private data NOT included in commit

## Cross-Testing

### ✅ Mode Switching

**Test rapid switching:**
1. [ ] Save prompt in dev mode
2. [ ] Close app, remove `.supervertaler.local`
3. [ ] Open app (user mode) - prompt should NOT be visible
4. [ ] Close app, restore `.supervertaler.local`
5. [ ] Open app (dev mode) - prompt should be visible

### ✅ File Isolation

**Test data separation:**
- [ ] Public folder only contains test/demo data
- [ ] Private folder contains your personal data
- [ ] No accidental mixing of public/private data

## Performance Testing

### ✅ Load Times
- [ ] App launches quickly in both modes
- [ ] Prompt library loads quickly
- [ ] Project library loads quickly
- [ ] No performance degradation

## Error Handling

### ✅ Edge Cases
- [ ] What happens if `user data_private/` doesn't exist? (should create automatically)
- [ ] What happens if `.supervertaler.local` is created mid-session? (app continues in same mode)
- [ ] What happens if a folder is empty? (should handle gracefully)

## Final Verification

### ✅ Clean Repository State
- [ ] `git status` shows only intended changes
- [ ] No private data tracked
- [ ] `.gitignore` working correctly
- [ ] No leftover `*_private/` folders

### ✅ Documentation
- [ ] Update README.md with dev mode instructions (if needed)
- [ ] Update INSTALLATION.md (if needed)
- [ ] Update .dev/PRIVATE_FEATURES_IMPLEMENTATION.md

### ✅ User Experience
- [ ] Public users won't see any private features
- [ ] Dev mode is clearly indicated
- [ ] No confusing UI elements
- [ ] Everything "just works"

---

## Sign-Off

**Tested by:** _______________  
**Date:** _______________  
**All tests passed:** [ ] Yes [ ] No  
**Issues found:** _______________  

**Notes:**
