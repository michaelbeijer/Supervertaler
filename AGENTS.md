# Supervertaler - AI Agent Documentation

> **This is the single source of truth for AI coding assistants working on this project.**
> **Last Updated:** December 18, 2025 | **Version:** v1.9.47

---

## 🎯 Project Overview

**Supervertaler** is a professional desktop translation application built with Python and PyQt6. It serves as a companion tool for translators, integrating AI-powered translation with traditional CAT (Computer-Assisted Translation) tool workflows.

| Property | Value |
|----------|-------|
| **Name** | Supervertaler |
| **Version** | v1.9.47 (December 2025) |
| **Framework** | PyQt6 (Qt for Python) |
| **Language** | Python 3.10+ |
| **Platform** | Windows (primary), Linux compatible |
| **Repository** | https://github.com/michaelbeijer/Supervertaler |
| **Website** | https://supervertaler.com |
| **Main File** | `Supervertaler.py` (~34,000+ lines) |
| **Modules** | 60+ specialized modules in `modules/` directory |

### Key Capabilities

- **Multi-LLM AI Translation**: OpenAI GPT-4, Anthropic Claude, Google Gemini, Local Ollama
- **CAT Tool Integration**: Trados SDLPPX/SDLRPX, memoQ XLIFF, Phrase/Memsource DOCX, CafeTran DOCX
- **Translation Memory**: Fuzzy matching TM with TMX import/export + Supermemory (ChromaDB vector search)
- **Terminology Management**: SQLite-based termbases with priority highlighting and automatic extraction
- **Document Handling**: DOCX, bilingual DOCX, PDF (via OCR), simple TXT, **Multi-file folder import**
- **Quality Assurance**: Spellcheck, tag validation, consistency checking
- **Superlookup**: Unified concordance hub with TM, Termbase, Supermemory, MT, and Web Resources

---

## 📁 Project Structure

```
Supervertaler/
├── Supervertaler.py          # Main application (~32,000+ lines)
├── modules/                   # 60+ specialized modules
│   ├── llm_clients.py        # OpenAI, Anthropic, Google Gemini, Ollama
│   ├── translation_memory.py # TM matching and storage
│   ├── termbase_manager.py   # Terminology management
│   ├── docx_handler.py       # DOCX import/export
│   ├── sdlppx_handler.py     # Trados Studio packages
│   ├── phrase_docx_handler.py# Phrase/Memsource bilingual
│   ├── cafetran_docx_handler.py # CafeTran bilingual
│   ├── supermemory.py        # Vector-indexed semantic TM (ChromaDB)
│   ├── spellcheck_manager.py # Spellcheck with pyspellchecker/Hunspell
│   ├── prompt_library.py     # AI prompt management
│   └── ...                   # See module list below
├── user_data/                 # User content (gitignored)
│   ├── prompts/              # .svprompt files
│   ├── termbases/            # .db termbase files
│   ├── translation_memories/ # .db TM files
│   ├── dictionaries/         # Custom spellcheck words
│   └── supermemory/          # ChromaDB vector database
├── assets/                    # Icons, images
├── docs/                      # Documentation site
├── tests/                     # Test files
└── legacy_versions/           # Historical Tkinter version
```

---

## 🔧 Key Technical Details

### Main Application (`Supervertaler.py`)

The main file is a large monolithic PyQt6 application. Key sections:

| Line Range | Purpose |
|------------|---------|
| 1-700 | Imports, constants, Project dataclass |
| 700-2000 | Custom widgets (grid editors, checkboxes) |
| 2000-4500 | MainWindow initialization, UI setup |
| 4500-8000 | Menu actions, file operations |
| 8000-12000 | Settings dialogs |
| 12000-18000 | Grid operations, navigation |
| 18000-25000 | Import/Export handlers |
| 25000-32000 | AI translation, batch operations |

### Key Classes

```python
@dataclass
class Project:
    segments: List[Segment]
    source_lang: str
    target_lang: str
    original_docx_path: Optional[str] = None
    memoq_source_path: Optional[str] = None
    sdlppx_source_path: Optional[str] = None
    phrase_source_path: Optional[str] = None
    original_txt_path: Optional[str] = None
    # ... 20+ fields total

@dataclass
class Segment:
    source: str
    target: str = ""
    status: str = "Not Started"
    notes: str = ""
    segment_type: str = "text"
    # ... additional fields
```

### File Extensions

