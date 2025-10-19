# 🔒 Security Setup Guide for Contributors

## Post-Clone Setup

After cloning the Supervertaler repository, run this to set up security protections:

### Automatic Setup (Recommended)

```bash
# Run this script after cloning
.dev\setup-security.ps1
```

### Manual Setup

```bash
# 1. Install pre-commit hook
cp .dev/git-hooks/pre-commit-security .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# 2. Verify .gitignore is correct
cat .gitignore | grep "user data_private"  # Should show: user data_private/
cat .gitignore | grep "api_keys.txt"       # Should show: api_keys.txt

# 3. Test the hook works
echo "Testing security hook..."
# The hook is now active - it will prevent commits that remove critical entries
```

## Understanding .gitignore Protection

### What Gets Protected?

Your pre-commit hook prevents you from accidentally committing:
- ❌ `user data_private/` - Your strategic plans, private prompts, confidential projects
- ❌ `api_keys.txt` - Your API credentials
- ❌ `user data/System_prompts_private/` - Custom private prompts
- ❌ `user data/Custom_instructions_private/` - Private settings
- ❌ `user data/Projects_private/` - Confidential work

### What Happens If You Try?

**Scenario:** You refactor `.gitignore` and accidentally remove `user data_private/`

```bash
# You stage the modified .gitignore
git add .gitignore

# You try to commit
git commit -m "Cleanup .gitignore"

# The pre-commit hook activates:
# ❌ SECURITY VIOLATION: Attempting to remove critical entry: user data_private/
# ❌ ERROR: Missing critical .gitignore entry: user data_private/

# Your commit is BLOCKED ✋
# You must restore the entry before committing
```

## Why This Matters

### The Incident (October 2025)

1. **Oct 15**: `user data_private/` was **accidentally removed** during refactoring
2. **Oct 15-19**: Files were added to the folder (now untracked by .gitignore)
3. **Oct 19**: Entire folder was pushed to GitHub public repository 😱
4. **Oct 19**: Required emergency cleanup with Git history rewrite

**Lessons Learned:**
- One-line mistake in .gitignore caused security incident
- Manual reviews can miss these removals
- Automated checks are essential

## Best Practices

### ✅ DO

- ✅ Always verify `.gitignore` before committing major refactors
- ✅ Use this command to check for critical entry changes:
  ```bash
  git diff .gitignore | grep -E "^-.*user data_private|^-.*api_keys"
  ```
- ✅ Trust the pre-commit hook - it's there to protect you
- ✅ Read security-related error messages carefully
- ✅ Back up `.gitignore` before making changes:
  ```bash
  cp .gitignore .gitignore.backup
  ```

### ❌ DON'T

- ❌ DON'T remove `.gitignore` protections with `--no-verify` unless absolutely necessary
- ❌ DON'T simplify `.gitignore` by removing entries you don't recognize
- ❌ DON'T commit `.gitignore` changes without reviewing them
- ❌ DON'T bypass the pre-commit hook unless you fully understand the implications

## Troubleshooting

### Hook Not Running?

```bash
# Check if hook exists and is executable
ls -la .git/hooks/pre-commit

# If missing, reinstall it
cp .dev/git-hooks/pre-commit-security .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### Need to Override (Use With Caution)

```bash
# Force commit without running pre-commit hook
# ⚠️ ONLY IF YOU ABSOLUTELY KNOW WHAT YOU'RE DOING
git commit --no-verify -m "Your message"

# Immediately verify what you committed
git show HEAD:.gitignore | grep -E "user data_private|api_keys"
```

### Hook Permission Issues on Windows

```powershell
# PowerShell: Set execution policy if needed
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Documentation

- **Overview**: `.dev/CRITICAL_GITIGNORE_ENTRIES.md`
- **Root Cause**: `.dev/SECURITY_INCIDENT_ROOT_CAUSE.md`
- **Cleanup Details**: `.dev/SECURITY_INCIDENT_CLEANUP.md`
- **Hook Source**: `.dev/git-hooks/pre-commit-security`

## Questions?

If you encounter issues:
1. Check `.dev/CRITICAL_GITIGNORE_ENTRIES.md`
2. Review the incident analysis in `.dev/SECURITY_INCIDENT_ROOT_CAUSE.md`
3. Contact project maintainers

---

**Status**: 🔐 PROTECTED  
**Hook Installed**: ✅ Yes  
**Last Updated**: October 19, 2025
