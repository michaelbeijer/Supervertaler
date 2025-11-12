# Supervertaler Release Notes

## Current Release: v1.4.0-Qt (November 12, 2025)

### 🎤 Major Feature: Supervoice Voice Dictation + Detachable Log Window

**AI-Powered Hands-Free Translation Input - OpenAI Whisper voice dictation with 100+ language support!**

### What's New

**✅ Supervoice Voice Dictation Module**
- **AI-Powered Speech Recognition** - Using OpenAI Whisper for accurate transcription
- **100+ Languages Supported** - Works with as many languages as Whisper can handle
- **F9 Global Hotkey** - Press-to-start, press-to-stop recording anywhere in the app
- **5 Model Sizes** - Choose from tiny, base, small, medium, or large models:
  - **tiny** - Fastest, lowest RAM (75 MB download)
  - **base** - Recommended balance (142 MB download)
  - **small** - Better accuracy (466 MB download)
  - **medium** - High accuracy (1.5 GB download)
  - **large** - Best quality (2.9 GB download)
- **Visual Feedback** - Dictate button changes color during recording
- **Grid Cell Integration** - Click any grid cell and press F9 to dictate directly
- **Language Auto-Detection** - Uses your project's target language setting
- **Future Voice Commands** - Planned parallel dictation system for workflow automation (confirm segment, go to top, filtering, etc.)

**✅ Detachable Log Window**
- **Multi-Monitor Support** - Detach log window to separate screen
- **Synchronized Auto-Scroll** - Both windows scroll together
- **Persistent State** - Remembers detached/attached preference
- **Independent Sizing** - Position and size the window as needed
- **One-Click Toggle** - "Detach Log" / "Attach Log" button in Settings

**✅ Comprehensive Documentation**
- **User Guide:** [VOICE_DICTATION_GUIDE.md](docs/VOICE_DICTATION_GUIDE.md) - Complete setup and usage instructions
- **Deployment Guide:** [VOICE_DICTATION_DEPLOYMENT.md](docs/VOICE_DICTATION_DEPLOYMENT.md) - FFmpeg bundling options
- **Troubleshooting:** [SUPERVOICE_TROUBLESHOOTING.md](docs/SUPERVOICE_TROUBLESHOOTING.md) - Common issues and solutions

### Fixed Issues

**🐛 Voice Dictation Bug Fixes**
- Fixed critical UnboundLocalError in voice_dictation_lite.py (duplicate `import os` statement)
- Fixed language detection from project settings
- Fixed button color restoration after recording stops
- Fixed auto-scroll synchronization between main and detached log windows

### How to Use

**Setup Supervoice:**
1. Install FFmpeg (Windows: `winget install FFmpeg` or `choco install ffmpeg`)
2. Open Supervertaler → Settings → 🎤 Supervoice
3. Select a model size (recommended: "base" for most users)
4. Click "💾 Save Supervoice Settings"

**Use Voice Dictation:**
1. Click on any segment (or grid cell) where you want to dictate
2. Press **F9** (or click "Dictate" button)
3. Speak your translation
4. Press **F9** again to stop recording
5. Text appears automatically in the selected field

**Detach Log Window (Optional):**
1. Open Settings (⚙️)
2. Click "Detach Log" button at bottom
3. Position log window on second monitor
4. Continue working - both windows stay synchronized

### Benefits

- **Hands-free translation** - Dictate instead of typing
- **100+ language support** - Works with virtually any language pair
- **Flexible accuracy** - Choose model size based on your needs
- **Multi-monitor workflow** - Detachable log for better screen space
- **Future-ready** - Foundation for voice command system
- **Comprehensive support** - Full documentation and troubleshooting guides

### Technical Details

