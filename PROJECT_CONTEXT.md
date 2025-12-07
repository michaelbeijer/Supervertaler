# Supervertaler Project Context

**Last Updated:** December 7, 2025
**Current Version:** v1.9.24
**Repository:** https://github.com/michaelbeijer/Supervertaler
**Maintainer:** Michael Beijer

---

## 📅 Recent Development Activity

### December 7, 2025 - Version 1.9.24: Smart Word Selection & Error Handling

**✨ Smart Word Selection Feature**
Implemented intelligent word selection inspired by CafeTran's UX:

- **Feature Behavior:**
  - Selecting part of a word (e.g., "ductiv" in "productivity") automatically expands to full word
  - Works in both source (read-only) and target (editable) grid columns
  - Supports compound words with hyphens: "self-contained", "mother-in-law"
  - Supports contractions with apostrophes: "don't", "can't", "l'homme"
  - 50-character threshold prevents interference with multi-word selections
  - Boundary detection only expands when selection is partial

- **Settings Integration:**
  - Added toggle checkbox in Settings → General → Editor Settings
  - Option: "Enable smart word selection" (enabled by default)
  - Helpful tooltip with examples and use cases
  - Setting persists in `general_settings.json`
  - Loaded on startup into `self.enable_smart_word_selection`

- **Implementation Details:**
  - Modified `ReadOnlyGridTextEditor` (lines 1506-1562): Added `mouseReleaseEvent()`
  - Modified `EditableGridTextEditor` (lines 1942-1989): Added identical `mouseReleaseEvent()`
  - Word character detection: `char.isalnum() or char in "_-'"` (alphanumeric + underscore + hyphen + apostrophe)
  - Both classes include `_get_main_window()` helper to access settings
  - Checks `main_window.enable_smart_word_selection` before expanding
  - Uses `QTextCursor` with `MoveMode.KeepAnchor` for selection

- **Settings UI Changes:**
  - Lines 11645-11662: New "Editor Settings" QGroupBox
  - Checkbox with tooltip explaining feature
  - Stored as `self.smart_selection_checkbox` for save operation
  - Line 11834: Added parameter to save button connection
  - Line 12983: Added `smart_selection_cb=None` parameter to save function
  - Line 13019: Saves to settings dict
  - Line 19437: Loads setting on startup

- **Documentation:**
  - Created `user_data_private/Development docs/SMART_WORD_SELECTION.md`
  - Comprehensive feature documentation with testing checklist
  - Known limitations, future enhancements, implementation details

**🛡️ Supermemory Error Handling**
Fixed PyTorch DLL loading errors with helpful user guidance:

- **Problem:**
  - User reported: `[WinError 1114] A dynamic link library (DLL) initialization routine failed`
  - PyTorch's `c10.dll` failed to load on Windows
  - Common issue: Missing Visual C++ Redistributables

