# Supervertaler - Changelog

All notable changes to Supervertaler are documented in this file.

**Current Version:** v1.7.6 (November 20, 2025)
**Framework:** PyQt6
**Status:** Active Development

**Note:** For historical information about legacy versions (Tkinter Edition, Classic Edition), see [legacy_versions/LEGACY_VERSIONS.md](legacy_versions/LEGACY_VERSIONS.md).

---

## 🌟 Recent Highlights - What's New in Supervertaler

**Latest Major Features:**

- 💾 **Auto Backup System (v1.7.6)** - Automatic project.json and TMX backups at configurable intervals to prevent data loss
- 🐛 **Critical TM Save Bug Fix (v1.7.5)** - Fixed massive unnecessary database writes during grid operations that caused 10+ second freezes
- 💾 **Project Persistence (v1.7.4)** - Projects now remember your primary prompt and image context folder
- 🧪 **Prompt Preview & System Template Editor (v1.7.3)** - Preview combined prompts with figure context detection and improved system template editor with better layout
- 🔧 **Termbase Critical Fixes (v1.7.2)** - Fixed term deduplication and termbase selection issues
- 🎨 **Termbase UI Polish (v1.7.1)** - Improved visual consistency with pink highlighting for project termbases and real-time term count updates
- 📚 **Project Termbases (v1.7.0)** - Dedicated project-specific terminology with automatic extraction and pink highlighting
- 📁 **File Dialog Memory (v1.6.5)** - File dialogs remember your last used directory for improved workflow
- 🌐 **Superbrowser (v1.6.4)** - Multi-chat AI browser with ChatGPT, Claude, and Gemini side-by-side in one window
- ⚡ **UI Responsiveness & Precision Scroll (v1.6.3)** - Debug settings, disabled LLM auto-matching, memoQ-style precision scroll buttons, auto-center active segment
- 🖼️ **Superimage (v1.6.2)** - Extract images from DOCX files with preview and auto-folder management
- 📚 **Enhanced Termbase System (v1.6.1)** - Extended metadata with notes, project, client fields and refresh functionality
- 📚 **Complete Termbase System (v1.6.0)** - Professional terminology management with interactive features
- 🎤 **Supervoice (v1.4.0)** - AI voice dictation with OpenAI Whisper, 100+ languages, F9 hotkey
- 📊 **Superbench (v1.4.1)** - Benchmark LLM translation quality on YOUR actual projects with chrF++ scoring
- 🤖 **AI Assistant (v1.3.4)** - ChatGPT-quality conversational prompt refinement built into the editor
- 📚 **Unified Prompt Library (v1.3.0)** - Unlimited folders, favorites, multi-attach, quick run
- 📝 **TMX Editor (v1.1.3)** - Database-backed editor handles massive 1GB+ TMX files
- ✋ **AutoFingers (v1.2.4)** - Automated TMX-to-memoQ pasting with fuzzy matching and tag cleaning
- 📄 **PDF Rescue** - AI OCR with GPT-4 Vision transforms locked PDFs into clean DOCX
- 🖼️ **Image Context** - Multimodal AI automatically includes images when translating technical documents
- 💾 **Translation Memory** - Fuzzy matching with TMX import/export, auto-propagation
- 🔄 **CAT Tool Integration** - memoQ, Trados, CafeTran bilingual table support

**See full version history below** ↓

---

## [1.7.6] - November 20, 2025

### 💾 Auto Backup System

**Added:**

- ✨ **Automatic Backup System** - Prevents data loss during translation work
  - Auto-saves project.json at configurable intervals (1-60 minutes, default: 5 minutes)
  - Auto-exports TMX backup file in same folder as project.json
  - TMX backup includes all segments for maximum recovery capability
  - Settings UI in Settings → General tab with enable/disable toggle
  - Non-intrusive background operation with timestamp logging
  - Settings persist across sessions in ui_preferences.json
  - Timer automatically restarts when settings are changed

**Technical Details:**

- QTimer-based system with millisecond precision
- Uses existing `save_project_to_file()` and `TMXGenerator` methods
- Graceful error handling without interrupting workflow
- Only runs when project is open and has a file path
- TMX file named `{project_name}_backup.tmx` for easy identification

---

## [1.7.5] - November 20, 2025

### 🐛 Critical Bug Fix - Translation Memory Save Flood

**Fixed:**

- ✅ **TM Save Flood During Grid Operations** - CRITICAL FIX
  - **Issue:** Every time `load_segments_to_grid()` was called (startup, filtering, clear filters), all segments with status "translated"/"confirmed"/"approved" would trigger false TM database saves 1-2 seconds after grid load
  - **Symptoms:**
    - 10+ second UI freeze on projects with 200+ segments
    - Massive unnecessary database writes (219 saves on a 219-segment project)
    - Made filtering operations completely unusable
    - Could potentially corrupt data or cause performance issues on large projects
  - **Root Cause:** Qt internally queues document change events when `setPlainText()` is called on QTextEdit widgets, even when signals are blocked. When `blockSignals(False)` was called after grid loading, Qt delivered all these queued events, triggering `textChanged` for every segment. By that time, the suppression flag had already been restored, so the suppression check failed.
  - **Solution:**
    - Added `_initial_load_complete` flag to `EditableGridTextEditor` class
    - Signal handler now ignores the first spurious `textChanged` event after widget creation
    - All subsequent real user edits are processed normally
    - Clean, minimal fix that doesn't interfere with Qt's event system
  - **Testing:** Verified on BRANTS project (219 segments) - zero false TM saves during startup, filtering, and filter clearing
  - **Files Modified:** Supervertaler.py (lines 835, 11647-11651)

**Impact:**
- **Performance:** Grid loading is now instant with no post-load freeze
- **Database:** Eliminates 200+ unnecessary database writes per grid operation
- **User Experience:** Filtering and grid operations are now fast and responsive
- **Data Integrity:** Prevents potential database corruption from excessive writes

---

## [1.7.4] - November 20, 2025

### 💾 Project Persistence Improvements

**Enhanced:**

- ✅ **Primary Prompt Persistence** - Projects now remember your selected primary prompt
  - Automatically restores primary prompt when reopening project
  - Updates UI label to show active prompt name
  - Works with Unified Prompt Library system
  
- ✅ **Image Context Folder Persistence** - Projects remember loaded image folders
  - Image context folder path saved to project.json
  - Automatically reloads all images from saved folder on project open
  - Updates UI status label showing image count and folder name
  - Logs success/warnings if folder path has changed
  
- ✅ **Attached Prompts Persistence** - All attached prompts are restored
  - Maintains complete prompt configuration across sessions
  - Updates attached prompts list UI on restore

**Technical:**
- Changed from `library.set_primary_prompt()` to `_set_primary_prompt()` for UI updates
- Changed from `library.attach_prompt()` to `_attach_prompt()` for UI updates
- Added `image_context_folder` to `prompt_settings` in project.json
- Proper UI synchronization on project load for all prompt settings

**User Experience:**
Now when you save a project, it remembers:
- ✓ Which primary prompt you selected
- ✓ Which prompts you attached
- ✓ Which image folder you loaded
- ✓ All settings restore automatically on project open

---

## [1.7.3] - November 20, 2025

### 🧪 Prompt Preview & System Template Improvements

**New Features:**

**Added:**
- ✅ **Preview Combined Prompts Button** - New "🧪 Preview Prompts" button in Project Editor segment action bar
  - Shows complete assembled prompt that will be sent to AI
  - Displays System Template + Custom Prompts + current segment text
  - Real-time composition info (segment ID, languages, character count, attached prompts)
  - Visual context indicator showing which images will be sent alongside text
  - Clear tooltip explaining functionality

**Enhanced:**
- ✅ **System Template Editor** - Improved layout and usability in Settings → System Prompts
  - Increased text editor height from 400px to 500px
  - Added stretch factors for proper expansion to fill available space
  - Enabled word wrap at widget width for easier reading
  - Set plain text mode to prevent formatting issues
  
- ✅ **Figure Context Detection** - Fixed regex pattern for accurate figure reference detection
  - Now correctly matches "Figuur 3" → "3" instead of "3toont"
  - Properly handles subfigures (e.g., Figure 1A, 2B)
  - Requires space between "figuur/figure/fig" and number

**Improved:**
- ✅ **Image Context Preview** - Preview dialog now shows detailed image information
  - 🖼️ Displays which images will be sent with prompt (e.g., "Figure 3")
  - ⚠️ Warns if references detected but images not found
  - ℹ️ Shows info when images loaded but not referenced in segment
  - Yellow banner highlights when images are being sent as binary data

**Technical:**
- Updated `UnifiedPromptManagerQt._preview_combined_prompt()` to access actual segment data
- Added `_preview_combined_prompt_from_grid()` method in main app
- Fixed attribute reference from `self.unified_prompt_manager` to `self.prompt_manager_qt`
- Improved figure reference regex from `[\w\d]+(?:[\s\.\-]*[\w\d]+)?` to `\d+[a-zA-Z]?`

---

## [1.7.2] - November 19, 2025

### 🔧 Termbase Critical Fixes - Term Deduplication & Selection

**Major Bug Fixes:**

**Fixed:**
- ✅ **Multiple Translations Display** - Fixed critical deduplication bug where only one translation was kept for terms with same source text
  - Example: "inrichting → device" AND "inrichting → apparatus" now both display correctly
  - Root cause: Used `source_term` as dict key, now uses `term_id` to allow multiple translations
- ✅ **Termbase Selection** - Terms now save only to selected termbases (previously saved to all active termbases)
  - Filter logic working correctly with INTEGER termbase IDs
  - Debug logging confirmed type matching works as expected
- ✅ **Segment Highlighting Consistency** - Termbase highlighting now works consistently across all segments
  - Fixed cache iteration to handle new dict structure with `term_id` keys
  - Updated all code paths that consume termbase matches

**Technical Changes:**
- **Dictionary Structure Change:**
  - Changed from: `matches[source_term] = {...}` (only one translation per source)
  - Changed to: `matches[term_id] = {'source': source_term, 'translation': target_term, ...}` (multiple translations allowed)
- **Code Locations Updated:**
  - `find_termbase_matches_in_source()` - Changed dict key from source_term to term_id
  - `highlight_termbase_matches()` - Updated to extract source term from match_info
  - `DocumentView._create_highlighted_html()` - Updated iteration logic
  - `_get_cached_matches()` - Fixed to extract source term from dict values (2 locations)
  - All hover tooltip and double-click handlers updated

**Impact:**
- 🎯 **Better Term Disambiguation** - Users can now add multiple translations for same source term
- 🎨 **Accurate Highlighting** - All matching terms highlighted correctly in grid
- ✅ **Correct Termbase Selection** - Terms added only to user-selected termbases

---

## [1.7.1] - November 19, 2025

