# 🚨 Security Incident Prevention Plan

## Incident Summary
- **Date**: October 15, 2025 (discovery: October 19, 2025)
- **Root Cause**: `user data_private/` was **accidentally removed** from `.gitignore` during refactoring commit `4b88cf1`
- **Impact**: Private data was tracked and pushed to GitHub
- **Resolution**: Forced history rewrite, folder removed, security rule re-added

## Root Cause Analysis

**The Mistake**: During a large refactoring, `.gitignore` was simplified and `user data_private/` entry was inadvertently deleted:

```diff
# Commit 4b88cf1 (Oct 15, 2025)
-# PRIVATE USER DATA (Dev Mode Only)
-# When .supervertaler.local exists, all user data saves to user data_private/
-user data_private/
+# (replaced with other rules, but user data_private forgotten)
```

This was a **refactoring oversight** - the entry was deleted without realizing its importance.

## Prevention Measures

### ✅ 1. .gitignore Safety Checks

**What to do before any refactoring of .gitignore:**
- Create a checklist of CRITICAL entries to never remove:
  - ❌ `user data_private/` - Contains ALL private data
  - ❌ `api_keys.txt` - API credentials
  - ❌ `user data/System_prompts_private/` - Private prompts
  - ❌ `user data/Custom_instructions_private/` - User settings
  - ❌ `user data/Projects_private/` - Private projects

- **Before committing any .gitignore changes**:
  ```bash
  # Verify these lines still exist
  git diff .gitignore | grep "user data_private"
  git diff .gitignore | grep "api_keys.txt"
  ```

### ✅ 2. Pre-Commit Hook

Create a Git pre-commit hook to prevent these entries from being removed:

**File**: `.git/hooks/pre-commit`

```bash
#!/bin/bash

# Check if .gitignore still contains critical security entries
GITIGNORE=".gitignore"
CRITICAL_ENTRIES=("user data_private/" "api_keys.txt")

if git diff --cached "$GITIGNORE" | grep -E "^-" | grep -qE "user data_private|api_keys.txt"; then
    echo "❌ ERROR: You're attempting to remove CRITICAL security entries from .gitignore!"
    echo "   Critical entries that must ALWAYS be in .gitignore:"
    echo "   - user data_private/"
    echo "   - api_keys.txt"
    echo ""
    echo "   If this is intentional, add --no-verify to override:"
    echo "   git commit --no-verify"
    exit 1
fi

# Check that critical entries are still present
for entry in "${CRITICAL_ENTRIES[@]}"; do
    if ! grep -q "^$entry" "$GITIGNORE"; then
        echo "❌ ERROR: $entry is missing from .gitignore!"
        echo "   Please restore this critical security entry."
        exit 1
    fi
done

exit 0
```

**Install the hook:**
```bash
cp .dev/.git-hooks/pre-commit-security .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### ✅ 3. Documentation - Critical Security Entries

**File**: `.dev/CRITICAL_GITIGNORE_ENTRIES.md`

```markdown
# ⚠️ CRITICAL .gitignore Entries

These entries MUST NEVER be removed from .gitignore:

| Entry | Reason | Contains |
|-------|--------|----------|
| `user data_private/` | **PRIMARY** - Contains ALL private data | Strategic plans, prompts, projects, credentials |
| `api_keys.txt` | API credentials | OpenAI, Anthropic, Google keys |
| `user data/System_prompts_private/` | Private AI prompts | Custom specialized instructions |
| `user data/Custom_instructions_private/` | User settings | Personal translation preferences |
| `user data/Projects_private/` | Private projects | Confidential client documents |

**If any of these are accidentally removed:**
1. ❌ DO NOT COMMIT
2. Restore immediately: `git checkout .gitignore`
3. Report to team
4. Investigate why removal happened
```

### ✅ 4. CI/CD Security Check

Add a GitHub Actions workflow to verify .gitignore:

**File**: `.github/workflows/security-checks.yml`

```yaml
name: Security - Verify .gitignore

on: [pull_request]

jobs:
  gitignore-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check critical .gitignore entries
        run: |
          CRITICAL_ENTRIES=(
            "user data_private/"
            "api_keys.txt"
            "user data/System_prompts_private/"
            "user data/Custom_instructions_private/"
            "user data/Projects_private/"
          )
          
          for entry in "${CRITICAL_ENTRIES[@]}"; do
            if ! grep -q "^$entry" .gitignore; then
              echo "❌ CRITICAL: Missing $entry from .gitignore"
              exit 1
            fi
          done
          echo "✅ All critical .gitignore entries present"
```

### ✅ 5. Code Review Checklist

**When reviewing ANY changes to .gitignore:**
- [ ] All critical entries still present?
- [ ] No new untracked private data paths?
- [ ] Comments explain why entries are critical?
- [ ] No entries accidentally removed during cleanup?

### ✅ 6. Backup Strategy

Create a reference copy of critical entries:

**File**: `.dev/.gitignore.critical`

```
# CRITICAL ENTRIES - If these are ever missing from .gitignore, restore from here!
user data_private/
api_keys.txt
user data/System_prompts_private/
user data/Custom_instructions_private/
user data/Projects_private/
```

## Action Items

- [ ] Add pre-commit hook to .git/hooks/pre-commit
- [ ] Create `.dev/CRITICAL_GITIGNORE_ENTRIES.md` documentation
- [ ] Set up GitHub Actions workflow for .gitignore verification
- [ ] Add to team/contributor guidelines
- [ ] Document in CONTRIBUTING.md
- [ ] Review all recent .gitignore changes

## Testing Prevention

**Verify the protections work:**

```bash
# Test: Try to remove user data_private from .gitignore
# sed -i '/user data_private/d' .gitignore
# git add .gitignore
# git commit -m "test"  # Should FAIL with pre-commit hook

# Test: Manually remove and see pre-commit catch it
grep -v "user data_private" .gitignore > .gitignore.tmp
mv .gitignore.tmp .gitignore
git add .gitignore
git commit -m "test"  # Should FAIL
```

## References

- **Incident commit**: `4b88cf1` (Oct 15, 2025)
- **Removal commit**: `89da7bb` (Oct 19, 2025)
- **History rewrite**: `4786f1f` (Oct 19, 2025)
- **GitHub issue**: None (proactive prevention)

## Status

✅ **Immediate Actions Completed**:
- `user data_private/` removed from GitHub history
- Entry re-added to .gitignore
- Local folder protected

⏳ **Prevention Measures (TODO)**:
- [ ] Pre-commit hook implementation
- [ ] GitHub Actions workflow
- [ ] Documentation update
- [ ] Contributor guidelines

---

**Last Updated**: October 19, 2025  
**Incident Status**: RESOLVED + PREVENTION PLANNED