| Extension | Purpose |
|-----------|---------|
| `.svproj` | Supervertaler project files (JSON) |
| `.svprompt` | Prompt files (JSON) |
| `.svntl` | Non-translatables lists (JSON) |

---

## 🔌 Complete Module List

### AI & LLM (`modules/`)
- `llm_clients.py` - OpenAI, Anthropic Claude, Google Gemini, Ollama integration
- `model_version_checker.py` - Auto-detect new LLM models from providers
- `model_update_dialog.py` - UI for selecting new models
- `prompt_library.py` - Prompt management and favorites
- `prompt_assistant.py` - AI-powered prompt generation
- `unified_prompt_library.py` - Unified prompt system
- `unified_prompt_manager_qt.py` - Prompt manager UI
- `voice_dictation.py` - Whisper-based voice input
- `ai_actions.py` - AI action system for prompt library
- `ai_attachment_manager.py` - File attachment persistence
- `ai_file_viewer_dialog.py` - File viewing dialog

### Translation Memory & Terminology
- `translation_memory.py` - Fuzzy matching TM system
- `supermemory.py` - ChromaDB vector semantic search (2100+ lines)
- `termbase_manager.py` - SQLite-based terminology
- `term_extractor.py` - Automatic term extraction
- `termbase_entry_editor.py` - Term editing UI
- `termbase_import_export.py` - TMX/TBX import/export
- `tm_manager_qt.py` - TM management UI
- `tm_metadata_manager.py` - TM metadata handling
- `tm_editor_dialog.py` - TM editing dialog
- `tmx_editor.py` / `tmx_editor_qt.py` - TMX file editing
- `tmx_generator.py` - TMX file generation

### File Handlers
- `docx_handler.py` - Standard DOCX import/export
- `sdlppx_handler.py` - Trados Studio SDLPPX/SDLRPX packages (767+ lines)
- `phrase_docx_handler.py` - Phrase/Memsource bilingual DOCX
- `cafetran_docx_handler.py` - CafeTran bilingual DOCX
- `trados_docx_handler.py` - Trados bilingual review DOCX
- `mqxliff_handler.py` - memoQ XLIFF files
- `simple_segmenter.py` - Text segmentation

### Spellcheck & QA
- `spellcheck_manager.py` - Dual-backend spellcheck (pyspellchecker + Hunspell)
- `non_translatables_manager.py` - Non-translatable term management
- `tag_cleaner.py` - CAT tool tag removal
- `tag_manager.py` - Tag handling

### UI Components
- `ribbon_widget.py` - Ribbon-style toolbar
- `translation_results_panel.py` - Match display panel
- `termview_widget.py` - Inline term display
- `superlookup.py` - Unified lookup window
- `superbrowser.py` - Multi-chat AI browser
- `quick_access_sidebar.py` - Quick access panel
- `keyboard_shortcuts_widget.py` - Shortcut management
- `project_home_panel.py` - Project home UI

### Utilities
- `database_manager.py` - SQLite database operations
- `database_migrations.py` - Database schema migrations
- `config_manager.py` - Settings management
- `file_dialog_helper.py` - File dialog utilities
- `find_replace.py` - Find and replace functionality
- `shortcut_manager.py` - Keyboard shortcut handling
- `theme_manager.py` - UI theme management
- `statuses.py` - Segment status definitions

### Specialized Tools
- `pdf_rescue_Qt.py` - AI OCR for PDF extraction
- `image_extractor.py` - Extract images from DOCX
- `figure_context_manager.py` - Image context for AI
- `document_analyzer.py` - Document analysis
- `encoding_repair.py` / `encoding_repair_Qt.py` - Fix encoding issues
- `autofingers_engine.py` - memoQ AutoFingers automation
- `tracked_changes.py` - Track changes analysis
- `supercleaner.py` / `supercleaner_ui.py` - Text cleaning

### Benchmarking
- `llm_leaderboard.py` - LLM quality benchmarking
- `superbench_ui.py` - Benchmark UI
- `local_llm_setup.py` - Ollama setup wizard

---

## 🏗️ Architecture Patterns

### UI Pattern
- PyQt6 with custom styled widgets
- Consistent styling:
  - Checkboxes: `CheckmarkCheckBox` (Standard), `PinkCheckmarkCheckBox` (Project), `BlueCheckmarkCheckBox` (Global)
  - Radio Buttons: `CheckmarkRadioButton` (Standard Green)
