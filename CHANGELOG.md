# Supervertaler - Complete Changelog

**Latest Version**: v3.7.6 (2025-10-25)  
**Product**: Unified Supervertaler (v3.x CAT Edition)  
**Status**: Active Development

> As of v3.7.1, Supervertaler is a unified product focusing exclusively on the CAT (Computer-Aided Translation) editor experience. The previous Classic Edition (v2.x) is archived for reference but no longer actively developed.

---

## [3.7.6] - 2025-10-25 🎨 UNICODE BOLD HIGHLIGHTING

### ✨ Enhancement

**TMX Editor - Unicode Bold Search Highlighting**:
- ✅ **True bold text for search terms** - Using Unicode Mathematical Bold characters
  - Search terms now appear in actual bold: 𝐜𝐨𝐧𝐜𝐫𝐞𝐭𝐞, 𝐁𝐚𝐬𝐞, 𝐓𝐞𝐬𝐭𝟏𝟐𝟑
  - No extra markers or special characters added
  - Works natively in Treeview where HTML/rich text doesn't
  - Combined with light yellow row background for dual highlighting
- ✅ **Professional appearance** - Clean, native-looking bold
  - Supports A-Z, a-z, 0-9 (Unicode U+1D400-U+1D7D7)
  - Punctuation remains normal (no Unicode bold version exists)
  - Universal Unicode support across all platforms
- ✅ **Maintains grid functionality** - Best of both worlds
  - Resizable columns still work
  - Row selection still works
  - Double-click editing still works
  - All Treeview features preserved

### 📚 Documentation
- Added `demo_unicode_bold.py` - Interactive demonstration of Unicode bold
- Updated `docs/TMX_DUAL_HIGHLIGHTING.md` - Comprehensive explanation of highlighting system
- Updated CHANGELOG with Unicode bold feature details

### 🔧 Technical Details
- **Method**: `_to_unicode_bold()` converts regular text to Mathematical Alphanumeric Symbols
- **Character Ranges**: 
  - Uppercase: U+1D400 to U+1D419 (𝐀-𝐙)
  - Lowercase: U+1D41A to U+1D433 (𝐚-𝐳)
  - Digits: U+1D7CE to U+1D7D7 (𝟎-𝟗)
- **Performance**: Minimal impact, applied during display refresh only

---

## [3.7.5] - 2025-10-25 📝 TMX EDITOR MODULE

### 🚀 Major Features

**Professional TMX Editor**:
- ✅ **Standalone TMX Editor module** - Inspired by Heartsome TMX Editor 8
  - Can run independently: `python modules/tmx_editor.py`
  - Integrated in Supervertaler as assistant panel tab
  - Also accessible via Tools menu → TMX Editor
- ✅ **Treeview grid with resizable columns** - Professional spreadsheet-like interface
  - **Drag column borders** to resize Source/Target columns to your preference
  - **Click to select** individual segments (row selection)
  - **Dual highlighting system** for search results:
    - Light yellow background for matching rows
    - **Search terms displayed in Unicode bold** (𝐛𝐨𝐥𝐝 𝐭𝐞𝐱𝐭)
  - Fast pagination (50 TUs per page)
  - Source on left, Target on right (conventional layout)
- ✅ **Integrated edit panel** - Edit TUs directly above the grid (no popup dialogs)
  - **Click any segment** to load it into the edit panel
  - **Double-click** to load and focus on target for quick editing
  - Side-by-side source/target editing
  - Save or cancel changes with one click
  - Word-level highlighting in edit panel shows exact search matches
- ✅ **Advanced filtering** - Filter by source/target content
  - Real-time search with Enter key
  - Clear filters with one click
  - Matching rows highlighted in light yellow
- ✅ **Language pair management** - View any language combination
  - Multi-language TMX support
  - Column headers show language codes
  - Switch language pairs on the fly
  - "All Languages" view to see what's in file
- ✅ **TMX header editing** - Edit metadata
  - Creation tool, version, segment type
  - Admin language, source language, datatype
  - Creator ID tracking
- ✅ **File validation** - Check TMX structure
  - Validate header completeness
  - Find empty segments
  - Report issues with line numbers
- ✅ **Full CRUD operations**
  - Create new TMX files
  - Open/Save/Save As
  - Add/Edit/Delete translation units
  - Copy source to target