### 🎨 Termbase UI Polish - Visual Consistency Improvements

**Bug Fixes & UI Improvements:**

**Fixed:**
- ✅ **Deleted Term Highlighting** - Fixed issue where deleted termbase terms remained highlighted after deletion and navigation
- ✅ **Termbase Name Display** - Termbase names now correctly shown in Term Info metadata area
- ✅ **Term Count Updates** - Term counts in termbase list now update immediately after adding terms
- ✅ **Project Termbase Colors** - Fixed project termbases showing blue instead of pink in translation results
- ✅ **Ranking Metadata** - Added missing `ranking` field to TranslationMatch metadata in all code paths

**Improved:**
- 🎨 **Visual Consistency** - Project termbase matches now display with same style as background termbases (colored number badge only)
- 🎯 **Effective Project Detection** - Uses `ranking == 1` as fallback when `is_project_termbase` flag is false
- 🔄 **Real-time Refresh** - Termbase list UI refreshes immediately via callback after term addition
- 📊 **Database Query Fix** - Fixed TEXT/INTEGER comparison with CAST for accurate term counts

**Technical:**
- Modified `highlight_termbase_matches()` to clear formatting before early return
- Added `termbase_name` extraction and display in translation results panel
- Implemented `refresh_termbase_list()` callback storage and invocation
- Added explicit boolean conversion for `is_project_termbase` from SQLite
- Updated `CompactMatchItem.update_styling()` to use consistent badge-only coloring
- Fixed two locations where `ranking` was missing from TranslationMatch metadata

---

## [1.7.0] - November 18, 2025

### 📚 Project Termbases - Dedicated Project Terminology

**Project-Specific Terminology Management** - A powerful new termbase system that distinguishes between project-specific terminology (one per project) and background termbases (multiple allowed), with automatic term extraction from project source text.

### Added

**Project Termbase System:**
- 📌 **Project Termbase Designation** - Mark one termbase per project as the official project termbase
- 🎨 **Pink Highlighting** - Project termbase matches highlighted in light pink (RGB 255, 182, 193) in both grid and results panel
- 🔵 **Background Termbases** - Regular termbases use priority-based blue shading as before
- 🔍 **Term Extraction** - Automatically extract terminology from project source segments
- 🧠 **Smart Algorithm** - Frequency analysis, n-gram extraction, scoring based on capitalization and special characters
- 🌐 **Multi-Language Support** - Stop words for English, Dutch, German, French, Spanish
- 📊 **Preview & Select** - Review extracted terms with scores before adding to termbase
- 🎯 **Configurable Parameters** - Adjust min frequency, max n-gram size, language, term count
- ⚙️ **Standalone Module** - Term extractor designed as independent module (`modules/term_extractor.py`) for future CLI tool

**Termbases Tab Enhancements:**
- 📋 **Type Column** - Shows "📌 Project" in pink or "Background" for each termbase
- 🔘 **Set/Unset Buttons** - Easy designation of project termbases
- 🔍 **Extract Terms Button** - Launch term extraction dialog (only enabled with project loaded)
- 🎨 **Visual Distinction** - Project termbase names shown in pink
- 🔒 **Validation** - System enforces "only one project termbase per project" rule

**Database Schema:**
- 🗄️ **is_project_termbase Column** - Added to termbases table with migration
- ✅ **Backward Compatible** - Existing databases upgraded automatically

**Termbase Manager Extensions:**
- `set_as_project_termbase(termbase_id, project_id)` - Designate project termbase
- `unset_project_termbase(termbase_id)` - Remove designation
- `get_project_termbase(project_id)` - Retrieve project termbase
- Enhanced `create_termbase()` with `is_project_termbase` parameter and validation
- Enhanced `get_all_termbases()` to sort project termbase first

**Match Pipeline Integration:**
- 🔗 **Metadata Tracking** - `is_project_termbase` flag passed through entire match pipeline
- 🎨 **Grid Highlighting** - Light pink backgrounds for project termbase matches in source column
- 📋 **Results Panel** - Light pink number badges for project termbase matches

### Changed
- Updated termbase search to include `is_project_termbase` field
- Modified `highlight_termbase_matches()` to use pink for project termbases
- Enhanced `TranslationMatch` metadata to capture project termbase status
- Updated `CompactMatchItem` styling to handle three-way color logic (forbidden=black, project=pink, background=blue)

### Technical Details
- **Term Extraction Algorithm:**
  - N-gram extraction (unigrams, bigrams, trigrams)
  - Frequency-based scoring with logarithmic scaling
  - Bonuses for capitalization (+3), special characters (+2), n-gram size (+1.5 per word)
  - Term classification: proper_noun, technical, phrase, word
  - Configurable filtering by frequency, type, score
- **Color Scheme:**
  - Project Termbase: `#FFB6C1` (light pink)
  - Forbidden Terms: `#000000` (black)
  - Background Termbases: `#4d94ff` (blue with priority-based darkening)

### Use Cases
- **Starting New Projects** - Extract project-specific terminology automatically
- **Consistency** - Ensure project terminology has visual precedence
- **Background Knowledge** - Maintain general termbases alongside project-specific ones
- **Source-Only Termbases** - Perfect for extracting terms before translation begins

---

## [1.6.5] - November 18, 2025

### 📁 File Dialog Memory - Smart Directory Navigation

**File Dialogs Remember Your Last Location** - A quality-of-life improvement that significantly streamlines workflow by automatically remembering the last directory you navigated to across all file dialogs throughout the application.

### Added

**File Dialog Helper System:**
- 📁 **Last Directory Memory** - File dialogs automatically open in the last used directory
- 💾 **Persistent Storage** - Last directory saved to config file between sessions
- 🔄 **Universal Coverage** - Works for all dialog types (open file, save file, select folder, multiple files)
- 🎯 **Automatic Detection** - Extracts directory from file paths automatically
- 🛠️ **Helper Module** - Created `modules/file_dialog_helper.py` with wrapper functions

**Config Manager Enhancements:**
- Added `get_last_directory()` - Retrieve the last used directory
- Added `set_last_directory()` - Save a directory as the last used location
- Added `update_last_directory_from_file()` - Extract and save directory from file path

**Integration Points:**
- Image Extractor (add DOCX files, select folder, output directory)
- TMX import/export dialogs
- Project open/save dialogs
- Export dialogs (JSON, TMX, etc.)

**Benefits:**
- No more navigating from program root every time
- Improved workflow when working with files in the same folder
- Transparent operation - works automatically without configuration
- Persists between application sessions

### Technical Implementation
- Created `modules/file_dialog_helper.py` with `get_open_file_name()`, `get_save_file_name()`, `get_existing_directory()`, `get_open_file_names()` wrappers
- Extended `config_manager.py` with directory tracking methods
- Updated key file dialog calls in `Supervertaler.py` to use helper functions
- Last directory stored in `~/.supervertaler_config.json` (or dev mode equivalent)

---

## [1.6.4] - November 18, 2025

### 🌐 Superbrowser - Multi-Chat AI Browser

**Work with Multiple AI Chats Simultaneously** - A revolutionary new tab that displays ChatGPT, Claude, and Gemini side-by-side in resizable columns with persistent login sessions, perfect for comparing AI responses or maintaining multiple conversation threads.

### Added

**Superbrowser Tab:**
- 🌐 **Three-Column Layout** - ChatGPT, Claude, and Gemini displayed simultaneously in resizable columns
- 🔐 **Persistent Sessions** - Login credentials saved between sessions (no need to log in every time)
- 🔧 **Collapsible Configuration** - Hide/show URL configuration panel to maximize screen space
- 🎨 **Color-Coded Columns** - Each AI provider has distinct color (green, copper, blue)
- 🏠 **Navigation Controls** - URL bar, reload, and home buttons for each column
- 💾 **Profile Storage** - Separate persistent storage for each AI provider (cookies, cache, sessions)
- 📱 **Minimal Headers** - Tiny 10px headers maximize space for chat windows
- 🎯 **Dev Mode Support** - Uses `user_data_private/` for dev mode, `user_data/` for production

**Technical Implementation:**
- Created `modules/superbrowser.py` - Standalone module with `SuperbrowserWidget`
- Integrated QtWebEngine with OpenGL context sharing for proper rendering
- Added persistent profile management using `QWebEngineProfile`
- Implemented `ChatColumn` class for individual browser columns
- Added to Specialised Tools as "🌐 Superbrowser" tab

**Use Cases:**
- Compare how different AI models respond to the same prompt
- Maintain separate conversation threads for different projects
- Quick access to all major AI assistants without switching browser tabs
- Research and development with multiple AI perspectives

### Fixed
- QtWebEngine DLL compatibility issues resolved (version matching)
- OpenGL context sharing properly initialized before QApplication creation
- Profile storage paths follow application's dev mode patterns

### Dependencies
- Added `PyQt6-WebEngine>=6.8.0,<6.9.0` requirement (version matched to PyQt6 6.8.1)

---

## [1.6.3] - November 18, 2025

### ⚡ UI Responsiveness & Precision Scroll Enhancements

**Major Performance Improvements & memoQ-Style Navigation** - Comprehensive UI responsiveness optimizations including debug settings system, disabled LLM auto-matching by default, precision scroll buttons, and auto-center active segment feature.

### Added

**Debug Settings System:**
- 🐛 **Debug Settings Tab** - New dedicated tab in Settings dialog for debugging and performance tuning
- 📝 **Verbose Logging Toggle** - Enable/disable detailed debug logs (textChanged events, update cycles, cell selection)
- 📤 **Debug Log Export** - Export debug logs to timestamped files (`supervertaler_debug_log_YYYYMMDD_HHMMSS.txt`)
- 🔄 **Auto-export Option** - Automatically export debug logs on application exit
- 🗑️ **Clear Log Buffer** - Manual clear button for debug log buffer (10,000 entry limit)
- ⏱️ **Debounce Delay Control** - Spinbox to adjust target text debounce delay (100-5000ms range, default 1000ms)
- ⚠️ **Performance Warnings** - Clear warnings about performance impact of verbose logging

**Precision Scroll Controls:**
- ⬆️⬇️ **Precision Scroll Buttons** - memoQ-style ▲▼ buttons for fine-grained grid scrolling
- 🎯 **Fixed Pixel Scrolling** - Uses fixed pixel amounts (5-50px) instead of variable row heights for predictable movement
- 🎚️ **Adjustable Precision** - Spinbox setting (1-10 divisor) to control scroll increment size:
  - Divisor 1 = 50 pixels (coarse)
  - Divisor 3 = 40 pixels (default)
  - Divisor 5 = 30 pixels (fine)
  - Divisor 10 = 5 pixels (very fine)