- Tag-based text formatting (`<b>`, `<i>`, `<u>`, `<li-o>`, `<li-b>`)
- Grid-based segment editor with source (read-only) and target (editable) columns

### Data Flow
1. Import file → Parse to segments → Display in grid
2. User translates/edits → Status updates → Grid refreshes
3. Export → Reconstruct original format with translations

### Settings Storage
- `user_data/general_settings.json` - App preferences
- `user_data/ui_preferences.json` - Window geometry, button states
- `.svproj` files - Per-project settings

---

## 📝 Development Guidelines

### When Editing Supervertaler.py
1. The file is large (~32K lines) - use line ranges when reading
2. Search for method names with `grep_search` before editing
3. Follow existing patterns for new features
4. Update `__version__` at the top when making changes

### When Adding New Modules
1. Create in `modules/` directory
2. Add import in main file where needed
3. Follow existing module patterns (docstrings, type hints)

### Documentation Updates
**Always update these files after changes:**
1. `AGENTS.md` - Add dated entry to development history
2. `CHANGELOG.md` - Add version entry
3. `README.md` - Update version badge if needed

### Commit Messages
Use semantic prefixes:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `refactor:` - Code restructuring
- `style:` - Formatting

---

## ⚠️ Common Pitfalls

1. **ElementTree namespaces** - Always use namespace dict when working with SDLXLIFF:
   ```python
   NAMESPACES = {'sdl': 'http://sdl.com/FileTypes/SdlXliff/1.0'}
   element.find('.//sdl:seg', NAMESPACES)
   ```

2. **Grid widget access** - Use `table.cellWidget()` for QTextEdit, `table.item()` for QTableWidgetItem

3. **File paths** - Store absolute paths, use `os.path.exists()` before accessing

4. **Status updates** - Remember to update both internal data and grid display

5. **Signal blocking** - When setting text programmatically, use `blockSignals(True/False)` to prevent cascading events

6. **Qt event queue** - Be aware that `setPlainText()` queues events even when signals are blocked

7. **Hidden widget styling** - Qt may not apply stylesheets to hidden widgets. If theme colors aren't appearing, apply styles when the widget becomes visible, not just at creation time

8. **Race conditions & timing** - When debugging UI issues, consider whether the problem might be timing-related:
   - Widgets created before theme manager is initialized
   - Styles applied while widgets are hidden
   - Signals firing before handlers are connected
   - Use `QTimer.singleShot()` for deferred initialization when needed

---

## 💡 Problem-Solving Tips for AI Agents

When stuck on a difficult bug, consider these approaches:

1. **Think about timing**: Is this a race condition? Are things happening in the wrong order?
   - Widget creation vs. theme application timing
   - Signal connections vs. signal emissions
   - Hidden vs. visible widget state changes

2. **Think outside the box**: The obvious solution may not work
   - If stylesheets aren't applying, try QPalette as an alternative
   - If a method isn't being called, check if the widget is even visible
   - If changes aren't reflected, check if there's caching involved

3. **Add debug output**: When behavior is mysterious, add logging to trace execution flow
   - Print method entry/exit with timestamps
   - Log parameter values and state
   - Write to a debug file if console output is too fast

4. **Question assumptions**: What do you THINK is happening vs. what is ACTUALLY happening?
   - The code might be running but not having the expected effect
   - A different code path might be executing
   - Something else might be overriding your changes

---

## 🧪 Testing

### Running Tests
```bash
pytest tests/
```

### Manual Testing Checklist
- [ ] Import DOCX, translate segment, export
- [ ] Save/load .svproj project
- [ ] TM matching works
- [ ] Termbase highlighting works
- [ ] AI translation (if API keys configured)
- [ ] Spellcheck toggles correctly
- [ ] SDLPPX import/export round-trip

---

## 🔑 API Keys

Store in `api_keys.txt` (gitignored):
```
openai_api_key=sk-...
anthropic_api_key=sk-ant-...
google_api_key=AI...
```

---

## 🔄 Recent Development History

### December 18, 2025 - Version 1.9.46: Workspace UI Redesign

**🏠 New Tab Hierarchy**

Cleaner, more intuitive tab structure:

- **Main tabs**: 🏠 Workspace → 🛠️ Tools → ⚙️ Settings
- **Workspace subtabs**: 📝 Editor (the grid) + 📚 Resources (TM, Termbases, Prompts, etc.)
- Removed Document View (unused feature)
- Simplified View menu (removed Grid/Document view switcher)

