# Supervertaler - AI Agent Documentation

> **This is the single source of truth for AI coding assistants working on this project.**
> **Last Updated:** December 31, 2025 | **Version:** v1.9.74

---

## 🎯 Project Overview

**Supervertaler** is a professional desktop translation application built with Python and PyQt6. It serves as a companion tool for translators, integrating AI-powered translation with traditional CAT (Computer-Assisted Translation) tool workflows.

| Property | Value |
|----------|-------|
| **Name** | Supervertaler |
| **Version** | v1.9.74 (December 2025) |
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
- `voice_commands.py` - Talon-style voice command system (NEW)
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

## � Future Investigation: TMX Tag Export Format

**Issue discovered December 22, 2025**: Our TMX Editor stores formatting tags (like `<b>`, `<i>`) as escaped text (`&lt;b&gt;`) in the `<seg>` element. This is valid XML but may not be the optimal approach.

**Three approaches exist:**

| Approach | Example in TMX file | Pros | Cons |
|----------|---------------------|------|------|
| **Escaped text** | `<seg>&lt;b&gt;text&lt;/b&gt;</seg>` | Simple, valid XML | Tags treated as plain text, lost semantic meaning |
| **TMX inline elements** | `<seg><bpt i="1" type="bold">&lt;b&gt;</bpt>text<ept i="1">&lt;/b&gt;</ept></seg>` | TMX 1.4 compliant, preserves tag semantics | More complex to implement |
| **Raw XML** (invalid) | `<seg><b>text</b></seg>` | Human readable | Invalid XML unless DTD defines `<b>` |

**What other tools do:**
- **memoQ**: Uses TMX inline elements (`<bpt>`, `<ept>`) for proper tag preservation
- **Trados Studio**: Similar, uses inline elements with type attributes
- **OmegaT**: Generally uses escaped text for simplicity
- **Many web tools**: Just escape everything

**Recommendation for future**: Consider implementing proper TMX inline elements (`<bpt>`, `<ept>`, `<ph>`) when exporting. This would:
1. Maintain compatibility with professional CAT tools
2. Preserve tag type information (bold, italic, etc.)
3. Allow round-tripping without tag loss

**Files to modify**: `modules/tmx_editor.py` - `TmxParser.save_file()` method

---

## �💡 Problem-Solving Tips for AI Agents

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

### December 31, 2025 - Version 1.9.73: External Prompt Editor Display

**📝 External Prompts Now Display in Editor**

When loading an external prompt file (not in the library), it now displays in the Prompt Editor panel:

- **Editor display**: External prompts show in the editor with name, description, and content fields
- **Read/write support**: External prompts can be edited and saved back to the original file
- **Format detection**: `.svprompt` files parsed as JSON to extract name, description, and content
- **Plain text support**: `.txt` and `.md` files displayed as raw content
- **Visual indicator**: Editor label shows "📁 External: {name}" to distinguish from library prompts
- **Save functionality**: Changes can be saved back to external files (JSON for .svprompt, plain text for others)
- **Project load fix**: Prompts stored in project files now display in editor when project is loaded (both external and library prompts)

**Files Modified:**
- `modules/unified_prompt_manager_qt.py` - Added `_display_external_prompt_in_editor()`, `_save_external_prompt()`, updated `_load_external_primary_prompt()`, `_save_current_prompt()`, and `_set_primary_prompt()`
- `Supervertaler.py` - Added call to `_display_external_prompt_in_editor()` in project load code

---

### December 30, 2025 - Version 1.9.67: memoQ Tag Highlighting & Batch Retry Fix

**🏷️ memoQ Content Tag Highlighting**

Fixed and improved tag highlighting for memoQ bilingual DOCX files:

- **Mixed bracket tags now highlighted**: `[uicontrol id="..."}`, `{uicontrol]`, `[image cid="..." href="..."]`
- **Closing tags**: `{tagname}` like `{MQ}`, `{tspan}` now properly pink
- **No false positives**: `[Company]`, `[Bedrijf]` placeholders stay black (only tags with attributes or mixed brackets highlighted)
- **Regex patterns fixed**: Patterns now exclude unwanted characters to prevent greedy matching across multiple tags

**Final Tag Patterns:**
```python
r'\[[^}\]]+\}'        # memoQ mixed: [anything}
r'\{[^\[\]]+\]'       # memoQ mixed: {anything]
r'\[[a-zA-Z][^}\]]*\s[^}\]]*\]'  # memoQ content: [tag attr...]
r'\{[a-zA-Z][a-zA-Z0-9_-]*\}'    # memoQ closing: {tagname}
```

**🔄 Batch Translate Retry Fix**

Fixed `UnboundLocalError: cannot access local variable 'provider_dialog'` when retry pass starts:

- **Root Cause**: Retry passes skipped the dialog but code still tried to use dialog variables
- **Fix**: Properly wrapped entire dialog section in `if not is_retry_pass:` block (~200 lines)
- **Retry passes**: Now correctly use stored settings and skip directly to progress dialog