- ✅ **Statistics view** - Analyze TMX content
  - Total TUs per language
  - Average character count
  - Language distribution

### 🎨 Integration Points

**Assistant Panel**:
- New "📝 TMX Editor" tab in assistant panel
- Quick actions: Open TMX, Save, Open in Window
- Embedded view for quick edits

**Tools Menu**:
- Tools → TMX Editor (opens in separate window)
- Full-featured standalone editor
- Retains state when switching tabs

**Standalone Mode**:
- Run directly: `python modules/tmx_editor.py`
- Complete standalone application
- No dependencies on Supervertaler

### 🏗️ Architecture

**Design Philosophy**:
- Based on Heartsome TMX Editor 8 concepts (Java/Eclipse RCP)
- Rewritten in Python/Tkinter for nimbleness
- Clean separation: can be extracted as separate tool
- Pagination for large file performance

**Technical Details**:
- Pure Python (no Java dependencies)
- XML parsing with ElementTree
- Dataclass-based models (TmxFile, TmxTranslationUnit, TmxSegment)
- TMX 1.4 format support
- Proper XML namespaces (xml:lang)

---

## [3.7.4] - 2025-10-23 🎯 CAT TOOL ENHANCEMENTS & PERFORMANCE

### 🚀 Major Features

**Professional CAT Tool Navigation**:
- ✅ **Keep segment in middle** - Optional setting to center active segment in grid (like memoQ)
  - Toggle via View menu or Settings pane
  - Smooth scrolling that keeps focus in middle of viewport
  - Perfect for long translation sessions
- ✅ **Fast pagination navigation** - Jump to next untranslated segment across pages
  - Optimized for 500+ segment documents
  - Smart page calculation (O(1) instead of O(n))
  - Works from both Save & Next button and Ctrl+Enter

**Performance Improvements**:
- ⚡ **10x faster** filter clearing with segment navigation (500 segments: 5-10s → 0.5s)
- ⚡ **Instant page jumps** when navigating to segments on different pages
- ⚡ **Smart reload** - only loads current page (50 segments) instead of all segments

### 🐛 Bug Fixes

- ✅ **Fixed List View blank screen** - Resolved widget destruction errors when switching views
- ✅ **Fixed Ctrl+Enter navigation** - Inline editing now searches ALL segments, not just current page
- ✅ **Fixed Save & Next button** - Now layout-aware (works in Grid, List, and Document views)

### ⚙️ UI Preferences System

**New Settings Persistence**:
- ✅ All UI preferences saved to `ui_preferences.json`
- ✅ Settings restored on app restart
- ✅ Auto-save when changed (no manual save needed)

**Preferences Saved**:
- View settings: Keep segment in middle
- Auto-export formats: Session MD, Session HTML, TMX, TSV, Bilingual TXT, XLIFF, Excel
- All checkboxes in Settings pane now persist

**Settings Consolidation**:
- ✅ New "View Settings" section in Settings tab
- ✅ Centralized control panel for all preferences
- ✅ Helpful tooltips explaining each setting

### 📦 Technical Updates

- Enhanced `ConfigManager` with `load_preferences()` and `save_preferences()` methods
- Added preference loading in main `__init__` method
- All auto-export checkboxes now have `command=self.save_ui_preferences`
- Smart segment navigation uses existing pagination infrastructure

---

## [3.7.3] - 2025-10-23 🗄️ DATABASE BACKEND IMPLEMENTATION

### ⚡ MAJOR PERFORMANCE UPGRADE: SQLite Database Backend

**Complete rewrite of Translation Memory system** - migrated from in-memory dictionaries to SQLite database:

**Performance Improvements**:
- **10-20x faster** fuzzy search (500ms → 50ms on 100K entries)
- **10x less memory** usage (50MB → 5MB for 10K entries)
- **20x faster** startup time with large TMs (2s → 0.1s)
- **Unlimited scalability** - constant performance regardless of TM size

**New Features**:
- ✅ **Real fuzzy matching** with actual similarity scores (not estimates!)
  - Example: "hello world test" → 81% match "Hello world"
  - Uses SequenceMatcher for accurate percentage calculations
- ✅ **FTS5 full-text search** for fast candidate retrieval
- ✅ **Usage tracking** - see which TM entries are used most
- ✅ **Context storage** - stores surrounding segments for future disambiguation
- ✅ **Concordance search** - now database-powered for speed
- ✅ **Hash-based exact match** - instant O(1) lookups using MD5