- Voice dictation engine: [modules/voice_dictation_lite.py](modules/voice_dictation_lite.py)
- Whisper model cache: `%USERPROFILE%\.cache\whisper\` (Windows)
- FFmpeg detection: Checks system PATH and bundled binaries
- Log window: Synchronized QTextEdit widgets with signal connections

---

## Previous Release: v1.3.4-Qt (November 10, 2025)

### 🤖 Major Feature: AI Assistant Enhanced Prompt Generation

**ChatGPT-Quality Prompt Generation - Create professional translation prompts with comprehensive summaries and extensive glossaries!**

### What's New
- **Comprehensive High-Level Summaries** - AI generates 3-4 paragraph detailed document analysis
- **Extensive Glossaries** - 30-40 key terms (up from 10-15) with context notes
- **Domain-Specific Constraints** - Tailored requirements for patents, technical, medical, legal documents
- **Full Document Analysis** - AI receives up to 50,000 characters for accurate analysis
- **One-Click Activation** - Generated prompts automatically created and activated

### Fixed Issues
- Fixed empty chat bubbles appearing when AI generates only ACTION blocks
- Fixed ACTION block parsing to accept both single-line and multi-line formats
- Fixed prompt generation sending only 5 segments (now sends full document)

---

## Previous Release: v1.3.3-Qt (November 10, 2025)

### 🏆 Major Feature: LLM Leaderboard + UI Standardization

**Translation Quality Benchmarking System - Compare translation quality, speed, and cost across multiple LLM providers!**

### What's New

**✅ LLM Leaderboard Module**
- **Benchmark translation quality** across OpenAI, Claude, and Gemini models
- **chrF++ scoring** - Objective translation quality assessment (0-100 scale)
- **Speed tracking** - See which models are fastest for your workflow
- **Cost analysis** - Compare pricing across providers
- **Multiple test datasets** included:
  - Technical (EN→NL, NL→EN)
  - Legal (EN→NL, NL→EN)
  - Medical (EN→NL, NL→EN)
  - Marketing (EN→NL, NL→EN)
- **Real-time progress** - Auto-scrolling log shows benchmark status
- **Excel export** - Professional reports with:
  - About sheet with branding and Supervertaler.com link
  - Summary sheet with model rankings
  - Detailed results with all metrics
  - Filename includes dataset name and timestamp

**✅ Standardized Module Headers**
- Professional consistent styling across all modules
- Trophy emoji 🏆 for LLM Leaderboard identity
- Blue branding (#1976D2) matching Supervertaler colors
- Light blue description boxes for clarity
- Applied to: LLM Leaderboard, TMX Editor, AutoFingers, PDF Rescue

**✅ Latest Model Support**
- **OpenAI:** GPT-4o, GPT-4o Mini, GPT-5 (Reasoning)
- **Claude:** Sonnet 4.5, Haiku 4.5, Opus 4.1
- **Gemini:** 2.5 Flash, 2.5 Flash Lite, 2.5 Pro, 2.0 Flash (Exp)
- Friendly model names in all dropdowns

**✅ Standalone Usage Support**
- Can run LLM Leaderboard independently
- Auto-creates `api_keys.txt` from `api_keys.example.txt` template
- Complete documentation in `modules/LLM_LEADERBOARD_STANDALONE.md`

### Fixed Issues

**🐛 LLM Leaderboard Bug Fixes**
- Fixed Claude API call parameters (proper text/custom_prompt separation)
- Fixed Gemini API key mapping ("gemini" provider → "google" API key)
- Fixed model dropdown showing generic names instead of selected models
- Fixed API key auto-creation from template

### How to Use

**Run a Benchmark:**
1. Click Tools tab → LLM Leaderboard
2. Select models from dropdowns (OpenAI, Claude, Gemini)
3. Choose a test dataset (Technical, Legal, Medical, or Marketing)
4. Select language direction (EN→NL or NL→EN)
5. Click "Run Benchmark"
6. Watch real-time progress in auto-scrolling log
7. View results in table with chrF++ scores, speed, and cost
8. Export to Excel for analysis

**Standalone Usage:**
1. Ensure `api_keys.txt` exists (auto-created from template)
2. Run: `python modules/llm_leaderboard_ui.py`
3. Add your API keys to the file
4. Follow benchmark steps above

### Benefits

- **Make informed decisions** about which LLM to use for your translation projects
- **Objective quality metrics** with chrF++ scoring (industry standard)
- **Compare costs** across providers to optimize your budget
- **Professional reports** you can share with clients or colleagues
- **Extensible datasets** - Add your own test segments for domain-specific benchmarks

### Technical Details

- Core engine: `modules/llm_leaderboard.py`
- Qt UI: `modules/llm_leaderboard_ui.py`
- Quality scoring: sacrebleu library (chrF++ implementation)
- Excel generation: openpyxl with professional formatting
- API integration: Unified via `modules/llm_clients.py`

---

## Previous Release: v1.3.2-Qt (November 9, 2025)

### 🎯 Major Feature: Segment-Level AI Access + Critical Bug Fix

**AI Assistant can now access and query individual segments from your translation project!**

### What's New

**✅ Segment-Level AI Actions**
- Ask "How many segments are in this document?" - AI counts and reports progress
- Ask "What is segment 5?" - AI retrieves and displays specific segment text
- Ask "Show me segments 10 through 15" - AI displays range of segments
- First 10 segments automatically included in AI context for quick reference
- Full segment properties available: source, target, status, type, notes, match_percent, etc.

**✅ CAT Tool Tag Handling**
- Proper HTML entity escaping for all CAT tool tags
- Supports Trados Studio, memoQ, Wordfast, CafeTran tags
- Handles `<tag>`, `&nbsp;`, quotes, and nested entities
- Order-aware escaping prevents double-escaping issues
- Segments displayed in code blocks for readability

**✅ Auto-Markdown Generation**
- Optional setting in Settings → General → AI Assistant Settings
- Checkbox: "Auto-generate markdown for imported documents"
- Automatically converts DOCX/PDF to markdown on import
- Markdown saved to `user_data_private/AI_Assistant/current_document/`
- Includes metadata JSON with conversion timestamp and file info

### Fixed Issues

**🐛 CRITICAL BUG FIX: Current Document Not Showing**
- Fixed attribute name mismatch causing context refresh to fail
- Current document now appears in AI Assistant sidebar after import
- Auto-markdown generation now triggers correctly
- This was preventing all document context from reaching the AI

### How to Use

**Query Segments:**
1. Load a project with segments
2. Open Prompt Manager → AI Assistant tab
3. Ask: "How many segments are in this document?"
4. Ask: "What is segment 42?"
5. Ask: "Show me segments 10-15"

**Enable Auto-Markdown:**
1. Click Settings button (⚙️)
2. Go to "General" tab
3. Check "Auto-generate markdown for imported documents"
4. Click "Save General Settings"
5. All future imports will auto-generate markdown

**Benefits:**
- AI can answer segment-specific questions
- Translation progress tracking via AI
- Direct segment content access by number
- CAT tool tags handled properly in display
- Optional markdown conversion for document analysis

### Technical Details

- Added `get_segment_count` and `get_segment_info` AI actions
- Segment access prioritizes `project.segments` for full properties
- HTML escaping order: `&` → `<` → `>` → `"` (prevents double-escaping)
- Auto-markdown uses markitdown library for conversion
- All 10 tests passing including new segment action tests