**Naming Philosophy:**
- "Workspace" - generic term that works for translation, localization, and copywriting
- "Editor" - describes what you do (edit content), not the UI (grid)
- "Resources" - all project resources in one place

**🐛 Critical Bug Fix: Termbase Activation**

Fixed termbase matches showing terms from non-activated termbases:
- Added `AND (ta.is_active = 1 OR tb.is_project_termbase = 1)` filter to `search_termbases()` query
- Now only returns terms from termbases with Read checkbox enabled

**Files Modified:**
- `Supervertaler.py` - `create_main_layout()`, navigation menu, view menu
- `modules/database_manager.py` - `search_termbases()` activation filter

---

### December 18, 2025 - Version 1.9.47: Code Cleanup

**🧹 Dead Document View Code Removed**

Removed ~811 lines of unused Document View code. The Document View feature was never used in production - the Grid View (Editor) is the primary and only workflow.

**Removed Items:**
- `LayoutMode` class (GRID/DOCUMENT enum)
- `create_editor_widget()` - View switcher with Grid/List/Document buttons
- `create_home_tab()`, `create_projects_manager_tab()` - Deprecated wrappers
- `create_editor_tab()`, `switch_view_mode()` - View switching logic
- `switch_home_view_mode()` - Home tab view switching
- `create_document_view_widget()`, `create_document_view_widget_for_home()` - Document view creation
- `refresh_document_view()` - ~300 lines of document rendering code
- `_find_document_container()`, `_register_document_container()`, `_set_active_document_host()`, `_get_document_container()`, `_locate_document_container()` - Container helpers
- `_find_widget_by_object_name()` - Widget search helper
- Document View Methods section (on_doc_segment_clicked, on_doc_status_change, etc.)
- Document view state variables (doc_segment_widgets, doc_current_segment_id, document_containers, active_document_host, current_view_mode)

**Result:**
- File reduced from 35,249 to 34,438 lines
- Cleaner codebase, easier to maintain
- No functional changes - Grid View (Editor) is unaffected

---

### December 17, 2025 - Version 1.9.45: Termbase Highlight Styles & Spellcheck Auto-Language

**🏷️ Configurable Termbase Highlight Styles**

Three visual styles for termbase term highlighting in the translation grid:

- **Background (Default)**: Pastel green shades based on priority (existing behavior)
- **Dotted Underline**: DotLine underline with priority-based colors
  - Priority 1: Red
  - Priority 2-3: Gray shades  
  - Priority 4+: User-configurable color (default dark green)
  - Reset button to restore default color
- **Semibold**: DemiBold font weight with tinted green foreground colors

**Settings UI:**
- New "🏷️ Termbase Highlight Style" section in Settings → View Settings
- Radio button selection for style type
- Color picker for dotted underline (Priority 4+)
- Reset button to restore default color

**🔤 Spellcheck Auto-Language Initialization**

Fixed spellcheck not using project's target language:

- **All Import Handlers**: DOCX, TXT, memoQ, CafeTran, Trados bilingual, SDLPPX, Phrase now initialize spellcheck for target language
- **Project Load**: Always sets spellcheck to project target language (ignores old saved language)
- **Short Code Support**: Added `SHORT_CODE_MAP` in spellcheck_manager.py to handle "nl" → "nl_NL", "de" → "de_DE", etc.

**Bug Fixes:**
- Fixed NT list crash (`lst.active` → `lst.is_active`)
- Fixed NonTranslatable attributes (`pattern` → `text`, `description` → `notes`)
- Fixed Ctrl+K going to Settings instead of Superlookup (tab index 3 → 2)
- Renamed Grid/Document tabs to "Grid View"/"Document View"

**Files Modified:**
- `Supervertaler.py` - `highlight_termbase_matches()`, `_create_view_settings_tab()`, `_save_view_settings_from_ui()`, all import handlers, `load_project()`
- `modules/spellcheck_manager.py` - Added `SHORT_CODE_MAP`, updated `set_language()` to handle short codes

---

### December 16, 2025 - Version 1.9.41: Dark Mode Complete Implementation

**🌙 Full Dark Theme Support**

Completed comprehensive dark mode implementation after extensive debugging session:

