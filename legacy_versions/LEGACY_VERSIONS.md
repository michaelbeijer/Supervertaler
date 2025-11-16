# Legacy Versions of Supervertaler

This document provides historical context and information about previous versions of Supervertaler that are no longer actively developed or publicly distributed.

---

## 📌 Current Status

**Active Version:** Supervertaler (v1.6.0+)  
**Framework:** PyQt6  
**Status:** Active Development  
**File:** `Supervertaler.py`

---

## 🗂️ Legacy Editions Overview

### 1. Tkinter Edition (v2.5.0 - v3.7.7)
**Framework:** tkinter (Python built-in)  
**Status:** Archived (October 2025)  
**Final Version:** v3.7.7 (October 27, 2025)  
**File:** `legacy_versions/Supervertaler_tkinter.py`

**Why It Was Created:**
- Built using Python's built-in tkinter framework for maximum compatibility
- No external GUI dependencies required
- Provided stable, production-ready translation workflow
- Served as the primary version from 2024-2025

**Key Features:**
- ✅ DOCX-based translation workflow
- ✅ Full Translation Memory with fuzzy matching
- ✅ Multiple AI providers (OpenAI, Claude, Gemini)
- ✅ CAT tool integration (memoQ, Trados, CafeTran)
- ✅ Grid pagination system (50 segments/page)
- ✅ PDF Rescue (AI-powered OCR)
- ✅ TMX editor
- ✅ AutoFingers automation
- ✅ Prompt Manager with variable substitution

**Why It Was Retired:**
- Limited UI capabilities compared to Qt
- Performance constraints with large projects
- Difficulty implementing modern features (e.g., Universal Lookup, detachable windows)
- Maintenance burden of supporting two separate codebases
- User feedback strongly favored Qt interface

**Migration Path:**
- All user data (projects, TM, termbases) fully compatible with Qt Edition
- Settings and configurations easily transferred
- No functionality lost in migration

---

### 2. Classic Edition (v1.0.0 - v2.4.4)
**Framework:** tkinter  
**Status:** Archived (October 2025)  
**Final Version:** v2.5.0-CLASSIC  
**File:** `legacy_versions/Supervertaler_v2.5.0-CLASSIC.py`

**Why It Was Created:**
- Original proof-of-concept version
- Simple workflow: Export from memoQ → AI translate → Import back
- Demonstrated value of AI-assisted translation with custom prompts

**Key Features:**
- ✅ Basic AI translation (OpenAI GPT-3/4)
- ✅ Simple prompt system
- ✅ Text file import/export
- ✅ Bilingual document support
- ✅ Basic terminology management

**Evolution:**
```
v1.0.0 (2024-01-xx) - Initial release
  └─> Simple text-based translation with GPT-3

v2.0.0 (2024-xx-xx) - DOCX support
  └─> Added Microsoft Word document handling

v2.4.4 (2024-xx-xx) - Stable classic
  └─> Feature-complete classic edition

v2.5.0-CLASSIC (2025-10-xx) - Final classic
  └─> Last version before "CAT Edition" fork
```

**Why It Was Retired:**
- Superseded by Tkinter Edition with full CAT capabilities
- Limited feature set compared to modern needs
- Simple architecture couldn't support advanced features
- Evolved into Tkinter Edition (v3.x series)

---

## 📚 Version Timeline

```
Classic Era (v1.x - v2.5.0 CLASSIC)
2024-2025: Original simple translation tool
├─ Basic AI integration
├─ Text/DOCX handling
└─ Simple prompts

Tkinter Era (v2.5.0 - v3.7.7)
2024-2025: Full CAT functionality
├─ Professional grid interface
├─ TM/Termbase support
├─ Multiple AI providers
├─ memoQ/Trados integration
└─ Advanced prompt management

Qt Era (v1.0.0+)
2025-Present: Modern professional tool
├─ PyQt6 interface
├─ Universal Lookup
├─ Complete termbase system
├─ Supervoice dictation
├─ AI Assistant
└─ Active development
```

---

## 🔄 Key Transitions

### Classic → Tkinter (October 2024)
**Reason:** Need for professional CAT features  
**Impact:** 10x feature expansion, grid interface, TM support  
**User Impact:** Major upgrade, some users stayed on classic for simplicity

### Tkinter → Qt (October 2025)
**Reason:** Modern UI requirements, performance, new features  
**Impact:** Complete rewrite, PyQt6 framework, enhanced capabilities  
**User Impact:** Seamless migration, all data compatible, better UX

---

## 📖 Changelog Archive

### Tkinter Edition Major Releases

**v3.7.7** (October 27, 2025) - Final Release
- Fixed memoQ bilingual DOCX alignment (perfect 1:1 matching)
- GPT-5/o3-mini temperature compatibility
- Enhanced professional context
- 198/198 segments translated successfully

