# Documentation Clarification Update - October 6, 2025

## Problem Identified

After repository cleanup, documentation didn't clearly distinguish between:
- **v2.4.0 (stable - production ready)** - Complete and tested
- **v2.5.0 (experimental - CAT editor development)** - Under active development

This could confuse users about which version to use and which documentation applies.

## Solutions Implemented

### 1. ✅ Updated README.md

**Added clear version section** at the top:
```markdown
## 📦 Available Versions

### v2.4.0 (Stable - Production Ready) ✅
- Fully tested and stable
- Complete documentation available
- Ready for professional translation work

### v2.5.0 (Experimental - CAT Editor Development) 🚧
- Under active development
- Features may change without notice
- Testing new CAT editor integration
- Full user guide pending

💡 Recommendation: Use v2.4.0 for production work
```

**Updated Documentation section** to clearly separate:
- v2.4.0: Points to complete User Guide
- v2.5.0: Points to feature-specific guides with note that full guide is pending

**Updated Features section** to show:
- v2.4.0 Feature Matrix
- v2.5.0 Experimental Features (with status indicators)

### 2. ✅ Updated User Guide (v2.4.0)

**Added prominent warning at top**:
```markdown
⚠️ IMPORTANT: This guide is for Supervertaler v2.4.0 (stable - production ready).py only.

If you're using v2.5.0 (experimental - CAT editor development).py, note that 
it's under active development and documentation is in progress.
```

### 3. ✅ Created VERSION_GUIDE.md

Comprehensive guide explaining:
- Which documentation to use for which version
- Status of each documentation set
- Quick reference table
- Guidance for new users
- Guidance for developers

### 4. ✅ Updated docs/README.md

Added prominent notice linking to VERSION_GUIDE.md for navigation help.

## Key Messages Established

### For Users
1. **Use v2.4.0 for production work** - It's stable and fully documented
2. **v2.5.0 is experimental** - Try it for new features, but expect changes
3. **Documentation is version-specific** - Follow the version guide

### For Contributors
1. **v2.4.0 documentation is complete** - User Guide has everything
2. **v2.5.0 documentation is in progress** - Feature-specific guides available
3. **Full v2.5.0 user guide pending** - Will be created once features stabilize

## Files Modified

1. **README.md** - Clear version distinction and documentation links
2. **docs/user_guides/Supervertaler User Guide (v2.4.0).md** - Added version warning
3. **docs/README.md** - Added version guide link
4. **docs/VERSION_GUIDE.md** - NEW - Comprehensive navigation guide

## Benefits

### Clarity
- Users immediately understand which version to use
- Clear documentation pathways for each version
- No confusion about feature availability

### Professionalism
- Sets proper expectations about experimental features
- Guides users to stable version for production
- Transparent about development status

### Maintainability
- Clear separation makes updates easier
- Version-specific docs prevent outdated information
- Easy to track what needs documentation

## Quick Reference

| Question | Answer |
|----------|--------|
| **Which version should I use?** | v2.4.0 for production, v2.5.0 to explore new features |
| **Where's the complete guide?** | `docs/user_guides/Supervertaler User Guide (v2.4.0).md` |
| **What about v2.5.0 docs?** | Feature-specific guides available, full guide pending |
| **How do I navigate docs?** | See `docs/VERSION_GUIDE.md` |
| **Is v2.5.0 ready for work?** | No - it's experimental, use v2.4.0 for production |

## Status

✅ **Complete** - All documentation now clearly indicates version applicability

Users can confidently:
- Choose the right version for their needs
- Find the appropriate documentation
- Understand feature status and stability
- Navigate between stable and experimental features

---

*Update completed: October 6, 2025*
*Related to: Repository cleanup and organization*