---

## Previous Release: v1.3.1-Qt (November 9, 2025)

### ✨ Major Feature: AI Assistant File Attachment Persistence (Phase 1)

**Complete persistent storage system for AI Assistant file attachments with view/manage UI**

Files attached to AI Assistant are now saved permanently and survive application restarts!

---

## Previous Release: v1.2.1-Qt (November 6, 2025)

### 🎨 UI Enhancement: Unified Tabbed Interface

**Added consistent tabbed panel structure to both Grid and List views for improved workflow!**

### What's New

**✅ Tabbed Panel in Grid View**
- **Tab 1: Translation Results** - View all match types (Termbase, TM, MT, LLM)
- **Tab 2: Segment Editor** - Edit source and target text, change status
- **Tab 3: Notes** - Add and edit segment notes
- Enables segment editing directly in Grid View (matching Tkinter edition functionality)

**✅ Tabbed Panel in List View**
- Same 3-tab structure for consistency across views
- Translation Results | Segment Editor | Notes
- Replaces single-panel layout with flexible tabbed interface

**✅ Synchronized Panel Updates**
- Clicking a segment in any view updates ALL tabs in ALL views
- Editing in any panel automatically syncs to other panels
- Changes saved to project data in real-time
- Smooth workflow with no manual synchronization needed

### Technical Improvements

**🔧 Robust Widget Architecture**
- Separate widget instances for Grid and List views (Qt single-parent compliance)
- Widget reference storage pattern for flexible access
- Centralized update function for consistent behavior
- Signal blocking prevents infinite update loops

### Fixed Issues

**🐛 Widget Parenting Crashes**
- Fixed Qt single-parent constraint violations
- Created independent TranslationResultsPanel instances per view

**🐛 Signal Handler Errors**
- Fixed AttributeError when editing segments in tabs
- Handlers now properly iterate all panels
- Graceful error handling per panel

### How to Use

**Grid View:**
1. Load a project
2. Select Grid View from "View:" dropdown
3. Click any segment to load it
4. Use tabs at bottom to switch between Translation Results, Segment Editor, and Notes

**List View:**
1. Select List View from "View:" dropdown
2. Click any segment
3. Same 3-tab interface available

**Benefits:**
- Edit segments without switching to Document view
- View translation matches while editing
- Add notes without changing tabs
- Consistent interface across both views

