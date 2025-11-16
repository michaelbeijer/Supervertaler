# Supervertaler Qt Edition - Changelog

All notable changes to the **Qt Edition** of Supervertaler are documented in this file.

The Qt Edition is the **primary version** for active development and new features. See [CHANGELOG_Tkinter.md](CHANGELOG_Tkinter.md) for the legacy Classic edition.

---

## 🌟 Recent Highlights - What's New in Supervertaler

**Latest Major Features:**

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