**📄 Pagination After Clear Filters**

Fixed pagination resetting when clearing filters:

- **Previously**: Clear Filters showed ALL segments, ignoring per-page setting
- **Now**: After clearing filters, `_apply_pagination_to_grid()` is called to maintain pagination

**🎨 Tag Color Setting Visibility**

Improved discoverability of tag color setting:

- **Group renamed**: "Translation Results Pane Font Size" → "Translation Results Pane & Tag Colors"
- **Tooltip updated**: Now explains the color applies to "CAT tool tags in the grid and results pane"

**Files Modified:**
- `Supervertaler.py` - TagHighlighter patterns, batch translate retry logic, clear_filters pagination, view settings labels

---

### December 30, 2025 - Version 1.9.68: memoQ Tag Color as Default

**🎨 Default Tag Color Changed to memoQ Dark Red**

Changed the default tag highlight color from light pink (`#FFB6C1`) to memoQ's actual dark red (`#7f0001`):

- **Color picked from memoQ**: The exact color memoQ uses for inline tags (`#7f0001` / RGB 127,0,1)
- **Updated everywhere**: Grid cells, Translation Results panel, Settings defaults
- **Preset colors**: Added 8 preset colors to the color picker (memoQ red, memoQ orange, Trados blue/purple, etc.)
- **Reset button**: Now resets to memoQ red with updated tooltip

**Tag Color Behavior:**
- **memoQ exports**: Preserve original memoQ colors from source file ✅
- **Trados exports**: Preserve original Trados colors from source file ✅
- **Phrase exports**: Preserve original Phrase colors from source file ✅
- **CafeTran exports**: Preserve original CafeTran colors from source file ✅
- **Supervertaler Bilingual Table**: Uses memoQ red (`RGBColor(127, 0, 1)`) ✅

**Files Modified:**
- `Supervertaler.py` - Default tag colors, preset colors, reset button, bilingual table export
- `modules/translation_results_panel.py` - Default tag color

---

### December 30, 2025 - Version 1.9.69: Page Up/Down Pagination Navigation

**📄 Page Up/Down Shortcuts for Pagination**

Added Page Up and Page Down keyboard shortcuts for navigating through pagination pages:

- **Page Up**: Go to previous page in pagination
- **Page Down**: Go to next page in pagination
- **Added to Settings**: Shortcuts now appear in Settings → Keyboard Shortcuts under "Grid Navigation" category

**Files Modified:**
- `Supervertaler.py` - Added `shortcut_page_up` and `shortcut_page_down` QShortcuts
- `modules/shortcut_manager.py` - Added `page_prev` and `page_next` shortcut definitions

---

### December 30, 2025 - Version 1.9.71: Go to Segment Dialog (Ctrl+G)

**⌨️ Improved Go to Segment Dialog**

Enhanced the Go to Segment feature with a streamlined dialog:

- **Global shortcut**: Ctrl+G now works from anywhere in the application (added as QShortcut)
- **Minimal dialog**: Small, focused dialog with just a text field
- **Type and Enter**: Just type the segment number and press Enter - no need to click buttons
- **Input validation**: Only accepts valid segment numbers within range
- **Shows current position**: Placeholder shows current segment number
- **Pagination-aware**: Automatically switches to the correct page when jumping to segments on other pages
- **Cursor placement**: Target cell is focused and cursor placed at end, ready to edit
- **Shortcut conflict fix**: Removed duplicate Ctrl+G assignment (was on both QShortcut and menu action)

**Already in Settings**: The shortcut was already listed in Settings → Keyboard Shortcuts under "Edit" category

**Files Modified:**
- `Supervertaler.py` - Added `shortcut_goto` QShortcut, redesigned `show_goto_dialog()` with pagination support, cursor focus, removed duplicate shortcut

---

### December 30, 2025 - Version 1.9.67: memoQ Tag Highlighting & Batch Retry Fix

**📚 Documentation Consolidation**

Merged two separate guides into a single comprehensive manual:

- **Previous**: `QUICK_START.md` + `CAT_WORKFLOW.md` (separate files)
- **Now**: `MANUAL.md` - Supervertaler Manual (consolidated into online Superdocs)
- **Contents**: Installation, API setup, CAT tool workflows (memoQ, Trados, CafeTran, Phrase), keyboard shortcuts, formatting, troubleshooting
- **Location**: `docs/guides/MANUAL.md` (archived); primary docs now hosted at https://supervertaler.gitbook.io/superdocs/

**⬆️⬇️ memoQ-Style Arrow Key Navigation**

Implemented intuitive segment navigation using Up/Down arrow keys:

- **Up Arrow at top line**: Moves to previous segment, positions cursor at last line
- **Down Arrow at bottom line**: Moves to next segment, positions cursor at first line
- **Cursor column preserved**: When moving between segments, cursor stays at same column position (or end of line if shorter)
- **Works in both Source and Target cells**: Navigation works whether you're in the read-only source cell or editable target cell
- **Normal behavior within cell**: Arrow keys work normally when cursor is NOT at first/last line