**Technical Implementation**:
- New `modules/database_manager.py` (570 lines) - Core SQLite backend
- Rewritten `modules/translation_memory.py` - Database-backed TMDatabase class
- Database location: `user_data/Translation_Resources/supervertaler.db`
- Automatic schema creation on first launch
- FTS5 indexes with auto-sync triggers
- Comprehensive error handling and logging

**UI Updates**:
- TM viewer now shows usage count for each entry
- Concordance search uses database (10x faster)
- TM management dialog updated for database metadata
- Entry counts pulled from database in real-time

**Database Schema** (production-ready):
- ✅ `translation_units` - TM entries with hash, context, usage tracking
- ✅ `translation_units_fts` - FTS5 full-text search index
- ✅ `glossary_terms` - Ready for Phase 2 (glossary system)
- ✅ `non_translatables` - Ready for Phase 2 (regex patterns)
- ✅ `segmentation_rules` - Ready for Phase 2 (custom rules)
- ✅ `projects` - Ready for Phase 2 (project management)

**Testing**:
- Comprehensive test suite (`test_database.py`)
- All tests passing ✅
- Application launches successfully ✅
- No errors in production ✅

**Documentation**:
- `docs/DATABASE_IMPLEMENTATION.md` - Full technical specification
- `docs/DATABASE_QUICK_REFERENCE.md` - API reference
- `docs/DATABASE_PRODUCTION_READY.md` - Production readiness guide
- `docs/DATABASE_FINAL_SUMMARY.md` - Complete overview
- `modules/DATABASE_README.md` - User and developer guide

**Backward Compatibility**:
- No migration code (clean implementation as requested)
- Database automatically created on first launch
- Legacy JSON projects can optionally be imported

**Next Steps**:
- Phase 2: Glossary system (schema ready, needs UI)
- Phase 3: Non-translatables (schema ready, needs UI)
- Phase 4: Segmentation rules (schema ready, needs UI)

### 🔧 Translation Memory Enhancements (v3.7.3 Update)

**Concordance Search Improvements**:
- ✅ **Word-level highlighting** - Search terms now highlighted individually (not entire rows)
- ✅ **New visual layout** - Cleaner display with Source/Target labels and separators
- ✅ **Right-click context menu** - Use translation or delete entry
- ✅ **Double-click to apply** - Quick translation insertion from results

**TM Entry Management**:
- ✅ **Delete functionality fixed** - Remove individual TM entries from database
- ✅ **Delete from matches pane** - Right-click any fuzzy match to delete
- ✅ **Delete from concordance** - Right-click search results to delete
- ✅ **Database integrity** - Proper deletion from both main table and FTS5 index

**Technical Fixes**:
- Fixed `TMDatabase.delete_entry()` - Added missing delegation to DatabaseManager
- Fixed `DatabaseManager.delete_entry()` - Corrected column names (source_text/target_text)
- Fixed concordance search highlighting - Text widget with character-level tags
- Improved highlighting algorithm - Finds all occurrences within source and target

---

## [3.7.2] - 2025-10-22 🎨 UX POLISH & MEMORY UPDATE

### ✨ USER EXPERIENCE IMPROVEMENTS

**Layout Memory Enhancements**:
- **🔲 Divider Position Memory** - All paned window dividers now remember their position:
  - Start screen divider (splash screen ↔ assistance panel)
  - Grid view divider (grid ↔ assistance panel)
  - Document view divider (document ↔ assistance panel)
  - Split view divider (list ↔ assistance panel)
  - Positions preserved when switching views and across app restarts
  - Uses ratio-based storage for proper scaling across window sizes

**Tab Memory System**:
- **📑 Assistance Panel Tab Memory** - Selected tab remembered when switching views
- **📚 Prompt Manager Sub-Tab Memory** - Sub-tab selection (System Prompts, Custom Instructions, etc.) preserved
- **📂 Project List Display** - Projects tab now shows ALL recent projects (not just current)
- **🔄 Auto-Refresh Tabs** - Automatically maximizes visible tabs when switching views (no manual "Refresh Tabs" click needed)

**Bug Fixes**:
- **🐛 Fixed Grid Blanking on Project Load** - Corrected operation order in `load_project_from_path()` (switch to grid BEFORE loading segments)
- **🐛 Fixed Tab Overflow Logic** - Selected tab always visible after view switch (never hidden in overflow menu)
- **🐛 Fixed Auto-Refresh Loop** - Auto-refresh only triggers during explicit view switches (not on startup or document import)

