# Supervertaler CLASSIC Edition - Changelog

**Version Line**: v2.x.x-CLASSIC (DOCX-based Workflow Architecture)

---

## [2.4.4-CLASSIC] - 2025-10-11 🔧 INFRASTRUCTURE UPDATE

> **📌 Infrastructure Update**: Parallel folder structure for consistency with v3.1.1-beta

### 🗂️ INFRASTRUCTURE CHANGES

**Parallel Folder Structure** - Same architecture as v3.1.1-beta

- **NEW: Dual Directory Trees**:
  ```
  user data/          (public, Git-tracked, for end users)
  user data_private/  (private, Git-ignored, for developers)
  ```
  
- **Feature Flag System**:
  - `.supervertaler.local` file enables dev mode
  - `get_user_data_path()` function routes to appropriate tree
  - Auto-routing for all user data folders

- **Dev Mode Banner**:
  - Red "🔒 DEV MODE" indicator at top of main window
  - Confirms private features are active

### 🔧 COMPATIBILITY

- **Unified with v3.1.1-beta**: Both versions now share same folder structure
- **No User Impact**: End users see no changes (no `.supervertaler.local` file)
- **Developer Friendly**: Create `.supervertaler.local` to enable private mode

---

## [2.4.3-CLASSIC] - 2025-10-10 🔧 FOLDER STRUCTURE UPDATE (Projects)

> **📌 Final Compatibility Update**: Migrated project folders to `user data/` for consistency with v3.1.0-beta.

### 🗂️ FOLDER STRUCTURE CHANGES

**Project Folder Migration**:
- **CHANGED**: Projects now saved to `user data/Projects/` (was: root `projects/`)
- **CHANGED**: Private projects now in `user data/Projects_private/` (was: root `projects_private/`)
- **BENEFIT**: All user data now centralized in `user data/` folder
- **BENEFIT**: Consistent structure across v2 and v3 versions

### 📦 BREAKING CHANGES

⚠️ **Project Location Change**:
- **Old location**: Root-level `projects/` and `projects_private/` folders
- **New location**: `user data/Projects/` and `user data/Projects_private/`
- **Migration**: Empty folders removed (no existing projects to migrate)
- **Users**: Future projects will save to new location automatically

### 🧹 CLEANUP

- **REMOVED**: Root-level `custom_prompts/` folder (obsolete, empty)
- **REMOVED**: Root-level `projects/` folder (replaced by `user data/Projects/`)
- **RESULT**: Cleaner root directory with only user-facing documentation

---

## [2.4.2-CLASSIC] - 2025-10-10 🔧 FOLDER STRUCTURE UPDATE

> **📌 Compatibility Update**: Updated folder structure to match v3.1.0-beta for cross-version compatibility.

### 🗂️ FOLDER STRUCTURE CHANGES

**BREAKING CHANGE**: Updated to unified folder structure

- **New Structure** (matches v3.1.0-beta):
  ```
  user data/
  ├── System_prompts/          (public, Git-tracked)
  └── System_prompts_private/  (private, Git-ignored)
  ```

- **OLD Structure** (deprecated):
  - ~~`custom_prompts/`~~ → `user data/System_prompts/`
  - ~~`custom_prompts_private/`~~ → `user data/System_prompts_private/`

### 🔧 TECHNICAL CHANGES

- Updated all folder path references to new structure
- `custom_prompts_dir` now points to `user data/System_prompts/`
- Private prompts now saved to `user data/System_prompts_private/`
- All load/save/refresh functions updated

### ✅ COMPATIBILITY

- ✅ **v2 and v3 now compatible** - Share same prompt storage
- ✅ **Automatic folder creation** - Backwards compatible
- ✅ **No data loss** - Creates new folders if missing

---

## [2.4.1-CLASSIC] - 2025-10-09 🎉 PRODUCTION RELEASE

> **📌 Version Note**: The "-CLASSIC" suffix was added to distinguish this from the v3.0 CAT editor architecture. This version uses the original DOCX-based workflow and is production-ready and stable.

### 🚀 NEW FEATURES

#### ☕ CafeTran Bilingual DOCX Support (AI-Based Formatting)
**Direct integration with CafeTran bilingual workflow!**