**New Methods in `EditableGridTextEditor`:**
- `_position_cursor_at_end_of_segment()` - Position cursor at last line of cell
- `_position_cursor_at_start_of_segment()` - Position cursor at first line of cell

**Also Added to `ReadOnlyGridTextEditor`:**
- Same Up/Down arrow key navigation
- Tab key now cycles to target cell (column 3)

**🔢 Grammar Fix**

Fixed "Batch Translate 1 Segments" → "Batch Translate 1 Segment" (proper singular/plural)

**Files Modified:**
- `Supervertaler.py` - Arrow key navigation in both editor classes, grammar fix
- `docs/guides/MANUAL.md` - New consolidated manual (now archived; primary docs live in Superdocs)
- Deleted: `docs/guides/QUICK_START.md`, `docs/guides/CAT_WORKFLOW.md`

---

### December 29, 2025 - Version 1.9.64: Grid Pagination & Batch Translate Retry

**📄 Working Grid Pagination**

The pagination controls now actually filter the displayed segments:

- **Previously**: Pagination UI existed but all segments were always shown
- **Now**: When you select "50 per page", only 50 segments are displayed at a time
- **Navigation**: First/Prev/Next/Last buttons or type a page number
- **Efficient**: Uses show/hide rows approach without reloading the grid

**New Pagination Methods:**
- `_get_total_pages()` - Calculate total pages based on segments and page size
- `_update_pagination_ui()` - Update labels and enable/disable buttons
- `_apply_pagination_to_grid()` - Show/hide rows for current page
- Updated `go_to_first_page()`, `go_to_prev_page()`, `go_to_next_page()`, `go_to_last_page()`, `go_to_page()`, `on_page_size_changed()`

**🔄 Batch Translate Retry Until Complete**

New option to automatically retry translating empty segments:

- **Checkbox**: "🔄 Retry until all segments are translated (recommended)" in batch translate dialog
- **Default**: Enabled by default
- **Behavior**: After first pass completes, checks for segments that are still empty. If any found, automatically starts another pass with just those segments.
- **Max Retries**: 5 passes maximum to prevent infinite loops
- **LLM Only**: Only works with LLM provider (not TM or MT modes)

**Instance Variables for Retry:**
- `_batch_retry_enabled` - Whether retry is enabled
- `_batch_retry_pass` - Current retry pass number (0 = first pass)
- `_batch_provider_type`, `_batch_provider_name`, `_batch_model` - Stored settings for retry passes

**🤖 Prompt Manager Tab Rename**

- "Prompts" tab renamed to "Prompt manager" in Project resources

**📁 External Prompt Restoration Fix**

Fixed external prompts not being restored when loading a project:

- External prompts are saved with `[EXTERNAL] /path/to/file.svprompt` prefix
- On load, detects `[EXTERNAL]` prefix and calls `library.set_external_primary_prompt()`
- Updates UI label with 📁 icon and prompt name
- Shows warning if external file no longer exists

**Files Modified:**
- `Supervertaler.py` - Pagination methods, batch translate retry, prompt restoration, tab rename
- `modules/unified_prompt_library.py` - (no changes, existing method used)

---

### December 30, 2025 - Version 1.9.66: Performance Boost & Cache Fix

**⚡ Termbase Cache Fix**

Fixed critical bug where termbase cache wasn't working - same segments were being re-searched repeatedly:

- **Root Cause**: Cache check was looking at whether `stored_matches` was empty, not whether the segment was in the cache. Empty results (`{}`) were never cached, causing repeated slow searches for segments with no termbase matches.

- **Fix**: Changed to proper membership check using `segment_id in self.termbase_cache`:
  - Uses `cache_checked` boolean flag to track if cache was consulted
  - Stores results in cache EVEN IF EMPTY so segments without matches are remembered
  - Removed duplicate cache-checking code blocks

**🔇 Reduced Logging Overhead**

Removed verbose logging that was contributing to navigation slowness:

- Removed per-word termbase search logging (was logging each of 50+ words per segment)
- Removed per-match termbase result logging
- Removed prefetch worker progress logging (every 10 segments)
- Removed MT/LLM scheduling/execution debug logging
- Removed TM search debug logging (project ID, activated TMs, match counts)
- Removed termbase highlighting debug logging
- Kept only error logs and essential status messages

**Result**: Navigation between segments should feel significantly faster, especially for segments with no termbase matches (which were being re-searched every time).

**Files Modified:**
- `Supervertaler.py` - Cache logic fix (~lines 24260-24290), removed verbose logging throughout

---

### December 29, 2025 - Version 1.9.63: Linux Memory Access Violation Fix

**🐧 Linux Stability Improvements**

Fixed memory access violations (segfaults) that could occur on Linux when clicking in the grid after importing a Trados package:

**Root Cause**: Native code libraries (Hunspell spellcheck, ChromaDB, Sentence-Transformers) can crash with segfaults on Linux, especially when:
- Hunspell dictionaries are not properly installed for the target language
- ChromaDB's Rust backend has thread safety issues
- Tokenizers library uses parallel processing

