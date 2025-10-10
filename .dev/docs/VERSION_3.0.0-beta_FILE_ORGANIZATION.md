# Version 3.0.0-beta - File Organization Summary

> **📌 Version Note**: This version was previously numbered v2.5.2. Renumbered to v3.0.0-beta to reflect major architectural change. See [VERSION_RENUMBERING_v3.0.0.md](VERSION_RENUMBERING_v3.0.0.md).

**Date**: October 9-10, 2025  
**Update**: Version renumbering and file reorganization

---

## 📁 Current File Structure

### Main Directory (`Supervertaler/`)

#### Production Version
- **`Supervertaler_v2.4.1-CLASSIC.py`** ✅
  - Status: Stable production release
  - Features: CafeTran & memoQ bilingual DOCX support
  - Architecture: Original DOCX workflow
  - Recommended for: Professional translation work

#### Beta Version  
- **`Supervertaler_v3.0.0-beta_CAT.py`** ✅ **LATEST**
  - Status: Beta testing (feature-complete, performance optimized)
  - NEW Features:
    - ⚡ Grid pagination (10x faster)
    - 🧠 Smart paragraph detection
    - 🛡️ Enhanced loading protection
  - Architecture: Complete CAT editor rewrite (v3.x = major change)
  - Recommended for: Testing new CAT editor features

### Previous Versions Directory (`previous versions/`)

#### Archived Versions
- **`Supervertaler_v2.5.1 (experimental - CAT editor development)(2025-10-09).py`** 📦
  - Archived: October 9, 2025
  - Reason: Superseded by v2.5.2
  - Contains: Pre-pagination version

- **`Supervertaler_v2.4.0 (stable - production ready)(2025-10-07).py`** 📦
  - Archived: October 7, 2025
  - Reason: Superseded by v2.4.1
  - Contains: Pre-bilingual format support

- *[Other historical versions...]*

---

## 🔄 Changes Made

### October 9, 2025 - Initial Update
#### 1. Version Bump (v2.5.1 → v2.5.2)
- **From**: v2.5.1 → **To**: v2.5.2
- **Reason**: Major performance improvements + new features

#### 2. File Renamed
- **Old**: `Supervertaler_v2.5.1 (experimental - CAT editor development).py`
- **New**: `Supervertaler_v2.5.2 (experimental - CAT editor).py`
- **Changes**:
  - ✅ Version number updated (2.5.1 → 2.5.2)
  - ✅ Name simplified (removed "development" for cleaner look)

#### 3. File Archived
- **Backup created**: `previous versions/Supervertaler_v2.5.1 (experimental - CAT editor development)(2025-10-09).py`
- **Purpose**: Preserve development history
- **Date stamped**: 2025-10-09 for reference

#### 4. Documentation Updated
- ✅ `README.md` - Updated filename reference
- ✅ `CHANGELOG.md` - Added v2.5.2 entry
- ✅ `docs/DOCUMENTATION_UPDATE_v2.5.2.md` - Updated file organization notes
- ✅ Internal version constants updated in source code

### October 10, 2025 - Version Renumbering
#### 5. Major Version Renumbering
- **v2.4.1.py** → **v2.4.1-CLASSIC.py**
  - Added "-CLASSIC" suffix to distinguish DOCX workflow
  - No code changes, filename only
  
- **v2.5.2 (...).py** → **v3.0.0-beta_CAT.py**
  - Renumbered to v3.0.0-beta (major architectural change)
  - Updated all internal version constants
  - "_CAT" suffix indicates CAT editor variant

#### 6. Documentation Updates
- ✅ `README.md` - Updated version table and file references
- ✅ `CHANGELOG.md` - Added v3.0.0-beta entry with renumbering explanation
- ✅ `docs/VERSION_RENUMBERING_v3.0.0.md` - New documentation explaining decision
- ✅ `docs/RELEASE_NOTES_v3.0.0-beta.md` - Renamed and updated
- ✅ `docs/DOCUMENTATION_UPDATE_v3.0.0-beta.md` - Renamed and updated

---

## 📊 Version Comparison

| Version | Status | File Size | Features | Use Case |
|---------|--------|-----------|----------|----------|
| v2.4.1-CLASSIC | Production | ~350KB | Bilingual DOCX (DOCX workflow) | Professional work |
| v3.0.0-beta | Beta | ~420KB | CAT editor + Pagination | Testing/Advanced |

---

## 🎯 Naming Convention

### Current Format (Post-Renumbering)
`Supervertaler_v{VERSION}-{EDITION}_{TAG}.py`

**Examples:**
- `Supervertaler_v2.4.1-CLASSIC.py` - Production, CLASSIC edition (DOCX workflow)
- `Supervertaler_v3.0.0-beta_CAT.py` - Beta status, CAT editor variant

### Legacy Format (Pre-Renumbering)
`Supervertaler_v{MAJOR}.{MINOR}.{PATCH} ({status} - {feature}).py`

**Examples:**
- `Supervertaler_v2.4.1.py` - Production, no special designation
- `Supervertaler_v2.5.2 (experimental - CAT editor).py` - Experimental, CAT editor focus

### Archive Format  
`Supervertaler_v{VERSION} ({status})({YYYY-MM-DD}).py`

**Example:**
- `Supervertaler_v2.5.1 (experimental - CAT editor development)(2025-10-09).py`

---

## ✅ Verification Checklist

- [x] Main directory contains exactly 2 current versions (v2.4.1-CLASSIC, v3.0.0-beta)
- [x] Old v2.5.1 archived with date stamp
- [x] README.md references correct filenames
- [x] CHANGELOG.md updated with v3.0.0-beta and renumbering explanation
- [x] Source code version constants updated (APP_VERSION = "3.0.0-beta")
- [x] Window title shows "v3.0.0-beta"
- [x] Startup log shows "v3.0.0-beta"
- [x] Documentation files updated and renamed
- [x] VERSION_RENUMBERING_v3.0.0.md created to explain decision

---

## 🚀 Recommendation for Users

**For production work**: Use **`Supervertaler_v2.4.1-CLASSIC.py`**  
**For testing/advanced features**: Use **`Supervertaler_v3.0.0-beta_CAT.py`**

**Version Scheme Note**: v3.x represents a major architectural change (CAT editor) from v2.x (DOCX workflow). The "-CLASSIC" and "-beta" suffixes help distinguish these fundamentally different architectures.

---

**All files organized and version numbers consistent!** 🎉