- **Compare Boxes Fixed**: Translation Results panel compare boxes (Current Source, TM Source, TM Target) now properly dark in dark mode
- **Termview Visibility**: All words in Termview pane now visible - non-matched words use light text color
- **Root Cause Discovery**: Qt doesn't reliably apply stylesheets to hidden widgets
- **Solution**: Added `_apply_compare_box_theme()` method called when compare frame becomes visible

**Technical Changes:**
- `modules/translation_results_panel.py` - Added `_apply_compare_box_theme()`, uses both stylesheet AND QPalette for reliability
- `modules/termview_widget.py` - Made `TermBlock` and `NTBlock` theme-aware with `theme_manager` parameter

**Key Lesson Learned:**
When Qt stylesheets aren't visually applying despite the code running correctly, consider:
1. Widget visibility state at time of styling
2. Using QPalette as an alternative/supplement to stylesheets
3. Re-applying styles when widget becomes visible

---

### December 17, 2025 - Version 1.9.42: Multi-File Project Support

**📁 Import Folder (Multiple Files)**

Major new feature allowing users to import entire folders of files as a single multi-file project:

- **New Menu Item**: File → Import → Folder (Multiple Files)...
- **Supported Formats**: DOCX and TXT files in selected folder
- **File Selection Dialog**: Preview files with size, select/deselect individual files
- **Language Pair Selection**: Set source/target language for all files
- **Progress Dialog**: Shows import progress with per-file segment counts

**🗂️ Per-File Progress Tracking**

- **File Progress Dialog**: View → File Progress... (or click on status bar)
- **Per-File Statistics**: Segments, words, translated, confirmed, progress bar for each file
- **Status Indicators**: ✅ Complete, 📝 Translated, 🔄 In Progress, ⬜ Not Started
- **Navigation**: Double-click file to jump to its first segment

**📊 Status Bar Enhancement**

- **Files Indicator**: Shows "📁 Files: X/Y" for multi-file projects (completed/total)
- **Clickable**: Click the files indicator to open File Progress dialog
- **Tooltip**: Hover for file count and completion summary

**🔍 File Filter Dropdown**

- **New Dropdown**: Appears in filter panel for multi-file projects
- **Filter by File**: Select a specific file to show only its segments
- **All Files**: Default option to show all segments from all files

**Data Model Changes:**
- `Segment` dataclass: Added `file_id` (int) and `file_name` (str) fields
- `Project` dataclass: Added `files` (list of file metadata) and `is_multifile` (bool) fields
- Backward compatible: Single-file projects work unchanged

**📤 Export Folder (Multiple Files)**

- **New Menu Item**: File → Export → Folder (Multiple Files)...
- **Format Options**: TXT (plain text), DOCX (formatted), Bilingual (Source/Target table)
- **File Preview**: Shows all files with format, segment count, and status
- **Progress Dialog**: Shows export progress with per-file updates

**New Methods in Supervertaler.py:**
- `import_folder_multifile()` - Folder import dialog
- `_import_multifile_project()` - Import multiple files into single project
- `export_folder_multifile()` - Folder export dialog
- `_export_multifile_to_folder()` - Export multiple files to folder
- `_export_file_as_txt()` - Export single file as plain text
- `_export_file_as_docx()` - Export single file as formatted DOCX
- `_export_file_as_bilingual()` - Export single file as bilingual DOCX table
- `show_file_progress_dialog()` - Per-file progress dialog
- `_add_overall_progress_section()` - Overall progress stats
- `_on_file_filter_changed()` - File filter dropdown handler
- `_update_file_filter_combo()` - Populate file filter dropdown

**🔧 Source File Backup & Recovery (added later)**

- **Automatic Backup**: Source files now copied to `_source_files/` folder inside project directory during import
- **Relocate Source Folder**: File → Relocate Source Folder... menu item to fix broken paths when source files are moved
- **Export Warning**: Shows helpful message when source files are missing, suggests using Relocate feature

**🔍 Superlookup Fixes**

- **Class Renamed**: `UniversalLookupTab` → `SuperlookupTab` for consistency
- **Theme Support**: Added `theme_manager` attribute for theme-aware search term highlighting
- **Fixed Error**: Resolved `'UniversalLookupTab' object has no attribute 'theme_manager'` error

**📋 Spellcheck Info Dialog Redesign**