**Fixes Applied:**

1. **Safer Hunspell Initialization** (`modules/spellcheck_manager.py`):
   - Added test spell check call during initialization to catch crashes early
   - Added `_crash_detected` flag to disable spellcheck permanently if it crashes
   - If spellcheck crashes mid-session, it's automatically disabled

2. **Protected Spellcheck Highlighting** (`Supervertaler.py`):
   - Added safety checks in `TagHighlighter._highlight_misspelled_words()`
   - Wrapped spellcheck loop in try/except to catch any errors
   - If errors occur, spellcheck is disabled for the session

3. **Skip AutoHotkey on Linux/Mac** (`Supervertaler.py`):
   - AutoHotkey registration now skipped entirely on non-Windows platforms
   - No more "AutoHotkey not found" warnings on Linux/Mac
   - Settings and menu items already hidden via `os.name == 'nt'` checks

**User Guidance for Linux:**
- If crashes persist, disable spellcheck in Settings → View Settings
- Ensure Hunspell dictionaries are installed: `sudo apt install hunspell-pl` (for Polish)
- Disable Supermemory auto-init if using ChromaDB causes issues

**Files Modified:**
- `modules/spellcheck_manager.py` - `_try_hunspell()`, `check_word()`, added `_crash_detected` flag
- `Supervertaler.py` - `_highlight_misspelled_words()`, `main()` Linux env vars

---

### December 22, 2025 - Version 1.9.61: DOCX Export Tag Fix & TagHighlighter Accuracy

**📄 DOCX Export List Tag Stripping**

Fixed `<li-o>` and `<li-b>` tags appearing in exported Word documents:

- Added `re.sub(r'</?li-[ob]>', '', text)` to both `_replace_paragraph_text()` and `_replace_paragraph_with_formatting()` in docx_handler.py
- These list item tags are now stripped during DOCX export, not passed through to the document

**Files Modified:**
- `modules/docx_handler.py` - `_replace_paragraph_text()`, `_replace_paragraph_with_formatting()`

**🎨 TagHighlighter - Fixed False Positives for Bracket Text**

Fixed `[Bedrijf]`, `[Company]` and other square-bracketed placeholder text being incorrectly highlighted in pink (tag color):

- **Root Cause**: The TagHighlighter patterns were too broad:
  - `r'\[[a-zA-Z][^}\]]*\]'` matched ANY `[text]` starting with a letter
  - `r'\{[a-zA-Z][^}\]]*\}'` matched ANY `{text}` starting with a letter
  
- **Fix**: Removed these overly broad patterns. Now only highlights:
  - HTML/XML tags: `<tag>`, `</tag>`, `<tag/>`
  - Trados numeric: `<1>`, `</1>`
  - memoQ numeric: `[1}`, `{1]`, `[1]`, `{1}` (numbers only, not arbitrary text)

- **Result**: `[Bedrijf]`, `[Company]`, `{placeholder}` etc. are no longer colored pink - only actual CAT tool tags get highlighted

**Files Modified:**
- `Supervertaler.py` - `TagHighlighter.highlightBlock()` - removed overly broad bracket patterns

---

### December 23, 2025 - Version 1.9.62: Dead Code Cleanup & Code Quality

**🧹 Dead Code Removal (~230+ lines)**

Removed deprecated and unused methods from the codebase:

- `toggle_sidebar()` - Quick Access sidebar removed long ago
- `update_sidebar_recent_files()` - Quick Access sidebar removed
- `handle_ribbon_action()` - Ribbon UI removed, replaced by menu bar
- `create_toolbar()` - Toolbar removed, replaced by ribbon (then menu)
- `_create_llm_settings_tab()` - Deprecated redirect, never called
- `_render_paragraph()` - Explicitly marked "no longer used"
- `_handle_target_text_debounced()` - Superseded by `_by_id` version
- `update_for_segment()` (termview) - Deprecated, use `update_with_matches()`
- `tokenize_source()` (termview) - Deprecated, use `tokenize_with_multiword_terms()`

**📋 Project Dataclass Cleanup**

- Added missing `spellcheck_settings: Dict[str, Any]` field to Project dataclass
- Added initialization in `__post_init__`
- Removed unnecessary `hasattr()` checks throughout codebase (fields now properly declared)

**🔇 Debug Logging Cleanup**

- Removed verbose TERMVIEW debug print statements from `termview_widget.py`
- Removed "💾💾💾 FINAL DEBUG" logging from project save
- Removed excessive "🔍 TERMVIEW:" log messages from main app

**🤖 AutoFingers UI Simplification**

- Removed unnecessary QTabWidget wrapper (was single tab "🎮 Control Panel")
- Control panel now displays directly without tab overhead

**Files Modified:**
- `Supervertaler.py` - Removed deprecated methods, added dataclass field, cleaned debug logs
- `modules/termview_widget.py` - Removed deprecated methods and debug prints

---

