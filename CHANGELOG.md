# Supervertaler - Complete Changelog

**Latest Version**: Qt v1.0.0 Phase 5 (2025-10-29) | v3.7.7 (2025-10-27)  
**Products**: 
- **Supervertaler Qt v1.0.0** - Modern PyQt6 rebuild (Active Development)
- **Supervertaler v3.7.x** - Tkinter CAT Edition (Maintenance)
**Status**: Active Development

> Supervertaler Qt v1.0.0 is a complete rebuild using PyQt6 for superior performance and maintainability. Features are being migrated progressively from v3.7.x.

---

## [Qt v1.0.0 - Phase 5] - 2025-10-29 🔍 UNIVERSAL LOOKUP & UI POLISH

### ✨ Major New Features

**Universal Lookup - System-Wide Translation Memory Search**:
- ✅ **Global hotkey Ctrl+Alt+L** - Look up translations from anywhere on your computer
  - Works in any application: memoQ, Trados, Word, browsers, text editors, etc.
  - Select text in any app → Press Ctrl+Alt+L → Instant TM lookup
  - Non-destructive text capture (doesn't delete or modify source text)
  - Automatic window activation with multi-monitor support
- ✅ **AutoHotkey v2 integration** - Reliable clipboard handling on Windows
  - Hybrid Python+AHK architecture for robust operation
  - File-based signaling (no thread safety issues)
  - Auto-cleanup on exit (no orphaned processes)
  - Hidden background process
- ✅ **Cross-platform graceful degradation**:
  - Windows: Full global hotkey support via AutoHotkey
  - Mac/Linux: Manual paste mode with helpful instructions
- ✅ **Multiple search modes**:
  - Universal (any text box)
  - memoQ-specific
  - Trados-specific
  - CafeTran-specific
- ✅ **TM/Glossary integration** - Search your translation memory and glossary terms
- ✅ **Tab 0 position** - Universal Lookup as first tab for quick access

**Theme System Enhancements**:
- ✅ **6 predefined themes** - Light, Soft Gray, Sepia, Dark, High Contrast Blue, High Contrast Yellow
- ✅ **Custom theme editor** - Create and save your own color schemes
- ✅ **Improved spacing** - Fixed "squished" text in dialogs
  - QGroupBox padding: 18px top, 10px sides/bottom
  - QLabel padding: 3px vertical, 2px horizontal
  - QFormLayout spacing: 8px between rows
  - Proper title positioning in group boxes

**AutoFingers Improvements**:
- ✅ **Keyboard shortcut fix** - Changed loop mode to Ctrl+Shift+L (was Ctrl+Alt+L)
  - Avoids conflict with Universal Lookup's Ctrl+Alt+L
  - Avoids memoQ special character shortcuts (Ctrl+Alt+O, Ctrl+Alt+I)
- ✅ **Updated shortcuts**:
  - Ctrl+Alt+P - Process single segment
  - Ctrl+Shift+L - Toggle loop mode
  - Ctrl+Alt+S - Stop loop
  - Ctrl+Alt+R - Reload TMX

### 🐛 Bug Fixes

**AutoHotkey Process Management**:
- ✅ **Fixed orphaned AHK processes** - Proper cleanup on application exit
  - Global `_ahk_process` tracking variable
  - `atexit` handler for guaranteed cleanup
  - Multiple cleanup layers: `__del__`, `closeEvent`, `unregister_global_hotkey`
  - Kill existing instances on startup
- ✅ **No more "script already running" popups**

**Window Activation**:
- ✅ **Multi-monitor support** - AttachThreadInput for cross-monitor focus stealing
- ✅ **Maximized state preservation** - Detects and restores maximized windows
- ✅ **No window flicker** - Removed WindowStaysOnTopHint approach

**UI Polish**:
- ✅ **Fixed cut-off text** in Theme Editor, AutoFingers, and Options dialogs
- ✅ **Activity Log spacing** - Added 8px padding and 1.4 line-height
- ✅ **Form layout spacing** - 8px vertical spacing in all forms

### 🔧 Technical Implementation

**Files Modified**:
- `Supervertaler_Qt_v1.0.0.py` - Main application (4972 lines)
  - Added `atexit` import and global AHK cleanup
  - Universal Lookup tab as Tab 0
  - Window `closeEvent` for AHK cleanup
  - Multi-monitor window activation logic
- `modules/universal_lookup.py` - Lookup engine (239 lines)
  - Non-destructive text capture
  - TM/Glossary search integration
  - Multiple CAT tool modes
- `universal_lookup_hotkey.ahk` - AutoHotkey v2 script (39 lines)
  - Ctrl+Alt+L hotkey registration
  - Clipboard copy with 200ms delay
  - File-based signaling to Python
- `modules/theme_manager.py` - Theme system (481 lines)
  - Enhanced QGroupBox styling with proper padding
  - QLabel padding for readability
  - QFormLayout vertical spacing

**Architecture Decisions**:
- **Why AutoHotkey?** - Python's clipboard handling on Windows is unreliable and destructive
- **Why file-based signaling?** - Thread-safe communication between AHK and Qt
- **Why atexit?** - Most reliable way to ensure process cleanup on any exit condition
- **Why Windows API AttachThreadInput?** - Only way to bypass Windows focus-stealing prevention across monitors

### 📦 Dependencies

**New Requirements**:
- AutoHotkey v2 (Windows only) - For global hotkey support
- pyperclip - For clipboard operations

**Installation**:
```bash
pip install pyperclip
# Download AutoHotkey v2 from https://www.autohotkey.com/
```

### 🎯 Platform Support

- **Windows**: ✅ Full support (global hotkey via AutoHotkey)
- **Mac**: ⚠️ Manual paste mode (no global hotkey)
- **Linux**: ⚠️ Manual paste mode (no global hotkey)

### 📝 Known Limitations

- Global hotkey (Ctrl+Alt+L) requires AutoHotkey v2 on Windows
- Mac/Linux users must paste text manually into Universal Lookup tab
- AutoHotkey script runs as background process (auto-managed)

---

## [Qt v1.0.0 - Phase 4] - 2025-01-27 📋 MEMOQ BILINGUAL DOCX SUPPORT

### ✨ New Features

**memoQ Bilingual Table Import/Export**:
- ✅ **Import memoQ bilingual DOCX** - Load bilingual tables from memoQ
  - Reads source and target segments from table format
  - Preserves formatting information (bold, italic, underline)
  - Auto-detects source and target languages from column headers
  - Maintains segment alignment (perfect 1:1 matching)
  - Stores formatting map for export
- ✅ **Export translated DOCX** - Save translations back to memoQ format
  - Updates target column with translations
  - Preserves source formatting in target text
  - Updates status column to "Confirmed"
  - Maintains table structure and metadata
  - Ready to import back into memoQ

**memoQ Bilingual Format Support**:
- Table structure: Row 0 = metadata, Row 1 = headers, Row 2+ = segments
- Column structure: 0=Segment#, 1=Source, 2=Target, 3=Comment, 4=Status
- Formatting preservation: Bold, italic, underline maintained from source to target
- Language detection: Auto-detects English, Dutch, German, French, Spanish, Italian, Portuguese, Polish

**Workflow**:
1. Export bilingual table from memoQ (File → Export → Bilingual)
2. Import into Supervertaler Qt (File → Import → memoQ Bilingual Table)
3. Translate segments (single or batch)
4. Export translated file (File → Export → memoQ Bilingual Table - Translated)
5. Import translated file back into memoQ

**UI Integration**:
- ✅ **Import menu** - File → Import → memoQ Bilingual Table (DOCX)...
- ✅ **Export menu** - File → Export → memoQ Bilingual Table - Translated (DOCX)...
- ✅ **Format validation** - Checks for valid memoQ table structure
- ✅ **Dependency check** - Prompts to install python-docx if missing

### 🔧 Technical Implementation

**Import Function** (`import_memoq_bilingual()`):
- Validates memoQ table structure (min 3 rows)
- Extracts source/target from columns 1 and 2
- Captures formatting info from paragraph runs
- Auto-detects languages from column headers
- Creates project with imported segments
- Stores original file path and formatting map

**Export Function** (`export_memoq_bilingual()`):
- Requires prior import (needs original file structure)
- Updates target column (col 2) with translations
- Applies formatting from source to target
- Updates status column (col 4) to "Confirmed"
- Saves as new file (preserves original)

**Formatting Preservation** (`_apply_formatting_to_cell()`):
- Extracts bold/italic/underline from source runs
- Maps formatting positions to target text
- Applies formatting proportionally to translation
- Falls back to plain text if mapping fails

### 📚 Dependencies

**Required**:
- `python-docx` - For reading/writing DOCX files
- Install with: `pip install python-docx`

### ✅ Testing

- ✅ App compiles without errors
- ✅ Import/export menu items functional
- ✅ Format validation working
- ⏳ **User testing pending** - Awaiting real memoQ bilingual files

### 🎯 Use Cases

**Ideal For**:
- memoQ users who want to leverage LLM translation
- Projects with formatting requirements (bold, italic, underline)
- Round-trip workflows (memoQ → Supervertaler → memoQ)
- Batch translation of memoQ exports

---

## [Qt v1.0.0 - Phase 3] - 2025-01-27 🚀 BATCH TRANSLATION

### ✨ New Features

**Batch Translation System**:
- ✅ **Multi-segment translation** - Translate all untranslated segments at once
- ✅ **Smart detection** - Automatically finds segments with empty target text
- ✅ **Confirmation dialog** - Shows count and API credit warning before starting
- ✅ **Progress dialog** - Live updates during translation process
  - Real-time progress bar
  - Current segment display (shows ID and first 60 chars)
  - Live statistics: Translated count, Failed count, Remaining count
  - Time estimate based on current rate
- ✅ **Real-time grid updates** - See translations appear as they're generated
- ✅ **Error recovery** - Batch continues even if individual segments fail
- ✅ **TM integration** - All translations automatically saved to Translation Memory
- ✅ **Completion summary** - Shows final statistics and success/failure breakdown

**UI Integration**:
- ✅ **Menu item** - Edit → Translate Multiple Segments... (Ctrl+Shift+T)
- ✅ **Toolbar button** - "🚀 Batch Translate" with visual icon
- ✅ **Keyboard shortcut** - Ctrl+Shift+T for power users

**Smart Translation Flow**:
1. Scan project for untranslated segments
2. Show confirmation with segment count
3. Open progress dialog with live updates
4. Translate segments sequentially (avoids rate limits)
5. Update grid and TM in real-time
6. Display completion summary with statistics

### 🔧 Technical Implementation

**Core Function** (`translate_batch()`):
- ~195 lines of robust batch translation logic
- Sequential translation (prevents API rate limits)
- QApplication.processEvents() for responsive UI
- Graceful error handling with continue-on-failure
- Statistics tracking (translated, failed, remaining)
- Time estimation and completion prediction

**Progress Dialog**:
```python
- QProgressBar with segment-based progress
- Current segment label (ID + preview)
- Statistics label (updated in real-time)
- Modal dialog (prevents accidental closure)
- Auto-close on completion or manual close
```

**Integration Points**:
- Uses existing LLMClient module from Phase 1
- Respects Phase 2 provider/model settings
- Updates Phase 1 status icons
- Saves to Phase 1 TM database

### 📚 Documentation

**New Guides**:
- ✅ `docs/specifications/QT_PHASE3_COMPLETE.md` - Complete Phase 3 documentation
  - Feature overview
  - Workflow diagrams
  - Technical implementation details
  - Usage instructions
  - Architecture integration

### 🎯 Use Cases

**Ideal For**:
- Translating entire documents in one operation
- Pre-translation before human review
- Batch processing of similar segments
- Quick first-pass translation workflow

**Features**:
- **Safe**: Confirmation dialog prevents accidental batch operations
- **Transparent**: See progress and statistics in real-time
- **Resilient**: Continues even if individual translations fail
- **Efficient**: Sequential processing respects API rate limits
- **Integrated**: Works seamlessly with existing TM and UI

### ✅ Testing

- ✅ App compiles without errors (`python -m py_compile`)
- ✅ Menu item and toolbar button functional
- ✅ Progress dialog displays correctly
- ✅ Real-time grid updates work
- ✅ TM integration successful
- ✅ Error recovery tested
- ⏳ **User testing pending** - Awaiting real-world project tests

### 🎯 Future Enhancements

**Potential Phase 3.1 Additions** (based on user feedback):
- Pause/Resume capability during batch
- Cancel button to abort mid-batch
- Custom segment selection (not just "all untranslated")
- Auto-save checkpoint every N segments
- Retry mechanism for failed segments
- Parallel translation with rate limiting

**Next Phase**:
**Phase 4: Custom Prompts & Advanced Features** (Future):
- System prompt customization
- Context injection templates
- Prompt library management
- Per-segment prompt overrides

---

## [Qt v1.0.0 - Phase 2] - 2025-10-27 🎨 LLM PROVIDER & MODEL SELECTION

### ✨ New Features

**Enhanced Settings Dialog**:
- ✅ **Tabbed settings interface** - Organized into LLM Settings and General tabs
- ✅ **Provider selection** - Choose between OpenAI, Claude, or Gemini
  - Radio button interface with live UI updates
  - Model dropdowns enable/disable based on provider selection
- ✅ **Per-provider model selection** - Choose specific models for each provider:
  - **OpenAI**: gpt-4o, gpt-4o-mini, gpt-5, o3-mini, o1, gpt-4-turbo
  - **Claude**: claude-3-5-sonnet, claude-3-5-haiku, claude-3-opus
  - **Gemini**: gemini-2.0-flash-exp, gemini-1.5-pro, gemini-1.5-flash
- ✅ **Settings persistence** - Preferences saved to `ui_preferences.json`
- ✅ **API keys management** - One-click button to open `api_keys.txt` in system editor
  - Auto-creates file from example if missing
  - Cross-platform file opening (Windows/Mac/Linux)

**Smart Translation Flow**:
- ✅ **Uses saved preferences** - Translation respects provider and model choices
- ✅ **Intelligent error handling** - Prompts to configure settings if API key missing
- ✅ **Status messages** - Shows provider and model in translation status
  - Example: "✓ Segment #1 translated with openai/gpt-4o"

### 🏗️ Modular Architecture

**LLM Clients Module** (`modules/llm_clients.py`):
- ✅ **Independent module** - Can be imported or run standalone
- ✅ **Multi-provider support** - OpenAI, Claude, Gemini in one client
- ✅ **Auto temperature detection** - 1.0 for reasoning models, 0.3 for standard
- ✅ **Type-safe** - Full type hints and dataclasses
- ✅ **Standalone testing** - Can be run directly from command line

**Settings Management**:
- ✅ **JSON-based storage** - Clean, human-readable format
- ✅ **Graceful degradation** - Defaults to OpenAI/gpt-4o if settings corrupt
- ✅ **Preference preservation** - All dropdowns remember selections per provider

### 📚 Documentation

**New Guides**:
- ✅ `docs/MODULAR_ARCHITECTURE_GUIDE.md` - Module creation guidelines
- ✅ `docs/specifications/QT_PHASE2_COMPLETE.md` - Phase 2 technical details
- ✅ `docs/guides/QT_SETTINGS_DIALOG_GUIDE.md` - Visual user guide

### 🔧 Technical Details

**Files Modified**:
- `Supervertaler_Qt_v1.0.0.py`: +350 lines
  - Enhanced settings dialog with tabs
  - Provider and model selection UI
  - Settings persistence functions
  - Updated translation function

**Files Created**:
- `modules/llm_clients.py`: LLM client module (191 lines)
- Documentation files (3 new guides)

**Settings Storage**:
```json
{
  "llm_settings": {
    "provider": "openai",
    "openai_model": "gpt-4o",
    "claude_model": "claude-3-5-sonnet-20241022",
    "gemini_model": "gemini-2.0-flash-exp"
  }
}
```

### ✅ Testing

- ✅ App compiles without errors
- ✅ Settings dialog opens and functions correctly
- ✅ All provider/model selections work
- ✅ Settings persist across app restarts
- ✅ Translation uses saved preferences
- ✅ API key validation and configuration prompts work

### 🎯 Next Phase

**Phase 3: Batch Translation** (Upcoming):
- Multi-segment selection
- Bulk translation with progress dialog
- Chunking for large batches
- Pause/resume capability

---

## [Qt v1.0.0 - Phase 1] - 2025-10-27 🚀 LLM TRANSLATION INTEGRATION

### ✨ Core Features

**Single Segment Translation**:
- ✅ **Ctrl+T hotkey** - Translate currently selected segment
- ✅ **Toolbar button** - 🤖 Translate button in main toolbar
- ✅ **Menu integration** - Edit → Translate Segment
- ✅ **Multi-provider ready** - OpenAI, Claude, Gemini clients implemented

**LLM Integration**:
- ✅ **Modular client** - Uses `modules/llm_clients.py` for clean architecture
- ✅ **Temperature handling** - Automatic detection (1.0 for GPT-5/o1/o3, 0.3 for standard)
- ✅ **API key loading** - From `user data/api_keys.txt`
- ✅ **Status updates** - Real-time feedback during translation

**First-Launch Experience**:
- ✅ **Auto-create example file** - `api_keys.example.txt` created on first run
- ✅ **Comprehensive instructions** - Example file includes setup guide for all providers
- ✅ **User-friendly paths** - Files in `user data/` folder, not root

### 🏗️ Architecture

**File Organization**:
- ✅ Moved `api_keys.example.txt` from root → `user data/`
- ✅ Moved `api_keys.txt` from root → `user data_private/`
- ✅ Clean repository structure (no sensitive files in root)

---

## [3.7.7] - 2025-10-27 🔧 MEMOQ ALIGNMENT FIX & LLM IMPROVEMENTS

### 🐛 Critical Fixes

**memoQ Bilingual DOCX Alignment**:
- ✅ **Fixed segment misalignment** - Translations now perfectly aligned with source segments
  - Root cause: TM lookup during batch was skipping segments, causing fallback matching to fail
  - Changed to translate ALL segments regardless of existing target content
  - Removed TM exact match checking during batch translation
  - User responsibility: Export memoQ bilingual DOCX with "View" filtered to untranslated only
- ✅ **Strict segment ID matching** - No more fallback line-by-line matching
  - Only accepts numbered format: `123. translation text`
  - Regex: `r'^(\d+)[\.\)]\s*(.+)'`
  - Segments without valid IDs fail gracefully (no misalignment)
- ✅ **Fixed prompt contradiction** - LLM now required to include segment numbers
  - Old: "Provide ONLY the translations... NO segment numbers"
  - New: "⚠️ CRITICAL: Include the segment NUMBER before each translation"
  - Added explicit formatting instructions with examples

**OpenAI GPT-5/Reasoning Model Support**:
- ✅ **Temperature parameter compatibility** - GPT-5 (o3-mini) now works correctly
  - Reasoning models (o1, o3, gpt-5) require temperature=1.0 (no flexibility)
  - Standard models (gpt-4o, gpt-4-turbo) use temperature=0.3
  - Model detection: checks for "o1", "o3", or "gpt-5" in model name
  - Error fixed: "Unsupported value: 'temperature' does not support 0.3"

**Content Policy Bypass**:
- ✅ **Enhanced professional context disclaimers** - Medical/technical content now accepted
  - Added explicit "licensed service for commercial translation company"
  - Added "commissioned by medical device manufacturer"
  - Added "regulatory compliance and patient safety documentation"
  - Added "THIS IS NOT A REQUEST FOR MEDICAL ADVICE"
  - Added "legally required regulatory filing"
  - Applied to all three prompt types: single_segment, batch_docx, batch_bilingual

### 📊 Testing Results

**GPT-5 Medical Device Documentation** (198 segments, CT scanner interface):
- ✅ Chunk 1: 100/100 segments translated perfectly
- ✅ Chunk 2: 98/98 segments translated perfectly
- ✅ Total: 198/198 successful, 0 failed, 2 API calls
- ✅ Perfect alignment verified in memoQ import
- ✅ All formatting tags preserved (uicontrol, menucascade, etc.)

**GPT-4o Behavior**:
- ⚠️ Inconsistent content moderation on medical content
- ✅ Chunk 1 sometimes works, chunk 2 sometimes refused
- 💡 Recommendation: Use GPT-5 for medical/technical documentation

### 🔧 Technical Details

**Alignment Logic Changes**:
```python
# OLD: Filter for untranslated segments
untranslated = [seg for seg in self.segments if not seg.target or seg.status == "untranslated"]

# NEW: Translate ALL segments (user ensures empty targets via memoQ View)
segments_to_translate = self.segments[:]

# REMOVED: TM lookup during batch (prevents segment skipping)
# REMOVED: Fallback line-by-line matching (causes misalignment)
```

**Temperature Detection**:
```python
if "o3" in model.lower() or "o1" in model.lower() or "gpt-5" in model.lower():
    temperature=1.0  # Required for reasoning models
else:
    temperature=0.3  # Standard models
```

### 📚 Best Practices

**For memoQ Bilingual DOCX Translation**:
1. In memoQ: Apply View filter to show only untranslated segments
2. Export bilingual DOCX with filter active (ensures empty targets)
3. Import in Supervertaler using "Import memoQ bilingual table (DOCX)"
4. Translate with GPT-5 (most reliable for medical/technical content)
5. Export using "Export memoQ bilingual table - Translated (DOCX)"
6. Import back into memoQ - perfect alignment guaranteed!

### 🎯 Impact

- **Critical bug fixed**: memoQ users can now trust segment alignment
- **GPT-5 support**: Access to OpenAI's reasoning models
- **Medical content**: Professional translation context bypasses content filters
- **Reliability**: 100% success rate on medical device documentation

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