- **Compact Layout**: Completely redesigned to fit on screen without scrolling off the bottom
- **Horizontal Top Row**: Status, language dropdown, and backend indicator on one line
- **Collapsible Troubleshooting**: Diagnostics section collapsed by default (click to expand)
- **Inline Links**: Download links for Hunspell dictionaries in horizontal row with separators
- **Max Height**: Dialog limited to 500px to prevent overflow

---

### December 12, 2025 - Trados Bilingual DOCX Workflow Documentation

**📚 Comprehensive Trados Workflow Documentation**

Added critical workflow documentation for Trados Bilingual Review DOCX format:

- **Import dialog warning**: `import_trados_bilingual()` now shows detailed ⚠️ CRITICAL WORKFLOW warning explaining the required preparation steps
- **CAT_WORKFLOW.md**: Updated Trados Studio section with both SDLPPX (recommended) and Bilingual DOCX (workaround) workflows
- **QUICK_START.md**: Added warning note directing users to full documentation

**The Critical Workflow:**
The Trados Bilingual Review format is designed for **review only**, not translation - it doesn't export empty target segments! ([RWS Community reference](https://community.rws.com/product-groups/trados-portfolio/trados-studio/f/studio/34874/export-for-bilingual-review-exports-only-source-text))

Required workaround:
1. In Trados: Copy source to target (fills empty segments)
2. Export as Bilingual Review DOCX
3. In Word: Delete all target text (cells exist but are empty)
4. Import into Supervertaler, translate, export
5. Reimport into Trados Studio

**Files Modified:**
- `Supervertaler.py` - `import_trados_bilingual()` warning dialog (line ~18562)
- `docs/guides/CAT_WORKFLOW.md` - Comprehensive Trados section with both workflows
- `docs/guides/QUICK_START.md` - Warning note with link to full documentation

---

### December 12, 2025 - Version 1.9.40: Superlookup Unified Concordance System

**🔍 Ctrl+K Now Opens Superlookup**

- Major consolidation: Concordance search now uses Superlookup instead of separate dialog
- All lookup resources in one place: TM, Termbase, Supermemory, MT, Web Resources
- Selected text in source/target automatically populates search field
- `show_concordance_search()` now calls `_go_to_superlookup()` and triggers search

**📊 Dual-View Toggle for TM Matches**

- Horizontal (Table): Source | Target columns side-by-side - compact, scannable
- Vertical (List): Dutch: ... / English: ... stacked - traditional concordance layout
- Radio button toggle in TM Matches tab
- Both views stay in sync with search results
- `toggle_tm_view_mode()` and `display_tm_results()` updated for dual display

**🗂️ Tab Reorganization**

- "Resources" renamed to "Project Resources"
- Tab order changed: Project Editor → Project Resources → Prompt Manager → Tools → Settings
- Removed "Concordance" and "Import/Export" tabs from Translation Memories (redundant)
- Source text box in Superlookup shrunk from 100px to 50px
- "Termbase Terms" renamed to "Termbase Matches"

**⚡ FTS5 Full-Text Search Optimization**

- `concordance_search()` in database_manager.py now uses FTS5 MATCH queries
- 100-1000x faster than previous LIKE queries on large databases
- Auto-sync: FTS5 index rebuilt on connect if out of sync
- New methods: `rebuild_fts_index()`, `check_fts_index()`

**🐛 ChromaDB Stability Fix**

- Removed all `collection.count()` calls that caused native Rust crashes
- Stats now use SQLite metadata count instead of ChromaDB collection queries
- ChromaDB 0.6.3 with tokenizers 0.22.0 (stable combination)

**Files Modified:**
- `Supervertaler.py` - show_concordance_search(), create_tm_results_tab(), display_tm_results(), tab ordering
- `modules/database_manager.py` - concordance_search() FTS5, rebuild_fts_index(), check_fts_index()
- `modules/supermemory.py` - Removed collection.count() calls, uses metadata for stats

---

### December 11, 2025 - Version 1.9.39: Superlookup Multilingual Search

**🔍 Multilingual Language Filtering**

- Added From/To language dropdown filters in Superlookup search bar
- Filter TM and termbase searches by source/target language pair
- Languages auto-populate from TMs and termbases on first tab view
- Alphabetically sorted with language family grouping (all Dutch variants together, etc.)
- Display format: "English (en)", "Dutch (nl-BE)" for clarity

**↔️ Search Direction Controls**

- Radio buttons: Both (bidirectional), Source only, Target only
- Concordance search respects direction setting
- Termbase search also respects direction for bidirectional term lookup