---

## Previous Release: v1.2.0-Qt (November 6, 2025) 🎉

### 🎯 MAJOR RELEASE: Complete Translation Matching System

**The Supervertaler CAT tool now provides comprehensive translation assistance with all match types working together!**

### What's New

**✅ Google Cloud Translation API Integration**
- Machine translation matches now displayed alongside TM and LLM results
- High-quality neural machine translation using Google Translate
- Automatic language detection
- Simple API key-based authentication
- Provider badge: "MT" in Translation Results Panel

**✅ Multi-LLM Support (OpenAI, Claude, Gemini)**
- **OpenAI GPT** - GPT-4o, GPT-5, o1, o3 models available
- **Claude 3.5 Sonnet** - Anthropic's latest model
- **Google Gemini** - Gemini 2.0 Flash, 1.5 Pro models
- All three LLM providers work simultaneously
- Each provides translations with confidence scores
- Provider badges: "OA", "CL", "GM"

**✅ Complete Match Chaining**
- **Termbase matches** → Displayed immediately (yellow highlight)
- **TM matches** → Fuzzy matching from translation memory database
- **MT matches** → Google Cloud Translation
- **LLM matches** → All enabled LLMs (OpenAI, Claude, Gemini)
- All four match types displayed together in Translation Results Panel
- Debounced search (1.5s delay) prevents excessive API calls

### Fixed Issues

**🐛 Termbase Match Preservation**
- Termbase matches no longer disappear when TM/MT/LLM results load
- Matches now properly preserved throughout search process

**🐛 Google Translate Authentication**
- Fixed API authentication using REST API approach
- Simpler configuration with direct API key

**🐛 Gemini Integration**
- Fixed to work with `google` API key (not just `gemini`)
- Backward compatible key naming

### How to Use

**Setup API Keys:**
1. Edit `api_keys.txt` in the root folder
2. Add your API keys:
   ```
   google = YOUR_GOOGLE_API_KEY
   claude = YOUR_CLAUDE_API_KEY
   openai = YOUR_OPENAI_API_KEY
   ```
3. Restart Supervertaler

**Enable Features:**
- Go to Settings → LLM Translation Settings
- Check "Enable LLM matching for Grid Editor"
- Select your preferred models
- Click Save

**Use the CAT Editor:**
1. Import a bilingual DOCX or create a new project
2. Click on any source segment
3. Wait 1.5 seconds - all matches will appear:
   - **Termbases** (Yellow) - Term matches
   - **Translation Memory** (Blue) - Previous translations
   - **Machine Translation** (Orange) - Google Translate
   - **LLM** (Purple) - AI translations from OpenAI/Claude/Gemini

### Performance
- Debounced search prevents API spam
- Parallel LLM calls for faster results
- Smart caching to reduce API costs
- Immediate termbase display (no delay)

### Requirements
- Python 3.8+
- PyQt6
- API keys for desired services (Google, OpenAI, Claude)
- Internet connection for MT and LLM features

---

## Previous Release: v1.1.9-Qt (November 6, 2025)

### New Feature: Keyboard Shortcuts Manager ⌨️

**Comprehensive Keyboard Shortcuts System**
- **View all shortcuts** - See all 40+ keyboard shortcuts in one organized table
- **Categories**: File, Edit, Translation, View, Resources, Match Insertion, Navigation, Editor
- **Search/Filter** - Quickly find shortcuts by action, category, or key combination
- **Edit shortcuts** - Double-click to customize any shortcut with key capture widget
- **Conflict detection** - Real-time warnings if shortcuts overlap
- **Reset options** - Reset individual shortcuts or all to defaults
- **Export/Import JSON** - Share shortcut configurations with your team
- **📄 Export HTML Cheatsheet** - Generate beautiful, printable keyboard reference
  - Professional styling with color-coded shortcuts
  - Organized by category
  - Print-friendly layout
  - Auto-open in browser

**Technical Implementation:**
- Modular architecture: `modules/shortcut_manager.py` + `modules/keyboard_shortcuts_widget.py`
- Context-aware shortcuts (editor vs. grid vs. match panel)
- Persistent storage in `user_data/shortcuts.json`
- Foundation for future dynamic shortcut updates

**Access:** Settings → ⌨️ Keyboard Shortcuts

---

## Previous Release: v1.1.8-Qt (November 5, 2025)

### Critical Bug Fix 🐛