- **Solution:**
  - Modified `modules/supermemory.py` (lines 45-51):
    - Changed `except ImportError` to `except (ImportError, OSError, Exception) as e`
    - Now properly catches Windows DLL errors (OSError)
    - Stores error message in `SENTENCE_TRANSFORMERS_ERROR`
  - Modified `Supervertaler.py` (lines 4116-4126):
    - Enhanced exception handler in `_auto_init_supermemory()`
    - Detects DLL-related errors ("DLL", "c10.dll", "torch" in error message)
    - Provides 3 specific fixes with direct links and commands:
      1. Install Visual C++ Redistributables (https://aka.ms/vs/17/release/vc_redist.x64.exe)
      2. Reinstall PyTorch: `pip uninstall torch sentence-transformers` then `pip install torch sentence-transformers`
      3. Disable Supermemory auto-init in Settings → AI Settings
    - Instructions appear automatically in log when DLL error occurs

- **User Impact:**
  - Clear, actionable error messages instead of cryptic Windows errors
  - Direct download links for required software
  - Exact pip commands to fix PyTorch installation
  - Fallback option to disable feature if fixes don't work

**Files Modified:**
- `Supervertaler.py`: Version 1.9.24, smart selection, error messages, settings UI
- `modules/supermemory.py`: Enhanced exception catching
- `CHANGELOG.md`: v1.9.24 entry
- `PROJECT_CONTEXT.md`: This update
- `user_data_private/Development docs/SMART_WORD_SELECTION.md`: Feature documentation

---

### December 7, 2025 - Version 1.9.23: Bilingual Table Landscape Orientation

**📄 Export Format Improvement**
Improved bilingual table exports for better readability:

- **Landscape Orientation:**
  - Changed Supervertaler Bilingual Table exports from portrait to landscape
  - Provides significantly more horizontal space for source and target columns
  - Improves visualization of long segments (common in technical/legal translation)
  - Applies to both export options: "With Tags" and "Formatted"

- **Implementation:**
  - Modified `Supervertaler.py` line 7820-7832 in `_export_review_table()` method
  - Added `from docx.enum.section import WD_ORIENT`
  - Set `section.orientation = WD_ORIENT.LANDSCAPE`
  - Swapped page dimensions: `section.page_width, section.page_height = section.page_height, section.page_width`
  - Maintained existing 0.5-inch margins on all sides

- **User Impact:**
  - Files → Export → Supervertaler Bilingual Table (both options) now create landscape documents
  - No changes to import functionality
  - Backwards compatible - can still import old portrait-mode tables

---

### December 7, 2025 - Version 1.9.22: Gemini 3 Pro Preview Support

**🤖 Google Gemini 3 Integration**
Added support for Google's latest AI model released November 2025:

- **Model Addition:**
  - Added `gemini-3-pro-preview` to Settings → LLM Settings → Gemini Models dropdown
  - Label: "gemini-3-pro-preview (Latest - Superior Performance)"
  - Tooltip updated to describe capabilities: "Latest model with superior reasoning and coding"
  - Also added missing models: `gemini-2.5-flash-lite` and `gemini-2.5-pro`

- **Implementation:**
  - Modified `Supervertaler.py` lines 10889-10902 (model dropdown)
  - Modified `modules/llm_clients.py` lines 220-229 (supported models list)
  - Updated module header documentation (lines 8-11)
  - Works in both single segment translation (Ctrl+T) and batch translation

- **Performance vs Gemini 2.5 Pro:**
  - 10-20% average improvement across benchmarks
  - 6.3x improvement on ARC-AGI-2 abstract reasoning
  - 20x improvement on MathArena Apex (23.4% vs <5%)
  - 35-50% higher accuracy on software engineering tasks
  - Pricing: $2/$12 per MTok (input/output) vs $1.25/$10 for 2.5 Pro

- **Technical Details:**
  - Model properly integrated with existing LLMClient architecture
  - Settings correctly loaded via `settings.get('gemini_model', 'gemini-2.5-flash')`
  - Batch translation uses model parameter from settings at line 25468-25471
  - Direct LLM search uses model parameter at line 27321

---

### December 5, 2025 - Version 1.9.20: SDLPPX Project Persistence

**📦 SDLPPX/SDLRPX Persistence & Bug Fixes**
Complete round-trip workflow now persists across sessions:

- **Project Persistence:**
  - Added `sdlppx_source_path` field to Project dataclass (line 658)
  - Added serialization in `to_dict()` - saves path when saving project
  - Added deserialization in `from_dict()` - loads path when opening project
  - Handler automatically restored in `load_project()` when .svproj has sdlppx_source_path

- **Export Bug Fix:**
  - Fixed SDLRPX export showing "0 translations updated"
  - Root cause: export was reading notes from `table.item(row, 5)` but notes column never populated as QTableWidgetItem
  - Fix: read from `segment.notes` in `self.current_project.segments` instead
  - Verified translations correctly written to return package via PowerShell ZIP inspection

- **Complete Workflow Now Supported:**
  1. Import SDLPPX → 2. Translate → 3. Save .svproj → 4. Close
  5. Reopen → 6. Open .svproj → 7. Continue translating → 8. Export SDLRPX ✅

---

### December 4, 2025 - Version 1.9.19: Trados Studio Package Support

**📦 SDLPPX/SDLRPX Package Support**
Full round-trip support for Trados Studio project packages:

- **New Handler Module:** `modules/sdlppx_handler.py` (767 lines)
  - `TradosPackageHandler` class for package management
  - `SDLXLIFFParser` for parsing SDL-extended XLIFF files
  - Handles `<g>`, `<x/>`, `<mrk mtype="seg">` tags
  - Preserves SDL namespaces and attributes

- **Import SDLPPX:**
  - File → Import → Trados Studio → Package (SDLPPX)
  - Extracts and parses SDLXLIFF files from package
  - Shows package info dialog with file list and segment counts
  - Automatic language detection from package metadata
  - Preserves segment IDs in notes for round-trip export

- **Export SDLRPX:**
  - File → Export → Trados Studio → Return Package (SDLRPX)
  - Updates SDLXLIFF files with translations
  - Creates properly formatted return package ZIP
  - Workflow for freelance translators receiving packages

- **Menu Reorganization:**
  - New "Trados Studio" submenu under Import and Export
  - Groups bilingual review DOCX and package options together

---

### December 4, 2025 - Version 1.9.18: Supermemory Concordance Integration

**🔍 Concordance Search Supermemory Integration**
- Added Supermemory semantic search tab to Concordance Search (Ctrl+K)
- Two-tab interface: "TM Matches" (exact) and "Supermemory" (semantic)
- Tab headers show result counts
- Similarity scores with color-coded High/Medium/Low indicators

**🧠 Supermemory UI Improvements**
- Moved Supermemory from Tools to Resources tab
- Added "Active" checkbox column to TM table
- Only active TMs are searched in Concordance
- Checkbox state persists in database

**📄 Trados Bilingual DOCX Fixes**
- Fixed `xml:space="preserve"` on text elements
- Fixed target language (was incorrectly setting nl-NL on runs)
- Added language selection dialog on import
- Source file path persisted in project
- "Source File Not Found" offers browse option

**Other Changes:**
- Renamed export menus to "Supervertaler Bilingual Table"
- memoQ/CafeTran source paths persisted
- Concordance window geometry saved to project

---

### December 3, 2025 - Version 1.9.17: Supermemory Enhanced - Domains & Filtering

**🧠 Major Supermemory Enhancements**
Complete domain management system, filtering, Superlookup integration, and export functionality.

**New Features:**
- **Domain Management System**
  - New `domains` table in metadata database with default domains (General, Patents, Medical, Legal, Technical, Marketing, Financial, Software)
  - Domain Manager dialog (🏷️ Domains... button) for creating/editing/deleting domains
  - Each domain has name, description, color, and active status
  - Domain column added to indexed TMs table with color coding
  
- **TMX Import with Domain Selection**
  - When adding TMX files, a dialog now asks to select a domain category
  - Domain is stored with TMX metadata and all ChromaDB entries
  
- **Advanced Filtering**
  - Language pair filter dropdown (populated from indexed TMs)
  - Domain filter with multi-select activation
  - "Use active domains only" checkbox for search filtering
  - Filter button shows active count (e.g., "3/8 Domains ▼")
  
- **Dynamic Column Headers**
  - Search results now show actual language codes (e.g., "Source (EN)", "Target (NL)")
  - Updates automatically based on search results
  
- **Superlookup Integration**
  - New 🧠 Supermemory tab in Superlookup (Tools → Superlookup)
  - Semantic search runs automatically alongside TM and termbase searches
  - Results table with Similarity, Source, Target, Domain, TM columns
  - Copy target on double-click
  
- **Export Functionality**
  - New 📤 Export button in Supermemory header
  - Export to TMX or CSV format
  - Filter by domain or specific TM before export
  - Progress feedback during export
  
- **AI Settings Consolidation**
  - All AI settings moved to new "🤖 AI Settings" tab
  - Includes: Provider selection, API models, Ollama settings, Supermemory options
  - Removed AI settings from General tab for cleaner organization

**Technical Implementation:**
- `modules/supermemory.py` - Expanded to 2100+ lines
  - Added `Domain` dataclass
  - Added `domain` field to `MemoryEntry`, `IndexedTM`, `SearchResult`
  - New database migration for `domain` column
  - `domains` table with CRUD operations
  - `search()` now supports `domains` parameter
  - `search_by_active_domains()` convenience method
  - `get_context_for_llm()` now respects active domains
  - `export_to_tmx()` and `export_to_csv()` methods
  - `DomainManagerDialog` class
  - Updated `SupermemoryWidget` with filter UI

- `Supervertaler.py`
  - New `_create_ai_settings_tab()` method
  - New `_save_ai_settings_from_ui()` method
  - `UniversalLookupTab` updated:
    - Added `create_supermemory_results_tab()` method
    - Added `search_supermemory()`, `init_supermemory()` methods
    - `perform_lookup()` now includes Supermemory search

**Files Changed:**
- `modules/supermemory.py` - Major expansion (~900 new lines)
- `Supervertaler.py` - AI Settings tab, Superlookup integration

**Database Changes:**
- New `domains` table in `user_data/supermemory/metadata.db`
- New `domain` column in `indexed_tms` table (auto-migrated)

---

### December 2, 2025 - Supermemory: Vector-Indexed Translation Memory (Phase 1)

**🧠 New Feature: Supermemory**
Semantic search across translation memories using AI embeddings. Find translations by meaning, not just fuzzy text matching.

**What It Does:**
- **Import TMX files** into a local vector database
- **Semantic search** - find translations by meaning, not exact text match
- **Cross-TM search** - search ALL your indexed TMs at once
- **LLM context injection** - provide relevant TM examples to Ollama/Claude

**Technical Stack (all local, no cloud):**
- **ChromaDB** - Local vector database for embeddings
- **Sentence-Transformers** - Multilingual text embeddings (paraphrase-multilingual-MiniLM-L12-v2)
- **SQLite** - Metadata storage

**Installation:**
```
pip install chromadb sentence-transformers
```
First run downloads embedding model (~420MB), then everything runs offline.

**Files Created:**
- `modules/supermemory.py` - Complete module (800+ lines initially, now 2100+)

**UI Location:** Tools → 🧠 Supermemory

**Completed Phases:**
- ✅ Phase 1: TMX indexer + semantic search UI
- ✅ Phase 2: Domain management + filtering + Superlookup integration
- 🔮 Phase 3: OPUS corpus integration, consistency checking

---

### December 1, 2025 - Version 1.9.16: Local LLM Support (Ollama)

**Feature Request:** Add UI to create custom Ollama models with optimized settings.

**Why Needed:**
- Default Ollama context window (2K-4K tokens) may be too small for long segments
- Custom system prompts improve translation quality for specific domains
- Lower temperature (0.2) is better for translation accuracy vs creativity

**Planned Implementation:**
A "Create Custom Model" button in Local LLM Setup that:
1. Lets user pick base model (qwen2.5:32b, aya-expanse:8b, etc.)
2. Sets optimal parameters:
   - `num_ctx 32768` (32K context window)
   - `temperature 0.2` (precision over creativity)
3. Adds configurable system prompt (e.g., patent translator persona)
4. Creates model via `ollama create <name> -f <Modelfile>`

**Manual Workaround (Current):**
Users can manually create a Modelfile:
```
FROM qwen2.5:32b
PARAMETER num_ctx 32768
PARAMETER temperature 0.2
SYSTEM """
You are a specialized translator. Preserve terminology, be literal over fluent.
Output only the translation without preamble.
"""
```
Then run: `ollama create my-translator -f Modelfile`

---

### November 30, 2025 - Version 1.9.15: Bilingual Table Export/Import

**📋 New Supervertaler Bilingual Table Feature**
Complete bilingual export/import workflow for all project types:

**Export Options (File → Export):**
- **"Bilingual Table - With Tags (DOCX)"**: Exports 5-column table with segment numbers, source, target (with raw Supervertaler tags), status, and notes column. Intended for proofreaders who will return the file for re-import
- **"Bilingual Table - Formatted (DOCX)"**: Same structure but applies formatting: `<b>` becomes actual bold, `<i>` becomes italic, `<u>` becomes underline, and list tags become visible markers (• for bullets, ◦ for nested). Shows warning that this version cannot be re-imported with tags

**Import Option (File → Import):**
- **"Bilingual Table (DOCX) - Update Project"**: Re-imports edited bilingual table, compares with current project by segment number, shows preview of all changes (old vs new target), applies approved changes with:
  - Target text updated
  - Status reset to "Not Started" for translator review
  - Review notes appended to segment notes
  - Validation: Source text must match (sanity check)

**Table Format:**
| # | Source | Target | Status | Notes |
|---|--------|--------|--------|-------|
| 1 | Hello  | Hallo  | Translated | |

**Document Header:**
- Title: "Supervertaler Bilingual Table" with hyperlink to supervertaler.com
- Title styled in blue (RGB 0, 102, 204)

**Technical Implementation:**
- `export_review_table_with_tags()` - Wrapper for tag-visible export
- `export_review_table_formatted()` - Wrapper for formatted export with warning dialog
- `_export_review_table(apply_formatting)` - Core export logic
- `_add_hyperlink_to_paragraph()` - Helper for Word hyperlinks
- `import_review_table()` - Import logic with change detection and preview

---

### November 30, 2025 - Version 1.9.14: Improved DOCX Export & Keyboard Navigation

**📤 DOCX Export Improvements**
Fixed critical issues with DOCX export:
- **Formatting Preservation:** Export now properly converts `<b>`, `<i>`, `<u>`, `<bi>` tags to actual Word formatting (bold, italic, underline)
- **Multi-Segment Paragraphs:** Export now handles paragraphs that contain multiple segments (e.g., "Our Ref. ZP10628EPNL" split across two segments)
- **Unicode Cleanup:** Removes problematic characters like U+FFFC (Object Replacement Character) that could appear in exports
- **Tag Stripping:** Properly strips all list tags (`<li-o>`, `<li-b>`, `<li>`) while preserving formatting tags

**⌨️ Keyboard Navigation Fix**
- Ctrl+Home now properly navigates to first segment even when editing inside a grid cell
- Ctrl+End now properly navigates to last segment even when editing inside a grid cell
- Added `_get_main_window()` helper to both `EditableGridTextEditor` and `ReadOnlyGridTextEditor`

**🔧 Technical Changes:**
- `export_target_only_docx()`: Added `apply_formatted_text_to_paragraph()` function that parses tags and creates properly formatted Word runs
- `export_target_only_docx()`: Added `replace_segments_in_text()` for partial segment replacement within paragraphs
- `export_target_only_docx()`: Added `clean_special_chars()` to remove Unicode replacement characters
- `EditableGridTextEditor.keyPressEvent()`: Added Ctrl+Home/End handlers
- `ReadOnlyGridTextEditor.event()`: Added Ctrl+Home/End handlers

---

### November 30, 2025 - Version 1.9.13: Document Preview & List Formatting Tags

**📄 New Preview Tab**
Added a new "Preview" tab alongside Source/Target views in the main panel:

**Preview Tab Features:**
- Shows formatted document view with headings, paragraphs, and lists
- Headings (H1-H6) displayed with proper font sizing and styling
- List items show correct prefix: numbers (1. 2. 3.) for ordered lists, bullets (•) for bullets
- Click any text to instantly navigate to that segment in the grid
- Read-only view provides document context during translation

**🔢 List Type Detection from DOCX**
New `_get_list_type()` method in docx_handler.py:
- Examines Word's numPr XML structure to distinguish bullet from numbered lists
- Looks for "bullet" in numFmt value or bullet characters (•, ○, ●, ■) in lvlText
- Caches list type lookups for performance
- Works for both regular paragraphs and table cells

**🏷️ New Short List Tags**
- `<li-o>` - Ordered list items (numbered: 1. 2. 3.)
- `<li-b>` - Bullet list items (•)
- Both tags are colored by the tag highlighter
- Both work with Ctrl+, shortcut for quick insertion
- Updated tag regex pattern to `[a-zA-Z][a-zA-Z0-9-]*` to support hyphenated tags

**Type Column Improvements:**
- Shows `#1`, `#2`, `#3` for ordered list items
- Shows `•` for bullet list items
- Shows `¶` (paragraph mark) for continuation paragraphs instead of `#`

**Files Changed:**
- `Supervertaler.py`:
  - Added `_setup_preview_tab()`, `_render_preview()`, `_render_formatted_text()` methods
  - Updated `extract_all_tags()` and `highlightBlock()` patterns for hyphenated tags
  - Updated Type column display logic in `load_segments_to_grid()`
- `modules/docx_handler.py`:
  - Added `_get_list_type()` method (lines 139-180)
  - Changed `<li>` to `<li-o>` or `<li-b>` based on detected list type
  - Added `self._list_type_cache` for performance

---

### November 28, 2025 - Version 1.9.12: Progress Indicator Status Bar

**📊 New Progress Status Bar**
Added permanent progress indicators to the status bar showing real-time translation progress:

**Features:**
- **Words translated**: X/Y words with percentage (counts words in segments that have translations)
- **Confirmed segments**: X/Y segments with percentage (confirmed, tr_confirmed, proofread, approved)
- **Remaining segments**: Count of segments still needing work (not_started, pretranslated, rejected)

**Color Coding:**
- Red (<50%): Low progress
- Orange (50-80%): Making progress
- Green (>80%): Almost done

**Auto-Updates:**
- Updates when project is loaded (`load_segments_to_grid`)
- Updates when segment is confirmed (Ctrl+Enter)
- Updates after AI translation completes
- Updates after user finishes typing (debounced)
- Resets to "--" when project is closed

**Files Changed:**
- `Supervertaler.py` - Added `_setup_progress_indicators()`, `update_progress_stats()`, `_get_progress_color()` methods
- Called from `load_segments_to_grid`, `confirm_and_next_unconfirmed`, `translate_current_segment`, `_handle_target_text_debounced_by_id`, `close_project`

---

### November 28, 2025 - Version 1.9.11 Additional Fixes: Status Reset & TM Improvements

**🔧 Status Reset When Editing Confirmed Segments**
- When user edits the target text of a **confirmed** segment, status now resets to **translated**
- This prevents auto-saving edited text to TM until user re-confirms
- Applied to both grid editor (`on_target_text_changed`) and tab editor (`on_tab_target_change`)
- Added `_refresh_segment_status_by_id()` helper method for status display updates

**🔧 TM List Button Fixes**
- Fixed "Delete TM" button not working (wrong column index 1→0)
- Fixed "Edit/Maintain TM" button not working (wrong column index 1→0)  
- Fixed "Export to TMX" not working (wrong column index 1→0)
- Fixed right-click context menu on TM list (wrong column index 1→0)

**🔧 TM Cache Invalidation**
- TM matches cache is now properly invalidated when TM Read activation toggle changes
- This ensures deactivated TMs don't continue showing matches until navigation

**🔧 Compare Box for MT/LLM Matches**
- MT and LLM translation matches now show in the compare box (bottom panel)
- Added `compare_source` field to TranslationMatch creation for MT results

**🔧 TM Save Only on Confirmed**
- Changed 7 locations to only save to TM when segment status is 'confirmed'
- Previously was saving on 'translated' and 'approved' as well

**🔧 Termbase Selection Persistence**
- "Add Term to Termbase" dialog now remembers selected termbases between sessions
- Stored per-user in `termbase_dialog_selections.json`

---

### November 28, 2025 - Version 1.9.11 Release: Non-Translatables Matching Improvements

**🔧 Case-Sensitive & Full-Word Matching for Non-Translatables**

**Matching Improvements:**
- Non-translatables matching is now **case-sensitive by default**
- Only matches **full words** (not partial words like "Product" inside "ProductName")
- Uses word boundary detection (`\b`) for accurate term matching
- Smart fallback for special characters like ® and ™ that don't work with word boundaries

**Bug Fixes:**
- Fixed crash when closing project: added missing `stop_termbase_batch_worker()` method in Supervertaler.py
- Fixed `.svprompt` files not showing in Prompt Library tree (added extension to both unified_prompt_library.py and unified_prompt_manager_qt.py)
- Added LLM refusal detection for batch translation with helpful error messages when AI refuses content (e.g., OpenAI refusing patent content)

**Files Changed:**
- `modules/non_translatables_manager.py` - Changed `case_sensitive` default to True, rewrote `matches()` method with word boundary regex
- `Supervertaler.py` - Added `stop_termbase_batch_worker()` method, added LLM refusal detection in batch translate
- `modules/unified_prompt_library.py` - Added `.svprompt` to file extension checks
- `modules/unified_prompt_manager_qt.py` - Added `.svprompt` to tree builder extension list

---

### November 28, 2025 - Version 1.9.10 Release: TM Search Fixes & Language Matching

**🔧 Fixed TM matches not appearing in Translation Results panel**

**Root Causes Found:**
1. `tm_metadata_mgr` was only initialized when user opened TM List tab, but TM search runs immediately on segment navigation
2. Database had mixed language formats ("Dutch", "nl", "nl-NL") but search only looked for ISO codes
3. Legacy hardcoded `enabled_only=True` filter would search only 'project' and 'big_mama' TMs that don't exist

**Fixes Applied:**
- Early initialization: `tm_metadata_mgr` now initializes in `initialize_tm_database()` when project loads
- Flexible language matching: New `get_lang_match_variants()` returns both ISO codes and full language names
- Bypass legacy filter: Added `enabled_only=False` to all `search_all()` calls
- Fallback search: When no TMs are explicitly activated, search now falls back to all TMs

**Database Cleanup:**
- Cleaned public database for new GitHub users
- Removed legacy 'project' and 'big_mama' TM hardcoding from TMDatabase class
- All TMs now managed through TMMetadataManager with proper database storage

**Files Changed:**
- `Supervertaler.py` - TM metadata manager early init, enabled_only=False for searches
- `modules/translation_memory.py` - Removed legacy tm_metadata dict
- `modules/database_manager.py` - Flexible language matching in get_exact_match() and search_fuzzy_matches()
- `modules/tmx_generator.py` - Added get_lang_match_variants() and updated get_base_lang_code()
- `user_data/Translation_Resources/supervertaler.db` - Cleaned for new users

---

### November 27, 2025 - Version 1.9.9 Release: memoQ-style Alternating Row Colors

**🎨 Grid Row Colors Enhancement**
- Added memoQ-style alternating row colors across all grid columns (ID, Type, Source, Target)
- Source and Target columns now have consistent alternating colors (previously Source was always gray, Target was always white)
- New user-configurable settings in Settings → View Settings tab:
  - Enable/disable alternating row colors checkbox
  - Color picker for even row color (default: white #FFFFFF)
  - Color picker for odd row color (default: light gray #F0F0F0)
  - "Reset to Default Colors" button
- Colors apply consistently to all columns including Source and Target QTextEdit widgets
- Settings are persisted in ui_preferences.json

**Technical Changes:**
- Added `set_background_color()` method to `ReadOnlyGridTextEditor` class
- Added `set_background_color()` method to `EditableGridTextEditor` class
- Added `_apply_row_color()` method for applying colors to individual rows
- Added `apply_alternating_row_colors()` method for refreshing all row colors
- Extended `_save_view_settings_from_ui()` to handle new color settings
- Added row color settings to `load_general_settings()`
- Added caching mechanism for row color settings to optimize performance

**Files Changed:**
- `Supervertaler.py` - All changes in main application file
- `PROJECT_CONTEXT.md` - Updated with session notes

---

### November 27, 2025 - Version 1.9.8 Release: CafeTran Integration & Editor Shortcuts

**🔄 CafeTran Enhancements**
- Pipe symbols (|) now highlighted in red/bold in grid editor
- Ctrl+, inserts pipe symbols for CafeTran formatting
- Ctrl+Shift+S copies source text to target cell
- Full round-trip workflow with CafeTran bilingual DOCX files

**⌨️ Keyboard Shortcuts Improvements**
- Keyboard shortcuts table now sortable by clicking column headers
- Removed "Save Project As" shortcut (Ctrl+Shift+S now dedicated to copy source)
- Fixed shortcut conflict that was intercepting editor shortcuts

**⚙️ Settings Changes**
- Batch size default changed from 100 to 20 segments per API call
- Better balance of speed vs. cost for typical workflows

**Files Changed:**
- `Supervertaler.py` - Version bump, pipe styling, shortcuts, batch size
- `modules/shortcut_manager.py` - Removed Save As shortcut, added editor shortcuts
- `modules/keyboard_shortcuts_widget.py` - Added sortable columns
- `CHANGELOG.md` - Added v1.9.8 entry
- `docs/index.html` - Updated website version
- `PROJECT_CONTEXT.md` - Updated with session notes

---

### November 27, 2025 - Version 1.9.7 Release: CafeTran Bilingual DOCX Support

**🔄 CafeTran Import/Export**
- Added full import/export support for CafeTran bilingual DOCX files
- New menu items: Import > CafeTran Bilingual Table (DOCX)...
- New menu items: Export > CafeTran Bilingual Table - Translated (DOCX)...
- Preserves pipe symbol formatting markers for round-trip workflows
- Uses existing `modules/cafetran_docx_handler.py` module

**Files Changed:**
- `Supervertaler.py` - Version bump, added menu items, added import/export methods
- `CHANGELOG.md` - Added v1.9.7 entry
- `docs/index.html` - Updated website version
- `PROJECT_CONTEXT.md` - Updated with session notes

---

### November 27, 2025 - Version 1.9.6 Release: Custom File Extensions & Monolingual Export

**📁 Custom File Extensions**
- Introduced branded file extensions for Supervertaler formats:
  - `.svproj` - Project files (was `.json`)
  - `.svprompt` - Prompt files (was `.md`/`.json`)
  - `.svntl` - Non-translatable lists (was `.ntl`)
- Full backward compatibility maintained - loads all legacy formats
- Industry standards retained: `.tmx` for TM exports, `.srx` planned for segmentation

**🌐 Monolingual DOCX Import Improvements**
- Added language pair selection dialog when importing monolingual DOCX
- User explicitly selects source and target languages (12 languages supported)
- Removed unreliable auto-detect language feature

**📤 Target-Only DOCX Export**
- New "Export > Target Only (DOCX)..." menu option
- Preserves original document structure (tables, formatting, styles)
- Copies original DOCX as template before replacing text
- Original DOCX path saved in project files for reliable exports

**📚 Documentation Reorganization**
- Created modular docs: QUICK_START.md, KEYBOARD_SHORTCUTS.md, CAT_WORKFLOW.md
- Archived legacy USER_GUIDE.md and INSTALLATION.md
- Copied FAQ.md to repository root (fixed dead link)
- Moved PROJECT_CONTEXT.md to repository root for AI agent access

**Files Changed:**
- `Supervertaler.py` - Version bump, new features, export function
- `modules/non_translatables_manager.py` - .svntl extension
- `modules/prompt_library.py` - .svprompt extension
- `modules/prompt_manager_qt.py` - Updated prompt creation
- `modules/prompt_library_migration.py` - Support new extensions
- `docs/index.html` - Updated website
- Various documentation files

---

### November 27, 2025 - Version 1.9.5 Release: Send Segments to TM & memoQ Tags

**📤 Send Segments to TM (Bulk Operation)**
- New dialog: Edit > Bulk Operations > Send Segments to TM
- Filter by scope (all, selection, range) and status
- Select multiple TMs to write to

**🏷️ memoQ Tag Insertion Shortcut**
- Ctrl+, inserts next memoQ tag pair or wraps selection
- Smart tag detection from source segment

---

### November 22, 2025 - Version 1.7.8 Release: Filter Highlighting Fix

**🔍 Version 1.7.8 Released - Search Term Highlighting in Filters**

Fixed a critical issue where search terms entered in the source/target filter boxes were not being highlighted in the filtered segments. The problem was architectural: the existing delegate-based highlighting approach was incompatible with the QTextEdit cell widgets used for source and target columns.

**🐛 Problem Identified:**

- **Architectural Mismatch:** Source/target cells use `setCellWidget()` with QTextEdit-based editors (`EditableGridTextEditor`, `ReadOnlyGridTextEditor`)
- **Delegate Bypass:** Qt completely bypasses `QStyledItemDelegate.paint()` when a cell has a widget, rendering the entire delegate highlighting system ineffective
- **Previous Implementation:** The code was correctly setting `global_search_term` on the delegate and calling `viewport().repaint()`, but these had no effect because `paint()` was never called for widget cells
- **Struggled Issue:** User and Claude Code had been working on this for over a day without identifying the root cause

**✅ Solution Implemented:**

**New Method: `_highlight_text_in_widget()`**
```python
def _highlight_text_in_widget(self, row: int, col: int, search_term: str):
    """Highlight search term within a QTextEdit cell widget using QTextCursor."""
    widget = self.table.cellWidget(row, col)
    if not widget or not hasattr(widget, 'document'):
        return
    
    # Clear existing highlights
    cursor = widget.textCursor()
    cursor.select(QTextCursor.SelectionType.Document)
    clear_format = QTextCharFormat()
    cursor.setCharFormat(clear_format)
    cursor.clearSelection()
    
    # Create yellow highlight format
    highlight_format = QTextCharFormat()
    highlight_format.setBackground(QColor("#FFFF00"))
    
    # Find and highlight all occurrences (case-insensitive)
    document = widget.document()
    text = document.toPlainText()
    text_lower = text.lower()
    search_term_lower = search_term.lower()
    
    pos = 0
    while True:
        pos = text_lower.find(search_term_lower, pos)
        if pos == -1:
            break
        cursor.setPosition(pos)
        cursor.movePosition(QTextCursor.MoveOperation.Right, 
                          QTextCursor.MoveMode.KeepAnchor, len(search_term))
        cursor.mergeCharFormat(highlight_format)
        pos += len(search_term)
```

**Modified `apply_filters()` Method:**
- Replaced delegate-based highlighting calls with `_highlight_text_in_widget()`
- Removed delegate `global_search_term` setting (no longer needed)
- Removed `viewport().repaint()` calls (no longer needed)
- Simplified code by removing unnecessary delegate interaction

**Highlight Clearing:**
- `clear_filters()` already calls `load_segments_to_grid()` which recreates all widgets
- Fresh widgets automatically have no highlights → no additional clearing logic needed

**📋 Technical Details:**

- **Files Modified:**
  - `Supervertaler.py` (lines ~15765-15810): New `_highlight_text_in_widget()` method
  - `Supervertaler.py` (lines ~15779-15860): Modified `apply_filters()` method
- **Key Technologies:**
  - `QTextCursor` for text navigation and selection within QTextEdit
  - `QTextCharFormat` for applying yellow background color
  - `QTextDocument` for accessing widget's text content
  - Case-insensitive matching using `.lower()` comparison
- **Performance:** No impact with large segment counts (tested with 219 segments)
- **Compatibility:** Works with both `EditableGridTextEditor` (target) and `ReadOnlyGridTextEditor` (source)

**📖 Documentation Added:**
- `docs/FILTER_HIGHLIGHTING_FIX.md` - Complete technical explanation with code examples, problem analysis, and solution details

**🎯 User Experience:**
- Filter source/target boxes now show yellow highlighting on matching terms
- Case-insensitive matching: "test", "TEST", "TeSt" all match "test"
- Multiple matches per cell highlighted correctly
- Highlights clear automatically when filters are removed
- Improves searchability and visual feedback during translation work

---

### November 21, 2025 - Automated Domain Detection & Prompt Generation Improvements

**🔧 Automated Domain Detection System**

Implemented comprehensive automated domain detection and enhancement rule generation for the AI-powered prompt assistant:

**Domain Detection:**
- Automatic identification of document domains (Legal, Medical, Technical, Patent) using multilingual keyword matching
- Keywords in English, Dutch, French, and German for accurate cross-language detection
- Minimum 2-match requirement to avoid false positives
- User-customizable keyword lists in Settings → Domain Detection tab

**Format Conversion Rules:**
- Automatic generation of number/date format conversion rules based on language pairs
- Dutch→English: comma decimal separator → period (718.592,01 → 718,592.01)
- English→Dutch: period → comma (reversed conversion)
- Thousands separator conversion included

**Domain-Specific Enhancement Rules:**
- Legal domain: "Meester + surname" preservation for Belgian notaries, notarial terminology
- Medical domain: Technical precision, standardized medical terminology
- Patent domain: Claims structure, technical specifications
- Technical domain: Imperative mood for instructions, measurement precision

**Post-Process Injection System:**
- Direct text manipulation after AI generation to guarantee rule appearance
- Removes problematic AI-generated "preserve formatting" instructions that contradict localization
- Regex patterns detect and remove variations like:
  - "Keep all numbers as formatted"
  - "Preserve all decimal separators exactly"
  - "Do not convert commas/dots"
  - "Preserve all original...decimal separators"
- Injects explicit conversion examples into PROJECT PROMPT section
- Ensures enhancement sections appear regardless of AI behavior

**Files Modified:**
- `modules/prompt_manager_qt.py`:
  - `_detect_domain_from_analysis()` (lines 2354-2448) - Multilingual domain detection
  - `_get_format_conversion_rules()` (lines 2410-2461) - Language pair format rules
  - `_get_legal_domain_rules()` (lines 2478-2507) - Legal-specific rules
  - `_inject_enhancement_rules()` (lines 2588-2664) - Post-process injection with cleanup
  - Integration in `_generate_translation_prompts()` (lines 3412-3438)
- `Supervertaler.py`:
  - `_create_domain_keywords_tab()` (lines 8257-8353) - Settings UI
  - `_load_domain_keywords()` (lines 8355-8390) - Load multilingual keywords
  - `_save_domain_keywords()` (lines 8392-8413) - Persist user customizations
  - `_reset_domain_keywords_to_defaults()` (lines 8415-8444) - Reset functionality

**Key Technical Details:**
- Multilingual keyword detection necessary because analysis text includes source language
- Legal keywords expanded from 18 → 38 (added Dutch: notariële akte, statuten, etc.)
- Medical keywords expanded from 15 → 38
- Patent keywords expanded from 10 → 18
- Technical keywords expanded from 11 → 32
- Post-process injection splits AI response by `---CUSTOM INSTRUCTIONS---` delimiter
- Injects only into PROJECT PROMPT section, leaving DOMAIN PROMPT untouched

**Identified Issue for Next Session:**
- User observation: Current approach still produces inconsistent results
- Better approach: Use **template-based system** with System Templates (already implemented)
- Templates would contain unchanging rules (e.g., number conversion for Dutch→English)
- AI would fill in document-specific parts (terminology, domain context)
- Need to fix crash in System Templates button (in unified_prompt_manager_qt.py)

---

### November 21, 2025 - Version 1.7.7 Release: Termbase Display Customization

**🎯 Version 1.7.7 Released - User-Configurable Termbase Display**

Today we released version 1.7.7, which introduces user-configurable sorting and filtering options for termbase matches in the translation results panel. This gives translators full control over how terminology is displayed, reducing clutter and improving focus on relevant multi-word terms.

**✨ New Features:**

**User-Configurable Termbase Sorting:**
- **Three Sorting Options** (accessible in Settings → General → TM/Termbase Options):
  - **Order of appearance in source text** (default) - Matches appear as they occur in the segment
  - **Alphabetical (A-Z)** - Matches sorted by source term alphabetically (case-insensitive)
  - **By length (longest first)** - Longer multi-word terms prioritized over shorter ones
- **Settings UI:**
  - Dropdown combo box with clear descriptions for each option
  - Helpful tooltips explaining the behavior of each sorting mode
  - Settings persist across sessions in `ui_preferences.json`
- **Implementation:**
  - New method `_sort_termbase_matches()` in `TranslationResultsPanel`
  - Sorting applied only to termbase matches; TM, MT, and LLM results maintain existing order
  - Position-in-source sorting uses metadata when available
  - Falls back to original order if position data not present

**Smart Substring Filtering:**
- **"Hide shorter termbase matches" checkbox** in Settings → General
- **Intelligent Filtering:**
  - Automatically filters out shorter terms that are fully contained within longer matched terms
  - Example: If both "cooling" and "cooling system" match, only "cooling system" is shown
  - Helps focus on the most relevant multi-word terminology
  - Reduces visual clutter in the translation results panel
- **Implementation:**
  - New method `_filter_shorter_matches()` in `TranslationResultsPanel`
  - Uses substring detection with length comparison
  - Case-insensitive matching for better accuracy
  - Can be toggled on/off without restarting the application

**Enhanced Visual Distinction:**
- **Bold Font for Project Resources:**
  - Project termbases now display with bold provider codes (TB) instead of asterisks
  - Project TMs also use bold font for cleaner visual distinction
  - Changed from "TB*" notation to bold "TB" for better aesthetics
  - Uses `font-weight: bold` CSS property

**📊 Technical Implementation:**

**Settings Architecture:**
- Settings stored in `ui_preferences.json` under `general_settings` key
- Two new settings variables:
  - `termbase_display_order`: 'appearance' | 'alphabetical' | 'length' (default: 'appearance')
  - `termbase_hide_shorter_matches`: boolean (default: False)
- Settings loaded at application startup in `load_general_settings()` method
- Settings saved when user clicks "Save Settings" in settings dialog

**Translation Results Panel Updates:**
- `TranslationResultsPanel` now accepts `parent_app` parameter for settings access
- New sorting method supports three strategies with fallback handling
- New filtering method identifies and removes substring matches
- Applied in `set_matches()` method before match limit is enforced
- Processing order: filter first (reduce set), then sort (organize remaining)

**Files Modified:**
- [Supervertaler.py](../Supervertaler.py):
  - Lines 2391-2393: Added settings instance variables
  - Lines 7377-7406: Settings UI controls (combo box + checkbox)
  - Lines 8316-8360: Save settings logic
  - Lines 8930, 9548: Pass `parent_app` when creating `TranslationResultsPanel`
  - Lines 12604-12606: Load settings on startup
- [modules/translation_results_panel.py](../modules/translation_results_panel.py):
  - Lines 626-628: Accept `parent_app` parameter in `__init__()`
  - Lines 133-145: Bold font for project resources
  - Lines 1201-1232: `_sort_termbase_matches()` method
  - Lines 1234-1276: `_filter_shorter_matches()` method
  - Lines 1324-1329: Apply sorting and filtering in `set_matches()`

**🎯 User Benefits:**
- **Cleaner Results Panel:** Hide redundant short terms that are part of longer matches
- **Better Organization:** Sort matches by relevance, alphabetically, or by term length
- **Improved Focus:** Prioritize multi-word terminology over single words
- **Workflow Optimization:** Choose sorting that matches your translation style
- **No Performance Impact:** Sorting and filtering happen instantly
- **Persistent Preferences:** Settings remembered across sessions

**🧪 Testing:**
- Application starts successfully with no errors
- Settings UI displays correctly with tooltips
- Settings persist across application restarts
- Sorting and filtering apply correctly to termbase matches only
- Bold font displays correctly for project resources

---

### November 20, 2025 - Version 1.7.6 Release: Auto Backup System

**💾 Version 1.7.6 Released - Automatic Backup System**

Today we released version 1.7.6, which introduces a comprehensive automatic backup system to prevent data loss during translation work. The system automatically saves both the project.json file and exports a TMX backup at regular intervals.

**✨ New Features:**

**Auto Backup System:**
- **Settings UI:** Added "Auto Backup Settings" section to Settings → General tab
  - Enable/disable automatic backups checkbox (enabled by default)
  - Configurable backup interval (1-60 minutes, default: 5 minutes)
  - Clear descriptions explaining both project.json and TMX are saved
- **Implementation:**
  - QTimer-based system that runs in the background during translation
  - Automatically saves project.json to the current project file location
  - Exports TMX file named `{project_name}_backup.tmx` in the same folder as project.json
  - Includes all segments (even empty translations) for maximum data recovery capability
  - Non-intrusive: backups run silently without interrupting user workflow
- **Settings Persistence:**
  - Backup preferences saved to `ui_preferences.json`
  - Timer automatically restarts when settings are changed
  - Settings persist across application sessions
- **Files Modified:**
  - [Supervertaler.py:7155-7198](../Supervertaler.py#L7155-L7198) - Settings UI
  - [Supervertaler.py:8220-8221](../Supervertaler.py#L8220-L8221) - Settings persistence
  - [Supervertaler.py:2408-2411](../Supervertaler.py#L2408-L2411) - Timer initialization
  - [Supervertaler.py:10609-10689](../Supervertaler.py#L10609-L10689) - Backup methods
- **User Benefits:**
  - Prevents data loss during translation work
  - TMX backup ensures recovery even if project.json gets corrupted
  - TMX can be imported into any CAT tool (memoQ, Trados, etc.) for maximum compatibility
  - Configurable intervals allow users to balance backup frequency with performance

**📊 Technical Details:**
- Timer runs at configurable interval (converted from minutes to milliseconds)
- Backup only runs when a project is open and has a file path
- Uses existing `save_project_to_file()` method for project.json
- Uses existing `TMXGenerator` module for TMX export
- Logs backup completion with timestamp for debugging
- Gracefully handles errors without interrupting user workflow

---

### November 20, 2025 - Version 1.7.5 Release: Critical TM Save Bug Fix

**🐛 Version 1.7.5 Released - Critical Bug Fix for Translation Memory Saves**

Today we released version 1.7.5, which fixes a critical bug that was causing massive unnecessary database writes during grid operations. This bug made filtering and grid operations unusable on large projects.

**✅ Critical Bug Fix:**

**TM Save Flood During Grid Loading (CRITICAL):**
- **Issue:** Every time `load_segments_to_grid()` was called (startup, filtering, clear filters), all segments with status "translated"/"confirmed"/"approved" would trigger false TM database saves 1-2 seconds after grid load completed
- **Symptoms:**
  - 10+ second UI freeze on projects with 200+ segments
  - Massive unnecessary database writes (219 saves on a 219-segment project)
  - Made filtering operations unusable
  - Could potentially corrupt data or cause performance issues
- **Root Cause:** Qt internally queues document change events when `setPlainText()` is called on QTextEdit widgets, even when signals are blocked. When `blockSignals(False)` was called in the finally block after grid loading, Qt delivered all these queued events, triggering `textChanged` for every segment. By that time, the suppression flag `_suppress_target_change_handlers` had already been restored to `False`, so the suppression check failed.
- **Technical Details:**
  1. Signals were blocked during `setPlainText()` in `EditableGridTextEditor.__init__()`
  2. Signals remained blocked through widget placement and signal handler connection
  3. Signals were unblocked in the finally block after grid loading
  4. Qt's internal event queue had pending `textChanged` events from the initial `setPlainText()` calls
  5. When `blockSignals(False)` was called, Qt delivered all queued events
  6. Each event triggered a 1000ms debounce timer that then saved to TM database
- **Fix:**
  - Added `_initial_load_complete` flag to `EditableGridTextEditor` class
  - Flag is set to `False` during widget construction
  - Signal handler checks this flag and ignores the first spurious `textChanged` event
  - After consuming the first queued event, flag is set to `True` and all subsequent real user edits are processed normally
  - Clean, surgical fix that doesn't interfere with Qt's event system
- **Files Modified:**
  - [Supervertaler.py](../Supervertaler.py) (lines 835, 11647-11651)
- **Testing:** Verified on BRANTS project (219 segments) - zero false TM saves during startup, filtering, and filter clearing

**📊 Impact:**
- **Performance:** Grid loading is now instant with no post-load freeze
- **Database:** Eliminates 200+ unnecessary database writes per grid operation
- **User Experience:** Filtering and grid operations are now fast and responsive
- **Data Integrity:** Prevents potential database corruption from excessive writes

**🔧 Implementation Details:**

The fix uses a per-widget state tracking approach:
```python
class EditableGridTextEditor(QTextEdit):
    def __init__(self, text: str = "", parent=None, row: int = -1, table=None):
        # Track initial load state to ignore spurious textChanged events
        self._initial_load_complete = False
        self.blockSignals(True)
        self.setPlainText(text)
        # Signals stay blocked until after handler connection
```

In the signal handler:
```python
def on_target_text_changed():
    # Ignore spurious textChanged event from Qt's queued document changes
    if not editor_widget._initial_load_complete:
        editor_widget._initial_load_complete = True
        return  # Ignore first event after signal unblock

    # Process all subsequent real user edits normally
    # ...
```

This solution was chosen because:
- ✅ Minimal code changes
- ✅ Per-widget state tracking is clean and maintainable
- ✅ Doesn't interfere with Qt's event system or signal blocking
- ✅ Allows one spurious event to be consumed per widget, then normal operation
- ✅ No changes to existing suppression flag logic

---

### November 12, 2025 - Version 1.4.1 Release: Superbench - Adaptive Project Benchmarking

**📊 Version 1.4.1 Released - Superbench LLM Benchmarking on Real Projects**

Today we released version 1.4.1, which adds the Superbench module - a powerful adaptive project benchmarking system that allows users to benchmark LLMs on their actual translation projects instead of just pre-made datasets.

**✅ Major Features Added:**

**Superbench - LLM Translation Quality Benchmarking System:**
- **Adaptive Project Benchmarking** - Create custom benchmark datasets from the current open project
- **Three Smart Sampling Methods:**
  - **Random** - Random segment selection across entire project
  - **Evenly-Spaced** - Uniform distribution from start to finish
  - **Smart** - 30% beginning, 40% middle, 30% end for representative coverage
- **Current Project Dataset Creation** - Test LLMs on actual project content with configurable sample sizes (10-1000 segments)
- **40+ Language Support** - Automatic language code-to-name conversion system
- **Multi-Model Benchmarking** - Simultaneously test GPT-4o, Claude Sonnet 4.5, Gemini 2.5 Flash
- **Quality Scoring** - Automatic chrF++ quality scoring when reference translations are available
- **Enhanced Excel Export** - Segment-grouped layout with improved visual design

**✅ Critical Bug Fixes:**

1. **Language Translation Bug (Critical):**
   - **Issue:** LLM translations appeared in English instead of the target language (e.g., Dutch)
   - **Root Cause:** `build_translation_prompt()` was passing language codes ("nl") instead of language names ("Dutch") to LLMs
   - **Fix:**
     - Created `_lang_code_to_name()` method with comprehensive 40+ language mappings
     - Rewrote `build_translation_prompt()` to dynamically parse any language direction format
     - LLMs now receive full language names in prompts: "Translate from English to Dutch"
   - **Files Modified:** [modules/llm_leaderboard.py](../modules/llm_leaderboard.py)

2. **Project Name Display Bug:**
   - **Issue:** Window title and recent projects menu showed import filename instead of custom project name
   - **Root Cause:** `save_project_as()` saved file but didn't update `self.current_project.name`
   - **Fix:** Added logic to extract filename stem and update project name when saving
   - **Files Modified:** [Supervertaler.py](../Supervertaler.py) (line 5915-5917)

3. **Excel Filename Sanitization:**
   - **Issue:** Export filenames could contain invalid Windows characters like `:`
   - **Fix:** Added comprehensive filename sanitization removing `<>:"/\|?*`
   - **Files Modified:** [modules/superbench_ui.py](../modules/superbench_ui.py) (line 724-732)

4. **Benchmark Crash Prevention:**
   - **Issue:** Occasional crashes during benchmark execution
   - **Fix:** Added comprehensive error handling throughout pipeline:
     - Segment data validation
     - Language direction validation
     - LLM client creation error handling
     - Translation API error handling with full tracebacks
     - Output validation
   - **Files Modified:** [modules/llm_leaderboard.py](../modules/llm_leaderboard.py), [modules/superbench_ui.py](../modules/superbench_ui.py)

**✅ User Experience Enhancements:**

1. **Enhanced Excel Colors:**
   - Changed model colors from light pastels to stronger, more saturated colors:
     - GPT-4o: #FFE6E6 → #FFCCCC (stronger pink)
     - Claude Sonnet 4.5: #E6F4EA → #CCFFCC (stronger green)
     - Gemini 2.5 Flash: #E3F2FD → #CCDDFF (stronger blue)
   - Better visual distinction in Results sheet
   - **Files Modified:** [modules/llm_leaderboard_ui.py](../modules/llm_leaderboard_ui.py) (line 982-986)

2. **Intelligent Export Paths:**
   - memoQ export dialog now defaults to original import file location
   - Significantly improves round-trip workflow convenience
   - **Files Modified:** [Supervertaler.py](../Supervertaler.py) (line 6734-6742)

**📁 Technical Implementation:**

**Language Code Converter System:**
```python
def _lang_code_to_name(self, code: str) -> str:
    """Convert language code to full language name for LLM prompts"""
    lang_map = {
        "en": "English", "nl": "Dutch", "de": "German", "fr": "French",
        "es": "Spanish", "it": "Italian", "pt": "Portuguese", "ja": "Japanese",
        "zh": "Chinese", "ko": "Korean", "ar": "Arabic", "ru": "Russian",
        # ... 40+ language mappings with regional variants
    }
```

**Dynamic Prompt Builder:**
- Parses any language direction format (e.g., "en→nl", "EN→NL", "de→fr")
- Converts both source and target codes to full language names
- Builds clear prompts: "Translate from English to Dutch... Target language: Dutch"

**Excel Export Format:**
- Segment-grouped layout (all model outputs for one segment grouped together)
- Model-specific background colors for easy comparison
- Summary sheet with overall statistics
- Raw Data sheet with all benchmark metadata

**📝 Key Changes Summary:**

1. **modules/llm_leaderboard.py:**
   - Added `_lang_code_to_name()` method (lines 133-180)
   - Rewrote `build_translation_prompt()` (lines 182-208)
   - Enhanced `_translate_segment()` validation (lines 247-360)

2. **modules/superbench_ui.py:**
   - Fixed filename sanitization (lines 724-732)
   - Enhanced Excel colors (lines 982-986)
   - Added comprehensive error handling to BenchmarkThread (lines 56-79)

3. **Supervertaler.py:**
   - Fixed `save_project_as()` project name update (lines 5915-5917)
   - Enhanced memoQ export path intelligence (lines 6734-6742)
   - Updated version to v1.4.1 (4 locations)

**🎯 Version 1.4.1 Impact:**

This release transforms the LLM Leaderboard from a pre-made dataset testing tool into "Superbench" - a practical, real-world benchmarking system that works on actual translation projects. The critical language bug fix ensures translations actually appear in the correct target language, making the feature genuinely usable for the first time.

---

### November 12, 2025 - Version 1.4.0 Release: Supervoice Voice Dictation + Documentation Update

**🎤 Version 1.4.0 Released - Supervoice Voice Dictation + Detachable Log**

Today we released version 1.4.0, which includes the completed Supervoice voice dictation feature and detachable log window. All version numbers and documentation have been updated to reflect this major release.

**✅ Version Update (1.3.4 → 1.4.0):**

Updated all version references across the codebase:
- **Supervertaler.py:**
  - Header docstring: "Version: 1.4.0 (Supervoice Voice Dictation + Detachable Log)"
  - `__version__ = "1.4.0"`
  - `__release_date__ = "2025-11-12"`
  - Welcome message: "Welcome to Supervertaler Qt v1.4.0"
  - All window titles updated
  - About dialog updated

**✅ Website Documentation Updated (docs/index.html):**

1. **Hero Badge Updated:**
   - Changed from "v1.3.4 - AI Assistant Enhanced"
   - To: "v1.4.0 - Supervoice Voice Dictation 🎤"

2. **New Supervoice Module Card Added:**
   - Placed as first module in grid (prominent positioning)
   - Red border (3px solid #FF6B6B) to highlight as NEW
   - Features highlighted:
     - 100+ languages via OpenAI Whisper
     - F9 global hotkey (start/stop)
     - 5 model sizes (tiny to large)
     - Configurable in Settings → 🎤 Supervoice
     - Future: voice commands and parallel command system
   - Links to [VOICE_DICTATION_GUIDE.md](VOICE_DICTATION_GUIDE.md)

3. **Features Section Updated:**
   - Updated highlight box to showcase v1.4.0 Supervoice (red/orange gradient)
   - Changed from LLM Leaderboard highlight to Supervoice highlight
   - Added 4 feature highlights:
     - 🌍 100+ Languages (OpenAI Whisper)
     - ⌨️ F9 Hotkey (press-to-start/stop)
     - 🎚️ 5 Model Sizes (balance speed vs accuracy)
     - 🚀 Future Voice Commands (workflow automation)
   - Added Supervoice feature card to features grid (first position, red border)

**✅ Documentation Files Updated:**

1. **README.md:**
   - Updated release info reference to v1.4.0
   - Updated Qt Edition version section:
     - Version: v1.4.0 (November 12, 2025)
     - Added complete Supervoice feature list
     - Highlighted 100+ language support
     - Mentioned future voice command system
     - Condensed previous features (v1.3.4, v1.3.3) for brevity

2. **CHANGELOG.md:**
   - Added comprehensive v1.4.0 entry at top
   - Documented all Supervoice features:
     - AI-powered speech recognition (OpenAI Whisper)
     - 100+ language support
     - F9 global hotkey
     - 5 model sizes with descriptions
     - FFmpeg detection and bundling
     - Grid cell integration
     - Language auto-detection
     - Future voice command plans
   - Documented detachable log window features
   - Listed all documentation files created
   - Documented bug fixes (UnboundLocalError, language detection, button color, auto-scroll)
   - Listed technical details

3. **CHANGELOG.md:**
   - Maintains complete version history from v1.0.0 to current
   - Top section includes marketing-style highlights of recent major features
   - Detailed release notes for all versions:
     - Categorized changes (Added, Fixed, Changed, Technical)
     - Complete "What's New" sections
     - Bug fixes and improvements
     - Documentation links
     - Step-by-step "How to Use" instructions
     - Benefits list
     - Technical details
   - Added v1.3.4 as "Previous Release" section

**📝 Key Messaging:**

All documentation now consistently mentions:
- **100+ languages** - "as many languages as Whisper can handle"
- **Future parallel dictation system** - for voice commands (confirm segment, go to top, filtering, workflow automation)
- **Press-to-start, press-to-stop** - Simple F9 hotkey workflow
- **5 model sizes** - Balance between speed and accuracy
- **Multi-monitor support** - Detachable log window feature

**🎯 Supervoice Features (Summary):**

The v1.4.0 release includes:
1. **Voice Dictation Core:**
   - OpenAI Whisper integration
   - 100+ language support
   - F9 global hotkey (start/stop)
   - 5 model sizes (tiny, base, small, medium, large)
   - Visual feedback (button color change)
   - Grid cell integration
   - Language auto-detection

2. **Supporting Features:**
   - FFmpeg detection and bundling infrastructure
   - User-friendly error messages
   - Comprehensive documentation (3 guides)
   - Settings configuration panel

3. **Detachable Log Window:**
   - Multi-monitor support
   - Synchronized auto-scroll
   - Persistent state
   - Independent positioning/sizing

4. **Bug Fixes:**
   - Fixed UnboundLocalError (duplicate `import os`)
   - Fixed language detection
   - Fixed button color restoration
   - Fixed log auto-scroll synchronization

**📚 Documentation Created/Updated:**

All documentation is complete and comprehensive:
- [VOICE_DICTATION_GUIDE.md](VOICE_DICTATION_GUIDE.md) - User guide
- [VOICE_DICTATION_DEPLOYMENT.md](VOICE_DICTATION_DEPLOYMENT.md) - Deployment guide
- [SUPERVOICE_TROUBLESHOOTING.md](SUPERVOICE_TROUBLESHOOTING.md) - Troubleshooting
- [docs/index.html](../docs/index.html) - Website updated
- [README.md](../README.md) - Updated
- [CHANGELOG.md](../CHANGELOG.md) - Complete version history with marketing highlights

**🚀 Next Steps:**

The foundation is now in place for the future parallel dictation system mentioned throughout the documentation. This will enable voice commands for:
- Segment navigation (go to top, go to segment X)
- Segment confirmation (confirm segment, next segment)
- Filtering and search operations
- Workflow automation commands

---

### November 10, 2025 (Continued) - Fixed CODE FENCE Parsing Issue

**🐛 Critical Fix: ACTION Block Parser Not Handling Markdown Code Fences**

Claude was wrapping ACTION blocks in markdown code fences (```yaml), causing the parser to fail. Only the text "`yaml`" was being displayed to the user.

**Problem:**
- Claude output: ````yaml\nACTION:create_prompt PARAMS:{...}\n```
- Parser removed ACTION block successfully
- But leftover "`yaml`" text was displayed as the AI response
- Empty chat bubbles or just "`yaml`" appearing

**Solution:**
Enhanced ACTION parser in `modules/ai_actions.py` to strip markdown code fences before parsing:
- Remove opening fence: ````yaml`, ````json`, or ``` (at start or after newline)
- Remove closing fence: ``` (at end or before newline)
- Remove standalone backticks and language markers
- Handle both block-level and inline code fences

**Files Modified:**
- [modules/ai_actions.py](../modules/ai_actions.py) - Lines 81-88: Added comprehensive code fence stripping

**Commit:** `42a86c2` - "Fix ACTION parser to strip markdown code fences from LLM responses"

**Impact:**
- AI Assistant now handles Claude's markdown-wrapped responses correctly
- No more "`yaml`" text appearing in chat
- ACTION blocks properly extracted and executed
- Works with all LLM providers (OpenAI, Claude, Gemini)

---

### November 10, 2025 (Later) - AI Assistant Enhanced Prompt Generation

**🎯 ChatGPT-Quality Automatic Prompt Generation**

Redesigned the AI Assistant's "Analyze Project & Generate Prompts" feature to create comprehensive, professional translation prompts matching the quality of ChatGPT/Claude web interfaces.

**✅ Enhanced Prompt Generation:**

1. **Comprehensive High-Level Summaries**
   - AI now generates 3-4 paragraph detailed document analysis
   - Paragraph 1: Document purpose and main topic
   - Paragraph 2: Key technical details and innovations
   - Paragraph 3: Scope, structure, and special considerations
   - Paragraph 4: Translation challenges and style requirements
   - Previously: Only brief metadata (Type, Domain, Language pair)

2. **Extensive Glossaries**
   - Template now requires 30-40 key terms (up from 10-15)
   - Each term includes context notes
   - Covers all technical terminology, domain-specific terms, frequently occurring terms
   - Includes challenging or ambiguous terms with usage guidance

3. **Domain-Specific Constraints**
   - **Patents:** Claim structure, legal precision, figure references
   - **Technical:** Measurement units, technical accuracy
   - **Medical:** Clinical terminology, regulatory compliance
   - **Legal:** Legal terms of art, formal language
   - AI identifies document type and applies appropriate constraints

4. **Full Document Analysis**
   - AI now receives up to 50,000 characters of document content
   - Previously: Only 5 sample segments (500 chars total)
   - Fallback: First 100 complete segments if markdown not cached
   - Dramatic improvement in prompt quality and accuracy

5. **One-Click Workflow**
   - Generated prompts automatically created in Project Prompts folder
   - Automatically activated as primary prompt
   - Ready for immediate use in translation
   - No manual prompt engineering needed

**🐛 Bug Fixes:**

1. **Empty Chat Bubble Fix**
   - Problem: Empty assistant messages appeared when AI generated only ACTION blocks
   - Root cause: `cleaned_response` was empty string after removing ACTION blocks
   - Fix: Only add assistant message if `cleaned_response.strip()` is non-empty
   - File: `modules/unified_prompt_manager_qt.py` lines 2576-2578

2. **Full Document Content Sending**
   - Problem: Only 5 segments sent to AI (100 chars each = 500 chars total)
   - User expectation: Full document analysis
   - Fix: Send cached markdown (50,000 chars) or first 100 complete segments
   - File: `modules/unified_prompt_manager_qt.py` lines 2019-2030

3. **ACTION Block Parsing**
   - Problem: Regex required newline but AI outputted single-line format
   - Fix: Changed pattern from `r'ACTION:(\w+)\s*\n\s*PARAMS:\s*'` to `r'ACTION:(\w+)\s+PARAMS:\s*'`
   - File: `modules/ai_actions.py` line 85

**Files Modified:**

- [modules/unified_prompt_manager_qt.py](../modules/unified_prompt_manager_qt.py)
  - Lines 1966-2022: Enhanced prompt generation template with comprehensive instructions
  - Lines 2576-2578: Empty bubble fix (only add assistant message if non-empty)
  - Lines 2019-2030: Full document sending (50,000 chars vs 500 chars)
- [modules/ai_actions.py](../modules/ai_actions.py)
  - Line 85: ACTION parsing fix (accept single-line format)

**Example Generated Prompt Quality:**

Before:
- 10-15 terms in glossary
- No high-level summary
- Generic constraints
- Based on 5 sample segments (500 chars)

After:
- 30-40 terms in glossary with context notes
- 3-4 paragraph comprehensive high-level summary
- Domain-specific constraints (patents, technical, medical, legal)
- Based on full document (50,000 chars)
- Professional formatting matching user's example prompts

**Technical Implementation:**

Enhanced template structure:
```
YOUR TASK:
1. **ANALYZE THE FULL DOCUMENT** - Read through all content
2. **WRITE A COMPREHENSIVE HIGH-LEVEL SUMMARY** (3-4 paragraphs)
3. **EXTRACT 30-40 KEY TERMS** for glossary
4. **IDENTIFY DOMAIN-SPECIFIC CONSTRAINTS**
5. **CREATE THE ACTION BLOCK** with all content
```

**Benefits:**
- Professional-quality prompts matching ChatGPT/Claude web quality
- Save significant time - no manual prompt engineering needed
- Comprehensive coverage - extensive glossaries and detailed summaries
- Domain awareness - AI recognizes and adapts to document type
- Immediate use - prompts activated automatically

**Status:** ✅ Complete - v1.3.4 release ready

---

### November 10, 2025 (Earlier) - LLM Leaderboard UI Standardization

**🎯 Complete UI Header Standardization Across Modules**

Standardized the visual branding across all Supervertaler modules (LLM Leaderboard, TMX Editor, AutoFingers) with consistent header styling and extended this branding to Excel exports.

**✅ Completed Features:**

1. **Standardized Module Headers**
   - Applied consistent header style across all modules:
     - LLM Leaderboard: "🏆 LLM Leaderboard"
     - TMX Editor: Similar professional styling
     - AutoFingers: Similar professional styling
   - Header styling:
     - Blue title color (#1976D2) - matches Supervertaler branding
     - 16pt bold font for visibility
     - Compact spacing (no stretch)
   - Description box styling:
     - Light blue background (#E3F2FD)
     - Gray text color (#666)
     - Rounded corners (3px border-radius)
     - 5px padding
     - Word wrap enabled
   - Subtitle format: "Translation Quality Benchmarking System - A Supervertaler Module"

2. **Excel Export Branding Consistency**
   - Updated Excel export title sheet to match UI header style:
     - Title: "🏆 LLM Leaderboard" (with trophy emoji)
     - 24pt bold title in blue (#1976D2)
     - Subtitle: "Translation Quality Benchmarking System"
     - 12pt italic subtitle in gray (#666666)
     - Module branding: "A Supervertaler Module"
     - Clickable hyperlink to https://supervertaler.com/
   - Complete visual consistency between UI and exported files

3. **Previous Session Fixes Completed**
   - ✅ Claude model crash fix - Updated to Claude 4 series model IDs
   - ✅ Gemini API key mapping - Maps "gemini" provider to "google" API key name
   - ✅ Model dropdown selection - Shows correct friendly names (e.g., "GPT-5 (Reasoning)", "Claude Opus 4.1")
   - ✅ Excel export with dataset info in filename - Format: `LLM_Leaderboard_{dataset_name}_{timestamp}.xlsx`
   - ✅ Auto-create API keys file - Copies api_keys.example.txt to api_keys.txt on first run
   - ✅ Auto-scroll log - Always shows latest benchmark messages
   - ✅ Comprehensive Excel export - Three sheets (About, Summary, Results) with professional formatting

**Files Modified:**
- [modules/superbench_ui.py](../modules/superbench_ui.py)
  - Lines 90-111: Standardized header with emoji and professional styling
  - Lines 547-565: Excel export title sheet with matching branding
  - Lines 782-825: Model name mapping for correct dropdown display
  - Lines 827-832: Auto-scrolling log implementation
  - Lines 479-776: Comprehensive Excel export system

**Technical Details:**

**UI Header Implementation:**
```python
# Header (matches TMX Editor / AutoFingers style)
header = QLabel("🏆 LLM Leaderboard")
header.setStyleSheet("font-size: 16pt; font-weight: bold; color: #1976D2;")
layout.addWidget(header, 0)

# Description box
description = QLabel(
    "Translation Quality Benchmarking System - A Supervertaler Module.\n"
    "Compare translation quality, speed, and cost across multiple LLM providers."
)
description.setWordWrap(True)
description.setStyleSheet(
    "color: #666; padding: 5px; "
    "background-color: #E3F2FD; border-radius: 3px;"
)
layout.addWidget(description, 0)
```

**Excel Export Title Sheet:**
```python
# Title with emoji (matches UI header style)
ws_info['A1'] = "🏆 LLM Leaderboard"
ws_info['A1'].font = Font(size=24, bold=True, color="1976D2")
ws_info.merge_cells('A1:D1')

# Subtitle
ws_info['A2'] = "Translation Quality Benchmarking System"
ws_info['A2'].font = Font(size=12, italic=True, color="666666")
ws_info.merge_cells('A2:D2')

# Branding with hyperlink
ws_info['A3'] = "A Supervertaler Module"
ws_info['A3'].font = Font(size=11, color="0066CC", underline="single")
ws_info['A3'].hyperlink = "https://supervertaler.com/"
ws_info.merge_cells('A3:D3')
```

**Benefits:**
- Professional, consistent branding across all modules
- Clear visual identity reinforcing Supervertaler ecosystem
- Excel exports maintain same professional appearance as UI
- User experience enhanced through visual consistency
- Easier module recognition and navigation

**Status:** ✅ Complete - All standardization tasks finished

---

### November 9, 2025 (Later) - Segment-Level AI Access + Critical Bug Fix

**🎯 Phase 2 Enhancement Complete: Segment-Level AI Actions**

Implemented segment-level access for AI Assistant allowing querying of specific segments and translation progress tracking.

**✅ Segment-Level AI Actions Implemented:**
- Added two new AI actions:
  - `get_segment_count` - Returns total segments, translated, and untranslated counts
  - `get_segment_info` - Retrieves specific segment(s) by ID, multiple IDs, or range
- AI Assistant can now answer:
  - "How many segments are in this document?"
  - "What is segment 5?"
  - "Show me segments 10 through 15"
- First 10 segments automatically included in AI context for quick reference
- Full segment properties available: id, source, target, status, type, notes, match_percent, etc.

**✅ CAT Tool Tag Handling:**
- Implemented comprehensive HTML entity escaping for segment display
- Proper escaping order: `&` → `<` → `>` → `"` (prevents double-escaping)
- Supports all CAT tool tags: Trados Studio, memoQ, Wordfast, CafeTran
- Segments displayed in code blocks with monospace font for readability

**✅ Auto-Markdown Generation Feature:**
- Added optional setting: Settings → General → AI Assistant Settings
- Checkbox: "Auto-generate markdown for imported documents"
- When enabled, automatically converts DOCX/PDF to markdown on import
- Markdown saved to `user_data_private/AI_Assistant/current_document/`
- Includes metadata JSON with conversion timestamp and file info
- Setting persists in `ui_preferences.json`

**🐛 CRITICAL BUG FIX:**
- Fixed attribute name mismatch: `self.prompt_manager` → `self.prompt_manager_qt`
- This was preventing:
  - Current document from showing in AI Assistant sidebar after import
  - Auto-markdown generation from triggering
  - Context refresh from working properly
- All document context integration now working correctly

**Files Modified:**
- [Supervertaler.py](../Supervertaler.py) - Fixed attribute names, added auto-markdown setting UI
- [modules/unified_prompt_manager_qt.py](../modules/unified_prompt_manager_qt.py) - Added segment info method and auto-markdown generation
- [modules/ai_actions.py](../modules/ai_actions.py) - Added segment actions and HTML escaping
- [test_ai_actions.py](../test_ai_actions.py) - Added tests 9 and 10 for segment actions
- [docs/AI_ASSISTANT_INTEGRATION.md](AI_ASSISTANT_INTEGRATION.md) - Updated with segment access documentation

**Testing:**
- ✅ All 10 tests passing
- ✅ Test 9: get_segment_count action
- ✅ Test 10: get_segment_info action (single, multiple, range)

**Benefits:**
- AI can answer segment-specific questions
- Translation progress tracking via AI
- Direct segment content access by number
- CAT tool tags handled properly in display
- Optional markdown conversion for document analysis
- Fixed critical bug preventing document context integration

**Version:** Released as v1.3.2

---

### November 9, 2025 (Earlier) - System Prompts Tab + AI Assistant Enhancement Plan

**🎯 Complete System Prompts UI + Phase 1 Enhancement Plan**

Major additions to the System Prompts accessibility and planning for file attachment and AI action integration.

**✅ System Prompts Settings Tab Implemented:**
- Added dedicated "📝 System Prompts" settings tab in Settings
- Mode selector dropdown for three translation modes:
  - Single Segment Translation
  - Batch DOCX Translation
  - Batch Bilingual Translation
- Rich text editor with monospace font for editing prompts
- Save functionality (to both memory and JSON)
- Reset to default with confirmation dialog
- Navigation from Prompt Library tab to Settings → System Prompts
- Stored in `user_data_private/Prompt_Library/system_prompts_layer1.json`

**Files Modified:**
- [Supervertaler.py](../Supervertaler.py) - Added System Prompts tab (lines 2965-3846)
- [modules/unified_prompt_manager_qt.py](../modules/unified_prompt_manager_qt.py) - Updated navigation (lines 1424-1439)

**🔄 PLANNED: AI Assistant Enhancement (November 9, 2025)**

Created comprehensive enhancement plan for fixing three critical issues with AI Assistant:

**Issue 1: File Attachments Not Persistent**
- Current: Files only stored in memory (`self.attached_files` list)
- Current: Files lost when application closes
- Current: No UI to view/manage attached files after uploading
- **Planned Solution (Phase 1 - HIGH PRIORITY):**
  - Create persistent storage: `user_data_private/AI_Assistant/attachments/`
  - Save markdown files with metadata (JSON)
  - Implement file viewer dialog with markdown preview
  - Add expandable attached files panel in context sidebar
  - Add view/remove functionality

**Issue 2: AI Cannot Act on Prompt Library**
- Current: AI context only mentions prompts exist
- Current: AI cannot list, create, or modify prompts
- Current: No structured action interface
- **Planned Solution (Phase 2 - MEDIUM PRIORITY):**
  - Implement function calling/action parsing system
  - Add tools: `list_prompts()`, `create_prompt()`, `update_prompt()`, etc.
  - Parse AI responses for ACTION markers
  - Execute actions and update prompt library in real-time

**Storage Structure (Phase 1):**
```
user_data_private/
  AI_Assistant/
    attachments/
      {session_id}/
        {file_hash}.md        # Converted markdown content
        {file_hash}.meta.json # Metadata (original name, type, date)
    index.json               # Master index of all attachments
    conversations/
      {conversation_id}.json # Conversation history with references
```

**Metadata Format:**
```json
{
  "file_id": "abc123...",
  "original_name": "project_brief.pdf",
  "original_path": "/path/to/original.pdf",
  "file_type": ".pdf",
  "size_bytes": 123456,
  "size_chars": 45678,
  "attached_at": "2025-11-09T10:30:00",
  "conversation_id": "conv_xyz",
  "markdown_path": "attachments/conv_xyz/abc123.md"
}
```

**UI Enhancements (Phase 1):**
- Expandable "📎 Attached Files" section in context sidebar
- File list showing: name, size, date
- View button → opens dialog with markdown preview
- Remove button → confirmation + delete from disk
- Files persist across sessions

**AI Actions System (Phase 2):**
- Structured response parsing (ACTION format)
- Available tools:
  - `list_prompts()` - List all prompts in library
  - `get_prompt(path)` - Get content of specific prompt
  - `create_prompt(name, content, folder)` - Create new prompt
  - `update_prompt(path, content)` - Update existing prompt
  - `search_prompts(query)` - Search prompts by content/name
- System prompt enhancement with action instructions

**Implementation Timeline:**
- Phase 1 (File Persistence & Viewing): 2-3 hours
- Phase 2 (AI Actions System): 3-4 hours
- Testing & Refinement: 1-2 hours
- **Total:** 6-9 hours development time

**Files to Create:**
- `modules/ai_attachment_manager.py` - File attachment persistence
- `modules/ai_actions.py` - AI action system and handlers
- `modules/ai_file_viewer_dialog.py` - File viewing dialog

**Documentation:**
- [docs/AI_ASSISTANT_ENHANCEMENT_PLAN.md](AI_ASSISTANT_ENHANCEMENT_PLAN.md) - Full technical specification

**Status:** ✅ Phase 1 COMPLETE, ✅ Phase 2 COMPLETE

**Phase 1 Implementation Complete (November 9, 2025):**

✅ **Files Created:**
- `modules/ai_attachment_manager.py` (390 lines) - Complete persistence system
- `modules/ai_file_viewer_dialog.py` (160 lines) - File viewer and removal dialogs
- `test_attachment_manager.py` - Comprehensive test suite (all tests passing)

✅ **Files Modified:**
- `modules/unified_prompt_manager_qt.py` - Full integration completed
  - Imported AttachmentManager and dialogs
  - Initialized AttachmentManager in `__init__`
  - Added `_load_persisted_attachments()` method
  - Modified `_attach_file()` to save to disk
  - Created `_create_attached_files_section()` - expandable panel
  - Added `_refresh_attached_files_list()` - dynamic file list
  - Added `_create_file_item_widget()` - file item with view/remove buttons
  - Added `_view_file()` - opens FileViewerDialog
  - Added `_remove_file()` - removes from disk and memory
  - Added `_toggle_attached_files()` - expand/collapse functionality
  - Updated `_update_context_sidebar()` to refresh file list
  - Updated `_load_conversation_history()` to refresh UI

✅ **Features Implemented:**
- **Persistent Storage:** Files saved to `user_data_private/AI_Assistant/attachments/`
- **Metadata Tracking:** JSON files with original name, path, type, size, date
- **Session Management:** Files organized by date-based sessions
- **Master Index:** `index.json` tracks all attachments across sessions
- **Expandable UI:** Collapsible attached files section in context sidebar
- **File List:** Shows name, type, size for each file
- **View Dialog:** Read-only markdown preview with copy to clipboard
- **Remove Function:** Confirmation dialog + disk deletion
- **Auto-Load:** Files persist and reload across app restarts

✅ **Testing Results:**
All 8 tests passed:
1. ✓ Module imports successful
2. ✓ AttachmentManager initialization
3. ✓ Session management
4. ✓ File attachment with metadata
5. ✓ File listing
6. ✓ File retrieval with content
7. ✓ Statistics tracking
8. ✓ File removal (tested separately)

**Phase 2 Implementation Complete (November 9, 2025):**

✅ **Files Created:**
- `modules/ai_actions.py` (665 lines) - Complete AI Actions system
  - AIActionSystem class with 12 action handlers
  - Smart JSON parser for ACTION blocks with proper brace matching
  - Action execution and result formatting
  - System prompt addition for AI instruction
- `test_ai_actions.py` (457 lines) - Comprehensive test suite (8/8 tests passing)

✅ **Files Modified:**
- `modules/unified_prompt_manager_qt.py` - Full AI Actions integration
  - Imported AIActionSystem (line 30)
  - Initialized AI Actions in `__init__` (lines 432-436)
  - Modified `_send_ai_request()` to parse and execute actions (lines 2176-2193)
  - Updated `_build_ai_context()` to include action instructions (line 2126)
  - Auto-reload prompt library after create/update/delete actions
  - Refresh tree widget UI when prompts are modified

✅ **Features Implemented:**
- **12 Available Actions:**
  1. `list_prompts` - List all prompts with optional folder filter
  2. `get_prompt` - Get full details of specific prompt
  3. `create_prompt` - Create new prompt with metadata
  4. `update_prompt` - Update existing prompt content/metadata
  5. `delete_prompt` - Delete prompt from library
  6. `search_prompts` - Search by name, content, tags, or all
  7. `create_folder` - Create new folder in library
  8. `toggle_favorite` - Toggle favorite status
  9. `toggle_quick_run` - Toggle Quick Run menu status
  10. `get_favorites` - List all favorite prompts
  11. `get_quick_run` - List all Quick Run prompts
  12. `get_folder_structure` - Get complete folder hierarchy

- **Smart ACTION Parser:**
  - Proper JSON extraction with brace matching
  - Handles nested JSON objects
  - Handles strings with escaped characters
  - Extracts multiple ACTION blocks from single response
  - Removes ACTION blocks from displayed response

- **Result Display:**
  - Formatted action results in chat
  - Success/failure indicators
  - Detailed result information
  - Error messages for failed actions

- **UI Integration:**
  - Actions executed automatically when AI includes them
  - Prompt Library UI refreshes after modifications
  - System messages show action results
  - Seamless conversational interface

✅ **Testing Results:**
All 8 tests passed:
1. ✓ AIActionSystem initialization
2. ✓ list_prompts action (all + folder filter)
3. ✓ create_prompt action
4. ✓ search_prompts action (by name, tags, all)
5. ✓ Parse and execute ACTION blocks from AI response
6. ✓ update_prompt and delete_prompt actions
7. ✓ toggle_favorite and toggle_quick_run actions
8. ✓ Format action results for display

**Example Usage:**
```
User: "Create a medical translation prompt for cardiology"

AI: I'll create that prompt for you.

ACTION:create_prompt
PARAMS:{"name": "Cardiology Translation Expert", "content": "You are an expert cardiology translator...", "folder": "Medical", "tags": ["medical", "cardiology", "heart"]}

The prompt has been created and is ready to use!

[System automatically executes action and shows:]
✓ **create_prompt**: Created prompt: Cardiology Translation Expert
  Path: Medical/Cardiology Translation Expert.md
```

**Benefits:**
- AI can now actively manage the Prompt Library
- No manual prompt creation needed
- Conversational prompt management
- Intelligent prompt suggestions
- Automated library organization

---

### November 8-9, 2025 - MAJOR: Unified Prompt System + AI Assistant

**🎯 Complete UI Reorganization + AI Assistant Implementation**

Major refactoring of the entire prompt management system from 4-layer to 2-layer architecture, PLUS integration of a full AI Assistant for conversational prompt generation and document analysis.

---

## ✅ FIXED: Chat UI Rendering (November 9, 2025)

**Status:** RESOLVED - Chat interface now renders perfectly with custom Qt delegates

**Solution Implemented:**
Replaced the problematic QTextEdit+HTML approach with a **QListWidget + Custom QStyledItemDelegate** solution. This provides full control over rendering using Qt's native painting system.

**Implementation Details:**

1. **New ChatMessageDelegate Class** ([unified_prompt_manager_qt.py:30-286](modules/unified_prompt_manager_qt.py#L30-L286))
   - Custom `QStyledItemDelegate` that paints chat bubbles using `QPainter`
   - Supports three message types: user, assistant, system
   - Proper text wrapping with `QFontMetrics.boundingRect()`
   - Dynamic height calculation in `sizeHint()`
   - Professional styling:
     - User messages: Right-aligned, Supervertaler blue gradient (#5D7BFF → #4F6FFF)
     - AI messages: Left-aligned, light gray (#F5F5F7)
     - System messages: Centered, subtle notification style
   - Avatar circles with gradient backgrounds (👤 user, 🤖 AI)
   - Proper shadows, rounded corners (18px radius), smooth antialiasing

2. **Updated Chat Display** ([unified_prompt_manager_qt.py:643-677](modules/unified_prompt_manager_qt.py#L643-L677))
   - Replaced `QTextEdit` with `QListWidget`
   - Applied `ChatMessageDelegate` as item delegate
   - Disabled selection/focus for clean appearance
   - Smooth pixel-based scrolling

3. **Simplified Message Adding** ([unified_prompt_manager_qt.py:1932-1959](modules/unified_prompt_manager_qt.py#L1932-L1959))
   - `_add_chat_message()` now creates `QListWidgetItem` with data
   - No more HTML/CSS - just data stored in `UserRole`
   - Auto-scroll to bottom on new messages

**What Now Works:**
- ✅ Perfect chat bubble rendering with gradients and shadows
- ✅ User text fully visible (white on blue gradient)
- ✅ AI text fully visible (dark on light gray)
- ✅ Avatars properly positioned and styled
- ✅ Text wraps correctly within 70% max width
- ✅ Professional appearance matching Supervertaler branding
- ✅ No truncation or formatting glitches
- ✅ Smooth scrolling and responsive layout

**Testing:**
- Created [test_chat_ui.py](test_chat_ui.py) - standalone test window
- Tests all three message types (user, assistant, system)
- Tests long messages for proper wrapping
- All visual issues resolved

**Files Modified:**
- [modules/unified_prompt_manager_qt.py](modules/unified_prompt_manager_qt.py)
  - Added `ChatMessageDelegate` class (lines 30-286)
  - Updated imports for Qt painting classes
  - Modified `_create_chat_interface()` to use QListWidget
  - Simplified `_add_chat_message()` method
  - Removed old HTML-based stub methods

---

### November 8, 2025 - MAJOR: Unified Prompt Library System

**🎯 Complete Refactoring: 4-Layer → 2-Layer Prompt Architecture**

Radically simplified the prompt system from a confusing 4-layer architecture to an intuitive 2-layer system inspired by CoTranslatorAI. This is a MAJOR refactoring affecting the entire prompt management system.

**🔄 Architecture Change:**

**OLD (Confusing):**
```
System Prompts tab      → CAT tool tags, formatting
Domain Prompts tab      → Industry/domain expertise
Project Prompts tab     → Project-specific rules
Style Guides tab        → Language formatting rules
```

**NEW (Simple):**
```
System Templates        → In Settings, auto-selected by mode
Prompt Library          → Unified workspace with folders, multi-attach
```

**✅ Completed Implementation:**

1. **Core Library Module** (`modules/unified_prompt_library.py` - 700+ lines)
   - ✅ Nested folder support (unlimited depth like CoTranslator)
   - ✅ Favorites system (stored in YAML frontmatter)
   - ✅ Quick Run menu for one-click prompts
   - ✅ Multi-attach capability (primary + multiple attached prompts)
   - ✅ Markdown files with YAML frontmatter
   - ✅ Full CRUD operations
   - ✅ Recursive folder loading
   - ✅ Path-based organization

2. **Migration System** (`modules/prompt_library_migration.py` - 500+ lines)
   - ✅ Automatic migration from 4-layer to unified structure
   - ✅ Backs up old folders with `.old` extension
   - ✅ Converts JSON prompts to Markdown
   - ✅ Adds metadata (favorite, quick_run, tags, folder)
   - ✅ Creates new Library/ folder structure
   - ✅ Preserves all existing prompts
   - ✅ One-time migration on first launch
   - ✅ **TESTED & WORKING** - All 5 tests passing

3. **New UI** (`modules/unified_prompt_manager_qt.py` - 900+ lines)
   - ✅ Single-tab interface replacing 4 separate tabs
   - ✅ Tree view with nested folders
   - ✅ Favorites section at top
   - ✅ Quick Run menu section
   - ✅ Active configuration panel showing:
     - Current mode (Single Segment, Batch DOCX, Batch Bilingual)
     - Primary prompt (main instructions)
     - Attached prompts (additional rules)
   - ✅ Right-click context menus:
     - Set as Primary / Attach to Active
     - Add to Favorites / Quick Run
     - Edit / Duplicate / Delete
     - Create folders and subfolders
   - ✅ Prompt editor with metadata fields
   - ✅ Preview combined prompt
   - ✅ System Templates access from main UI

4. **Test Suite** (`tests/test_unified_prompt_library.py`)
   - ✅ Test 1: Migration (PASSED)
   - ✅ Test 2: Library Loading (PASSED - 16 prompts)
   - ✅ Test 3: Favorites & Quick Run (PASSED)
   - ✅ Test 4: Multi-Attach (PASSED)
   - ✅ Test 5: Prompt Composition (PASSED)
   - **Result: 5/5 tests passed** ✅

5. **Demo Application** (`tests/demo_unified_prompt_ui.py`)
   - ✅ Standalone UI demo
   - ✅ Shows complete new interface
   - ✅ Run with: `python tests/demo_unified_prompt_ui.py`

6. **User Documentation** (`docs/UNIFIED_PROMPT_LIBRARY_GUIDE.md`)
   - ✅ Complete user guide
   - ✅ Migration explanation
   - ✅ Usage examples
   - ✅ FAQ and troubleshooting
   - ✅ Tips and best practices

**📁 New File Structure:**

```
user_data/Prompt_Library/
├── 1_System_Prompts.old          (backed up - old system prompts)
├── 2_Domain_Prompts.old          (backed up - old domain prompts)
├── 3_Project_Prompts.old         (backed up - old project prompts)
├── 4_Style_Guides.old            (backed up - old style guides)
├── .migration_completed          (migration flag file)
└── Library/                      (NEW unified structure)
    ├── Style Guides/
    │   ├── Dutch.md
    │   ├── English.md
    │   ├── French.md
    │   ├── German.md
    │   └── Spanish.md
    ├── Domain Expertise/         (migrated from 2_Domain_Prompts)
    │   ├── Medical Translation Specialist.md
    │   ├── Legal Translation Specialist.md
    │   ├── Financial Translation Specialist.md
    │   └── ... (8 prompts total)
    ├── Project Prompts/           (migrated from 3_Project_Prompts)
    │   ├── Professional Tone & Style.md
    │   ├── Preserve Formatting & Layout.md
    │   └── Prefer Translation Memory Matches.md
    └── Active Projects/           (user creates own subfolders)
        └── (empty - ready for user organization)
```

**🔧 Technical Details:**

**Terminology Decision:**
- **"System Templates"** (not "Base Templates" or "Tag Processing Rules")
- Hidden in Settings > Translation (not in main UI)
- Auto-selected based on document type

**Metadata Format (YAML Frontmatter):**
```yaml
---
name: "Medical Translation Specialist"
description: "Expert medical device translation"
domain: "Medical"
version: "1.0"
task_type: "Translation"
favorite: false
quick_run: false
folder: "Domain Expertise"
tags: ["medical", "technical", "regulatory"]
created: "2025-10-19"
modified: "2025-11-08"
---

# Prompt content here...
```

**Multi-Attach System:**
```python
# User Configuration:
Primary Prompt:  Medical Translation Specialist
Attached:        Dutch Style Guide
Attached:        Professional Tone & Style

# System automatically combines:
final_prompt = system_template + primary + attached[0] + attached[1]
```

**Prompt Composition Logic:**
```python
def build_final_prompt(source_text, source_lang, target_lang, mode):
    # Layer 1: System Template (auto-selected)
    system = get_system_template(mode)  # single, batch_docx, batch_bilingual
    
    # Layer 2: Library Prompts
    library = ""
    if active_primary_prompt:
        library += primary_prompt
    for attached in attached_prompts:
        library += "\n\n" + attached
    
    # Combine
    final = system + library
    
    # Replace placeholders
    final = final.replace("{{SOURCE_LANGUAGE}}", source_lang)
    final = final.replace("{{TARGET_LANGUAGE}}", target_lang)
    final = final.replace("{{SOURCE_TEXT}}", source_text)
    
    return final
```

---

## ✨ AI ASSISTANT IMPLEMENTATION (November 8-9, 2025)

**Complete AI-Powered Conversational Interface**

After completing the unified prompt system, we restructured the Prompt Manager interface to include an AI Assistant for conversational prompt generation and document analysis.

### UI Structure Change

```
OLD: Single "📚 Prompt Library" tab

NEW: "🤖 Prompt Manager" with two sub-tabs:
     ├── 📚 Prompt Library (original functionality)
     └── ✨ AI Assistant (NEW conversational AI)
```

### AI Assistant Features Implemented

**1. Core Functionality** ✅
- LLM Integration: OpenAI, Claude, Gemini
- Auto-detects LLM provider from main app settings
- Conversation persistence (JSON storage)
- Message history (last 10 on load, full history saved)
- Clear chat functionality with confirmation

**2. Context Awareness** ✅
- Access to all 38+ prompts in unified library
- Current document tracking
- Recent conversation memory (last 5 messages in context)
- Attached files content included in AI requests

**3. File Attachments** ✅
- PDF/DOCX/PPTX/XLSX auto-conversion using `markitdown`
- TXT/MD direct import
- Multiple file support
- Content included in AI context (first 2000 chars per file)
- Persistent across sessions

**4. Project Analysis** ✅
- "🔍 Analyze Project & Generate Prompts" button
- Analyzes current project context
- Suggests relevant existing prompts
- Generates new custom prompts with complete text
- Lists available resources (prompts, TMs, termbases)

**5. UI Components** ⚠️ (FUNCTIONAL BUT STYLING BROKEN)

Context sidebar (left):
- 📄 Current Document
- 📎 Attached Files (with count)
- 💡 Prompt Library (38 prompts)
- 💾 Translation Memories (placeholder)
- 📚 Termbases (placeholder)

Chat area (right):
- Message display with chat bubbles
- Multi-line input (Shift+Enter for new lines)
- 🗑️ Clear Chat button
- Send button

### Technical Implementation

**Files Modified:**
- `modules/unified_prompt_manager_qt.py` (1,600+ lines)
  - `_init_llm_client()` - Initialize AI with API keys
  - `_load_conversation_history()` - Restore previous chats
  - `_save_conversation_history()` - Persist to JSON
  - `_create_ai_assistant_tab()` - Build UI
  - `_create_context_sidebar()` - Resource panel
  - `_create_chat_interface()` - Chat display + input
  - `_send_chat_message()` - Handle user input
  - `_send_ai_request()` - Call LLM API
  - `_add_chat_message()` - Render chat bubbles
  - `_attach_file()` - File attachment + conversion
  - `_analyze_and_generate()` - Project analysis
  - `_clear_chat()` - Clear conversation

**Dependencies Added:**
```python
# pyproject.toml
dependencies = [
    ...
    "markitdown>=0.0.1",  # Document conversion
]
```

**Data Storage:**
```
user_data/ai_assistant/
└── conversation.json
    {
      "history": [
        {
          "role": "user|assistant|system",
          "content": "message text",
          "timestamp": "2025-11-08T..."
        }
      ],
      "files": [
        {
          "path": "full/path/to/file",
          "name": "filename.pdf",
          "content": "converted markdown...",
          "type": ".pdf",
          "size": 12345,
          "attached_at": "2025-11-08T..."
        }
      ],
      "updated": "2025-11-08T..."
    }
```

**Integration Points:**
- Uses `modules/llm_clients.py` for provider-agnostic API calls
- Uses `UnifiedPromptLibrary` to access prompt data
- Connects to parent app for settings and current document
- Same LLM provider/model as main translation engine

### 🚨 CURRENT PROBLEM: Chat UI Rendering

**Status:** BROKEN - Functional but visually unusable

**Issues:**
1. User input text appears invisible (white on white background)
2. Chat bubbles oddly formatted and truncated
3. HTML/CSS styling not rendering correctly in QTextEdit
4. Avatar positioning incorrect (bottom instead of top)
5. Message wrapping issues

**What's Been Tried:**
- ✅ Table-based layout → messages truncated
- ✅ Div-based with inline-block → formatting weird  
- ✅ Solid colors vs gradients → still issues
- ✅ Various text color combinations → input still invisible
- ✅ Vertical-align: top/bottom → avatars misaligned

**Root Cause:**
QTextEdit has limited HTML/CSS support. Advanced styling (flexbox, proper inline-block, gradients) doesn't work well.

**Recommendations for Fixing:**

**Option 1: QListWidget with Custom Delegates** (RECOMMENDED)
```python
class ChatMessageDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        # Custom painting of chat bubbles
        # Full control over rendering
        pass
```

**Option 2: QScrollArea + Custom Widgets**
```python
chat_container = QVBoxLayout()
for message in messages:
    bubble = ChatBubbleWidget(message)
    chat_container.addWidget(bubble)
```

**Option 3: QWebEngineView**
```python
# Use HTML/CSS/JS in web view
# Best styling control, but heavier
```

**What Works:**
- ✅ AI communication (all providers)
- ✅ Message sending and receiving
- ✅ Conversation persistence
- ✅ File attachments with markitdown conversion
- ✅ Context building and prompt analysis
- ✅ Error handling and logging

**What's Broken:**
- ❌ Chat bubble visual styling
- ❌ User input text visibility
- ❌ Avatar positioning
- ❌ Message truncation

**Goal:**
Professional chat interface matching Supervertaler website colors (#5D7BFF blue gradient), with:
- Clean chat bubbles (user right in blue, AI left in gray)
- Avatar icons (👤 for user, 🤖 for AI)
- Proper text visibility and wrapping
- Elegant spacing and shadows
- Similar to iMessage/Slack/modern chat UIs

**Files to Fix:**
- `modules/unified_prompt_manager_qt.py`
  - Lines ~1540-1650: `_add_chat_message()` method
  - Lines ~350-450: `_create_chat_interface()` method

**Documentation Created:**
- `docs/AI_ASSISTANT_GUIDE.md` - Complete user guide
- `docs/AI_ASSISTANT_IMPLEMENTATION.md` - Technical details
- `docs/AI_ASSISTANT_QUICK_REFERENCE.md` - Quick reference card

---

**📊 Migration Results:**

Actual migration output from test run:
```
============================================================
🔄 Starting Prompt Library Migration
============================================================

📚 Migrating Domain Prompts...
   ✓ Migrated 8 domain prompts

📋 Migrating Project Prompts...
   ✓ Migrated 3 project prompts

🎨 Migrating Style Guides...
   ✓ Migrated 5 style guides

💾 Creating backups of old folders...
   ✓ Backed up: 1_System_Prompts → 1_System_Prompts.old
   ✓ Backed up: 2_Domain_Prompts → 2_Domain_Prompts.old
   ✓ Backed up: 3_Project_Prompts → 3_Project_Prompts.old
   ✓ Backed up: 4_Style_Guides → 4_Style_Guides.old

============================================================
✅ Migration Complete! Migrated 16 prompts
============================================================
```

**🎯 Key Design Decisions:**

1. **No Legacy Mode** - Clean break, simpler codebase
2. **Favorites in YAML** - No separate favorites.json file
3. **Unlimited Nesting** - Like CoTranslator's folder structure
4. **System Templates Hidden** - In Settings, not fighting for attention
5. **Multi-Attach** - More flexible than old single-active system

**🚧 Remaining Integration Work:**

**Status: Ready for main app integration**

Files created and tested:
- ✅ `modules/unified_prompt_library.py`
- ✅ `modules/unified_prompt_manager_qt.py`
- ✅ `modules/prompt_library_migration.py`
- ✅ `tests/test_unified_prompt_library.py`
- ✅ `tests/demo_unified_prompt_ui.py`
- ✅ `docs/UNIFIED_PROMPT_LIBRARY_GUIDE.md`

Next steps to complete:
1. **Integrate into Supervertaler.py:**
   - Replace `from modules.prompt_manager_qt import PromptManagerQt`
   - With `from modules.unified_prompt_manager_qt import UnifiedPromptManagerQt`
   - Update all calls to `build_final_prompt()`
   - Update state tracking for active prompts

2. **Add System Templates to Settings:**
   - Create Settings > Translation > System Templates section
   - Allow viewing/editing mode-specific templates
   - Show warning about modifying CAT tool formats

3. **Final Testing:**
   - Test in actual translation workflow
   - Test mode switching (single → batch_docx → batch_bilingual)
   - Test with real documents
   - Verify tag preservation still works
   - Test with various LLM providers

**💡 User-Facing Benefits:**

- **Simpler:** One workspace instead of 4 tabs
- **Flexible:** Organize prompts however you want
- **Powerful:** Multi-attach for combining instructions
- **Familiar:** Like CoTranslatorAI's prompt library
- **Visual:** See folder structure, favorites, quick run
- **Safe:** Automatic migration with backups

**🔍 Files Modified/Created:**

**New Files:**
- `modules/unified_prompt_library.py` (700+ lines)
- `modules/unified_prompt_manager_qt.py` (900+ lines)
- `modules/prompt_library_migration.py` (500+ lines)
- `tests/test_unified_prompt_library.py` (200+ lines)
- `tests/demo_unified_prompt_ui.py` (60 lines)
- `docs/UNIFIED_PROMPT_LIBRARY_GUIDE.md` (comprehensive guide)

**Files to be Modified:**
- `Supervertaler.py` (replace prompt manager integration)
- Settings dialog (add System Templates section)

**Old Files (to be deprecated):**
- `modules/prompt_manager_qt.py` (4000+ lines - will be replaced)
- `modules/prompt_library.py` (680 lines - no longer needed)
- `modules/style_guide_manager.py` (316 lines - no longer needed)

**🎓 Learning Notes for Future AI:**

This refactoring demonstrates:
1. **User-centric design:** Simplify confusing architectures
2. **Inspiration from competitors:** CoTranslatorAI's approach was better
3. **Safe migration:** Always backup, provide rollback
4. **Modular design:** Each component testable independently
5. **Documentation:** User guide written before integration
6. **Test-driven:** Verify functionality before touching main app

**⚠️ Important Context:**

- This ONLY affects Supervertaler.py (Qt version)
- Supervertaler_tkinter.py is separate and unchanged
- Old prompt manager kept in codebase temporarily for reference
- Migration runs automatically on first launch of new version
- User can manually rollback by renaming .old folders

---

## 📅 Previous Development Activity

### November 7, 2025 - TagCleaner Module & AutoFingers Enhancement

**🎯 New Module: TagCleaner - CAT Tool Tag Removal System**

Implemented a standalone, modular tag cleaning system that removes CAT tool tags from translation text. Follows Supervertaler's modular architecture philosophy - can be used independently or integrated with other modules.

**✅ Completed Features:**

1. **Standalone TagCleaner Module** ([modules/tag_cleaner.py](../modules/tag_cleaner.py))
   - ✅ Fully independent module with no core dependencies
   - ✅ Granular control per CAT tool and tag type
   - ✅ Settings export/import via `to_dict()` / `from_dict()`
   - ✅ Extensible architecture for adding new tag patterns
   - ✅ Can be launched standalone or used programmatically

2. **memoQ Index Tag Support** (Initial Implementation)
   - ✅ Regex pattern: `(?:\[\d+\}|\{\d+\])`
   - ✅ Removes tags like `[1}`, `{2]`, `[7}`, `{8]`, `[99}`, `{100]`, etc.
   - ✅ Supports unlimited digit range (not limited to specific numbers)
   - ✅ Tested with real-world translation projects

3. **AutoFingers Integration**
   - ✅ TagCleaner instance automatically available: `engine.tag_cleaner`
   - ✅ Tags cleaned before pasting translation (line 290 in autofingers_engine.py)
   - ✅ Clean separation of concerns - modular design
   - ✅ Optional on-the-fly tag cleaning when pasting from TMX to memoQ

4. **User Interface Controls** (Supervertaler.py:12777-12843)
   - ✅ Master switch: "Enable tag cleaning" checkbox
   - ✅ Granular tag type selection (indented hierarchy):
     - ✅ memoQ index tags ([1} {2]) - **Active and functional**
     - ⏸️ Trados Studio tags - Framework ready (coming soon)
     - ⏸️ CafeTran tags - Framework ready (coming soon)
     - ⏸️ Wordfast tags - Framework ready (coming soon)
   - ✅ Scrollable settings panel for smaller screens

5. **Settings Persistence**
   - ✅ Structured JSON format in autofingers_settings.json
   - ✅ Nested structure matching modular architecture
   - ✅ Backward compatible with existing AutoFingers settings
   - ✅ Auto-save and auto-load on startup

**🔧 Technical Implementation:**

**Files Created:**
- `modules/tag_cleaner.py` - Standalone TagCleaner module (273 lines)
- `test_tag_cleaner_integration.py` - Comprehensive test suite

**Files Modified:**
- `modules/autofingers_engine.py` - Integrated TagCleaner (line 15, 87, 290)
- `Supervertaler.py` - Added UI controls and settings management
- `user_data_private/autofingers_settings.json` - Extended structure

**Architecture Highlights:**
```python
# Standalone usage
from modules.tag_cleaner import TagCleaner

cleaner = TagCleaner()
cleaner.enable()
cleaner.enable_memoq_index_tags()
cleaned = cleaner.clean("Text [1}with{2] tags")
# Result: "Text with tags"

# Integration with AutoFingers
engine.tag_cleaner.enable()
# Tags automatically cleaned during translation paste
```

**Test Results:**
- ✅ All 3 test suites passing
- ✅ Standalone module test
- ✅ AutoFingers integration test
- ✅ Settings export/import test
- ✅ Real-world project validation

**📦 Future Extensibility:**

The TagCleaner module is designed for easy expansion:

1. **Additional CAT Tools** (Ready to implement):
   - Trados Studio tag patterns
   - CafeTran Espresso tags
   - Wordfast tags
   - SDL Passolo tags
   - Others as requested by users

2. **Standalone Features** (Planned):
   - Dedicated TagCleaner tab in Supervertaler
   - Menu integration (Tools → Clean Tags)
   - Batch tag cleaning for TMX files
   - CLI mode for automation scripts
   - Drag-and-drop file cleaning

3. **Advanced Patterns** (Extensible):
   - Custom regex patterns via UI
   - Tag pattern libraries
   - Import/export tag pattern sets
   - Community-contributed patterns

**💡 Design Philosophy:**

TagCleaner embodies Supervertaler's modular architecture:
- **Independent**: Can run without Supervertaler core
- **Reusable**: Other modules can import and use it
- **Configurable**: Granular control, not all-or-nothing
- **Extensible**: New tag types = add pattern, no refactoring
- **User-Requested**: Future features driven by community needs

**🎯 User Impact:**

- Translators using AutoFingers with tagged TMX files can now clean tags automatically
- No manual tag removal needed after pasting from TMX
- Supports mixed CAT tool workflows (e.g., Trados TMX → memoQ target)
- Foundation for future standalone tag cleaning workflows

**📝 Version:** 1.2.4 (2025-11-07)

---

### November 6, 2025 - LLM & MT Integration Complete

**🎯 Major Achievement: Complete Translation Matching System**

Successfully integrated all translation sources (Termbase, TM, MT, LLM) with proper chaining and display:

**✅ Completed Features:**
1. **Multi-LLM Support Fully Operational**
   - ✅ OpenAI GPT integration working (GPT-4o, GPT-5, etc.)
   - ✅ Claude 3.5 Sonnet integration (API key issue - user needs credits)
   - ✅ Google Gemini integration working (Gemini 2.0 Flash)
   - ✅ Flexible API key naming: supports both `google` and `google_translate` keys
   - ✅ Flexible Gemini key naming: supports both `gemini` and `google` keys

2. **Google Cloud Translation API Integration**
   - ✅ Proper implementation using `google-cloud-translate` library
   - ✅ Added `load_api_keys()` function to `modules/llm_clients.py` for standalone operation
   - ✅ Backward compatible key naming (checks both `google_translate` and `google`)
   - ✅ Uses Translation API v2 with direct API key authentication
   - ✅ Returns structured response with translation, confidence, and metadata

3. **Termbase Match Preservation**
   - ✅ Fixed issue where termbase matches disappeared when TM/MT/LLM appeared
   - ✅ Root cause: delayed search wasn't receiving termbase matches parameter
   - ✅ Solution: Pass `current_termbase_matches` to `_add_mt_and_llm_matches()`
   - ✅ Termbase matches now display consistently across all scenarios

4. **Performance Optimization**
   - ✅ Debounced search with 1.5-second delay prevents excessive API calls
   - ✅ Timer-based cancellation when user moves between segments
   - ✅ Immediate termbase display, deferred TM/MT/LLM loading

**🔧 Technical Implementation:**

**File: `modules/llm_clients.py`**
- Added standalone `load_api_keys()` function (lines 27-76)
- Fixed Google Translate to use loaded API keys instead of undefined function
- Supports multiple API key locations (user_data_private/, root)
- Handles both key naming conventions for backward compatibility

**File: `Supervertaler.py`**
- Fixed Gemini integration to check for both `gemini` and `google` API keys (line ~10620)
- Enhanced Google Translate integration with comprehensive logging
- Termbase match preservation through delayed search parameter passing
- Structured match chaining: Termbase → TM → MT → LLM

**🐛 Resolved Issues:**
1. ✅ Google Translate error: `name 'load_api_keys' is not defined` 
   - Fixed by adding function to llm_clients.py module
2. ✅ Gemini not being called despite API key present
   - Fixed by checking both `gemini` and `google` key names
3. ✅ Termbase matches disappearing when TM/MT/LLM loaded
   - Fixed by passing termbase matches to delayed search function

**📦 Dependencies:**
- `google-cloud-translate` - Google Cloud Translation API library
- `openai` - OpenAI API client  
- `anthropic` - Anthropic Claude API client
- `google-generativeai` - Google Gemini API client
- `httpx==0.28.1` - HTTP client (version locked for LLM compatibility)

**💡 Key Design Decisions:**

1. **API Key Flexibility:**
   - Support both `google_translate` and `google` for Google Cloud Translation
   - Support both `gemini` and `google` for Gemini API
   - Provides backward compatibility and user flexibility

2. **Standalone Module Design:**
   - `llm_clients.py` can function independently with its own `load_api_keys()`
   - No dependency on main application for API key loading
   - Enables reuse in other projects

3. **Match Preservation Architecture:**
   - Termbase matches stored in panel's `_current_matches` dictionary
   - Passed explicitly to delayed search functions
   - Never overwritten, only appended to by TM/MT/LLM results

**🎯 Next Steps:**
- [ ] Test all LLM providers with real API keys
- [ ] Add user feedback for API errors (better than console logs)
- [ ] Consider adding DeepL integration
- [ ] Implement match insertion keyboard shortcuts

---

## 🎯 Project Overview

**Supervertaler** is a dual-platform AI-powered translation tool for professional translators. Currently maintaining two active versions during transition to Qt as primary platform.

### Two Active Versions

| Aspect | Qt Edition | Tkinter Edition (Classic) |
|--------|-----------|---------------------------|
| **File** | `Supervertaler.py` | `Supervertaler_tkinter.py` |
| **Version** | v1.0.1+ (Active Development) | v2.5.0+ (Maintenance) |
| **Framework** | PyQt6 | Tkinter |
| **Status** | Primary (new features) | Legacy (feature parity) |
| **UI** | Modern ribbon + compact panels | Tabbed interface |
| **Database** | SQLite (shared schema) | SQLite (shared schema) |
| **Changelog** | `CHANGELOG.md` | `legacy_versions/CHANGELOG_Tkinter.md` |

**Migration Strategy:** Move all tkinter functionality to Qt version, then deprecate tkinter in v2.0.0

---

## 📁 Repository Structure (Lean)

```
/
├── Supervertaler.py              # Qt Edition (PRIMARY)
├── Supervertaler_tkinter.py         # Tkinter Edition (legacy)
├── README.md                         # Repository overview
├── CHANGELOG.md                      # Complete version history
├── CHANGELOG_Tkinter.md              # Tkinter version history
│
├── modules/                          # Shared modules
│   ├── database_manager.py           # SQLite backend
│   ├── termbase_manager.py           # Termbases CRUD
│   ├── project_home_panel.py         # Project home UI (Qt)
│   ├── translation_results_panel.py  # Results UI (Qt)
│   ├── autofingers_engine.py         # Auto-fingers feature
│   ├── config_manager.py             # Settings/config
│   └── [other modules]
│
├── docs/
│   ├── PROJECT_CONTEXT.md            # ← THIS FILE (Single source of truth)
│   ├── QUICK_START.md                # Getting started
│   ├── ARCHITECTURE.md               # System design
│   ├── DATABASE.md                   # Database schema
│   ├── sessions/                     # Archived session summaries
│   ├── guides/                       # How-to guides
│   └── archive/                      # Old documentation (reference)
│
├── user_data/                        # User projects & database
├── user_data_private/                # Dev database (gitignored)
├── tests/                            # Unit tests
└── assets/                           # Icons, images
```

---

## 🔑 Key Features (Both Versions)

### Translation Memory (TM)
- SQLite-based persistent storage
- Full-text search with fuzzy matching
- TM matches with relevance scores
- Context-aware suggestions
- Import/export (TMX format)

### Termbases
- Multiple termbases per project
- Global and project-specific scopes
- Term search with filtering
- Priority-based matching
- Sample data: 3 termbases (Medical, Legal, Technical) with 48 terms

### CAT Functionality
- Segment-based translation editing
- Translation memory integration
- Match insertion (keyboard shortcuts)
- Project management
- Auto-fingers support

### AI Integration
- OpenAI GPT support
- Claude support (configurable)
- API key management

---

## 🗄️ Database Schema (SQLite)

### Core Tables
- **translation_units** - TM entries (source_text, target_text, language pairs)
- **termbases** - Termbase definitions (name, source_lang, target_lang, project_id)
- **termbase_terms** - Individual terms (source_term, target_term, domain, priority)
- **termbase_activation** - Project termbase activation tracking
- **non_translatables** - Locked terms
- **projects** - Translation projects

### Important Constraints
- `termbase_terms.source_lang` DEFAULT 'unknown' (NOT NULL removed)
- `termbase_terms.target_lang` DEFAULT 'unknown' (NOT NULL removed)
- Never use `glossary_terms` table (renamed to `termbase_terms`)
- Never use `glossary_id` column (renamed to `termbase_id`)

---

## ⚙️ Current Status (v1.1.1-Qt)

**Completed (Nov 1, 2025):**
✅ AutoFingers UI simplification - removed redundant "Use Alt+N" setting  
✅ Single "Confirm segments" checkbox now controls behavior (checked = Ctrl+Enter, unchecked = Alt+N)  
✅ Backward compatibility maintained for existing settings files  
✅ Version bumped to 1.1.1  

**Completed (Oct 29-30, 2025):**
✅ Termbases feature complete  
✅ Terminology standardized ("termbase" everywhere)  
✅ Database schema fixed (NOT NULL constraints)  
✅ Bug fixes: method names, Project object access  
✅ Sample data: 3 termbases with 48 terms  

**In Progress:**
- [ ] Terminology Search (Ctrl+P)
- [ ] Concordance Search (Ctrl+K)
- [ ] Test create/edit dialogs

**Known Issues:** None

---

## 📝 Naming Conventions

**ALWAYS USE:**
- ✅ "Termbase" (one word, lowercase)
- ✅ "Qt Edition" / "Tkinter Edition"
- ✅ "Translation Memory" or "TM"

**NEVER USE:**
- ❌ "Glossary" (replaced with "Termbase")
- ❌ "Term Base" (two words - always one word)
- ❌ `glossary_terms` or `glossary_id` (renamed to termbase_*)

---

## 🚀 Running Applications

### Qt Edition
```bash
python Supervertaler.py
```

### Tkinter Edition
```bash
python Supervertaler_tkinter.py
```

---

## 📚 Key Reference Files

| File | Purpose |
|------|---------|
| `docs/PROJECT_CONTEXT.md` | This file - source of truth |
| `CHANGELOG.md` | Complete version history |
| `CHANGELOG_Tkinter.md` | Tkinter version history |
| `modules/database_manager.py` | Database layer |
| `modules/termbase_manager.py` | Termbase operations |

---

## 🔍 Before Starting Work

1. **Consult this document first** - It's your source of truth
2. Understand which version you're working on (Qt vs Tkinter)
3. Check naming conventions (Termbase, never Glossary)
4. Review current focus items above
5. Verify database table/column names are correct

---

## 💡 Repository Philosophy

**Lean = Efficient:**
- ✅ Only essential source code
- ✅ Current documentation in `docs/`
- ✅ Old docs archived, summarized in PROJECT_CONTEXT.md
- ✅ Smaller repo = faster AI operations = lower costs

---

**Last Updated:** November 1, 2025
**Next Review:** Start of development sprint

**Hidden folders** (.gitignored):
- `.dev/` - Tests, scripts, backup files, documentation tools
- `.supervertaler.local` - Dev mode feature flag

---

## ✨ Key Features

### v1.0.0-Qt (Modern CAT Interface)

1. **Modern Ribbon Interface**
   - 4 context-sensitive ribbon tabs (Home, Translation, Tools, Settings)
   - Minimalist design, non-intrusive controls
   - Proper CAT workflow integration

2. **Professional Tab Organization**
   - **Project Group:** Project Manager, Project Editor
   - **Resources Group:** Translation Memories, Termbases, Non-Translatables, Prompts
   - **Modules Group:** TMX Editor, Reference Images, PDF Rescue, Encoding Repair, AutoFingers, Tracked Changes
   - **Settings Group:** Settings, Log
   - **Utilities:** Universal Lookup (Ctrl+Alt+L)

3. **Translation Results Panel (NEW - PRODUCTION READY) ✨**
   - **Compact memoQ-style design** - Minimal wasted space, maximum info density
   - **Stacked match sections:** NT, Machine Translation, Translation Memory, Termbases
   - **Collapsible headers** - Toggle sections to see only what matters
   - **Match items display:**
     * Type badge (NT/MT/TM/Termbase)
     * Relevance percentage (0-100%)
     * Target text (main content, line-wrapped)
     * Source context when available
   - **Drag/drop support** - Drag matches directly into target field
   - **Compare boxes** - Shows Current Source | TM Source | TM Target side-by-side
   - **Diff highlighting** - Color-coded differences (ready to integrate)
   - **Segment info** - Shows current segment number and source preview
   - **Notes section** - For translator annotations (compact, below matches)

4. **AutoFingers Automation**
   - Replicates memoQ AutoFingers functionality
   - TMX-based translation automation
   - Hotkey-driven (Ctrl+Alt+P for single, Ctrl+Shift+L for loop)
   - Thread-safe match pane display
   - Simplified UI: Single "Confirm segments" checkbox controls behavior
     * Checked: Uses Ctrl+Enter to confirm segment before moving to next
     * Unchecked: Uses Alt+N to move to next without confirming

5. **Universal Lookup (Ctrl+Alt+L)**
   - Global hotkey search across all resources
   - Real-time results display
   - Integration with all translation memory sources

### v2.5.0-CLASSIC

1. **Multi-LLM Support**
   - Gemini, Claude, OpenAI/GPT
   - API key management in settings
   - Model selection per project

2. **DOCX Import/Export Workflow**
   - Load bilingual DOCX files
   - Extract/manage segments
   - AI translation with custom prompts
   - Export results to DOCX format

3. **Custom Prompts System**
   - System prompts (define AI role/expertise)
   - Custom instructions (user preferences/context)
   - Public and private storage
   - Reusable across projects

4. **Post-Translation Analysis (NEW - v2.5.0)**
   - **Tracked Changes Review**: Analyze editing patterns from memoQ/CafeTran
   - Load bilingual DOCX with tracked changes
   - Browse and filter changes
   - **Export to Markdown Report** with:
     - 3-column table (Source, Original, Revised)
     - AI-powered change summaries (4th column, optional)
     - Configurable batch processing (1-100 segments)
     - Precise change detection (quotes, punctuation, terminology)
   - **Export to TSV** for analysis/sharing

5. **Session Management**
   - Session reports in markdown
   - Statistics and summaries
   - Translation history

### v3.1.1-beta

- Segment-based CAT editor interface
- **Prompt Library** with tree-based organization
- Filter and search capabilities
- UK English lowercase UI style ("System prompts" not "System Prompts")
- Same AI backend as CLASSIC but with different workflow

---

## 📊 Tracked Changes Feature Details

**Purpose:** Help translators review how much they edited AI-generated translations

**Workflow:**
1. Translate project in CAT tool (memoQ, CafeTran, etc.) with tracked changes enabled
2. Export bilingual document with tracked changes
3. Load in Supervertaler
4. Browse changes (with optional search/filter)
5. Export analysis report (Markdown with optional AI summaries)

**AI Analysis (Optional):**
- Asks currently selected AI to provide precise change summaries
- Uses batch processing (default 25 segments/API call)
- Configurable batch size via slider (1-100)
- Examples:
  - ✅ `"pre-cut" → "incision"`
  - ✅ `Curly quotes → straight quotes: "roll" → "roll"`
  - ✅ `"package" → "packaging"`
  - ❌ "Fixed grammar" (too vague - not used)

**Report Format:** Paragraph-based Markdown
```markdown
### Segment 1

**Target (Original):**  
[AI-generated text]

**Target (Revised):**  
[Your edited text]

**Change Summary:**  
[AI analysis of what changed]
```

---

## 🔧 Technical Details

### File Naming Conventions

- Main executables: `Supervertaler_vX.X.X-[CLASSIC|CAT].py`
- Version bumps affect:
  - File name itself
  - First line comment in file
  - README.md references
  - CHANGELOG entries

### Code Organization

**CLASSIC version:**
- `TrackedChangesAgent` - Core logic for tracked changes parsing
- `TrackedChangesBrowser` - UI dialog for browsing changes
- `export_to_tsv()` / `export_to_md()` - Export functionality
- AI analysis with batch processing

**CAT version:**
- `PromptLibrary` - Manages system prompts and custom instructions
- Tree-based UI for organization
- Same TrackedChangesAgent (shared logic)
- Separate UI browser (to be ported)

### AI Integration

**Supported Providers:**
- Gemini (`google-generativeai`)
- Claude (`anthropic`)
- OpenAI (`openai`)

**Current Prompts (Batch Processing):**
```
You are a precision editor analyzing tracked changes...
Compare original and revised text and identify EXACTLY what changed.
- Be extremely specific and precise
- Quote exact words/phrases that changed
- Use format: "X" changed to "Y"
- PAY SPECIAL ATTENTION to quotes/punctuation
- Do NOT use vague terms
- DO quote actual changed text
```

**Token Limits:**
- Batch: 2000 tokens (for 25 segments)
- Single: 100 tokens (fallback)
- Response max: 10 words per change (enforced in parsing)

---

## 📝 Version History

### v2.5.0-CLASSIC (Current)
- ✨ **NEW:** Tracked Changes Review feature
- ✨ **NEW:** AI-powered change summaries
- ✨ **NEW:** Batch processing for faster analysis
- ✨ **NEW:** Configurable batch size slider
- 🐛 Infrastructure updates for parallel folder structure
- 🎨 UK English lowercase style throughout

### v3.1.1-beta (Current)
- 🐛 Fixed system_prompts_dir initialization
- 🐛 Fixed prompt loading in dev mode
- 🐛 Fixed emoji rendering issues
- 🎨 Applied UK English lowercase style
- 📝 Removed private UI elements
- 🔧 Parallel folder structure implementation

---

## 🎯 Development Strategy

### Chat History Management
- **Daily exports:** `docs/chat-logs/copilot_chat_history_YYYY-MM-DD (MB).txt`
- **Purpose:** Full context preservation between sessions
- **Benefit:** Faster issue resolution, historical context
- **Maintenance:** Automated via GitHub Copilot Chat Exporter

### Documentation
- **README.md** - User-facing overview
- **CHANGELOG.md** - Main navigation (links to split logs)
- **CHANGELOG-CLASSIC.md** - v2.x.x history
- **CHANGELOG-CAT.md** - v3.x.x-beta history
- **.dev/** folder - Development tools, scripts, tests

### Quality Assurance
- Both programs compile without syntax errors
- UK English lowercase style enforced
- Emoji rendering tested (Unicode escape codes)
- Cross-version consistency maintained

---

## 🎯 Strategic Refocus: Companion Tool Philosophy (November 2025)

### Vision Shift

**Original Goal:** Build a full-featured CAT tool with grid editing, TM/termbase matching, and comprehensive translation workflows.

**New Focus:** **Companion Tool** - Work alongside existing CAT tools (memoQ, Trados, CafeTran, Wordfast, etc.) rather than replacing them.

### Rationale

1. **Complexity Management:** Building a fully functional CAT tool grid, TM matching, and termbase integration is beyond scope and duplicates existing professional tools.
2. **Play to Strengths:** Supervertaler excels at AI-powered features and specialized modules that CAT tools don't offer.
3. **User Value:** Translators can continue using their trusted CAT tools while leveraging Supervertaler's unique capabilities.

### Core Strengths to Preserve

✅ **AI-Powered Translation/Proofreading/Localization**
- Comprehensive prompt management system
- Multi-layer prompts (System, Domain, Project, Style Guide)
- Multiple LLM providers (OpenAI, Claude, Gemini)

✅ **Specialized Modules**
- **AutoFingers** - Get translations back into CAT tools via TMX
- **PDF Rescue** - Extract text from images using AI OCR
- **Omni-Lookup** - Universal search across all resources
- **Text Encoding Repair** - Fix encoding issues
- **Tracked Changes Review** - Analyze editing patterns

✅ **CAT Tool Integration**
- TMX export/import for seamless workflow
- Compatible with memoQ, Trados, CafeTran, Wordfast formats

### Simplification Strategy

#### Grid View - Simplified to Review Tool

**Keep:**
- ✅ View-only with minor editing capability (quick fixes allowed)
- ✅ All filtering capabilities (essential for quality review)
- ✅ Comprehensive find & replace system
- ✅ Multiple views (Grid/List/Document) + extensibility for future views
- ✅ Translation quality review tools

**Simplify/Remove:**
- ❌ Full editing capabilities (reduce to minor edits only)
- ❌ Complex segment editing workflows
- ❌ Advanced CAT features that duplicate CAT tool functionality

#### TM/Termbase Matching - Optional Feature

**Implementation:**
- ✅ Add **toggle switch** to enable/disable TM/termbase matching
- ✅ When disabled: Hide assistance panel or show only AI translations
- ✅ When enabled: Show matches as read-only reference (no insertion workflows)

**What "Complex Lookup/Insert Workflows" Means:**
- Automatic TM/termbase search when selecting segments
- Click-to-insert matches from assistance panel
- Keyboard shortcuts (Ctrl+1-9) to insert matches by number
- Drag-and-drop match insertion
- Auto-population of target fields from matches

**Simplified Approach:**
- Keep matching as **optional read-only reference**
- Remove insertion workflows (let CAT tool handle that)
- Focus on **quality review** rather than active editing

#### AutoFingers - Keep As-Is

- ✅ Leave AutoFingers functionality unchanged
- ✅ Continue TMX-based translation automation
- ✅ Maintain hotkey-driven workflow (Ctrl+Alt+P, Ctrl+Shift+L)

### Updated Feature Priorities

**High Priority (Core Companion Features):**
1. AI translation/proofreading with prompt management
2. Grid view for quality review (simplified)
3. All specialized modules (AutoFingers, PDF Rescue, etc.)
4. TMX export/import

**Medium Priority (Quality of Life):**
1. Optional TM/termbase matching (toggle)
2. Find & replace
3. Multiple view modes

**Low Priority (Future):**
1. Advanced grid editing features
2. Full CAT tool duplication features

### Migration Path

**Phase 1: Add Toggle for TM/Termbase Matching**
- Add settings option to enable/disable matching
- Update assistance panel to respect toggle
- Keep code but make it optional

**Phase 2: Simplify Grid Editing**
- Reduce editing capabilities to "minor edits only"
- Remove complex insertion workflows
- Keep view and filtering intact

**Phase 3: Documentation Update**
- Update user guides to reflect companion tool philosophy
- Emphasize integration with CAT tools
- Highlight unique AI-powered features

---

## 🚀 Next Steps / Roadmap

### Immediate (Refocus Implementation)
- [ ] Add toggle switch for TM/termbase matching (Settings → View/Display)
- [ ] Simplify grid editing to allow only minor edits
- [ ] Remove complex match insertion workflows (keep as read-only reference)
- [ ] Update documentation to reflect companion tool philosophy

### Short-term
- [ ] User manual updates (companion tool workflow)
- [ ] Integration guides for memoQ/Trados/CafeTran
- [ ] API key security improvements
- [ ] Performance optimization for large files

### Future Considerations
- [ ] Multi-language UI support
- [ ] Custom model parameter tuning
- [ ] Export to additional formats (Excel, PDF)
- [ ] Enhanced CAT tool integration features

---

## �️ Qt Edition Architecture (v1.0.0)

### Implementation Details

**Main Application File:** `Supervertaler.py` (21,600+ lines)
- Modern PyQt6 application with professional CAT interface
- 14-tab main interface organized into 4 functional groups
- Context-sensitive ribbon with 4 ribbon tabs
- Horizontal splitter layout: Grid (left) | TranslationResultsPanel (right)
- Universal Lookup integration with global hotkey (Ctrl+Alt+L)
- AutoFingers CAT automation with TMX support

**Translation Results Panel:** `modules/translation_results_panel.py` (345 lines)
- **TranslationResultsPanel** - Main widget class
  - Manages stacked match sections
  - Handles match selection and compare box display
  - Compact, memoQ-inspired design
  - Integration point for all match types

- **MatchSection** - Collapsible section for each match type
  - Header with toggle button and match count
  - Scrollable container for multiple matches
  - Emits signals when matches selected

- **CompactMatchItem** - Individual match display
  - Type badge + relevance percentage
  - Target text preview (line-wrapped)
  - Metadata/context display
  - Drag/drop support
  - Click-to-select functionality

- **Supporting Classes:**
  - `TranslationMatch` - Data class for matches
  - Helper methods for compare boxes and diff display

**Integration with Editor Tab:**
- `create_editor_tab()` - Creates horizontal splitter with grid and panel
- `create_assistance_panel()` - Instantiates TranslationResultsPanel
- `on_cell_selected()` - Populates panel when segment selected
- `search_and_display_tm_matches()` - Queries TM and generates matches

### Compact Design Philosophy

The TranslationResultsPanel was designed to minimize wasted space while maximizing usability, following memoQ's principles:

1. **Collapsible Sections** - Hide/show match types as needed
2. **Compact Match Items** - Essential info only (type, %, text preview)
3. **Stacked Layout** - Multiple matches visible without excessive scrolling
4. **Minimal Padding** - 2-4px margins between elements
5. **Smart Typography** - Varied font sizes (8-10pt) for hierarchy
6. **Visual Hierarchy** - Color coding (badges) for quick scanning
7. **Integrated Notes** - No separate panel needed, built into bottom of results

### Database Integration

- **TM Database:** `modules/database_manager.py` (SQLite with FTS5 search)
  - `search_all(source_text, max_matches)` - Returns list of TM matches
  - Each match includes: source, target, match_pct, metadata
  
- **Match Loading:**
  - `on_cell_selected()` calls `tm_database.search_all()`
  - Results transformed to `TranslationMatch` objects
  - Sorted by relevance (100% exact matches first)
  - Limited to 10 matches per type for performance

### Performance Optimizations

- **Lazy Loading:** Matches loaded only when segment selected
- **Scrollable Sections:** Large match sets handled with QScrollArea
- **Signal/Slot:** Minimal UI updates via Qt signals
- **Compact HTML:** Previous diff display also works (fallback)
- **Metadata Trimming:** Context limited to first 40 characters

### Diff Highlighting System

Already implemented in `search_and_display_tm_matches()`:
```python
from difflib import SequenceMatcher

# Green: added text (underline + bold)
# Red: deleted text (strikethrough)
# Handles insertions, deletions, and replacements
```

Ready to integrate into TranslationResultsPanel's compare boxes.

---

## 🔗 Related Files

### Qt Edition (v1.0.0)
- **Main Application:** `Supervertaler.py` (Primary CAT interface, 21,600+ lines)
- **UI Components:**
  - `modules/translation_results_panel.py` - Match display panel (345 lines, NEW)
  - `modules/ribbon_widget.py` - Modern ribbon UI
  - `modules/universal_lookup.py` - Global hotkey search
  - `modules/autofingers_engine.py` - CAT automation
- **Core Functionality:**
  - `modules/database_manager.py` - TM database (SQLite + FTS5)
  - `modules/simple_segmenter.py` - Text segmentation
  - `modules/config_manager.py` - Settings management

### Classic & CAT Editions
- **Main programs:** `Supervertaler_v2.5.0-CLASSIC.py`, `Supervertaler_v3.1.1-beta_CAT.py`
- **Documentation:** `/docs/` folder
- **Chat logs:** `/docs/chat-logs/` folder
- **Development tools:** `/.dev/` folder
- **Core modules:** `/modules/` folder
- **User data:** `/user_data/` (public), `/user_data_private/` (dev only)

---

## 💡 Key Decisions & Rationale

1. **Parallel folder structure over suffix pattern**
   - Cleaner separation of public/private
   - Simpler .gitignore (1 line vs 7)
   - Future-proof for new data types

2. **Batch processing for AI analysis**
   - ~90% faster than segment-by-segment
   - Better consistency (AI sees context)
   - Reduced API costs
   - Configurable via slider for flexibility

3. **Markdown over table format for tracked changes**
   - More readable for translators
   - Handles long text better
   - Better for mobile viewing
   - Easier to share/print

4. **Tracked changes as post-translation tool, not context**
   - Avoids circular context (translator reviewing own changes)
   - Makes purpose clearer (analysis, not translation context)
   - Proper workflow: translate → review changes → iterate

5. **UK English lowercase style**
   - "System prompts" not "System Prompts"
   - Cleaner, more professional appearance
   - Consistent across both versions
   - User preference from initial discussions

---

## 📞 Contact / Maintenance

**Active Development By:** Michael Beijer
**Project Started:** October 2025
**Last Major Update:** November 7, 2025

**Development Workflow:**
1. Develop in workspace folder
2. Export daily chat history
3. Update PROJECT_CONTEXT.md periodically
4. Commit changes to GitHub
5. Reference previous chats as needed for continuity

---

## Recent Updates (November 7, 2025) - v1.2.3

### Status Column UI Improvements
Fixed and enhanced the status column display in Grid view:

**Visual Fixes:**
- Fixed status column background stretching issues when using auto-resize rows
- Removed fixed minimum height from status widgets - now adapts to row height
- Increased minimum row height from 20px to 32px to prevent icon cutoff
- Status widgets now properly center vertically regardless of row height
- Match percentage label only shows when match data exists (eliminates empty gaps)

**Icon Improvements:**
- **Not started**: ❌ (red X, 11px) - matches memoQ style
- **Pre-translated**: 🤖 (robot) - clearer indication of automatic translation
- **Translated**: ✏️ (pencil) - matches Trados style for manual work
- **Confirmed**: ✔ (green checkmark via CSS) - clean, consistent with ❌
- Swapped Translated and Confirmed icons for better semantic meaning
- Improved comment icon: 🗨️ with text-shadow for better visibility

**Interaction Changes:**
- Disabled click-to-change-status on status column (prevents visual glitches)
- Status changes now only via Segment Editor (more intentional workflow)

**Technical Changes:**
- Background color now on table item, widget is transparent (prevents rendering issues)
- Status icon size varies by status: 11px for ❌, 14px for others
- Green color (#2e7d32) applied via CSS to confirmed checkmark
- All changes in `Supervertaler.py` and `modules/statuses.py`