**🎨 UI Improvements**

- Yellow highlighting of search terms in TM/termbase results
- Compact results display with word wrap and 60px max row height
- Tooltips show full text on hover
- Hidden row numbers for cleaner display
- Removed Manual Capture button (redundant with paste)
- Removed Operating Modes dropdown (only Universal mode used)

**Files Modified:**
- `Supervertaler.py` - UniversalLookupTab UI, language dropdowns, direction radio buttons, display methods
- `modules/superlookup.py` - search_tm() accepts direction and language parameters
- `modules/translation_memory.py` - concordance_search() accepts language filters
- `modules/database_manager.py` - concordance_search() filters by source_lang/target_lang

---

### December 11, 2025 - Version 1.9.38: Project File & UX Improvements

**📁 Reorganized .svproj File Structure**

- Metadata now at top of file (name, languages, dates, ID)
- Settings next (prompts, TM, termbases, spellcheck)
- Source paths follow (DOCX, memoQ, Trados, CafeTran, SDLPPX)
- Segments moved to END of file for easier human inspection

**💡 Improved Batch Translate Warning**

- Added tip about using Select All + Clear Target from right-click menu
- Users no longer need to re-import memoQ files just to clear targets

**Files Modified:**
- `Supervertaler.py` - `Project.to_dict()`, batch translate warning message

---

### December 11, 2025 - Version 1.9.37: User-Configurable Grid Fonts

**🔤 Font Customization in Settings → View Settings**

- Added font family dropdown with 10 popular fonts (Calibri, Segoe UI, Arial, Consolas, Verdana, Times New Roman, Georgia, Courier New, Tahoma, Trebuchet MS)
- Added live preview panel showing sample source/target text with tags - updates in real-time as you adjust settings
- Font family now persists between sessions (previously only font size was saved)
- Fixed font size spinbox up/down arrows with improved styling and click targets
- Added friendly note: "If your favourite font is missing, contact the developer!"

**Files Modified:**
- `Supervertaler.py` - `_create_view_settings_tab()`, `_save_view_settings_from_ui()`, `load_font_sizes_from_preferences()`, `save_current_font_sizes()`

---

### December 10, 2025 - Version 1.9.35: memoQ Red Tag Color Fix + Universal Tag Coloring

**🔴 memoQ Inline Tag Color Preservation (Export)**

Fixed critical issue where red/magenta inline tags (e.g., `{1}`, `[2}`) in memoQ bilingual exports were appearing as black text in the target column.

**Root Cause Discovery:**
- memoQ stores tag colors in **character styles** (e.g., `mqInternal`), not directly on the run
- The `mqInternal` style defines color `800000` (dark red) at the style level
- `python-docx` API (`run.font.color.rgb`) returns `None` for style-based colors

**Solution Implemented:**
- Added 3-tier color extraction method in `export_memoq_bilingual()`:
  1. Check `run.font.color.rgb` (direct color)
  2. Check XML `w:color` element in `rPr` (inline XML color)
  3. **NEW**: Check `w:rStyle` element, lookup character style, extract style's color

---

**🎨 Universal Tag Coloring in Grid (Display)**

Extended `TagHighlighter` to color ALL CAT tool tags with pink (`#FFB6C1`) in the translation grid:

| Format | Tag Examples | Status |
|--------|-------------|--------|
| HTML/XML | `<b>`, `<i>`, `<u>`, `<li-o>` | ✅ Already worked |
| memoQ | `{1}`, `[2}`, `{3]`, `[4]` | ✅ NEW |
| Trados | `<1>`, `</1>` | ✅ NEW |
| Phrase | `{1}`, `{2}` | ✅ NEW |

**CafeTran Pipe Fix:**
- Pipe symbols (`|`) now only highlighted red in **CafeTran projects**
- Previously, pipes were red in ALL project types (bug)
- Added `TagHighlighter._is_cafetran_project` class flag

**Files Modified:**
- `Supervertaler.py` - `TagHighlighter.highlightBlock()`, CafeTran import function

### December 10, 2025 - Version 1.9.34: UI Fixes

**🎨 Global UI Standardization**
- Replaced standard OS radio buttons with custom green `CheckmarkRadioButton`.
- Unified design across Filters, Import, AutoFingers, and Find/Replace dialogs.
- Replaced default radio buttons in Import TMX dialogue with standard `CheckmarkRadioButton` widgets
- Ensures consistency with application's green UI theme