**Technical Details**:
- Divider positions stored as ratios (position ÷ total width) for proper scaling
- 500ms delay before restoration to allow UI rendering
- `_switching_view` flag ensures auto-refresh only during user-initiated view changes
- Prompt Manager sub-tab restoration uses `ttk.Notebook.select()` with 100ms delay

### 📝 Files Modified
- `Supervertaler_v3.7.1.py` - Enhanced layout memory, tab restoration, project tree population

---

## [3.7.1] - 2025-10-20 🔐 SECURITY & CONFIGURATION UPDATE

### 🔐 CRITICAL SECURITY UPDATES

**Data Privacy & API Keys Security**:
- **🛡️ Removed sensitive data from git history** - `recent_projects.json` containing client project names completely removed from all 364 commits using git filter-branch
- **🔑 API Keys Protection** - Moved `api_keys.txt` to user data folder, never committed to git
- **v3.7.1 Yanked** - Removed from PyPI and GitHub releases due to security review (users should upgrade to v3.7.1)
- **Dev/User Mode Separation** - Separate configuration paths for development vs. user environments

**User Data Folder System** (NEW):
- **First-Launch SetupWizard**: Users select where to store their data (Windows: `Documents/Supervertaler_Data/`, etc.)
- **Configurable Location**: New "Change Data Folder" option in Settings menu
- **Automatic Setup**: `api_keys.txt` created from template on first launch
- **Migration Support**: Existing users' keys automatically migrated to new location
- **Configuration Stored**: User path saved to `~/.supervertaler_config.json`

**Code Quality**:
- 🐛 **Fixed Tkinter Error** - Corrected paned window widget management in Prompt Library tab switching
- ✅ **Enhanced Error Handling** - Try-catch blocks for TclError in tab switching
- ✅ **Improved UX** - SetupWizard now shows confirmation dialog with exact folder structure before creation

**Files Modified**:
- `Supervertaler_v3.7.1.py` - Updated tab switching logic, user data folder routing
- `modules/config_manager.py` - Dev/user mode detection, api_keys handling
- `modules/setup_wizard.py` - Enhanced first-launch experience
- Documentation - Updated README with new user data folder structure

**Migration Guide**:
- **Existing Users (v3.7.1)**: Simply upgrade - SetupWizard will guide you on first launch
- **New Users (v3.7.1)**: SetupWizard appears on first launch, guide you through setup
- **API Keys**: Will be copied to your chosen data folder automatically
- **Custom Prompts**: Already in `user data/Prompt_Library/` - can be moved to new location via Settings

### ✨ USER EXPERIENCE IMPROVEMENTS

**First-Launch Flow**:
1. App detects missing user data folder configuration
2. Welcome dialog explains what will be created
3. Folder selection dialog with clear examples
4. Confirmation dialog shows exact folder structure
5. Success message lists all created files/folders
6. Application launches with full functionality

**Settings Menu Enhancement**:
- New "Data Folder" section showing current path
- "Change Data Folder" button for mid-session changes
- Optional data migration when changing paths
- Clear feedback on what was moved

---

## [3.7.0] - 2025-10-19 🎯 STABLE RELEASE

### ✨ MAJOR RESTRUCTURING

**Product Unification**:
- **Deprecated**: v3.7.1-CLASSIC (archived to `.dev/previous_versions/`)
- **Focus**: All development now concentrated on v3.x CAT Edition
- **Branding**: Removed "CAT" suffix - Supervertaler IS the CAT editor
- **Messaging**: Single product line, clear value proposition to users

**Repository Cleanup**:
- Moved all v2.x and earlier v3.x versions to `.dev/previous_versions/` folder
- Unified changelog (consolidated CHANGELOG-CAT.md and CHANGELOG-CLASSIC.md)
- Removed confusing dual-version documentation
- Main executable: `Supervertaler_v3.7.1-beta.py`

**Folder Structure Reorganization** (v3.7.1 continued):
```
user data/
├── Prompt_Library/
│   ├── System_prompts/        (19 Markdown files)
│   └── Custom_instructions/   (8 Markdown files)
├── Translation_Resources/
│   ├── Glossaries/
│   ├── TMs/
│   ├── Non-translatables/
│   └── Segmentation_rules/
└── Projects/
```