### December 22, 2025 - Version 1.9.60: Tag-Aware TM Matching & AutoFingers Cleanup

**🔍 Tag-Aware TM Matching**

Translation Memory fuzzy matching now works regardless of whether segments contain formatting tags:

- **Dual Search Strategy**: Searches both with original text (including tags) AND with tags stripped
  - `<b><u>Technisch mankement</u></b>` generates search terms: `['Technisch', 'mankement']`
  - Also includes any tag-derived terms (in case TM was indexed with tags)
  - Single FTS query with combined terms - negligible performance impact

- **Tag-Stripped Similarity Calculation**: `calculate_similarity()` now strips HTML/XML tags before comparing
  - `<b>Hello</b>` vs `Hello` now gives 100% match instead of ~70%
  - More accurate fuzzy match percentages

- **Benefits**:
  - TMs imported with tags now match segments without tags (and vice versa)
  - Similarity scores based on actual text content, not tag presence
  - Debug output shows combined search terms

**Files Modified:**
- `modules/database_manager.py` - `search_fuzzy_matches()` dual search, `calculate_similarity()` tag stripping

**🧹 TMX Tag Cleaner - Additional Tags**

- Added `<li-b></li-b>` (bullet list item) and `<li-o></li-o>` (ordered list item) tags to Formatting category
- Both enabled by default

**Files Modified:**
- `modules/tmx_editor_qt.py` - Added list item tags to `DEFAULT_TAG_PATTERNS`

**🤖 AutoFingers Cleanup**

- Removed TMX Manager tab (unused features)
- Added "📥 Import from TM" button to Control Panel's TMX File group
- Simplified TMX status display: now shows "✓ X TUs loaded" instead of verbose multi-line stats
- Removed unused `create_tmx_tab()` method

**Files Modified:**
- `Supervertaler.py` - AutoFingers UI cleanup, removed tab, added button

---

### December 22, 2025 - Version 1.9.59: TMX Tag Cleaner & UX Improvements

**🧹 TMX Tag Cleaner - Complete Implementation**

Tag cleaning functionality in both TMX Editor and main application:

- **TMX Editor Access**: 
  - Toolbar button: "🧹 Clean Tags"
  - Edit menu: Edit → Bulk Operations → 🧹 Clean Tags...
  - Tools menu: Tools → 🧹 Clean Tags...

- **Main App Access**:
  - Edit menu: Edit → Bulk Operations → 🧹 Clean Tags...
  - Cleans tags from currently loaded project segments

- **Tag Selection Dialog**:
  - User can select/deselect individual tag patterns to clean
  - Tags grouped by category: Formatting, TMX/XLIFF, memoQ, Trados, Generic
  - Quick select buttons: "Select All", "Select None", "Select Formatting Only"
  
- **Supported Tag Types**:
  - **Formatting**: `<b>`, `<i>`, `<u>`, `<bi>`, `<sub>`, `<sup>`
  - **TMX/XLIFF**: `<bpt>`, `<ept>`, `<ph>`, `<it>`, `<hi>`, `<ut>`
  - **memoQ**: `{1}`, `[2}`, `{3]` index tags
  - **Trados**: `<1>`, `</1>` numbered tags, `{1}`, `{/1}` curly tags
  - **Generic**: All XML-style tags

- **Replacement Options**:
  - Remove tags completely (no replacement)
  - Replace tags with a space

- **Scope Options**:
  - Clean both source and target segments
  - Clean source segments only
  - Clean target segments only

- **Implementation**:
  - Works in both RAM mode and database mode
  - Progress dialog with cancel option
  - Shows statistics on completion (TUs modified, tags removed)
  - Automatically refreshes grid after cleaning

**New Class:**
- `TmxTagCleanerDialog` - Configuration dialog with checkboxes for each tag pattern

**Files Modified:**
- `modules/tmx_editor_qt.py` - Added `TmxTagCleanerDialog`, `show_clean_tags_dialog()`, `clean_tags()`, toolbar button, menu items

---

### December 22, 2025 - Version 1.9.57: Flattened Tab Structure

**🏠 Simplified Main Navigation**

Reorganized the main tab structure from nested to flat hierarchy:

- **Before**: Workspace (containing Editor + Resources subtabs) → Tools → Settings
- **After**: Project editor → Project resources → Tools → Settings

**Changes Made:**
- Removed nested `project_home_tabs` QTabWidget
- Grid widget now added directly to `main_tabs` as "📝 Project editor"
- Resources tab added directly to `main_tabs` as "🗂️ Project resources"
- Updated all tab index references throughout codebase (Tools is now index 2, Settings is now index 3)
- Updated View → Navigate To menu items
- Updated keyboard shortcut action mappings
- Updated all navigation methods: `_go_to_superlookup()`, `_open_superdocs_tab()`, `show_autofingers()`, `show_image_extractor_from_tools()`, `_open_mt_settings()`, `_navigate_to_termbase_entry()`