- 📊 **Live Preview** - Setting shows "Coarse/Medium/Fine/Very fine" label based on divisor value
- 📍 **Smart Positioning** - Buttons positioned to left of scrollbar, never cut off or overlapping
- 🎨 **Hover Effects** - Blue highlight on hover, visual feedback on click
- 🔄 **Auto-repositioning** - Buttons reposition on window resize and table changes

**Auto-Center Active Segment:**
- 🎯 **Keep Active Segment Centered** - Optional toggle to auto-scroll and center selected segment in viewport
- 🔄 **CAT Tool Behavior** - Matches memoQ, Trados, and other professional CAT tools
- ✅ **Settings Persistence** - Auto-center preference saved to `ui_preferences.json`
- 🖱️ **Smooth Navigation** - Active segment always visible and centered when navigating

**Performance Optimizations:**
- 🚫 **LLM Auto-matching Disabled by Default** - Changed `enable_llm_matching` from `True` to `False` to prevent 10-20 second UI freezes
- ⚡ **Conditional Debug Logging** - All verbose logs wrapped in `if self.debug_mode_enabled:` checks
- ⏱️ **Increased Debounce Delay** - Target text change debounce increased from 500ms to 1000ms
- 🎛️ **LLM Matching Toggle** - Added checkbox in General Settings with warning tooltip
- 💾 **Settings Persistence** - Debug mode, LLM matching, precision scroll, and auto-center settings saved/loaded

**UI/UX Improvements:**
- 📑 **Precision Scroll Settings Section** - New section in General Settings with all scroll-related controls
- ℹ️ **Helpful Tooltips** - Detailed explanations for all new settings
- ⚠️ **Warning Messages** - Clear warnings about LLM performance impact (10-20 sec per segment)
- 🎨 **Consistent Styling** - Settings UI follows existing design patterns

### Changed

- 🔧 **Default LLM Behavior** - LLM translations no longer trigger automatically on segment selection (use "Translate with AI" button instead)
- ⏱️ **Debounce Timing** - Target text debounce delay increased from 500ms to 1000ms for better stability
- 📊 **Debug Logging** - Performance-heavy debug logs now conditional (only when debug mode enabled)
- 🎯 **Scroll Algorithm** - Precision scroll now uses fixed pixel amounts instead of row-height-based calculations

### Fixed

- 🐛 **UI Freezing on Segment Selection** - Eliminated 10-20 second freezes caused by automatic LLM API calls
- 🐛 **Unpredictable Scroll Jumping** - Fixed precision scroll skipping segments due to variable row heights
- 🐛 **Button Positioning** - Fixed scroll buttons being cut off by scrollbar
- 🐛 **Method Name Mismatch** - Fixed `create_tabbed_assistance_panel` vs `create_assistance_panel` naming error
- 🐛 **Duplicate Method Definition** - Removed duplicate `position_precision_scroll_buttons` method
- 🐛 **TranslationResultsPanel Initialization** - Fixed incorrect `main_window` and `match_limits` parameters

### Technical Details

**Files Modified:**
- `Supervertaler.py` - Core application with all new features
- `ui_preferences.json` - Stores debug_mode_enabled, debug_auto_export, enable_llm_matching, precision_scroll_divisor, auto_center_active_segment

**Performance Impact:**
- MT engines (1-2 sec) remain enabled for auto-matching ✅
- LLM translations (10-20 sec) now on-demand only (via button) ✅
- Debug logging overhead eliminated in production use ✅
- Smoother segment navigation with predictable scroll behavior ✅

**Location:**
- Settings → 🐛 Debug (Debug settings tab)
- Settings → General Settings (LLM matching toggle, precision scroll settings)
- Grid → Right edge (Precision scroll buttons ▲▼)

---

## [1.6.2] - November 17, 2025

### 🖼️ Image Extractor (Superimage)

**Extract Images from DOCX Files** - New tool for extracting all images from DOCX files with preview and batch processing capabilities.

### Added

**Image Extraction:**
- 📄 **DOCX Image Extractor** - Extract all images from DOCX files (located in word/media/ folder)
- 🖼️ **PNG Output** - Convert all image formats to PNG with sequential naming (Fig. 1.png, Fig. 2.png, etc.)
- 📁 **Auto-folder Mode** - Option to automatically create "Images" subfolder next to source DOCX
- 📚 **Batch Processing** - Add multiple DOCX files or entire folders for bulk extraction
- 🎯 **Custom Prefix** - Configurable filename prefix (default: "Fig.")

**Image Preview:**
- 👁️ **Click-to-Preview** - Click any extracted file in list to view in preview panel
- 🖼️ **Resizable Preview** - Horizontal splitter between results and preview (60% preview area)
- ⬅️➡️ **Navigation Buttons** - Previous/Next buttons synced with file list
- 🔍 **Auto-scaling** - Images automatically scaled to fit viewport while maintaining aspect ratio

**UI/UX:**
- 🎨 **Compact Layout** - Optimized vertical space with single-row controls
- 📝 **Resizable Status Log** - Extraction progress log with minimum 50px height
- 📋 **File List Management** - Add files, add folder, clear list functionality
- 🛠️ **Tools Menu Integration** - Quick access via Tools → Image Extractor (Superimage)

**Technical:**
- 🔧 **New Module** - `modules/image_extractor.py` with `ImageExtractor` class
- 📖 **Documentation** - Complete user guide in `modules/IMAGE_EXTRACTOR_README.md`
- 🧪 **Test Script** - `tests/test_image_extractor.py` for validation
- 🎨 **PIL/Pillow** - Image format conversion (RGBA→RGB with white background)

**Location:**
- Translation Resources → Reference Images tab
- Tools → Image Extractor (Superimage)...

---

## [1.6.1] - November 17, 2025

### 📚 Enhanced Termbase Metadata System

**Extended Metadata & Improved UX** - Comprehensive termbase metadata with notes, project, and client fields, plus instant refresh functionality.

### Added

**Enhanced Metadata Fields:**
- 📝 **Notes Field** - Multi-line notes field replacing old definition field for context, usage notes, and URLs
- 🔗 **Clickable URLs** - URLs in notes automatically become clickable links (opens in external browser)
- 📁 **Project Field** - Track which project a term belongs to
- 👤 **Client Field** - Associate terms with specific clients
- 🏷️ **Domain Field** - Already existed, now fully integrated throughout system

**Termbase Viewer Enhancements:**
- 📖 **Dedicated Termbase Viewer** - New panel at bottom of Translation Results showing selected termbase entry
- 🔄 **Refresh Data Button** - Manual refresh button to reload latest data from database
- ✏️ **Edit Button** - Direct access to edit dialog from termbase viewer
- 🖱️ **Right-Click Edit** - Context menu on termbase matches for quick editing
- ♻️ **Auto-Refresh on Edit** - Termbase viewer automatically updates after editing entry

**Improved Table Views:**
- 📊 **Extended Columns** - Edit Terms dialog now shows: Source, Target, Domain, Priority, Notes (truncated), Project, Client, Forbidden
- 📏 **Smart Column Widths** - Optimized column sizing for better visibility
- ✂️ **Notes Truncation** - Long notes truncated to 50 characters with "..." in table view

**Database Enhancements:**
- 🗄️ **Database Migration System** - Automated schema updates for backward compatibility
- ➕ **New Columns** - Added `notes`, `project`, `client` columns to `termbase_terms` table
- 🔗 **Synonyms Table** - Created `termbase_synonyms` table structure (foundation for future feature)
- 🔄 **Legacy Support** - Old `definition` column preserved for backward compatibility

### Fixed

**Metadata Flow Issues:**
- ✅ **Complete Metadata Chain** - All termbase metadata now flows correctly: Dialog → Database → Search → Display
- ✅ **Edit Button Caching** - Fixed issue where edit buttons didn't work until adding first new term
- ✅ **Thread-Safe Queries** - Background termbase worker now includes all metadata fields (term_id, termbase_id, etc.)
- ✅ **Initial Load** - Termbase matches loaded at startup now include full metadata for immediate editing
- ✅ **Field Consistency** - Standardized on "notes" (plural) throughout codebase

**UI/UX Improvements:**
- ✅ **Visible Refresh Button** - Changed from just "🔄" to "🔄 Refresh data" for better visibility
- ✅ **Metadata Display** - Termbase viewer shows all fields with proper formatting
- ✅ **URL Rendering** - QTextBrowser with `setOpenExternalLinks(True)` for clickable links
- ✅ **Edit Dialog Fields** - Updated TermMetadataDialog to show notes, project, client (removed old definition field)

### Changed

**API Updates:**
- 🔄 **termbase_manager.add_term()** - Updated signature to accept `notes`, `project`, `client` instead of `definition`
- 🔄 **termbase_manager.get_terms()** - Now returns all new fields in term dictionaries
- 🔄 **termbase_manager.update_term()** - Updated to handle new field structure
- 🔄 **database_manager.search_termbases()** - SELECT query includes all new columns
- 🔄 **TranslationMatch metadata** - All creation points include complete metadata with IDs

**Code Quality:**
- 📦 **Modular Migrations** - `database_migrations.py` handles all schema updates
- 🔒 **Type Safety** - Proper Optional types for new fields throughout
- 🧹 **Cleanup** - Removed all references to old "definition" field (except database column for compatibility)

### Technical Details

**Database Migration:**
```sql
-- Migration adds new columns to termbase_terms
ALTER TABLE termbase_terms ADD COLUMN notes TEXT;
ALTER TABLE termbase_terms ADD COLUMN project TEXT;
ALTER TABLE termbase_terms ADD COLUMN client TEXT;

-- New synonyms table (foundation for future feature)
CREATE TABLE IF NOT EXISTS termbase_synonyms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    term_id INTEGER NOT NULL,
    synonym_text TEXT NOT NULL,
    language TEXT NOT NULL,
    created_date TEXT,
    FOREIGN KEY (term_id) REFERENCES termbase_terms(id) ON DELETE CASCADE
);
```

**Metadata Flow:**
1. **Add Term**: TermMetadataDialog → get_metadata() → add_term_pair_to_termbase() → termbase_mgr.add_term() → Database INSERT
2. **Load Terms**: Database SELECT → search_termbases() → TranslationMatch metadata → Termbase viewer display
3. **Edit Term**: Edit button → TermbaseEntryEditor → update_term() → Database UPDATE → Refresh viewer
4. **Cache Population**: Background worker → _search_termbases_thread_safe() → Complete metadata → termbase_cache

---

## [1.6.0] - November 16, 2025

### 📚 Complete Termbase System with Interactive Features

**The Ultimate Terminology Management** - Full-featured termbase system rivaling commercial CAT tools with memoQ-inspired interactive features.

### Added

