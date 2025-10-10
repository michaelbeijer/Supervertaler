# Version Renumbering: v2.5.2 → v3.0.0-beta

## Executive Summary

On October 9, 2025, we renumbered the experimental CAT editor from **v2.5.2** to **v3.0.0-beta** to better reflect the major architectural change from the original DOCX workflow. This document explains the rationale and details of this decision.

## Rationale

### Problem
The previous version numbering scheme (v2.4.1 vs v2.5.2) suggested these were incremental updates to the same application, when in fact they are **fundamentally different architectures**:

- **v2.4.1**: Original DOCX-based workflow (import DOCX → translate → export DOCX)
- **v2.5.2**: Complete rewrite as segment-based CAT editor with grid/list/document views

### Solution
Adopt semantic versioning to clearly communicate the architectural difference:

- **v2.4.1-CLASSIC**: Original DOCX workflow (dignified "CLASSIC" status for production-ready legacy version)
- **v3.0.0-beta**: CAT editor architecture (major version bump signals major change, "beta" indicates experimental status)

## Version Naming Scheme

### File Naming Convention
```
[Product]_v[VERSION]-[EDITION]_[TAG].py
```

**Examples:**
- `Supervertaler_v2.4.1-CLASSIC.py` - v2.4.1, CLASSIC edition (DOCX workflow)
- `Supervertaler_v3.0.0-beta_CAT.py` - v3.0.0-beta, CAT tag (segment editor)

### Semantic Versioning Rules

**Major version (v3.x vs v2.x):**
- Signals **major architectural change**
- v2.x = DOCX-based workflow
- v3.x = Segment-based CAT editor

**Edition suffix:**
- `-CLASSIC` = Original architecture (not deprecated, still production-ready!)
- `-beta` = Experimental/testing phase

**Tag suffix:**
- `_CAT` = Computer-Aided Translation editor variant

## Timeline of Changes

### 2025-10-09: Version Renumbering

**Files Renamed:**
1. `Supervertaler_v2.4.1.py` → `Supervertaler_v2.4.1-CLASSIC.py`
2. `Supervertaler_v2.5.2 (experimental - CAT editor).py` → `Supervertaler_v3.0.0-beta_CAT.py`

**Internal Constants Updated:**
- v3.0.0-beta file:
  - `APP_VERSION = "2.5.2"` → `APP_VERSION = "3.0.0-beta"`
  - Window title: `"Supervertaler v2.5.2..."` → `"Supervertaler v3.0.0-beta..."`
  - Startup log: `"Supervertaler v2.5.2 ready..."` → `"Supervertaler v3.0.0-beta ready..."`

**Documentation Updated:**
- README.md: Updated version table and file references
- CHANGELOG.md: Added v3.0.0-beta entry, explained renumbering, added note to v2.5.2
- New file: docs/VERSION_RENUMBERING_v3.0.0.md (this document)

## User Communication

### Key Messages

**For v2.4.1-CLASSIC users:**
- ✅ Your version is still **production-ready and fully supported**
- ✅ The "-CLASSIC" suffix gives it **dignified legacy status** (not "deprecated"!)
- ✅ No functional changes - just a filename/branding update
- ✅ Continue using for production work

**For v3.0.0-beta users:**
- 🚀 Major version bump (v3.x) reflects **major architectural rewrite**
- 🧪 "beta" status indicates **experimental/testing phase**
- ⚡ Cutting-edge features: pagination, smart paragraph detection, three view modes
- 📋 Please report issues - this is a completely new architecture

### Migration Path

**Current recommendation:**
- **Production work** → Use v2.4.1-CLASSIC (stable, tested)
- **Testing/feedback** → Try v3.0.0-beta (experimental, feature-rich)

**Future roadmap:**
- v3.0.0-beta → v3.0.0 (stable) once beta testing complete
- v3.1.x, v3.2.x = incremental improvements to CAT editor
- v2.4.x-CLASSIC continues for DOCX workflow users

## Technical Differences

### v2.4.1-CLASSIC (DOCX Workflow)
- **Architecture**: Document-centric
- **Workflow**: Import DOCX → Translate → Export DOCX
- **UI**: Simple single-view interface
- **Use case**: Quick DOCX translations, CAT tool bilingual file processing

### v3.0.0-beta (CAT Editor)
- **Architecture**: Segment-centric
- **Workflow**: Import multiple formats → Grid/List/Document views → Export multiple formats
- **UI**: Professional CAT tool interface with:
  - Grid pagination (50 segments/page)
  - Three view modes (Grid, List, Document)
  - Smart paragraph detection
  - Column management
  - Dual text selection
- **Use case**: Full-featured CAT editor, translation project management

## Benefits of Renumbering

### Clarity
- ✅ Version number immediately signals architectural difference
- ✅ Users understand v3.x ≠ incremental update from v2.x
- ✅ "-CLASSIC" and "-beta" suffixes provide additional context

### Semantic Versioning
- ✅ Follows industry-standard semantic versioning principles
- ✅ Major version bump (v2 → v3) = major breaking change
- ✅ Communicates stability (CLASSIC) vs experimental (beta)

### Future-Proofing
- ✅ Clear upgrade path: v3.0-beta → v3.0 → v3.1 → v3.2...
- ✅ v2.x-CLASSIC can continue in parallel for DOCX workflow
- ✅ No confusion about which version is which

### Professional Image
- ✅ Proper versioning looks more professional
- ✅ "-CLASSIC" gives legacy version respect (not abandonment)
- ✅ "beta" tag manages expectations appropriately

## Historical Note

**Previous version history:**
- v2.5.0: First CAT editor prototype
- v2.5.1: Early development (had API cost issue)
- v2.5.2: Performance improvements (pagination, smart paragraphs)
- v3.0.0-beta: **Renumbered from v2.5.2** to reflect architectural significance

The v2.5.x series is now considered part of the v3.0 development cycle, retrospectively.

## Related Documentation

- **README.md**: Updated version table with new naming scheme
- **CHANGELOG.md**: Full v3.0.0-beta changelog with renumbering note
- **docs/VERSION_GUIDE.md**: General version guidance (may need update)
- **docs/RELEASE_NOTES_v2.5.2.md**: Should be updated/renamed to v3.0.0-beta

## Conclusion

The version renumbering to v3.0.0-beta better communicates the significance of the architectural change. Users can now clearly distinguish between:
- **v2.4.1-CLASSIC**: Stable DOCX workflow (production-ready)
- **v3.0.0-beta**: New CAT editor (experimental, feature-rich)

This semantic versioning approach will guide future development and help users make informed decisions about which version to use.

---

**Document created**: October 9, 2025  
**Author**: Michael Beijer + AI Assistant  
**Version**: 1.0