**Prompt Generation Fixed** 🎯
- **CRITICAL FIX:** "Generate Prompts" feature in Prompt Assistant now works perfectly
- **Problem:** Was producing incomplete prompts (Domain: 2 sentences, Project: partial termbase)
- **Root Cause:** Using translation method for text generation (fundamentally wrong approach)
- **Solution:** Switched to direct LLM API calls with proper chat completion structure
- **Result:** Complete professional prompts with full termbase tables (36+ terms)
- **Impact:** Critical feature that was broken is now fully functional

**Technical Details:**
- Direct API calls to OpenAI/Claude/Gemini (not via translation wrapper)
- Proper system/user message separation
- Temperature 0.4 for creative generation
- Max tokens 8000 with truncation detection
- Matches working tkinter implementation exactly

This was a critical fix for a core feature - the Prompt Assistant's "Generate Prompts" functionality is now production-ready.

---

## Previous Release: v1.1.7-Qt (November 4, 2025)

### What's New

**Home Screen Redesign** 🏠
- Complete restructuring of primary workspace
- Editor (Grid/List/Document) on left, Prompt Manager on right
- Resizable horizontal splitter for flexible layout
- Real-time prompt tweaking while viewing changes
- Translation results panel in compact form at bottom

**Strategic Refocus** 🎯
- Pivoted to companion tool philosophy (not full CAT tool)
- Grid simplified for viewing/reviewing
- Focus on AI-powered features and specialized modules

---

## Previous Release: v1.1.6-Qt (November 3, 2025)

### What's New

**Detachable Universal Lookup** 🔍 (NEW!)
- **Multi-Screen Support:** Open Universal Lookup in a separate window for multi-monitor workflows
- **Flexible Workflow:** Keep your translation project on one screen while using Universal Lookup on another
- **Easy Detach/Reattach:** One-click detach button on Home tab, seamless reattach functionality
- **Smart Positioning:** Automatic window positioning that works correctly with multiple monitors
- **Improved Home Tab:** Universal Lookup prominently featured on Home screen for instant access

**Previous Release (v1.1.5): Multiple View Modes** 🎨

### What's New

**Multiple View Modes** 🎨
- **Three Ways to Work:** Choose the view that fits your workflow
  - **Grid View (Ctrl+1):** Spreadsheet-style table - perfect for fast segment-by-segment editing
  - **List View (Ctrl+2):** Segments list with dedicated editor panel - ideal for focused translation
  - **Document View (Ctrl+3):** Natural document flow with clickable segments - great for review
- **View Switcher Toolbar:** Quick buttons to switch between views instantly
- **Keyboard Shortcuts:** Ctrl+1, Ctrl+2, Ctrl+3 for rapid view switching
- **Synchronized Views:** All three views share the same project data - changes in one view instantly appear in others
- **Translation Results Pane:** Now available in all views - TM, LLM, MT, and Termbase matches always accessible

**Previous Release (v1.1.4): Encoding Repair Tool** 🔧

### What's New

**Encoding Repair Tool** 🔧 (NEW!)
- **Full Port from Tkinter:** Complete encoding corruption detection and repair functionality
- **Detect & Fix Mojibake:** Automatically repairs UTF-8 text incorrectly decoded as Latin-1/Windows-1252
- **File & Folder Support:** Scan single files or entire folders recursively
- **Automatic Backups:** Creates `.backup` files before repair to ensure safety
- **Standalone Mode:** Run independently with `python modules/encoding_repair_Qt.py`
- **Embedded Mode:** Integrated as a tab in Supervertaler Qt
- **Test File Available:** `docs/tests/test_encoding_corruption.txt` for user testing
- **Clean Qt Interface:** Matches PDF Rescue and TMX Editor design patterns

**4-Layer Prompt Architecture** 🎯 (Previous Release - v1.1.3)
- **Revolutionary Prompt Management:** Unique layered approach for maximum translation precision
- **Layer 1 - System Prompts:** Editable infrastructure (CAT tags, formatting rules, language conventions)
- **Layer 2 - Domain Prompts:** Domain-specific expertise (Legal, Medical, Technical, Financial, etc.)
- **Layer 3 - Project Prompts:** Client and project-specific instructions
- **Layer 4 - Style Guides:** Language-specific formatting guidelines
- **Prompt Assistant:** AI-powered prompt refinement using natural language (unique to Supervertaler!)
- **Beautiful UI:** Color-coded layer interface with activation system and preview
- **Full Integration:** Standardized headers matching other modules (TMX Editor, PDF Rescue)