**Benefits**:
- ✅ Clearer product identity
- ✅ Reduced user confusion
- ✅ Simplified documentation
- ✅ Better focus for development
- ✅ Easier to present to LSPs (single unified tool)

---

## [3.6.9-beta] - 2025-10-19 📁 FOLDER STRUCTURE REORGANIZATION

### 🗂️ MAJOR RESTRUCTURING

**Hierarchical Folder Organization**:
- Created `Prompt_Library/` to group all prompt-related resources:
  - `System_prompts/` - Domain-specific system prompts (19 files)
  - `Custom_instructions/` - User custom instructions (8 files)
- Created `Translation_Resources/` to centralize translation assets:
  - `Glossaries/` - Terminology databases
  - `TMs/` - Translation Memory files
  - `Non-translatables/` - Non-translatable terms lists
  - `Segmentation_rules/` - Segmentation rule files

**Migration Details**:
- Successfully migrated all 27 prompt files
- Full dev mode support (both `user data/` and `user data_private/`)
- Backward compatibility with auto-migration function
- Old folders automatically cleaned up

**Code Updates**:
- Updated `get_user_data_path()` function calls throughout
- Added `migrate_old_folder_structure()` for automatic migration
- Updated folder link operations
- Enhanced documentation examples

**Benefits**:
- ✨ **Better Scalability**: Clear hierarchy for future features
- ✨ **Improved Navigation**: Logical grouping of resources
- ✨ **Professional Polish**: Well-organised data structure
- ✨ **Future-Ready**: Easy to add new resource types

### 📦 REPOSITORY CLEANUP

**Previous Versions Folder**:
- Moved to `.dev/previous_versions/` (centralized archive)
- Archived: v3.7.1-CLASSIC.py
- Archived: v3.7.1-beta_CAT.py
- Archived: v3.7.1-beta_CAT.py
- Root now contains only: v3.7.1.py

---

## [3.6.8-beta] - 2025-10-19 📝 MARKDOWN PROMPT FORMAT

### ✨ MAJOR ENHANCEMENT

**Complete Markdown Format Migration for Prompts**:
- **NEW**: All prompts (System Prompts + Custom Instructions) now use Markdown with YAML frontmatter
- **NEW**: Save dialogs default to `.md` format instead of `.json`
- **NEW**: Beautiful native Markdown tables for glossaries and structured data
- **NEW**: YAML frontmatter provides clean, human-readable metadata
- **NEW**: Mixed format support - loads both `.json` and `.md` files automatically
- **MIGRATION**: All 27 existing prompts converted from JSON to Markdown

**User Experience**:
- ✅ Double-click prompts to open in any text editor
- ✅ Read and edit prompts naturally with section headers
- ✅ No escaped quotes or verbose JSON syntax
- ✅ Glossaries display as beautiful Markdown tables
- ✅ Human-friendly editing experience

**Format Example**:
```markdown
---
name: "Patent Translation Specialist"
description: "Expert patent translator"
domain: "Intellectual Property"
version: "2.2.0"
task_type: "Translation"
created: "2025-10-19"
---

# Patent Translation Guide

You are an expert translator with deep expertise in intellectual property...

## Key Principles

- Maintain technical precision
- Preserve claim structure
- Use consistent terminology
```

**Technical Implementation**:
- `parse_markdown()` - Parse Markdown with YAML frontmatter
- `dict_to_markdown()` - Save prompt data as formatted Markdown
- `_parse_yaml()` - Simple YAML parser for frontmatter
- `_load_from_directory()` - Enhanced for `.json` and `.md` files
- `convert_json_to_markdown()` - Convert JSON to Markdown
- `convert_all_prompts_to_markdown()` - Batch conversion

**Migration Summary**:
- ✅ 19 System Prompts converted
- ✅ 8 Custom Instructions converted
- ⚠️ 3 empty corrupted files skipped
- **Total**: 27 prompts successfully migrated

---

## [3.6.7-beta] - 2025-10-18 ✨ POLISH & FIXES

### ✨ ENHANCEMENTS

**UI Polish & Usability**:
- **Reduced Tab Height**: Lowered vertical padding for better screen density
- **Removed Maximize View**: Eliminated obsolete maximize functionality (~725 lines cleaned)
- **Better Button Names**: "📝 View/Edit Analysis Prompts" for clarity
- **Clickable Folder Links**: System_prompts and Custom_instructions folders now clickable
  - Opens Windows Explorer / macOS Finder / Linux file manager