**Core Termbase Features:**
- 📊 **SQLite-Based Storage** - Robust database backend for termbases and terms
- 🔍 **Real-Time Term Matching** - Automatic detection of termbase matches in source segments
- 🎨 **Priority-Based Highlighting** - Terms highlighted in source cells with color intensity matching priority (1-99)
- 🎯 **Visual Match Display** - All termbase matches shown in Translation Results panel with metadata
- ⚫ **Forbidden Term Marking** - Forbidden terms highlighted in black (source cells and translation results)
- 🗂️ **Multi-Termbase Support** - Create and manage multiple termbases per project
- ✅ **Termbase Activation** - Enable/disable specific termbases for each project

**Interactive Features (memoQ-Inspired):**
- 💡 **Hover Tooltips** - Mouse over highlighted terms to see translation, priority, and forbidden status
- 🖱️ **Double-Click Insertion** - Double-click any highlighted term to insert translation at cursor
- 📝 **Dual Selection Workflow** - Select source term → Tab → select target translation → Ctrl+E to add
- 🎹 **Keyboard Shortcuts** - Ctrl+E to add term pair, right-click context menu alternative

**Termbase Management UI:**
- 📋 **Termbase List** - View all termbases with term counts and activation toggles
- ➕ **Create/Delete** - Full CRUD operations with confirmation dialogs
- ✏️ **Edit Terms Dialog** - Modify source/target terms, priority (1-99), and forbidden flag
- 🔢 **Priority Editing** - Click priority cells to edit directly in table
- 🚫 **Forbidden Toggle** - Checkbox for marking terms as forbidden (do-not-use)
- 📊 **Metadata Entry** - Add definition, domain, priority, and forbidden status when creating terms

**Technical Implementation:**
- 🗄️ **Three-Table Schema** - `termbases`, `termbase_terms`, `termbase_activation` for flexible management
- 🔍 **FTS5 Full-Text Search** - Fast term matching even with large termbases
- 💾 **Smart Caching** - Term matches cached per segment for performance
- 🔄 **Automatic Refresh** - Adding/editing terms immediately updates highlighting and results
- 🎨 **QTextCharFormat Highlighting** - Non-intrusive background color without replacing widgets
- 🖱️ **Mouse Tracking** - Enable hover detection with `setMouseTracking(True)`
- 📍 **Position Detection** - `cursorForPosition()` for finding text under mouse cursor

