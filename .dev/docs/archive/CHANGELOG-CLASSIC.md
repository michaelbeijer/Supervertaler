# Supervertaler Classic Edition - Changelog

**Version Branch**: v2.x.x-CLASSIC (Stable Production)

This changelog tracks changes specific to the **Classic Edition** of Supervertaler - the stable, production-ready DOCX-based workflow.

For the CAT Edition changelog, see [CHANGELOG-CAT.md](CHANGELOG-CAT.md).  
For the unified changelog, see [CHANGELOG.md](CHANGELOG.md).

---

## [2.5.0-CLASSIC] - 2025-10-14 ✅ PRODUCTION RELEASE

> **🎉 Stable Release**: Production-ready with unified folder structure and full CAT tool integration.

### ✨ FEATURES

**CAT Tool Integration**:
- ✅ CafeTran bilingual DOCX support - AI-based pipe formatting
- ✅ memoQ bilingual DOCX support - Programmatic formatting preservation
- ✅ Two complementary formatting approaches (AI-based & programmatic)
- ✅ 100% success rate in production testing

**Core Features**:
- Translation Memory with fuzzy matching
- Multiple AI providers (OpenAI GPT-4, Anthropic Claude, Google Gemini)
- Custom prompts with variable substitution
- Full document context awareness
- Tracked changes ingestion (learning from revisions)
- Import/Export: DOCX, TXT, TMX

**User Data Management**:
- All user data centralized in `user data/` folder
- Projects saved to `user data/Projects/` and `Projects_private/`
- Unified folder structure with v3.x for easy version switching

### 📖 DOCUMENTATION

- **User Guide**: [USER_GUIDE.md](USER_GUIDE.md)
- **CafeTran Guide**: [`.dev/docs/features/CAFETRAN_SUPPORT.md`](.dev/docs/features/CAFETRAN_SUPPORT.md)
- **memoQ Guide**: [`.dev/docs/features/MEMOQ_SUPPORT.md`](.dev/docs/features/MEMOQ_SUPPORT.md)

---

## [2.4.3-CLASSIC] - 2025-10-10 🔧 FOLDER STRUCTURE UPDATE

> **📌 Final Compatibility Update**: Migrated project folders to `user data/` for consistency with v3.1.0-beta.

### 🗂️ FOLDER STRUCTURE CHANGES

**Project Folder Migration**:
- **CHANGED**: Projects now saved to `user data/Projects/` (was: root `projects/`)
- **CHANGED**: Private projects now in `user data/Projects_private/` (was: root `projects_private/`)
- **BENEFIT**: All user data now centralized in `user data/` folder
- **BENEFIT**: Consistent structure across v2 and v3 versions

### 🧹 CLEANUP

- **REMOVED**: Root-level `custom_prompts/` folder (obsolete, empty)
- **REMOVED**: Root-level `projects/` folder (replaced by `user data/Projects/`)
- **RESULT**: Cleaner root directory with only user-facing documentation

### 🔄 COMPATIBILITY

- ✅ Full compatibility with v3.1.0-beta folder structure
- ✅ Users can switch between v2.4.3 and v3.1.0 seamlessly
- ✅ All user data (prompts, projects, TMs, glossaries) in unified location

---

## [2.4.0-CLASSIC] - 2025-10-07 📦 ARCHIVED

**File**: `.dev/previous_versions/Supervertaler_v2.4.0 (stable - production ready)(2025-10-07).py`

- 📦 Archived on 2025-10-07
- ✅ Fully backward compatible with v2.4.3
- 💡 Upgrade to v2.4.3-CLASSIC recommended for CAT tool integration

---

## [2.3.0] - Revolutionary Project Management

### ✨ NEW FEATURES

**Project Management System**:
- Save and load complete translation projects
- JSON-based project files with all context preserved
- Project metadata (source/target language, AI settings, etc.)

**Domain-Specific Custom Prompts**:
- Medical Translation Specialist
- Legal Translation Specialist
- Financial Translation Specialist
- Technical Translation Specialist
- Marketing & Creative Translation
- Patent Translation Specialist

**Custom Prompt Library**:
- Browse and manage custom prompts in dedicated UI
- Create, edit, and delete prompts
- Organize prompts by domain
- Variable substitution support

### 🎨 UI IMPROVEMENTS

- **Custom Prompt Manager**: Dedicated dialog for managing prompts
- **Active Prompt Indicators**: Visual feedback showing active translation/proofreading prompts
- **Clickable Folder Path**: Open custom prompts folder directly from UI

---

## [2.2.0] - Custom Prompt Library & Enhanced GUI

### ✨ NEW FEATURES

**Custom Prompt Library**:
- Store custom translation and proofreading prompts
- JSON-based prompt files in `custom_prompts/` folder
- Load prompts from library via UI
- Example prompts included

**GUI Enhancements**:
- Improved layout and spacing
- Better visual hierarchy
- Enhanced button styling
- Clearer section separation

---

## [2.1.1] - Bug Fixes & Stability

### 🐛 BUG FIXES

- Fixed project save/load issues
- Improved error handling
- Enhanced stability

---

## [2.1.0] - Output Generation Improvements

### ✨ NEW FEATURES

**Output Generation Agent**:
- Improved TXT file writing
- Enhanced TMX export
- Better file handling

### 🔧 IMPROVEMENTS

- Refactored agent classes for clarity
- Enhanced code structure
- Improved maintainability

---

## [2.0.0] - Semantic Versioning & Multi-LLM Support

> **📌 Major Version**: Adopted semantic versioning. Previously v10.3.

### ✨ NEW FEATURES

**Multiple AI Provider Support**:
- OpenAI GPT-4 / GPT-4 Turbo
- Anthropic Claude 3.5 Sonnet
- Google Gemini 1.5 Pro/Flash

**Enhanced Context Sources**:
- Full document context
- Translation memory matching
- Tracked changes ingestion
- Custom instructions
- Glossaries and non-translatables

### 🔧 IMPROVEMENTS

- Semantic versioning adopted (v2.0.0)
- Improved agent architecture
- Better error handling
- Enhanced UI/UX

---

## Version History Summary

- **v2.5.0-CLASSIC** (2025-10-14): Production release with CAT integration
- **v2.4.3-CLASSIC** (2025-10-10): Folder structure update
- **v2.4.0-CLASSIC** (2025-10-07): Stable, archived
- **v2.3.0** (2025): Project management & domain-specific prompts
- **v2.2.0** (2025): Custom prompt library
- **v2.1.1** (2025): Bug fixes
- **v2.1.0** (2025): Output generation improvements
- **v2.0.0** (2025): Multi-LLM support & semantic versioning

---

**For detailed version history and all updates**, see the main [CHANGELOG.md](CHANGELOG.md).