**Capitalization Style:**
- Tab names use lowercase for subtabs: "Project editor", "Project resources" (NOT "Project Editor", "Project Resources")
- Tools and Settings remain capitalized as they are top-level concepts

**Files Modified:**
- `Supervertaler.py` - `create_main_layout()`, navigation menu, shortcut actions, all navigation methods

---

### December 22, 2025 - Version 1.9.56: Glossary Renaming Feature

**✏️ Glossary Renaming via Right-Click**

Fixed the glossary (termbase) renaming functionality:

- **Problem**: Editing the glossary name directly in the table appeared to work but changes were never saved to the database
- **Root Cause**: `QTableWidgetItem` in the Name column was editable by default, but no handler saved the edited value
- **Solution Implemented**:
  - Added right-click context menu to glossary table with "✏️ Rename Glossary" and "🗑️ Delete Glossary" options
  - New `rename_termbase()` method in `TermbaseManager` class updates the name in the database
  - New `_show_termbase_context_menu()` method shows context menu at right-click position
  - New `_rename_termbase_dialog()` method shows QInputDialog for entering new name
  - Disabled inline editing with `setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)`

**Files Modified:**
- `modules/termbase_manager.py` - Added `rename_termbase()` method
- `Supervertaler.py` - Added context menu, rename dialog, disabled inline editing

---

### December 22, 2025 - Version 1.9.54: Superlookup UX Improvements & Terminology Rename

**🔍 Superlookup Enhancements**

Several usability fixes for the Superlookup unified lookup window:

- **Enter Key Behavior**: Pressing Enter in search box now triggers search (Shift+Enter for newline)
- **Edit in Glossary Navigation**: Right-click "Edit in Glossary" now correctly selects the glossary in the Resources tab
- **Fuzzy Search Filter**: Minimum term length filter prevents single-letter terms from matching long search queries (e.g., "A" no longer matches "Machine Fingerprint")
- **TM Source Column**: Added new "TM" column to TM results showing which Translation Memory the match came from

**📝 User-Facing Terminology Rename: Termbase → Glossary**

Comprehensive rename of user-facing terminology throughout the application:

- **Tab Names**: "Termbase Matches" → "Glossaries", "TM Matches" → "TMs"
- **Dialog Titles**: "Create New Termbase" → "Create New Glossary", "Import Termbase" → "Import Glossary"
- **Settings Labels**: "TM/Termbase lookup delay" → "TM/Glossary lookup delay", "Termbase Highlight Style" → "Glossary Highlight Style"
- **Button Text**: "Add to Termbase" → "Add to Glossary", "TM/Termbase ON" → "TM/Glossary ON"
- **Tooltips**: All termbase-related tooltips updated to use "glossary"
- **Context Menus**: "Add to Termbase" → "Add to Glossary", "Edit in Termbase" → "Edit in Glossary"
- **Warning Messages**: All QMessageBox dialogs updated to use "glossary" terminology
- **Checkboxes**: "Enable TM & Termbase Matching" → "Enable TM & Glossary Matching"

**Technical Notes:**
- Internal code (variable names, method names, database columns) remains unchanged for backward compatibility
- Only user-visible strings were modified
- Project files (.svproj) still use `termbase_settings` key for compatibility

**Files Modified:**
- `Supervertaler.py` - Comprehensive UI string updates throughout

---

### December 21, 2025 - Version 1.9.55: Lightning-Fast Filtering

**⚡ Optimized Filter Performance**

Major performance optimization for filter operations (Ctrl+Shift+F):

- **Before**: ~12 seconds to apply or clear a filter
- **After**: Instant (typically <200ms)

**Root Cause**: Filter operations were calling `load_segments_to_grid()` which recreates all QTextEdit widgets for every segment. With 500+ segments, this took ~12 seconds.