**Color System:**
- 🔵 **Priority Colors** - Higher priority (lower number) = darker blue, lower priority = lighter blue
- ⚫ **Forbidden Terms** - Black background (#000000) with white text for maximum visibility
- 🎨 **Consistent Rendering** - Same color scheme in source highlights and translation results

**Workflow Integration:**
- ⚡ **Fast Term Entry** - Select in source → Tab → select in target → Ctrl+E → done
- 🔄 **Immediate Visibility** - New terms appear instantly in highlights and results
- 📊 **Project-Based Activation** - Each project remembers which termbases are active
- 🎯 **Settings Toggle** - Enable/disable grid highlighting in Settings → General

### Fixed
- ✅ Language code handling - Proper conversion from language names (Dutch → nl, English → en)
- ✅ Term search issues - Fixed "unknown" language codes preventing matches
- ✅ Activation persistence - Termbase toggles now save correctly across sessions
- ✅ Priority editing - Term priority changes now persist to database
- ✅ Delete functionality - Delete button now works with confirmation dialog
- ✅ Project ID tracking - Hash-based project ID for termbase activation
- ✅ Highlight consistency - Clear formatting before re-applying to prevent accumulation
- ✅ Cache clearing - Both termbase_cache and translation_matches_cache cleared after changes

### Technical Details
**Database Schema:**
```sql
-- Termbases table
CREATE TABLE termbases (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    created_date TEXT,
    modified_date TEXT
)

-- Termbase terms with FTS5 search
CREATE VIRTUAL TABLE termbase_terms USING fts5(
    termbase_id UNINDEXED,
    source_term,
    target_term,
    source_lang,
    target_lang,
    definition,
    domain,
    priority UNINDEXED,
    forbidden UNINDEXED,
    created_date UNINDEXED,
    modified_date UNINDEXED
)

-- Project-specific termbase activation
CREATE TABLE termbase_activation (
    project_id TEXT NOT NULL,
    termbase_id INTEGER NOT NULL,
    is_active INTEGER DEFAULT 1,
    PRIMARY KEY (project_id, termbase_id)
)
```

**Key Classes:**
- `TermbaseManager` - Database operations and term search
- `ReadOnlyGridTextEditor` - Source cell with highlighting, tooltip, and double-click
- `TermMetadataDialog` - Modal dialog for entering term metadata
- `find_termbase_matches_in_source()` - Search engine returning match dict
- `highlight_termbase_matches()` - Visual highlighting with priority/forbidden colors

### Documentation
- Added comprehensive termbase workflow documentation
- Updated keyboard shortcuts reference
- Documented color system and priority levels
- Added tooltip and double-click feature guides

---

## [1.5.1] - November 16, 2025

### ⌨️ Source/Target Tab Cycling for Termbase Workflow

**New Feature:**
- 🔄 **Tab Key Cycling** - Press `Tab` in target cell to jump to source cell, then `Tab` again to return to target
  - Enables fast termbase workflow: select term in source, Tab to target, select translation
  - Works bidirectionally: Target → Source → Target
  - Both source and target cells support text selection with keyboard and mouse
  - Arrow keys work in both cells for cursor movement
- 🔠 **Ctrl+Tab** - Insert actual tab character when needed (in both source and target)

**Technical Implementation:**
- Source cells (`ReadOnlyGridTextEditor`) now intercept Tab at the `event()` level for reliable cycling
- Target cells (`EditableGridTextEditor`) handle Tab in `keyPressEvent()`
- Text selection enabled in source cells via `TextSelectableByKeyboard | TextSelectableByMouse` flags
- Focus policy set to `StrongFocus` on both cell types

**Workflow Benefits:**
- Facilitates termbase entry: select source term → Tab → select target translation → add to termbase
- Maintains active text selections in both cells simultaneously for termbase operations
- No need to click between cells, keyboard-only navigation

---

## [1.5.0] - November 15, 2025

### 🔍 Translation Results Enhancement + Match Insertion Shortcuts

**Major Features:**
- 🎯 **Progressive Match Loading** - Termbase, TM, MT, and LLM results now accumulate instead of replacing each other
- ⌨️ **Match Navigation Shortcuts** - `Ctrl+Up/Down` to cycle through translation matches from the grid
- 🚀 **Quick Insert Shortcuts** - `Ctrl+1-9` to instantly insert specific matches at cursor position
- ⏎ **Smart Match Insertion** - `Ctrl+Space`, `Space`, or `Enter` in results panel to insert selected match
- 🏷️ **Tag Display Control** - Optional setting to show/hide HTML/XML tags in translation results (Settings → View Settings)
- 📊 **Status Management** - Manual edits now reset segment status to "Not started" requiring explicit confirmation

**Bug Fixes:**
- ✅ Fixed translation results panel showing only the last match type (now accumulates all: termbase → TM → MT → LLM)
- ✅ Fixed `add_matches()` method not found error (implemented progressive match accumulation)
- ✅ Fixed `save_mode` parameter errors in TM saving (removed deprecated parameter)
- ✅ Fixed match insertion not working (now correctly inserts at cursor position in target cell)
- ✅ Fixed `scroll_area` AttributeError (corrected to `matches_scroll`)

**Keyboard Shortcuts Added:**
- `Ctrl+Up` - Navigate to previous match in results panel
- `Ctrl+Down` - Navigate to next match in results panel
- `Ctrl+1` through `Ctrl+9` - Insert match #1-9 at cursor position
- `Ctrl+Space` - Insert currently selected match
- `Space` or `Enter` - Insert selected match (when focused on results panel)

**Documentation:**
- Updated shortcut manager with complete match navigation and insertion shortcuts
- Added comprehensive shortcut documentation in Settings → Shortcuts section

**Technical Improvements:**
- Implemented `add_matches()` method for progressive match accumulation
- Added `insert_match_by_number()` for direct match insertion by number
- Added `insert_selected_match()` for keyboard-driven match insertion
- Improved `on_match_inserted()` to insert at cursor position using `textCursor().insertText()`
- Added tag formatting control with `show_tags` class variable and `_format_text()` method

---

## [1.4.0] - November 12, 2025

### 🎤 Major Feature: Supervoice Voice Dictation + Detachable Log Window

**AI-Powered Hands-Free Translation Input** - OpenAI Whisper voice dictation with 100+ language support, plus multi-monitor log window capability.

### Added
- **🎤 Supervoice Voice Dictation Module**
  - AI-powered speech recognition using OpenAI Whisper
  - Support for 100+ languages (as many as Whisper can handle)
  - Press-to-start, press-to-stop recording with F9 global hotkey
  - 5 model sizes: tiny, base, small, medium, large (balance speed vs accuracy)
  - Configurable in Settings → 🎤 Supervoice
  - Automatic FFmpeg detection and bundling support
  - User-friendly error messages with installation instructions
  - Visual feedback: button color changes during recording
  - Seamless integration with segment editor and grid cells
  - Language auto-detection from project settings
  - Manual stop functionality (press F9 again to stop recording)
  - Future: Planned parallel dictation system for voice commands (confirm segment, go to top, filtering, workflow automation)

- **🪟 Detachable Log Window**
  - Log window can be detached into separate floating window
  - Perfect for multi-monitor setups
  - Synchronized auto-scroll between main and detached logs
  - "Detach Log" / "Attach Log" button in Settings
  - Remembers detached state across sessions
  - Independent positioning and sizing

- **📚 Comprehensive Documentation**
  - [VOICE_DICTATION_GUIDE.md](docs/VOICE_DICTATION_GUIDE.md) - Complete user guide
  - [VOICE_DICTATION_DEPLOYMENT.md](docs/VOICE_DICTATION_DEPLOYMENT.md) - Deployment options
  - [SUPERVOICE_TROUBLESHOOTING.md](docs/SUPERVOICE_TROUBLESHOOTING.md) - Troubleshooting guide
  - FFmpeg licensing information
  - Model selection recommendations
  - Corrupt model file recovery instructions

### Fixed
- **🐛 Voice Dictation Bug Fixes**
  - Fixed critical UnboundLocalError in `voice_dictation_lite.py:118` (duplicate `import os` statement)
  - Fixed language detection from project settings
  - Fixed button color restoration after recording
  - Fixed auto-scroll synchronization between log windows

### Changed
- **🔧 Version Update**
  - Updated version from 1.3.4 to 1.4.0
  - Updated all version strings in code and documentation
  - Updated window titles and welcome messages
  - Updated website (docs/index.html) with Supervoice module card
  - Updated hero badge to "v1.4.0 - Supervoice Voice Dictation"

### Technical
- New module: `modules/voice_dictation_lite.py` - Core dictation engine
- Enhanced `Supervertaler_Qt.py` - Integrated voice dictation and detachable log
- Updated `docs/index.html` - Added Supervoice feature highlight and module card
- Created FFmpeg detection and bundling infrastructure
- Whisper model caching in `%USERPROFILE%\.cache\whisper\`

---

## [1.3.3] - November 10, 2025

### 🏆 Major Feature: LLM Leaderboard + UI Standardization

**Translation Quality Benchmarking System** - Compare translation quality, speed, and cost across multiple LLM providers in a professional, standardized interface.

### Added
- **🏆 LLM Leaderboard Module** (Complete Implementation)
  - Benchmark translation quality across OpenAI, Claude, and Gemini models
  - chrF++ quality scoring for objective translation assessment
  - Speed and cost tracking for each translation
  - Multiple test datasets: Technical, Legal, Medical, Marketing (EN→NL, NL→EN)
  - Comprehensive Excel export with:
    - About sheet with clickable Supervertaler.com link
    - Summary sheet with rankings and statistics
    - Detailed results with all metrics
    - Dataset info in filename (e.g., `LLM_Leaderboard_Technical_EN-NL_20251110.xlsx`)
  - Auto-scrolling log for real-time progress monitoring
  - Standalone usage support with api_keys.example.txt template
  - Professional documentation in `modules/LLM_LEADERBOARD_STANDALONE.md`

- **🎨 Standardized Module Headers**
  - Consistent professional styling across all modules
  - Blue header color (#1976D2) matching Supervertaler branding
  - Light blue description boxes (#E3F2FD) with rounded corners
  - Trophy emoji 🏆 for LLM Leaderboard identity
  - Applied to: LLM Leaderboard, TMX Editor, AutoFingers, PDF Rescue

- **📊 Model Selection Enhancements**
  - Friendly model names in dropdowns (e.g., "GPT-5 (Reasoning)", "Claude Opus 4.1")
  - Support for latest models:
    - OpenAI: GPT-4o, GPT-4o Mini, GPT-5
    - Claude: Sonnet 4.5, Haiku 4.5, Opus 4.1
    - Gemini: 2.5 Flash, 2.5 Flash Lite, 2.5 Pro, 2.0 Flash (Exp)

### Fixed
- **🐛 LLM Leaderboard Bug Fixes**
  - Fixed Claude API call parameters (text vs custom_prompt)
  - Fixed Gemini API key mapping ("gemini" provider → "google" API key)
  - Fixed model dropdown display names (was showing generic names instead of selected models)
  - Fixed API key auto-creation from template file

### Changed
- **🔧 Excel Export Branding**
  - Title sheet matches UI header style with trophy emoji
  - Blue title color (#1976D2) for brand consistency
  - Clickable hyperlink to https://supervertaler.com/
  - Professional subtitle formatting

- **🔧 API Key Management**
  - Auto-creates `api_keys.txt` from `api_keys.example.txt` on first run
  - Supports standalone LLM Leaderboard usage outside Supervertaler

### Technical
- Enhanced `modules/llm_leaderboard.py` - Core benchmarking engine
- Enhanced `modules/superbench_ui.py` - Qt UI with standardized header
- Updated `modules/llm_clients.py` - Auto-create API keys functionality
- Updated `Supervertaler_Qt.py` - Gemini API key mapping fix
- Created `api_keys.example.txt` - Template for standalone usage
- Created `modules/LLM_LEADERBOARD_STANDALONE.md` - Complete documentation

---

## [1.3.2] - November 9, 2025

### 🎯 Major Feature: Segment-Level AI Access + Critical Bug Fix

**AI Assistant can now access and query individual segments from your translation project**

### Added
- **🔢 Segment-Level AI Actions** (Phase 2 Enhancement)
  - `get_segment_count` - Get total segments and translation progress
  - `get_segment_info` - Query specific segments by ID, multiple IDs, or range
  - AI can answer "How many segments?" and "What is segment 5?"
  - First 10 segments automatically included in AI context
  - Full segment properties: id, source, target, status, type, notes, match_percent, etc.

- **📊 Segment Information Display**
  - AI Assistant shows segment details in formatted chat bubbles
  - HTML entity escaping for CAT tool tags (`<tag>`, `&nbsp;`, etc.)
  - Proper handling of Trados, memoQ, Wordfast, CafeTran tags
  - Segments displayed in code blocks for readability

- **⚙️ Auto-Markdown Generation Setting**
  - Optional setting in Settings → General → AI Assistant Settings
  - "Auto-generate markdown for imported documents" checkbox
  - Automatically converts DOCX/PDF to markdown on import
  - Markdown saved to `user_data_private/AI_Assistant/current_document/`
  - Includes metadata JSON with conversion info

### Fixed
- **🐛 CRITICAL: Current Document Not Showing After Import**
  - Fixed attribute name mismatch: `self.prompt_manager` → `self.prompt_manager_qt`
  - Current document now appears in AI Assistant sidebar after import
  - Auto-markdown generation now triggers correctly
  - Context refresh now works properly

### Changed
- **🔧 AI Assistant Context Building** (`modules/unified_prompt_manager_qt.py`)
  - Added `_get_segment_info()` method for structured segment data
  - Added `generate_markdown_for_current_document()` public method
  - Modified context building to prioritize segment-level access
  - Document content fallback when segments unavailable

- **🔧 AI Actions System** (`modules/ai_actions.py`)
  - Added `parent_app` parameter to constructor
  - Added segment action handlers with full validation
  - Enhanced `format_action_results()` with segment display logic
  - Comprehensive HTML entity escaping (order-aware to prevent double-escaping)

- **🔧 Main Application** (`Supervertaler_Qt.py`)
  - Added auto-markdown setting to Settings UI
  - Setting persists in `ui_preferences.json`
  - Document import triggers markdown generation when enabled
  - Context refresh called after document import

### Technical
- **Segment Access Order:**
  1. `project.segments` - Full segment objects (PREFERRED)
  2. `parent_app.segments` - Currently loaded segments
  3. `project.source_segments` - Project source text
  4. Cached markdown conversion
  5. On-demand file conversion with markitdown

- **HTML Escaping Order:** `&` → `<` → `>` → `"` (prevents double-escaping)
- **Segment Data Structure:** Full dataclass with 12 properties per segment

### Testing
- ✅ Updated test suite (`test_ai_actions.py`)
- ✅ Added Test 9: get_segment_count action
- ✅ Added Test 10: get_segment_info action (single, multiple, range)
- ✅ All 10 tests passing

### Documentation
- Updated `docs/AI_ASSISTANT_INTEGRATION.md` with segment access details
- Added segment action examples and use cases
- Updated troubleshooting section

### Benefits
- ✅ **Segment-specific queries** - AI can find and analyze specific segments
- ✅ **Translation progress tracking** - AI reports completion status
- ✅ **CAT tool tag handling** - All tag types properly escaped and displayed
- ✅ **Auto-markdown option** - Users control document conversion
- ✅ **Fixed critical bug** - Current document now shows correctly

---

## [1.3.1] - November 9, 2025

### ✨ Major Feature: AI Assistant File Attachment Persistence (Phase 1)

**Complete persistent storage system for AI Assistant file attachments with view/manage UI**

### Added
- **📎 AttachmentManager Module** (`modules/ai_attachment_manager.py` - 390 lines)
  - Complete persistent storage system for attached files
  - Session-based organization (files grouped by date)
  - Master index tracking all attachments across sessions
  - Metadata storage with JSON (original name, path, type, size, date)
  - Full CRUD operations: attach, get, list, remove files
  - Statistics tracking (total files, size, sessions)

- **👁️ File Viewer Dialogs** (`modules/ai_file_viewer_dialog.py` - 160 lines)
  - FileViewerDialog - displays file content with metadata
  - Read-only markdown preview with monospace font
  - Copy to clipboard functionality
  - FileRemoveConfirmDialog - confirmation before deletion

- **🎨 Expandable Attached Files Panel** (AI Assistant context sidebar)
  - Collapsible "📎 Attached Files" section with expand/collapse button (▼/▶)
  - Dynamic file list showing name, type, size for each file
  - View button (👁) - opens file viewer dialog
  - Remove button (❌) - deletes from disk with confirmation
  - + button to attach new files
  - Auto-refresh on file operations

### Changed
- **🔧 AI Assistant Integration** (`modules/unified_prompt_manager_qt.py`)
  - Initialized AttachmentManager in `__init__`
  - Modified `_attach_file()` to save files to persistent storage
  - Added `_load_persisted_attachments()` method - loads files on startup
  - Created `_create_attached_files_section()` - expandable panel UI
  - Added `_refresh_attached_files_list()` - dynamic file list updates
  - Added `_create_file_item_widget()` - individual file items with buttons
  - Added `_view_file()` - opens FileViewerDialog
  - Added `_remove_file()` - removes from disk and memory
  - Added `_toggle_attached_files()` - expand/collapse functionality
  - Updated `_update_context_sidebar()` to refresh file list
  - Updated `_load_conversation_history()` to refresh UI after load

### Technical
- **Storage Structure:**
  - Base: `user_data_private/AI_Assistant/`
  - Attachments: `attachments/{session_id}/{file_hash}.md`
  - Metadata: `attachments/{session_id}/{file_hash}.meta.json`
  - Master index: `index.json`
- **Session Management:** Date-based sessions (YYYYMMDD format)
- **File Hashing:** SHA256-based unique IDs (path_hash + content_hash)
- **Backward Compatibility:** Old `self.attached_files` list still maintained

### Testing
- ✅ Created comprehensive test suite (`test_attachment_manager.py`)
- ✅ All 8 tests passing (imports, init, session, attach, list, get, stats, remove)
- ✅ UTF-8 console output handling for Windows

### Benefits
- ✅ **Files no longer lost** when application closes
- ✅ **Users can view** attached files anytime via viewer dialog
- ✅ **Users can remove** unwanted files with confirmation
- ✅ **Session organization** keeps files organized by date
- ✅ **Persistent across app restarts** - automatic reload on startup

### Documentation
- Updated `docs/PROJECT_CONTEXT.md` with Phase 1 implementation details
- Created `docs/AI_ASSISTANT_ENHANCEMENT_PLAN.md` with full specification
- Updated website (`docs/index.html`) to reflect new features

### Next
- Phase 2: AI Actions System (allow AI to create/modify prompts in library)

---

## [1.2.2] - November 6, 2025

### 🎨 Major Enhancement: Translation Results, Document Formatting & Tag System

**Fixed translation results display, enhanced document view with formatting, and activated the tag system!**

### Fixed
- **🐛 Translation Results Panels Not Working** - CRITICAL FIX
  - Removed lingering `assistance_widget` references that blocked match processing
  - Fixed termbase, TM, MT, and LLM matches not displaying in panels
  - Updated all 6 locations where matches were being set to use `results_panels`
  - All three views (Grid, List, Document) now show matches correctly

- **🐛 Menu Bar Blocked by Error Indicator** 
  - Removed 15+ obsolete `assistance_widget` references causing Qt errors
  - Fixed red error triangle that blocked File and Edit menus
  - Updated zoom functions, font settings, and close project cleanup

### Added
- **✅ Document View Formatting**
  - Renders inline formatting tags: `<b>bold</b>`, `<i>italic</i>`, `<u>underline</u>`, `<bi>bold+italic</bi>`
  - New list item tag: `<li>content</li>` renders with orange bullet (•)
  - Proper QTextCharFormat application for bold, italic, underline
  - Tag parsing with formatting stack for nested tags

- **✅ Enhanced Type Column**
  - Shows **H1, H2, H3, H4** for heading levels (blue background)
  - Shows **Title** for document titles
  - Shows **Sub** for subtitles
  - Shows **li** for list items (green background)
  - Shows **¶** for regular paragraphs
  - Color-coded for easy document structure visualization

- **✅ List Item Tag System**
  - DOCX import detects bullets and numbered lists
  - Automatically wraps list items in `<li>` tags
  - Detection works on Word numbering format, bullet characters, and numbered prefixes
  - Tags preserved through translation and export workflow

### Technical
- Updated `tag_manager.py` to support `<li>` tag (TAG_PATTERN regex)
- Enhanced `docx_handler.py` to detect and tag list items during import
- Document view parses tags and renders with proper formatting
- Type column detects `<li>` tags, heading styles, and text patterns
- Tag colors: Bold=#CC0000, Italic=#0066CC, Underline=#009900, BoldItalic=#CC00CC, ListItem=#FF6600

---

## [1.2.1] - November 6, 2025

### 🎨 UI Enhancement: Unified Tabbed Interface

**Added consistent tabbed panel structure to both Grid and List views for improved workflow!**

### Added
- **✅ Tabbed Panel in Grid View**
  - Tab 1: Translation Results (TM, MT, LLM, Termbase matches)
  - Tab 2: Segment Editor (source/target editing, status selector)
  - Tab 3: Notes (segment notes with save functionality)
  - Enables segment editing directly in Grid View (like Tkinter edition)

- **✅ Tabbed Panel in List View**
  - Same 3-tab structure as Grid View for consistency
  - Translation Results | Segment Editor | Notes
  - Replaces single-panel layout with flexible tabbed interface

- **✅ Synchronized Panel Updates**
  - Clicking segment in any view updates ALL tabs in ALL views
  - Editing in any panel automatically syncs to other panels
  - Prevents infinite loops with signal blocking
  - Multiple independent widget instances for Grid/List views

### Fixed
- **🐛 Widget Parenting Issues** - Fixed Qt single-parent constraint violations
  - Created separate TranslationResultsPanel instances for each view
  - Stored widget references on panel objects for flexible access
  - Maintains `results_panels` and `tabbed_panels` lists for batch updates

- **🐛 Signal Handler Crashes** - Fixed AttributeError when editing segments
  - Updated `on_tab_target_change()`, `on_tab_segment_status_change()`, `on_tab_notes_change()`
  - Handlers now iterate all panels instead of accessing non-existent attributes
  - Proper error handling per panel to prevent cascade failures

### Technical
- Unified panel creation via `create_tabbed_assistance_panel()`
- Widget reference storage pattern: `panel.editor_widget.source_editor`
- Centralized update function: `update_tab_segment_editor()` iterates all panels
- Signal blocking prevents infinite update loops during synchronization

---

## [1.2.0] - November 6, 2025 🎉

### 🎯 MAJOR RELEASE: Complete Translation Matching System

**The Supervertaler CAT tool now provides comprehensive translation assistance with all match types working together!**

### Added
- **✅ Google Cloud Translation API Integration**
  - Machine translation matches displayed alongside TM and LLM results
  - Uses Google Translate REST API v2 for direct API key authentication
  - Automatic language detection support
  - High-quality neural machine translation
  - Provider badge: "MT" in match display

- **✅ Multi-LLM Support (OpenAI, Claude, Gemini)**
  - **OpenAI GPT** integration (GPT-4o, GPT-5, o1, o3)
  - **Claude 3.5 Sonnet** integration (Anthropic)
  - **Google Gemini** integration (Gemini 2.0 Flash, 1.5 Pro)
  - All three LLM providers work simultaneously
  - Each provides translations with confidence scores
  - Provider badges: "OA" (OpenAI), "CL" (Claude), "GM" (Gemini)

- **✅ Complete Match Chaining System**
  - **Termbase matches** → Displayed immediately (yellow highlight)
  - **TM matches** → Displayed after 1.5s delay (prevents excessive API calls)
  - **MT matches** → Google Translate integrated in delayed search
  - **LLM matches** → All enabled LLMs called in parallel
  - All match types preserved and displayed together in Translation Results Panel

- **✅ Flexible API Key Management**
  - Supports both `google` and `google_translate` key names for Google Cloud Translation
  - Supports both `gemini` and `google` key names for Gemini API
  - Backward compatibility with existing configurations
  - Standalone `load_api_keys()` function in `modules/llm_clients.py`

### Fixed
- **🐛 Termbase Match Preservation** - Termbase matches no longer disappear when TM/MT/LLM results load
  - Root cause: Delayed search wasn't receiving termbase matches parameter
  - Solution: Pass `current_termbase_matches` to `_add_mt_and_llm_matches()`
  - Termbase matches now persist throughout the entire search process

- **🐛 Google Translate Authentication** - Fixed "Client.__init__() got an unexpected keyword argument 'api_key'"
  - Switched from google-cloud-translate SDK to direct REST API calls
  - Simpler authentication using API key in URL parameters
  - More reliable and easier to configure

- **🐛 Gemini Integration** - Gemini now properly called when using `google` API key
  - Added fallback to check both `gemini` and `google` key names
  - Fixed LLM wrapper to support Google's API key for Gemini

### Technical Implementation
- **File: `modules/llm_clients.py`**
  - Added standalone `load_api_keys()` function (lines 27-76)
  - Fixed `get_google_translation()` to use REST API instead of SDK
  - Backward compatible API key naming (checks multiple key names)
  - Module can now operate independently without main application

- **File: `Supervertaler_Qt.py`**
  - Enhanced `_add_mt_and_llm_matches()` with comprehensive logging
  - Fixed Gemini integration to check both key naming conventions
  - Improved match chaining with proper termbase preservation
  - Debounced search (1.5s delay) prevents excessive API calls

### Performance Optimizations
- **Debounced Search** - 1.5-second delay before calling TM/MT/LLM APIs
- **Timer Cancellation** - Previous searches cancelled when user moves to new segment
- **Immediate Termbase Display** - Termbase matches shown instantly (no delay)
- **Parallel LLM Calls** - All LLM providers called simultaneously for faster results

### Dependencies
- `requests` - For Google Translate REST API calls (standard library)
- `openai` - OpenAI GPT integration
- `anthropic` - Claude integration
- `google-generativeai` - Gemini integration
- `httpx==0.28.1` - HTTP client (version locked for LLM compatibility)

### Documentation
- Updated `docs/PROJECT_CONTEXT.md` with November 6, 2025 development activity
- Documented all LLM & MT integration details
- Listed resolved issues and technical decisions

### Match Display
All match types now display in the Translation Results Panel:
- **Termbases** (Yellow section) - Term matches from termbase databases
- **Translation Memory** (Blue section) - Fuzzy matches from TM database
- **Machine Translation** (Orange section) - Google Cloud Translation
- **LLM** (Purple section) - OpenAI GPT, Claude, and/or Gemini translations

Each match shows:
- Provider badge (NT/TM/MT/OA/CL/GM)
- Relevance percentage (0-100%)
- Target translation text
- Source context (when available)

---

## [1.1.9] - November 6, 2025

### Added
- **⌨️ Keyboard Shortcuts Manager** - Comprehensive keyboard shortcuts management system
  - New Settings tab: "⌨️ Keyboard Shortcuts"
  - View all 40+ keyboard shortcuts organized by category (File, Edit, Translation, View, Resources, Match Insertion, etc.)
  - Search/filter shortcuts by action, category, or key combination
  - Edit shortcuts with custom key capture widget
  - Conflict detection with warnings
  - Reset individual shortcuts or all shortcuts to defaults
  - Export shortcuts to JSON (share with team)
  - Import shortcuts from JSON
  - **Export HTML Cheatsheet** - Beautiful, printable keyboard reference with professional styling
  - Modular architecture: `modules/shortcut_manager.py` and `modules/keyboard_shortcuts_widget.py`

### Technical Details
- **ShortcutManager** class - Backend logic for managing shortcuts
- **KeyboardShortcutsWidget** - Full-featured UI for Settings tab
- **KeySequenceEdit** - Custom widget for capturing key presses
- **Conflict detection** - Real-time warnings for duplicate shortcuts
- **Context-aware shortcuts** - Different contexts (editor, grid, match panel) to prevent conflicts
- Data stored in `user_data/shortcuts.json`

### Documentation
- Added `Keyboard_Shortcuts_Implementation.md` in development docs
- Added `Competitive_Analysis_CotranslatorAI.md` in development docs

### Improved
- **Repository Philosophy** - Continued modular architecture to keep main file maintainable
- **AI-Friendly Codebase** - Complex features extracted to focused modules (easier for AI agents to understand)

---

## [1.1.8] - November 5, 2025

### Fixed
- **🎯 Prompt Generation (CRITICAL FIX):** Fixed incomplete prompt generation in Prompt Assistant
  - **Root Cause:** Using `client.translate()` for text generation instead of proper chat completion API
  - **Solution:** Switched to direct LLM API calls (OpenAI/Claude/Gemini) with proper message structure
  - Domain Prompts now generate complete 3-5 paragraph prompts (was 2 sentences)
  - Project Prompts now include full termbase tables + intro/closing paragraphs (was partial/truncated)
  - Added truncation detection and warnings for all providers
  - Temperature set to 0.4 for creative generation (was 0.3)
  - Max tokens set to 8000 (with full flexibility, not constrained by translation wrapper)
- **Documentation:** Added complete debugging session documentation (docs/2025-11-05.md)

### Technical Details
- Removed hybrid approach (programmatic termbase extraction + AI generation)
- Reverted to pure AI-only approach matching working tkinter version
- Direct API calls now match tkinter implementation exactly:
  - OpenAI: `chat.completions.create()` with system/user messages
  - Claude: `messages.create()` with proper system parameter
  - Gemini: `generate_content()` with combined prompt
- All providers now check `finish_reason`/`stop_reason` for truncation

### Impact
- **Generate Prompts** feature now works perfectly, producing complete professional prompts
- Critical feature that was broken is now fully functional
- Matches quality and completeness of tkinter version

---

## [1.1.7] - November 4, 2025

### Major Changes
- **🏠 Home Screen Redesign:** Complete restructuring of the primary workspace
  - Editor (Grid/List/Document views) on the left with Prompt Manager on the right
  - Resizable horizontal splitter between editor and prompt manager
  - Translation results panel moved to bottom of grid in compact form
  - Real-time prompt tweaking while viewing changes in the grid
  - Removed separate Editor and Prompt Manager tabs (integrated into Home)

### Strategic Refocus
- **🎯 Companion Tool Philosophy:** Pivoted from full CAT tool to companion tool
  - Grid simplified for viewing/reviewing (minor edits only)
  - Focus on AI-powered features and specialized modules
  - Documentation updated to reflect companion tool approach

### Added
- **Custom Styled Widgets:** Beautiful checkboxes and radio buttons with white checkmarks
  - `CheckmarkCheckBox` class for all checkboxes
  - `CustomRadioButton` class for LLM Provider selection
  - Square indicators with green background when checked, white checkmark overlay
- **Prompt Manager Enhancements:**
  - Preview Combined Prompt button shows exact prompt sent to AI
  - Deactivate buttons for Domain and Project prompts
  - Prompt Assistant tab moved to first position

### Improved
- **Grid Simplification:**
  - Double-click only editing (removed F2 key) - companion tool philosophy
  - Simplified styling with subtle colors for review-focused interface
  - Light blue selection highlight instead of bright blue
- **Segment Number Styling:**
  - All segment numbers start with black foreground
  - Only selected segment number highlighted in orange (like memoQ)
  - Fixed black numbers issue after navigation

### Fixed
- **Filter Crash:** Added safety checks for table and filter widgets
- **removeWidget Error:** Fixed QSplitter widget removal (use setParent instead)
- **Project Loading:** Fixed doc_segment_widgets AttributeError
- **Translation Results Panel:** Now properly visible at bottom of grid

### Technical
- Improved widget reparenting logic for splitter management
- Enhanced error handling in filter operations
- Better initialization of view state variables

---

## [1.1.6] - November 3, 2025

### Added
- **🔍 Detachable Universal Lookup:** Multi-screen support for Universal Lookup module
  - Detach button on Home tab to open Universal Lookup in separate window
  - Perfect for multi-monitor workflows - move lookup to second screen while translating
  - Proper window positioning and multi-monitor detection
  - Reattach functionality to return to embedded mode

### Improved
- **🏠 Home Tab Enhancements:**
  - Integrated About section directly into header with improved visibility
  - Better text styling with purple gradient for subtitle and version (larger, bold)
  - Reorganized layout: About in header, Resources & Support next, Projects at bottom
  - Projects section with distinct background color for visual separation
  - Universal Lookup prominently featured on right side of Home tab

### Fixed
- **Multi-Monitor Support:** Fixed window positioning for detached Universal Lookup
  - Correct screen detection using `QApplication.screenAt()` API
  - Proper window activation and focus handling
  - Window flags configured for proper minimize/maximize behavior
  - Improved error handling for window detachment process

### Technical
- Updated window positioning logic for Qt6 compatibility
- Enhanced screen detection for multi-monitor setups
- Improved window activation using QTimer for reliable focus management

---

## [1.1.5] - November 2, 2025

### Added
- **🏠 New Home Tab:** Brand new first-screen experience
  - Integrated About section with version info and purple gradient header
  - Quick access to resources (Website, GitHub, Discussions, Documentation)
  - Project management panel for recent projects
  - Embedded Universal Lookup for instant translations
  - Clean, modern design with proper visual hierarchy
  
- **Major UI Reorganization:** Complete restructuring of main interface
  - **Tab Order Redesigned:** 
    1. 🏠 Home (NEW - welcome screen)
    2. 💡 Prompt Manager (moved up from #5)
    3. 📝 Editor (renamed from "Project Editor")
    4. 📚 Resources (organized nested tabs)
    5. 🧩 Modules (renamed from "Specialised Modules")
    6. ⚙️ Settings (moved from Tools menu, includes Log)
  - **Navigation Menu:** Added "Go to Home" action (🏠 Home menu item)
  - **Removed Quick Access Sidebar:** Functionality integrated into Home tab
  - Cleaner, more intuitive workflow with logical feature grouping

- **Multiple View Modes:** Three different ways to view and edit your translation project
  - **Grid View (Ctrl+1):** Spreadsheet-like table view - perfect for quick segment-by-segment editing
  - **List View (Ctrl+2):** Segment list on left, editor panel on right - ideal for focused translation work
  - **Document View (Ctrl+3):** Natural document flow with clickable segments - great for review and context
  - View switcher toolbar with quick access buttons
  - All views share the same translation results pane (TM, LLM, MT, Termbase matches)
  - All views stay synchronized - changes in one view instantly reflected in others
  - Keyboard shortcuts (Ctrl+1/2/3) for rapid view switching

### Improved
- **Translation Results Pane:** Now visible and functional in all three view modes
  - Properly integrated into Grid, List, and Document views
  - Dynamic reparenting when switching between views
  - Consistent assistance panel across all view modes

### Technical
- **View Management:** Implemented QStackedWidget architecture for seamless view switching
  - Each view maintains its own splitter layout
  - Shared assistance widget dynamically moved between views
  - Clean separation of view-specific logic

---

## [1.1.4] - November 2, 2025

### Added
- **Encoding Repair Tool:** Full port from tkinter edition with standalone capability
  - Detect and fix text encoding corruption (mojibake) in translation files
  - Scan single files or entire folders recursively
  - Automatic backup creation (.backup files) before repair
  - Supports common corruption patterns (en/em dashes, quotes, ellipsis, bullets, etc.)
  - Clean Qt interface matching other modules (PDF Rescue, TMX Editor style)
  - **Standalone Mode:** Run independently with `python modules/encoding_repair_Qt.py`
  - **Embedded Mode:** Integrated as a tab in Supervertaler Qt
  - Test file available at `docs/tests/test_encoding_corruption.txt` for user testing

### Improved
- **Prompt Manager:** Fixed System Prompts tab to show list widget (matching Domain Prompts layout)
  - Added proper list/editor splitter layout for consistency
  - System Prompts now use shared editor panel with metadata fields hidden
  - Better visual consistency across all prompt tabs

### Fixed
- **About Dialog:** Updated with clickable website link (https://supervertaler.com/)
  - Changed description from "Professional Translation Memory & CAT Tool" to "AI-powered tool for translators & writers"
  - Improved dialog layout with better formatting

### Technical
- **Module Architecture:** Created `encoding_repair_Qt.py` as standalone, reusable module
  - Uses existing `encoding_repair.py` backend (shared with tkinter version)
  - Proper path handling for standalone execution
  - Consistent with other Qt modules (PDF Rescue, TMX Editor patterns)

---

## [1.1.3] - November 2, 2025

### Added
- **Prompt Manager:** Complete 4-Layer Prompt Architecture system integrated into Qt Edition
  - **Layer 1 - System Prompts:** Editable infrastructure prompts (CAT tags, formatting rules, language conventions)
  - **Layer 2 - Domain Prompts:** Domain-specific translation expertise (Legal, Medical, Technical, Financial, etc.)
  - **Layer 3 - Project Prompts:** Client and project-specific instructions and rules
  - **Layer 4 - Style Guides:** Language-specific formatting guidelines (numbers, dates, typography)
  - **Prompt Assistant:** AI-powered prompt refinement using natural language (unique to Supervertaler!)
  - **Full UI Integration:** Beautiful tab interface with activation system and preview
  - **Standardized Headers:** Consistent UI/UX matching other modules (TMX Editor, PDF Rescue, AutoFingers)
  - **Import/Export:** Save, reset, import, and export prompts for sharing and backup

### Website
- **4-Layer Architecture Documentation:** Comprehensive new section on website explaining the unique approach
- **Visual Design:** Color-coded layer cards with detailed explanations
- **Navigation:** Added dedicated navigation link for Architecture section
- **Hero Section:** Updated badges and feature highlights to showcase new architecture
- **Footer Links:** Integrated architecture documentation into site navigation

### Technical
- **Terminology Standardization:** Renamed all infrastructure/Custom Instructions references to System/Project Prompts
- **Code Quality:** Systematic refactoring with consistent naming conventions throughout
- **Module Architecture:** `prompt_manager_qt.py` created as standalone, reusable module
- **Backward Compatibility:** Maintained compatibility with existing prompt library files

---

## [1.1.2] - November 1, 2025

### Improved
- **PDF Rescue:** Simplified to OCR-only mode (removed dual-mode complexity)
  - Removed text extraction mode and 504 lines of complex layout detection code
  - Reverted to simple, reliable image-based OCR workflow
  - Updated UI description to clarify OCR-only purpose
  - Better results with simpler approach

### Fixed
- **PDF Rescue Prompt:** Restored original concise prompt that produced better OCR results
  - Removed verbose "CRITICAL ACCURACY RULES" that degraded performance
  - Simplified instructions for clearer AI guidance
  - Improved OCR accuracy with focused prompts

- **PDF Rescue DOCX Export:** Fixed excessive line breaks in Word documents
  - Changed paragraph detection from single newlines to double newlines
  - Single newlines now treated as spaces within paragraphs
  - Reduced paragraph spacing from 12pt to 6pt for tighter layout
  - Applied fix to both formatted and non-formatted export modes

### Added
- **PDF Rescue Branding:** Added clickable hyperlink in DOCX exports
  - "Supervertaler" text now links to https://supervertaler.com/
  - Professional branding with working hyperlinks in Word documents

- **Website Navigation:** Added "Modules" link to header navigation
  - Appears after "Features" in main menu
  - Provides direct access to modules documentation

### Removed
- **Website:** Removed "AI-First Philosophy" section (93 lines)
  - Streamlined website content
  - Removed from navigation menu
  - Content deemed redundant with other sections

---

## [1.1.1] - November 1, 2025

### Improved
- **AutoFingers Settings:** Simplified behavior settings by removing redundant "Use Alt+N" checkbox
  - Now uses single "Confirm segments" checkbox: checked = Ctrl+Enter (confirm), unchecked = Alt+N (skip confirmation)
  - More intuitive UI with clearer label and comprehensive tooltip
  - Maintains backward compatibility with existing settings files

---

## [1.1.0] - November 1, 2025

### Added
- **TMX Editor:** Professional translation memory editor integrated into Qt Edition
  - **Database-Backed TMX System:** Handle massive TMX files (1GB+) with SQLite backend
  - **Dual Loading Modes:** Choose RAM mode (fast for small files) or Database mode (handles any size)
  - **Smart Mode Selection:** Auto mode intelligently selects best loading method based on file size
  - **Inline Editing:** Edit source and target text directly in the grid (no popup dialogs)
  - **Real-time Highlighting:** Search terms highlighted with green background (Heartsome-style)
  - **Heartsome-Inspired UI:** Three-panel layout with top header (language selectors + filters), center grid, and right attributes panel
  - **Filtering:** Advanced search with case-insensitive matching and tag filtering
  - **Pagination:** Efficient 50 TUs per page for smooth performance
  - **Export/Import:** Save edited TMX files and export to new files
  - **Progress Indicators:** Clear progress bars with batch operations for fast loading
  - **Custom Checkboxes:** Consistent green checkmark style matching AutoFingers design

### Improved
- **Database Integration:** New TMX database tables (`tmx_files`, `tmx_translation_units`, `tmx_segments`) with foreign keys and indexes
- **Batch Operations:** Database commits every 100 TUs for 10-50x faster loading performance
- **UI Consistency:** Mode selection dialog uses custom CheckmarkCheckBox style throughout
- **Progress Feedback:** Immediate progress bar display with clearer blue styling

### Technical
- **Database Schema:** Added three new tables for TMX storage with proper indexing
- **Mode Detection:** Automatic recommendation based on file size thresholds (50MB, 100MB)
- **Transaction Management:** Optimized database operations with batch commits
- **Memory Efficiency:** Database mode frees RAM immediately after loading

---

## [1.0.2] - October 31, 2025

### Fixed
- **Broken Emoji Icons:** Fixed broken emoji characters in tab labels for Termbases (🏷️), Prompt Manager (💡), Encoding Repair (🔧), and Tracked Changes (🔄)
- **Checkbox Rendering:** Improved checkmark visibility on small displays with better padding and scaling

### Added
- **Startup Settings:** Added option to automatically restore last opened project on startup (Tools → Options → General → Startup Settings)
- **Font Size Persistence:** Added font size settings panel (Tools → Options → View/Display Settings) to save and restore:
  - Grid font size (7-72 pt)
  - Match list font size (7-16 pt)
  - Compare boxes font size (7-14 pt)
- **Auto-Save Font Sizes:** Font sizes are automatically saved when adjusted via zoom controls (Ctrl++/Ctrl+- for grid, Ctrl+Shift++/Ctrl+Shift+- for results pane)

### Improved
- **Checkbox Styling:** Implemented custom green checkboxes with white checkmarks (Option 1 style) for AutoFingers Behavior section - more intuitive than previous blue/white design
- **AutoFingers Layout:** Reorganized Settings section into 2-column grid layout (Languages/Timing on left, Behavior/Save on right) for better organization
- **Small Screen Support:** Moved Activity Log to right side of Settings for improved space utilization on laptop displays

---

## [1.0.1] - October 29, 2025

### Fixed
- **Terminology Standardization:** Replaced all "glossary" references with "termbase" throughout codebase
- **Database Schema:** Fixed NOT NULL constraint errors on `termbase_terms.source_lang` and `termbase_terms.target_lang` (changed to `DEFAULT 'unknown'`)
- **Method Naming:** Renamed `create_glossary_results_tab()` → `create_termbase_results_tab()`
- **Project Object Access:** Fixed Project attribute access patterns (changed from dict `.get()` to object attribute `.id`)
- **Tab Label:** Updated from "Term Bases" → "Termbases" (single word)

### Changed
- **Database Tables:** Renamed `glossary_terms` → `termbase_terms`, `glossary_id` → `termbase_id`
- **SQL Queries:** Updated all queries to use new table/column names

### Added
- **Sample Data:** Created 3 test termbases (Medical, Legal, Technical) with 48 total terms for testing

---

## [1.0.0] - October 28, 2025

### Added
- **Qt Edition Launch:** Initial release of PyQt6-based modern CAT interface
- **Translation Memory:** Full-text search with fuzzy matching and relevance scoring
- **Termbases:** Multiple termbase support with global and project-specific scopes
- **CAT Editor:** Segment-based translation editing interface
- **Project Management:** Create, manage, and switch between translation projects
- **Auto-fingers:** Smart terminology suggestions based on context
- **AI Integration:** OpenAI GPT and Claude support with configurable API keys
- **Database Backend:** SQLite persistent storage with 7 core tables

---

## Versioning Strategy

- **Major.Minor.Patch** (e.g., 1.0.1)
  - **Major:** Significant architecture changes or breaking changes
  - **Minor:** New features or substantial improvements
  - **Patch:** Bug fixes and minor adjustments

---

## Future Roadmap

### Planned for v1.1.0
- Terminology Search (Ctrl+P)
- Concordance Search (Ctrl+K)
- Create/Edit termbase dialogs

### Planned for v1.2.0
- TMX Editor with visual highlighting
- Advanced filtering options
- Custom keyboard shortcuts

### Planned for v2.0.0
- Full feature parity with Tkinter edition
- Deprecation of Tkinter edition

---

**Note:** This changelog focuses exclusively on the Qt Edition. See [CHANGELOG_Tkinter.md](CHANGELOG_Tkinter.md) for Classic edition history.

**Last Updated:** October 30, 2025
- ✅ Fixed Project object access pattern (changed from dict `.get()` to object attributes)
- ✅ Fixed database schema issues in private database folder

### 📋 Terminology Standardization
- Replaced all "glossary" references with "termbase" throughout codebase
- Updated database table: `glossary_terms` → `termbase_terms`
- Updated column: `glossary_id` → `termbase_id`
- Unified UI labels to use "Termbases" (one word, consistent)
- **Files Updated**: 5+ Python files, database schema, UI labels

### 🎯 Known Issues
- Terminology Search (Ctrl+P) - Planned for next release
- Concordance Search (Ctrl+K) - Planned for next release

---

## [v1.0.0] - 2025-10-29 🎯 Phase 5.3 - Advanced Ribbon Features Complete

### 🎨 Major UX Enhancements - ALL 5 FEATURES IMPLEMENTED

**1. ✅ Context-Sensitive Ribbon**
- Ribbon automatically switches based on active tab
- Universal Lookup tab → Shows Translation ribbon
- Project Editor tab → Shows Home ribbon
- Intelligent tab selection for better workflow

**2. ✅ Quick Access Toolbar (QAT)**
- Mini toolbar above ribbon with most-used commands
- **Actions**: New 📄, Open 📂, Save 💾, Universal Lookup 🔍, Translate 🤖
- **Minimize Ribbon toggle** ⌃ - Collapse ribbon to tabs-only
- Always visible for quick access to favorites
- Icon-only buttons for compact display

**3. ✅ Quick Access Sidebar** (NEW)
- memoQ-style left navigation panel
- **Collapsible sections**:
  - **Quick Actions**: New, Open, Save
  - **Translation Tools**: Universal Lookup, AutoFingers, TM Manager
  - **Recent Files**: Double-click to open
- Resizable via splitter
- Toggle on/off via View menu

**4. ✅ Ribbon Minimization**
- Minimize ribbon to tabs-only mode (saves vertical space)
- Click tabs to show ribbon temporarily
- Toggle via ⌃ button in QAT

**5. ✅ Ribbon Customization Foundation**
- Signal-based architecture for easy customization
- Action mapping system for flexibility
- Extensible group/button structure

### 📦 New Modules
- `modules/quick_access_sidebar.py` - Reusable sidebar components
- `modules/project_home_panel.py` - Project-specific home panel

### 🔧 Technical Improvements
- Renamed splitters for clarity (sidebar_splitter, editor_splitter)
- Connected sidebar actions to ribbon action handler
- Automatic recent files update
- Context-sensitive ribbon switching
- Professional multi-panel layout

---

## [v1.0.0 - Phase 5.2] - 2025-10-29 🎨 Ribbon Interface - Modern CAT UI

### ✨ Major Features
- ✅ **Modern Ribbon Interface** - Similar to memoQ, Trados Studio, Microsoft Office
- ✅ **Four Ribbon Tabs**:
  - **Home**: New, Open, Save, Copy, Paste, Find, Replace, Go To
  - **Translation**: Translate, Batch Translate, TM Manager, Universal Lookup
  - **View**: Zoom In/Out, Auto-Resize Rows, Themes
  - **Tools**: AutoFingers, Options
- ✅ **Grouped Buttons** - Related functions organized into visual groups
- ✅ **Emoji Icons** - Clear, colorful visual indicators
- ✅ **Hover Effects** - Modern button styling with transparency and borders
- ✅ **Full Integration** - All actions connected to existing functionality

### 🎯 Architecture
- Created `modules/ribbon_widget.py` - Reusable ribbon components
- Tab-based ribbon system with dynamic button groups
- Action signals connected to main window handlers
- Professional styling matching modern CAT tools

---

## [v1.0.0 - Phase 5.1] - 2025-10-28 📊 Translation Results Panel Complete

### ✨ Features Implemented
- ✅ **Compact Stacked Layout** - Collapsible match sections (NT, MT, TM, Termbases)
- ✅ **Relevance Display** - Shows match percentages and confidence levels
- ✅ **Metadata Display** - Domain, context, date information
- ✅ **Drag/Drop Support** - Insert matches into translation field
- ✅ **Compare Boxes** - Side-by-side comparison (Source | TM Source | TM Target)
- ✅ **Diff Highlighting** - Red/green styling for visual comparison
- ✅ **Segment Info** - Metadata and notes display
- ✅ **Integration** - Fully integrated into Project Editor tab

### 📦 New Module
- `modules/translation_results_panel.py` - Compact, production-ready results display

### 🎯 Layout
- Stacked match sections with collapsible headers
- Compact match items for efficient use of space
- Relevance percentage display
- Metadata columns (domain, context, source)
- Notes and segment information panel

---

## [v1.0.0 - Phase 5.0] - 2025-10-27 🚀 Qt Edition Launch

### ✨ Core Features
- ✅ **PyQt6 Framework** - Modern, cross-platform UI
- ✅ **Dual-Tab Interface**:
  - Project Editor - Main translation workspace
  - Universal Lookup - Dictionary/search tool
- ✅ **Project Management** - Load/save translation projects
- ✅ **Translation Memory** - Full TMX support
- ✅ **Segment Grid** - Professional translation grid view
- ✅ **AI Integration** - Multiple LLM provider support (OpenAI, Anthropic, etc.)
- ✅ **Keyboard Shortcuts** - Comprehensive hotkey system
- ✅ **AutoHotkey Integration** - System-wide lookup support

### 🎯 Application Structure
- Professional CAT tool architecture
- Modular design for extensibility
- Clean separation of concerns
- Database-backed translation memory
- Responsive UI with drag/drop support

---

## Release History - Previous Phases

For Qt development history before Phase 5.0, see `docs/RELEASE_Qt_v1.0.0_Phase5.md`

---

## Version Numbering

Supervertaler Qt uses semantic versioning:
- **MAJOR** - Major feature additions or breaking changes
- **MINOR** - New features, backward compatible
- **PATCH** - Bug fixes and improvements
- **PHASE** - Development phase tracking (Phase 5+)

**Current**: v1.0.2 (Phase 5.4)