**v3.7.6** (October 15, 2025)
- Enhanced DOCX reading reliability
- Improved table detection and parsing
- Better formatting preservation
- Fixed encoding issues

**v3.7.5** (September 2025)
- Stability improvements
- Bug fixes for large projects

**v3.7.4** (September 2025)
- Performance optimizations
- UI refinements

**v3.1.1** (Beta CAT Editor)
- Experimental CAT features
- Grid improvements

**v2.5.0** (October 30, 2025)
- Tkinter base edition
- Full TM support
- AI integration

### Classic Edition Major Releases

**v2.5.0-CLASSIC** (October 2025) - Final Classic
- Stable classic feature set
- Basic CAT functionality
- Simple prompt system

**v2.4.4** (2024)
- Production-ready classic
- DOCX support
- Basic TM

**v2.0.0** (2024)
- DOCX handling added
- Improved UI

**v1.0.0** (2024)
- Initial release
- Text-only translation
- GPT-3 integration

---

## 🗃️ File Locations

All legacy versions are stored in the `legacy_versions/` directory for AI agent reference and historical purposes:

```
legacy_versions/
├── Supervertaler_tkinter.py          # Tkinter Edition v3.7.7 (final)
├── Supervertaler_v2.5.0-CLASSIC.py   # Classic Edition (final)
├── CHANGELOG_Tkinter.md              # Complete Tkinter changelog
└── LEGACY_VERSIONS.md                # This file
```

**Note:** These files are excluded from public distribution but remain accessible to AI agents for context and reference.

---

## 💡 Lessons Learned

### From Classic Edition:
1. ✅ **Simplicity matters** - Users appreciated straightforward workflow
2. ✅ **Custom prompts are powerful** - Core value proposition validated
3. ❌ **Limited scalability** - Simple architecture couldn't support growth
4. ❌ **Manual workflows** - Too much copy/paste friction

### From Tkinter Edition:
1. ✅ **CAT features essential** - Professional translators need grid, TM, termbases
2. ✅ **Multiple AI providers** - Flexibility is crucial
3. ✅ **Pagination system** - Huge performance improvement for large projects
4. ❌ **tkinter limitations** - UI constraints prevented modern features
5. ❌ **Code complexity** - Monolithic architecture hard to maintain

### Applied to Qt Edition:
1. ✅ **Modern framework** - PyQt6 enables advanced features
2. ✅ **Modular architecture** - Separate modules for maintainability
3. ✅ **Performance first** - Database-backed everything (TM, termbases)
4. ✅ **User experience focus** - Keyboard shortcuts, tooltips, visual feedback
5. ✅ **Active development** - New features shipped regularly

---

## 🎯 Why One Unified Version?

**Decision Made:** November 16, 2025  
**Effective:** v1.6.0 Qt Edition

**Reasons:**
1. **Development Focus** - Resources concentrated on Qt Edition
2. **User Confusion** - Two versions confused new users
3. **Maintenance Burden** - Supporting multiple codebases slowed development
4. **Feature Parity** - Qt Edition now equals/exceeds tkinter in all areas
5. **Better Documentation** - Single version = clearer docs

**Benefits:**
- ✅ Faster feature development
- ✅ Better testing and quality
- ✅ Clearer communication
- ✅ Reduced maintenance overhead
- ✅ More focused documentation

---

## 🔍 For AI Agents

When users reference "the old version" or "tkinter edition", they likely mean:

1. **Tkinter Edition (v3.7.7)** - Most recent legacy version
2. **Classic Edition (v2.5.0)** - Original simple version

**Key Differences from Qt Edition:**
- Tkinter: Grid-based, DOCX workflow, no Universal Lookup, no Supervoice
- Qt: Modern UI, database-backed, termbase system, voice dictation, AI Assistant

**Data Compatibility:**
- ✅ Projects (.json)
- ✅ Translation Memory (.db)
- ✅ Termbases (.db)
- ✅ Custom prompts
- ⚠️ Some settings may need manual migration

---

## 📅 Deprecation Timeline

- **October 30, 2025** - Tkinter Edition enters maintenance mode (v2.5.0)
- **November 16, 2025** - Legacy versions moved to `legacy_versions/` directory
- **November 16, 2025** - Single unified CHANGELOG.md created for Qt Edition
- **Future** - Legacy files remain for AI reference, not public distribution

---

## 📞 Support

**Current Version Support:** Full support for Qt Edition (v1.6.0+)

**Legacy Version Support:**
- ❌ No new features
- ❌ No bug fixes (except critical security issues)
- ✅ Migration assistance available
- ✅ Historical documentation maintained

**Migration Help:**
- See main README.md for migration guide
- Data is fully compatible
- AI agents can answer questions about differences

---

**Last Updated:** November 16, 2025  
**Maintained For:** AI agent context and historical reference  
**Public Status:** Archived, not distributed