**Solution Implemented**:
- `apply_filters()` now uses `setUpdatesEnabled(False)` to batch UI changes, only shows/hides rows and applies yellow highlights without recreating widgets
- `clear_filters()` now clears only yellow filter highlights (preserves termbase/tag formatting) and unhides rows in place
- New `_clear_filter_highlights_in_widget()` method surgically removes only yellow (#FFFF00) highlights while preserving green termbase highlights and pink tag colors

**🔄 Ctrl+Shift+F Toggle Behavior**

The filter shortcut now works as a true toggle:
- **First press** (with text selected): Filters on selected text
- **Second press** (with filter active): Clears the filter immediately

**📋 Keyboard Shortcuts Update**

Added "Clear filter" entry in keyboard shortcuts (same Ctrl+Shift+F shortcut) for discoverability. Updated shortcut description to reflect toggle behavior.

**Files Modified:**
- `Supervertaler.py` - `apply_filters()`, `clear_filters()`, `_highlight_text_in_widget()`, `_clear_filter_highlights_in_widget()` (new), `filter_on_selected_text()`
- `modules/shortcut_manager.py` - Added `clear_filter` shortcut entry, updated descriptions

---

### December 21, 2025 - Version 1.9.53: Superlookup Termbase Enhancements

**📋 Improved Termbase Matches Tab**

Enhanced the Superlookup Termbase Matches tab with additional metadata columns:

- **Renamed Column Headers**: "Term (Source)" → "Source", "Translation (Target)" → "Target"
- **New Columns Added**: Termbase (source name), Domain, Notes
- **Full Metadata in Results**: Each termbase match now includes domain, notes, priority, project, client, forbidden status
- **Tooltips**: Hover over cells to see full content (especially useful for long notes)

**📥 Termbase Import Progress Dialog**

New real-time progress dialog when importing termbases from TSV files:

- **Visual Progress Bar**: Shows percentage and entry count (e.g., "245/500 (49%)")
- **Live Statistics**: Running counters for imported (✅), skipped (⏭️), and errors (❌)
- **Scrolling Log Window**: Dark-themed console showing each entry as it's processed
  - ✅ Imported: source → target
  - ⏭️ Skipped duplicate: source
  - 🔄 Updated: source → target (when update mode selected)
  - ❌ Line X: error message
- **Auto-Refresh**: Termbase table automatically updates term counts after import

**Files Modified:**
- `Supervertaler.py` - `create_termbase_results_tab()`, `display_termbase_results()`, `search_termbases()`, `_import_termbase()`, `_refresh_termbase_table()`
- `modules/termbase_import_export.py` - `import_tsv()` now accepts `progress_callback` parameter

---

### December 20, 2025 - Version 1.9.52: Superlookup Web Resources

**🌐 Expanded Web Resources Tab**

Complete overhaul of the Superlookup Web Resources tab with 14 reference sites and persistent sessions:

- **New Web Resources (6 added)**:
  - Juremy (ISO 639-3 language codes)
  - michaelbeijer.co.uk (translator's personal site)
  - AcronymFinder (uppercase language codes)
  - BabelNet (multilingual knowledge graph)
  - Wiktionary Source & Target (separate dictionary for each language)

- **Persistent Login Sessions**:
  - QWebEngineProfile with `ForcePersistentCookies` policy
  - Cookies stored in `user_data/web_cache/`
  - Stay logged in to ProZ, Linguee, IATE, etc.

- **Auto Language Selection**:
  - `set_project_languages()` method sets Superlookup dropdowns from project
  - Called automatically on project load
  - Language pair auto-fills when opening Superlookup

- **Compact UI Layout**:
  - Single-line search bar with direction controls
  - "Search" label replaced with 🔍 icon
  - Simplified direction labels: "Both", "Source", "Target"
  - Settings checkboxes control sidebar button visibility

- **Language Code Formats**:
  - iso2, iso3, iso639_3, full_lower, iso2_upper
  - `_get_web_lang_code()` handles all format conversions
  - `_build_web_search_url()` with sl_upper/tl_upper placeholders

**Files Modified:**
- `Supervertaler.py` - Web resources tab, language handling, persistent profile, UI layout

---

### December 20, 2025 - Version 1.9.51: Superlookup MT Integration

**🔍 Complete Machine Translation in Superlookup**

Full MT integration with multiple providers and improved error handling:

- **MT Provider Status Display**: New compact status panel in Machine Translation tab
  - Shows active providers (✅), disabled providers (⏸️), and missing API keys (❌)
  - "⚙️ Configure in Settings" link navigates directly to Settings → MT Settings

- **All MT Providers Now Working**:
  - Google Translate, Amazon Translate, DeepL, Microsoft Translator, ModernMT, MyMemory
  - Error messages now displayed in red with full details (no more silent failures)
  - Successful translations shown in blue with copy button

- **Language Name Mapping Fix**: Critical fix for all MT providers
  - App stores languages as full names ("Dutch", "English")
  - MT APIs require ISO codes ("nl", "en")
  - Added `lang_name_to_code` mapping dictionary to Google Translate, Amazon Translate, MyMemory
  - Supports 24+ languages including European, Asian, and Middle Eastern

- **Dependencies**: Added `boto3` and `deepl` to requirements.txt

- **Termbases Tab Improvements**:
  - Search filter now functional (filters termbase list as you type)
  - New split-view with editable terms grid on right side
  - All term columns visible: Source, Target, Priority, Domain, Notes, Project, Client, Forbidden

- **Cleanup**:
  - Removed debug print spam (ROW COLOR DEBUG messages)
  - Removed redundant MT sub-tab from Superlookup Settings (MT config now in main Settings → MT Settings)

**Files Modified:**
- `Supervertaler.py` - MT provider calls, language mapping, Superlookup MT tab, Termbases split view
- `requirements.txt` - Added boto3, deepl

---

### December 18, 2025 - Version 1.9.50: Voice Commands Complete

**🎤 Voice Commands System - Final Polish**

Complete hands-free translation system with all features working:

- **OpenAI Whisper API Integration**: Added dual recognition engine support
  - OpenAI Whisper API (recommended): Fast, accurate, works great for short voice commands
  - Local Whisper model (fallback): Works offline but less accurate for short clips
  - Recognition engine dropdown in Supervoice settings

- **Grid Toolbar Button**: New 🎧 Voice ON/OFF toggle button in the grid toolbar
  - Shows current state: 🎧 Voice ON (green), 🔴 REC (red), ⏳ Processing (orange)
  - Click to toggle always-on listening without going to settings

- **Status Bar Indicator**: Always-on indicator in status bar (bottom-right)
  - 🎤 VOICE ON / 🔴 REC / ⏳ ... 
  - Clickable to toggle on/off

- **Bug Fixes**:
  - Fixed `copy_source_to_grid_target()` not working - was using wrong column (1 instead of 3) and wrong method (`table.item()` instead of `table.cellWidget()`)
  - Fixed `clear_grid_target()` same issue
  - Fixed `get_api_key()` AttributeError - changed to `load_api_keys()` which returns dict

**Files Modified:**
- `Supervertaler.py` - Grid toolbar button, status bar indicator, API key loading fix, copy/clear target fixes
- `modules/voice_commands.py` - OpenAI Whisper API transcription path

---

### December 18, 2025 - Version 1.9.49: Always-On Voice Listening

**🎧 Always-On Listening Mode**

New VAD-based (Voice Activity Detection) continuous listening mode that eliminates the need to press F9 twice:

- **How it works:**
  1. Continuously monitors microphone audio levels
  2. When speech detected (RMS above threshold) → starts recording
  3. When silence detected (0.8s of quiet) → stops and transcribes
  4. Processes result as command or dictation
  5. Repeats automatically

- **Settings UI:** Settings → 🎤 Supervoice → "🎧 Always-On Listening Mode" section:
  - Start/Stop toggle button with status indicator
  - Visual feedback: 🟢 Listening → 🔴 Recording → ⏳ Processing
  - Microphone sensitivity: Low/Medium/High (for different environments)

- **F9 Behavior Update:**
  - If always-on is active: F9 stops it
  - If always-on is inactive: F9 works as push-to-talk (original behavior)

- **Technical Details:**
  - VAD uses amplitude-based speech detection (RMS threshold)
  - Minimum speech duration: 0.3s (ignores short sounds)
  - Maximum recording: 15s (prevents runaway recordings)
  - Silence timeout: 0.8s (adjustable via sensitivity)
  - Model loaded once, cached for fast subsequent transcriptions

**Classes Added/Modified:**
- `ContinuousVoiceListener` - Complete rewrite with VAD
- `_VADListenerThread` - New background thread with proper VAD loop
- Settings persistence for sensitivity level

**Files Modified:**
- `modules/voice_commands.py` - ContinuousVoiceListener, _VADListenerThread
- `Supervertaler.py` - Import, initialization, toggle function, UI, signal handlers

---

### December 18, 2025 - Version 1.9.48: Voice Commands System (Talon-style)

**🎤 Voice Command System**

New Talon-style voice command system that lets users control Supervertaler and other applications by voice:

- **3-Tier Architecture:**
  - **Tier 1: Internal Commands** - Control Supervertaler (confirm segment, navigate, translate, etc.)
  - **Tier 2: System Commands** - AutoHotkey integration for controlling other apps (memoQ, Trados, Word)
  - **Tier 3: Dictation Fallback** - If no command matches, insert as text

- **Built-in Commands:**
  - Navigation: "next segment", "previous", "first segment", "last segment"
  - Editing: "confirm", "copy source", "clear target", "undo", "redo"
  - Translation: "translate", "translate all"
  - Lookup: "lookup", "concordance"
  - memoQ: "glossary" (Alt+Down), "tag next" (multi-key sequence)
  - Trados: "confirm trados" (Ctrl+Enter)

- **Settings UI:** Settings → 🎤 Supervoice tab now includes:
  - Enable/disable voice commands toggle
  - Voice commands table with all phrases, aliases, actions
  - Add/Edit/Remove custom commands
  - Reset to defaults button
  - AutoHotkey status indicator

- **Custom Command Support:**
  - Phrase + aliases (fuzzy matching)
  - Action types: internal, keystroke, AHK inline code, AHK script file
  - Categories for organization
  - User commands stored in `user_data/voice_commands.json`

**New Files:**
- `modules/voice_commands.py` - VoiceCommandManager, VoiceCommand dataclass, fuzzy matching
- `voice_commands.ahk` - AutoHotkey v2 bridge script for system-level automation
- `user_data/voice_commands.json` - User command library (auto-created)

**Files Modified:**
- `Supervertaler.py` - Added VoiceCommandManager, VoiceCommandEditDialog, enhanced Supervoice settings

---

### December 18, 2025 - Version 1.9.46: Workspace UI Redesign

**🏠 New Tab Hierarchy**

Cleaner, more intuitive tab structure:

- **Main tabs**: 🏠 Workspace → 🛠️ Tools → ⚙️ Settings
- **Workspace subtabs**: 📝 Editor (the grid) + 🗂️ Resources (TM, Termbases, Prompts, etc.)
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
*Last updated: December 30, 2025 - v1.9.71*