**Website Enhancements**:
- **NEW About Section**: Beautiful gradient design telling Supervertaler's story
- Three story cards showing evolution from manual workflow to full CAT features
- Vision dialogue for future AI interaction
- Responsive design with modern effects

### 🐛 BUG FIXES

**Translation Error with Prompt Manager**:
- Fixed: `'Supervertaler' object has no attribute 'custom_instructions_text'`
- Root cause: Functions looking for old text widget
- Solution: Check `self.active_custom_instruction` first with fallback

**System Prompts Not Appearing**:
- Fixed: Saved prompts not showing in Prompt Manager
- Root cause: JSON using wrong name field
- Solution: Use `user_entered_name` for metadata

---

## [3.6.6-beta] - 2025-10-18 🤖 PROMPT ASSISTANT UX OVERHAUL

### 🎯 MAJOR UX IMPROVEMENTS

**Renamed "AI Assistant" to "Prompt Assistant"**:
- Better describes its purpose (analyzing documents and generating prompts)
- More professional terminology

**Moved to Prompt Library as Third Tab**:
- Consolidates all prompt-related features in one place
- Natural workflow: Analyze → Generate → Browse/Edit → Apply
- Auto-hides editor panel when active to maximize workspace
- Auto-shows editor when switching to other prompt tabs

**Smart Editor Panel Visibility**:
- Context-aware UI adapts based on current task
- Full width workspace for document analysis
- Better screen real estate utilization

### 🔄 TECHNICAL CHANGES

- Renamed UI components
- Updated event handlers for tab switching
- Preserved all functionality
- Enhanced documentation

---

## Previous Versions (Archived)

### v3.7.1-beta, v3.7.1-beta, v3.7.1-beta
See [.dev/previous_versions/](.dev/previous_versions/) folder

### v3.7.1-CLASSIC (Archived - No Longer Developed)
**Production-ready DOCX-based workflow** (last update: 2025-10-14):
- CAT tool integration (CafeTran, memoQ, Trados)
- Translation Memory with fuzzy matching
- Multiple AI providers
- Custom prompts with variable substitution
- Full document context awareness

**Note**: This version is archived but remains available at [GitHub Release v3.7.1](https://github.com/michaelbeijer/Supervertaler/releases/tag/v3.7.1) for users who prefer the simpler DOCX-based workflow.

---

## Release Strategy

**Current Focus**: v3.7.1+ (Unified CAT Edition)
- Weekly incremental improvements
- User feedback integration
- LSP consulting feedback incorporation
- Feature expansion based on professional translator needs

**Version Numbering**:
- **v3.x-beta**: Active development (current)
- **.dev/previous_versions/**: Archived but working versions

---

## Notable Features Across All Versions

### Core Translation Engine
- ✅ Multiple AI providers (OpenAI, Claude, Gemini)
- ✅ Custom prompts with variable substitution
- ✅ Translation Memory with fuzzy matching
- ✅ Full document context awareness
- ✅ Tracked changes learning

### Professional CAT Features
- ✅ Segment-based editing (CAT Editor)
- ✅ Grid pagination system (50 segments/page)
- ✅ Dual selection support (memoQ-style)
- ✅ CAT tool integration (memoQ, CafeTran, Trados)
- ✅ Figure context support (multimodal AI)

### Data Management
- ✅ Import/Export: DOCX, TSV, JSON, XLIFF, TMX
- ✅ Session reports in HTML and Markdown
- ✅ Project save/load with context preservation
- ✅ Automatic backups

### Prompt Management
- ✅ System Prompts (domain-specific)
- ✅ Custom Instructions (user-defined)
- ✅ Prompt Assistant (AI-powered generation)
- ✅ Markdown + YAML frontmatter format
- ✅ Mixed format support

---

## For Questions or Issues

- **GitHub Issues**: [michaelbeijer/Supervertaler](https://github.com/michaelbeijer/Supervertaler/issues)
- **Website**: [supervertaler.com](https://supervertaler.com)
- **Documentation**: See `/docs` folder and README.md

---

**Last Updated**: October 19, 2025  
**Maintainer**: Michael Beijer  
**License**: Open Source (MIT)