- **NEW: CafeTran bilingual DOCX import/export** - Native CafeTran format support
- **AI-based pipe placement** - Intelligent formatting marker preservation
- **Pipe symbol format**: `|formatted text|` marks bold, italic, underline, etc.
- **Smart AI handling** - Pipes included in source, AI places them contextually in translation
- **Visual formatting** - All pipe symbols displayed as BOLD + RED in exported DOCX
- **UI Integration**:
  - Green "☕ Import CafeTran DOCX" button
  - Green "☕ Export to CafeTran DOCX" button
  - Automatic workflow configuration
- **Benefits**:
  - ✅ Eliminates manual copy-paste between CafeTran and Supervertaler
  - ✅ AI intelligently preserves formatting markers
  - ✅ Works perfectly with word order changes
  - ✅ Complete round-trip workflow (export → translate → reimport)

#### 📊 memoQ Bilingual DOCX Support (Programmatic Formatting)
**Professional CAT tool integration with programmatic formatting preservation!**

- **NEW: memoQ bilingual DOCX import/export** - Industry-standard CAT format
- **Programmatic formatting preservation** - Algorithm-based bold/italic/underline
- **Smart threshold logic** - >60% formatted = entire segment, else first words
- **CAT tag handling** - Complex `[1}{2]` tag format fully supported
- **Extract-and-apply workflow** - Source formatting extracted, applied to target
- **UI Integration**:
  - Green "📊 Import memoQ DOCX" button
  - Green "💾 Export to memoQ DOCX" button
  - Status automatically updated to "Confirmed"
- **Benefits**:
  - ✅ Direct memoQ integration
  - ✅ Preserves document-level formatting
  - ✅ Maintains all CAT metadata and segment IDs
  - ✅ Verified round-trip compatibility with memoQ

### 📊 STATISTICS FROM PRODUCTION TESTING

**CafeTran Test** (18 segments with pipe formatting):
- ✅ 18/18 segments translated successfully
- ✅ All pipe symbols correctly placed by AI
- ✅ 100% formatting markers preserved
- ✅ Successful reimport to CafeTran verified

**memoQ Test** (27 segments with formatting):
- ✅ 27/27 segments imported successfully
- ✅ 15/15 segments with formatting preserved programmatically
- ✅ All CAT tool tags maintained
- ✅ Successful reimport to memoQ verified

**Performance**:
- Import: < 1 second for both formats
- Export: < 1 second for both formats
- No additional AI costs
- No manual intervention required

---

## [2.4.0] - 2025-09-14

### Added
- **GPT-5 Support**: Full compatibility with OpenAI's GPT-5 model
- **Switch Languages Button**: One-click swap between source and target languages
- **Session Reporting**: Comprehensive markdown reports generated alongside translation outputs

### Fixed
- **GPT-5 Compatibility Issues**: Resolved empty responses, parameter errors, temperature incompatibility
- **Proofreading Output Format**: Fixed doubled line count issue, proper 1:1 line mapping
- **Gemini Proofreading Agent**: Fixed critical API format incompatibility

---

## [2.3.0] — 2025-09-08

### Added
- **MAJOR UPDATE**: Revolutionary Project Management System
- **NEW: Project Library** - Complete workspace configuration management
- **NEW: Domain-Specific Custom Prompt Collections** - 8 professional prompt libraries (Medical, Legal, Financial, Technical, Cryptocurrency, Gaming, etc.)
- **NEW: Private Custom Prompts Support** - `custom_prompts_private/` folder for confidential prompts
- **FIXED: OpenAI Integration** - Complete OpenAI support implementation
- **ENHANCED: Documentation Structure** - Streamlined user guide
- **NEW: Clickable Folder Paths** - Direct file system access

---

## [2.2.0] — 2025-09-08

### Added
- **NEW: Custom Prompt Library** - Save and organize custom system prompt sets
- **Enhanced GUI Design**: Complete 3-panel resizable layout with professional fonts
- **Advanced System Prompts Enhancements**: Added "📁 Prompt Library" tab

---

## [2.1.1] — 2025-09-05

### Added
- **NEW: Advanced System Prompts GUI** - Collapsible section for viewing/editing system prompts
- **NEW: Custom Prompt Library** - Save custom system prompt sets to local files

---

For older versions and detailed technical history, see: `CHANGELOG_full_backup.md`

**Last updated**: October 11, 2025
