# 🔐 Critical .gitignore Entries - Never Remove!

## ESSENTIAL SECURITY ENTRIES

These entries **MUST ALWAYS** be in `.gitignore`. Removing them risks leaking sensitive data:

| Entry | Why Critical | Contains | Impact if Leaked |
|-------|-------------|----------|------------------|
| `user data_private/` | **PRIMARY** - All private data | Strategic plans, business documents, confidential prompts, private projects, test files | 🔴 CATASTROPHIC |
| `api_keys.txt` | Credentials | OpenAI, Anthropic, Google API keys | 🔴 CRITICAL - API abuse |
| `user data/System_prompts_private/` | Private prompts | Specialized AI instructions, custom domain knowledge | 🟠 HIGH |
| `user data/Custom_instructions_private/` | User settings | Personal translation preferences, custom rules | 🟠 HIGH |
| `user data/Projects_private/` | Private work | Confidential client documents, test data | 🟠 HIGH |

## What's Inside `user data_private/`

**DO NOT TRACK THIS FOLDER:**
- Strategic discussion archives (business plans, monetization strategy)
- Private prompt libraries (custom AI instructions)
- Private projects (client work, confidential documents)
- Test documents (may contain sensitive information)
- Translation resources (private glossaries, terminology)
- PDF files with extracted content
- Screenshots and sensitive images

## How to Prevent Accidental Removal

### ✅ Before Refactoring .gitignore

**Checklist:**
```bash
# 1. Create a backup
cp .gitignore .gitignore.backup

# 2. Make your changes
# ... edit .gitignore ...

# 3. Verify critical entries still exist
grep "^user data_private/$" .gitignore
grep "^api_keys.txt$" .gitignore

# 4. Compare with backup
diff .gitignore.backup .gitignore
```

### ✅ After Making Changes

**Verify before committing:**
```bash
# Check what changed
git diff .gitignore

# Make sure you're NOT removing these:
git diff .gitignore | grep -E "^-.*user data_private"  # Should return nothing
git diff .gitignore | grep -E "^-.*api_keys.txt"       # Should return nothing
```

### ✅ If You Accidentally Remove Them

**Immediate recovery:**
```bash
# Option 1: Discard all .gitignore changes
git checkout -- .gitignore

# Option 2: Restore from backup
cp .gitignore.backup .gitignore
git add .gitignore

# Option 3: Just re-add the missing entries manually
echo "user data_private/" >> .gitignore
echo "api_keys.txt" >> .gitignore
git add .gitignore
```

## Installing the Pre-Commit Hook

The pre-commit hook will **prevent** these entries from being removed:

### Installation (One-time)

**Option 1: Manual Setup**
```bash
# Copy hook to git hooks directory
cp .dev/git-hooks/pre-commit-security .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# Verify it's working
echo "user data_private/" > .gitignore.test
rm .gitignore.test
git add .gitignore
git commit -m "test"  # Should show security warning
```

**Option 2: Automated Setup (add to setup script)**
```bash
#!/bin/bash
if [ ! -f .git/hooks/pre-commit ]; then
    cp .dev/git-hooks/pre-commit-security .git/hooks/pre-commit
    chmod +x .git/hooks/pre-commit
    echo "✅ Pre-commit security hook installed"
fi
```

## CI/CD Verification

GitHub Actions will also verify these entries:
- Runs on every Pull Request
- Checks that critical entries are NOT removed
- Blocks merges if violations detected

See: `.github/workflows/security-checks.yml`

## What to Do If This Happens Again

**If critical entries are removed despite safeguards:**

1. **DO NOT PANIC** - This has happened once, we have defenses now
2. Check the git log: `git log --oneline -- .gitignore`
3. Identify the problematic commit
4. Create a fix commit that restores the entries
5. Review who made the change and why
6. Consider additional training for contributors

## Testing the Protections

**Test that the pre-commit hook works:**

```bash
# Create a test branch
git checkout -b test/gitignore-protection

# Try to remove a critical entry
sed -i '/user data_private/d' .gitignore

# Stage the change
git add .gitignore

# Try to commit (should FAIL)
git commit -m "test removal"

# Expected: Pre-commit hook blocks the commit
# ❌ SECURITY VIOLATION: Attempting to remove critical entry: user data_private/

# Clean up test
git checkout -- .gitignore
git checkout main
git branch -D test/gitignore-protection
```

## Key Contacts

**If you have questions about security:**
- Review: `.dev/SECURITY_INCIDENT_ROOT_CAUSE.md`
- Check: `.dev/SECURITY_INCIDENT_CLEANUP.md`
- Contact: Project maintainers

## Reference Dates

- **Incident Date**: October 15, 2025 (removal from .gitignore)
- **Discovery Date**: October 19, 2025
- **Resolution Date**: October 19, 2025
- **Prevention Implemented**: October 19, 2025

---

**Status**: 🔐 PROTECTED - Pre-commit hooks and CI/CD verification active  
**Last Updated**: October 19, 2025