**Previous Release (v1.1.0): TMX Editor - Professional Translation Memory Editor** 🎉
- **Database-Backed Large File Support:** Handle massive TMX files (1GB+) efficiently with SQLite backend
- **Dual Loading Modes:** Choose RAM mode (fast for small files) or Database mode (handles any size)
- **Smart Auto Mode:** Intelligently selects best loading method based on file size thresholds
- **Heartsome-Inspired UI:** Three-panel layout with top header (language selectors + filters), center grid, and right attributes panel
- **Inline Editing:** Edit source and target text directly in the grid - no popup dialogs needed
- **Real-time Highlighting:** Search terms highlighted with green background (Heartsome-style)
- **Advanced Filtering:** Case-insensitive search with tag filtering support
- **Efficient Pagination:** 50 TUs per page for smooth performance
- **Batch Operations:** Database commits every 100 TUs for 10-50x faster loading
- **Progress Indicators:** Clear progress bars with immediate display
- **Custom UI:** Consistent green checkmark style matching AutoFingers design

**Technical Improvements** ⚡
- New database tables: `tmx_files`, `tmx_translation_units`, `tmx_segments` with proper indexing
- Optimized transaction management for batch database operations
- Memory-efficient: Database mode frees RAM immediately after loading
- Automatic mode detection based on file size (50MB/100MB thresholds)

**Previous Release (v1.0.2): UI Improvements & Bug Fixes** ✅

### What's New

**UI Improvements & Bug Fixes** ✅
- Fixed broken emoji icons in tab labels (Termbases 🏷️, Prompt Manager 💡, Encoding Repair 🔧, Tracked Changes 🔄)
- Improved checkbox styling with custom green checkboxes and white checkmarks
- Better small-screen support with reorganized AutoFingers layout
- Activity Log moved to right side for improved space utilization

**New Features** ✨
- **Startup Settings:** Option to automatically restore last opened project on startup (Tools → Options → General)
- **Font Size Persistence:** New settings panel to save and restore all font sizes:
  - Grid font size (source/target columns)
  - Translation results match list font size
  - Translation results compare boxes font size
- **Auto-Save:** Font sizes automatically saved when adjusted via zoom keyboard shortcuts

**Previous Release (v1.0.1): Termbases Feature Complete** ✅
- Full termbase CRUD operations (Create, Read, Update, Delete)
- Multiple termbases per project with independent term sets
- Global and project-specific termbase scopes
- Sample data with 3 test termbases (48 terms total)

**Terminology Standardization**
- All references standardized to "Termbase" (single word)
- Consistent terminology throughout UI and codebase
- Eliminated ambiguity between "glossary" vs "termbase"

### Key Improvements

- **User Preferences:** Font sizes and startup behavior now persist across sessions
- **Startup Experience:** Option to automatically reopen your last project on launch
- **UI Polish:** Custom checkbox styling for better visual feedback
- **Layout:** 2-column grid layout for AutoFingers Settings section
- **Responsive Design:** Improved rendering on smaller laptop displays
- **Database:** Fixed NOT NULL constraint errors on language fields (v1.0.1)
- **Code Quality:** Fixed method naming and Project object access patterns

### System Requirements

- **Python:** 3.8+
- **OS:** Windows, macOS, Linux
- **GUI Framework:** PyQt6
- **Database:** SQLite (built-in)

---

## Known Issues

- None reported for v1.0.2

---

## Deprecated Features

- **Tkinter Edition:** Now in maintenance mode. Features being ported to Qt Edition.

---

## Breaking Changes

None in this release.

---

## Upgrading

### From v1.0.1 to v1.0.2

No database migration required. Simply install the new version:

### From v1.0.0 to v1.0.1

No database migration required. Simply install the new version:

```bash
python Supervertaler_Qt.py
```

---

## Support

For questions or bug reports, see [PROJECT_CONTEXT.md](docs/PROJECT_CONTEXT.md) for development team information.

---

## Future Releases

### v1.1.0 (Planned)
- Terminology Search (Ctrl+P)
- Concordance Search (Ctrl+K)
- Enhanced create/edit dialogs

### v1.2.0 (Planned)
- TMX Editor with visual highlighting
- Advanced filtering
- Custom keyboard shortcuts

### v2.0.0 (Future)
- Full feature parity with Tkinter edition
- Tkinter deprecation

---

**Documentation:** See [docs/PROJECT_CONTEXT.md](docs/PROJECT_CONTEXT.md) for complete project information.

**Last Updated:** November 2, 2025