---

### December 10, 2025 - Version 1.9.32: Trados SDLRPX Status Fix

**📦 Fixed Critical SDLRPX Export Bug**
- Fixed segments staying in "Draft" status instead of being updated to "Translated" in exported SDLRPX packages
- Trados Studio now correctly recognizes translated segments when client opens return package
- Added `_update_segment_status()` method to `modules/sdlppx_handler.py`
- Updates `conf` attribute in `sdl:seg-defs` section of SDLXLIFF files

**Root Cause:**
- The `_update_xliff_tree()` function was updating target text but not updating the `conf` attribute
- SDL/Trados uses `conf="Draft"` vs `conf="Translated"` in `<sdl:seg>` elements

---

### December 10, 2025 - Version 1.9.33: Spellcheck Update Fix

**🐛 Fixed Spellcheck Highlighting Bug**
- Fixed issue where adding/ignoring words only removed underline in the current cell
- Now triggers global refresh of all highlighters
- Modified `_add_to_dictionary` and `_ignore_word` in `EditableGridTextEditor`

---

### December 10, 2025 - Version 1.9.31: Spellcheck Language Fix

- Spellcheck now correctly uses the project's target language instead of defaulting to English
- Added language dropdown in Spellcheck Info dialog

---

### December 10, 2025 - Version 1.9.30: Critical LLM Fix

- Removed hardcoded debug file path that caused "No such file or directory" errors

---

### December 10, 2025 - Version 1.9.29: Spellcheck Integration

- Red wavy underlines for misspelled words
- Right-click context menu with suggestions
- Add to Dictionary, Ignore Word
- New module: `modules/spellcheck_manager.py`

---

### December 9, 2025 - Version 1.9.28: Phrase DOCX & Show Invisibles

- Phrase (Memsource) bilingual DOCX support
- Show Invisibles feature (spaces, tabs, line breaks)

---

### December 9, 2025 - Version 1.9.27: Simple Text Import/Export

- Import text files (each line = segment)
- Export translations as text

---

### December 8, 2025 - Version 1.9.26: Model Version Checker

- Auto-detect new LLM models from OpenAI, Anthropic, Google

---

### December 7, 2025 - Version 1.9.24: Smart Word Selection

- Selecting part of word expands to full word

---

### December 5, 2025 - Version 1.9.20: SDLPPX Persistence

- Package path saved in .svproj files

---

### December 4, 2025 - Version 1.9.19: Trados Package Support

- Import SDLPPX, export SDLRPX
- New module: `modules/sdlppx_handler.py`

---

### December 3-4, 2025 - Version 1.9.17-18: Supermemory

- Domain management, filtering, Superlookup integration
- Concordance Search with semantic tab

---

### December 2, 2025 - Supermemory: Vector TM

- ChromaDB + Sentence-Transformers
- Semantic search across TMs
- Module: `modules/supermemory.py` (2100+ lines)

---

### December 1, 2025 - Version 1.9.16: Ollama Support

- Local LLM translation with Ollama

---

### November 30, 2025 - Versions 1.9.13-15

- Document Preview tab
- Bilingual Table export/import

---

### November 27-28, 2025 - Versions 1.9.8-11

- CafeTran integration
- Navigation improvements

---

### November 8-9, 2025 - Unified Prompt System

- 2-layer prompt architecture
- AI Assistant for prompt generation

---

### November 7, 2025 - TagCleaner

- CAT tool tag removal module

---

### November 6, 2025 - LLM Integration Complete

- Multi-LLM support operational

---

## 🗄️ Database Schema (SQLite)

### Core Tables
- **translation_units** - TM entries
- **termbases** - Termbase definitions
- **termbase_terms** - Individual terms
- **termbase_activation** - Project termbase tracking
- **non_translatables** - Locked terms
- **projects** - Translation projects

### Naming Conventions
- ✅ Use "Termbase" (one word)
- ❌ Never use "Glossary" or "glossary_terms"

---

## 📚 Additional Resources

| File | Purpose |
|------|---------|
| `CHANGELOG.md` | Complete version history |
| `README.md` | User-facing documentation |
| `FAQ.md` | Common questions |
| `docs/guides/` | User guides |

---

*This file replaces the previous CLAUDE.md and PROJECT_CONTEXT.md files.*
*Last updated: December 16, 2025 - v1.9.41*
