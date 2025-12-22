# Supervertaler - Changelog

All notable changes to Supervertaler are documented in this file.

**Current Version:** v1.9.57 (December 22, 2025)
**Framework:** PyQt6
**Status:** Active Development

**Note:** For historical information about legacy versions (Tkinter Edition, Classic Edition), see [legacy_versions/LEGACY_VERSIONS.md](legacy_versions/LEGACY_VERSIONS.md).

---

## 🌟 Recent Highlights - What's New in Supervertaler

**Latest Major Features:**

- 🏠 **Flattened Tab Structure (v1.9.57)** - Simplified main navigation from nested tabs to flat structure. The old "Workspace → Editor / Resources" hierarchy is now: **Project editor** | **Project resources** | **Tools** | **Settings**. All four tabs are now at the top level for easier navigation. Capitalization follows lowercase style for subtabs (e.g., "Project editor" not "Project Editor").
- ✏️ **Glossary Renaming (v1.9.56)** - Right-click on any glossary in Project resources → Glossaries tab to rename it. Previously, editing the name in the UI appeared to work but didn't actually save to the database. Now uses proper rename dialog with database persistence. Name column is no longer misleadingly editable inline.
- ⚡ **Lightning-Fast Filtering (v1.9.55)** - Filter operations (Ctrl+Shift+F) now run instantly instead of taking ~12 seconds! Optimized to avoid grid reload - only shows/hides rows and applies yellow highlights. **Ctrl+Shift+F toggle**: press once to filter on selected text, press again to clear the filter. Clear filter also listed separately in keyboard shortcuts for discoverability.
- 📋 **Superlookup Termbase Enhancements (v1.9.53)** - Improved Glossaries tab with additional metadata columns: Glossary name, Domain, Notes. Full metadata in results including priority, project, client, forbidden status. Tooltips show full content on hover.
- 📥 **Glossary Import Progress Dialog (v1.9.53)** - Real-time progress dialog when importing glossaries from TSV files. Visual progress bar, live statistics (✅ imported, ⏭️ skipped, ❌ errors), scrolling log window with color-coded entries.
- 🌐 **Superlookup Web Resources (v1.9.52)** - Expanded web resources tab with 14 reference sites! New resources: Juremy, michaelbeijer.co.uk, AcronymFinder, BabelNet, Wiktionary (Source & Target). Persistent login sessions with cookies stored in `user_data/web_cache/`. Auto-select language pair from project on load. Compact single-line search layout. Settings checkboxes control sidebar button visibility.
- 🔍 **Superlookup MT Integration (v1.9.51)** - Complete Machine Translation integration in Superlookup! Search now returns results from Google Translate, Amazon Translate, DeepL, Microsoft Translator, ModernMT, and MyMemory. MT provider status display shows active/disabled/missing API key providers with "⚙️ Configure in Settings" link. Error messages now shown in red with details (no more silent failures). Fixed language name mapping: "Dutch" → "nl", "English" → "en" for all MT providers. Added boto3 and deepl to requirements.txt. Removed debug print spam. Termbases tab now has search filter and split-view with editable terms grid.
- 🎤 **Voice Commands System (v1.9.50)** - Complete hands-free translation with Talon-style voice commands! Say "next segment", "confirm", "source to target", "translate", and more. **Always-On Listening Mode** with VAD (Voice Activity Detection) - no need to press F9. Dual recognition engines: **OpenAI Whisper API** (recommended, fast & accurate) or local Whisper model. New grid toolbar button (🎧 Voice ON/OFF) for easy toggle. Status bar indicator shows listening/recording/processing state. AutoHotkey integration for controlling external apps (memoQ, Trados, Word) by voice. Custom voice commands with fuzzy matching. Configure in Tools → Supervoice tab.
- 🎤 **Always-On Listening (v1.9.49)** - VAD-based continuous listening eliminates pressing F9 twice. Automatically detects speech, records, transcribes, and processes as command or dictation. Configurable mic sensitivity (Low/Medium/High). Visual feedback: 🟢 Listening → 🔴 Recording → ⏳ Processing. F9 stops always-on mode if active.
- 🎤 **Talon-Style Voice Commands (v1.9.48)** - 3-tier voice command architecture: Internal commands (control Supervertaler), System commands (AutoHotkey for other apps), Dictation fallback. Built-in commands: navigation, editing, translation, lookup. Custom command editor with phrase, aliases, and action configuration.
-  🧹 **Code Cleanup (v1.9.47)** - Removed ~811 lines of dead Document View code. The Document View feature was never used in production - the Grid View (Editor) is the primary and only workflow. Cleanup includes: removed `LayoutMode` class, removed `create_editor_widget()`, `create_document_view_widget()`, `refresh_document_view()` and all related helper methods. File reduced from 35,249 to 34,438 lines. No functional changes.
- 🏠 **Workspace UI Redesign (v1.9.46)** - Cleaner tab hierarchy with renamed tabs: **Workspace** (main tab) containing **Editor** (the grid) and **Resources** (TM, Termbases, Prompts, etc.). Removed Document View (unused). Simplified navigation menu. Fixed critical bug where termbase matches showed terms from non-activated termbases.
- 🏷️ **Termbase Highlight Styles (v1.9.45)** - Three configurable styles for termbase matches in the translation grid: **Background** (default pastel green shades), **Dotted Underline** (priority-based colors: red for P1, grays for P2-3, customizable for P4+), and **Semibold** (bold weight with tinted foreground). Configure via Settings → View Settings. Auto-spellcheck for target language: spellcheck now automatically initializes to project target language on import/load. Fixed short language codes (nl, de, fr) not mapping to dictionaries.
- 📚 **UI Reorganization (v1.9.44)** - Prompt Manager moved under Project Resources tab (prompts are project resources). Superlookup hotkey script now shows Supervertaler icon in system tray. Fixed termbase import "Could not find termbase ID" error. Removed dotted focus outline from Superlookup Search button.
- 🔑 **Superlookup Hotkey Improvements (v1.9.43)** - Fixed Ctrl+Alt+L global hotkey not bringing Superlookup to foreground. Added AutoHotkey setup helper (Help → Setup AutoHotkey for Superlookup). New AutoHotkey path configuration in Settings → General Settings. Better error handling when AutoHotkey is not installed.
- 📁 **Multi-File Project Support (v1.9.42)** - Import entire folders of files as a single multi-file project! File → Import → Folder (Multiple Files) supports DOCX and TXT files. Per-file progress tracking in View → File Progress dialog (or click status bar). New file filter dropdown to show segments from specific files. Status bar shows completion progress across all files. Source files automatically backed up to `_source_files/` folder. Relocate Source Folder feature to fix broken paths. Export to folder with TXT, DOCX, or Bilingual Table formats (export in progress - basic functionality available).
- 🔍 **Superlookup Fixes (v1.9.42)** - Renamed `UniversalLookupTab` to `SuperlookupTab` for consistency. Fixed `theme_manager` attribute error when using Ctrl+Alt+L hotkey. Theme-aware search term highlighting now works properly.
- 📋 **Spellcheck Info Dialog Redesign (v1.9.42)** - Two-column horizontal layout fits on screen without scrolling. Clear explanation of auto-switching between built-in pyspellchecker and Hunspell backends. Compact diagnostics section.
- 🌙 **Dark Mode (v1.9.41)** - Complete dark theme implementation with proper styling across the entire application. Dark compare boxes in Translation Results panel, dark Termview with visible text for non-matched words, and consistent theming throughout all UI components. Switch themes via View → Theme Editor.
- 🔍 **Superlookup Unified Concordance System (v1.9.40)** - Major consolidation: Ctrl+K now opens Superlookup instead of a separate concordance dialog. All lookup resources in one place: TM concordance, Termbase matches, Supermemory semantic search, Machine Translation, and Web Resources. New dual-view toggle: Horizontal (table) or Vertical (list) layout. Tab reorganization: "Project Resources" now comes before "Prompt Manager". Removed redundant tabs from Translation Memories (Concordance and Import/Export - functionality already available in Superlookup and TM List). FTS5 full-text search now properly used for blazingly fast concordance on millions of segments.
- 🔍 **Superlookup Multilingual Search (v1.9.39)** - Complete overhaul of Superlookup with multilingual language filtering. New From/To language dropdowns filter TM and termbase searches by source/target language pair. Search direction radio buttons (Both/Source only/Target only) for precise concordance searches. Yellow highlighting of search terms in results. Compact results display with tooltips for full text. Languages auto-populate from your TMs and termbases, grouped alphabetically by language family. UI cleanup: removed Manual Capture button and Operating Modes selector.
- 📁 **Improved Project File Format (v1.9.38)** - `.svproj` files now have all metadata at the top (name, languages, dates, settings, paths) with segments at the end for easier inspection in text editors. Added helpful tip in batch translate warning about using Select All + Clear Target instead of re-importing.
- 🔤 **User-Configurable Grid Fonts (v1.9.37)** - Choose your preferred font family for the translation grid from 10 popular options. Live preview shows font changes in real-time with sample source/target text and tags. Font family now persists between sessions.
- 🎨 **Universal Tag Coloring (v1.9.36)** - All CAT tool tags now highlighted in pink: memoQ `{1}`, `[2}`, Trados `<1>`, `</1>`, Phrase `{1}`, and HTML `<b>`, `<i>`. CafeTran pipe symbols only red in CafeTran projects (bug fix).
- 🎨 **memoQ Red Tags Support (v1.9.35)** - Fixed memoQ bilingual export not preserving red tag color. Tags in the target column now correctly inherit the red/magenta color from the source column, ensuring perfect formatting for memoQ re-import.
- 🎨 **UI Fixes (v1.9.34)** - Replaced all standard radio buttons with green-themed CheckmarkRadioButton.
- 🐛 **Spellcheck Update Fix (v1.9.33)** - Fixed issue where adding/ignoring words only removed underline in the current cell. Now triggers instant global refresh of all highlighters across the entire grid. No more false positive red underlines after you've whitelisted a word

- 📦 **Trados SDLRPX Status Fix (v1.9.32)** - Fixed critical bug where exported SDLRPX return packages kept segments in "Draft" status instead of updating to "Translated". Trados Studio now correctly recognizes translated segments. Client deliverables no longer show as MT draft content

- 🔤 **Spellcheck Language Fix (v1.9.31)** - Spellcheck now correctly uses the project's target language instead of defaulting to English. Added language dropdown in Spellcheck Info dialog to manually change spellcheck language. Language changes take effect immediately with highlighting refresh
- 🐛 **Critical LLM Fix (v1.9.30)** - Fixed OpenAI/LLM translation failing with "No such file or directory" error. Removed hardcoded debug file path that prevented translation when running from non-development directories
- 📝 **Spellcheck Integration (v1.9.29)** - Built-in spellcheck for target language. Works out of the box with pyspellchecker (8 languages bundled). Optional Hunspell support for more languages. Red wavy underlines for misspelled words. Right-click for suggestions, Add to Dictionary, Ignore. Custom dictionary with persistent word list. Spellcheck state saved per-project in .svproj files. Button state persists across restarts
- 📄 **Phrase (Memsource) Bilingual DOCX Support (v1.9.28)** - Full round-trip support for Phrase TMS bilingual DOCX files. Import preserves inline tags like `{1}`, `{1>text<1}`. Export writes translations back to Column 5 for seamless return to Phrase workflow. File → Import → Phrase (Memsource) Bilingual (DOCX) and File → Export → Phrase (Memsource) Bilingual
- 👁️ **Show Invisibles Feature (v1.9.28)** - Display invisible characters in the translation grid: spaces (·), tabs (→), non-breaking spaces (°), and line breaks (¶). Dropdown menu with granular control for each character type. Toggle All option. Smart handling preserves copy/paste (Ctrl+C copies original characters), double-click word selection, and Ctrl+Arrow word navigation. Configurable symbol color in Settings → View Settings
- 📄 **Simple Text File Import/Export (v1.9.27)** - Import simple text files where each line becomes a source segment. Translate with AI, then export a matching file with translations. Perfect for line-by-line translation of plain text content. Language pair selection, encoding options (UTF-8, Latin-1, etc.), and empty line handling. File → Import → Simple Text File (TXT) and File → Export → Simple Text File - Translated (TXT)
- 📦 **SDLPPX Project Persistence (v1.9.20)** - SDLPPX package path now saved in .svproj files. Full round-trip workflow persists across sessions - import SDLPPX, translate, save project, close, reopen, continue translating, export SDLRPX. Fixed export bug that showed "0 translations updated". Handler automatically restored on project load
- 📦 **Trados Studio Package Support (v1.9.19)** - Import SDLPPX packages directly from Trados Studio project managers. New File → Import → Trados Studio submenu with Package (SDLPPX) option. Translates SDLXLIFF files within the package, preserves SDL-specific markup and segment IDs. Export as SDLRPX return package (File → Export → Trados Studio → Return Package) for seamless delivery back to Trados users. Full round-trip workflow for freelance translators receiving packages
- 🔍 **Supermemory Concordance Integration (v1.9.18)** - Concordance Search (Ctrl+K) now includes Supermemory semantic search with two-tab interface. TM Matches tab for exact text search, Supermemory tab for meaning-based search. Active checkbox column in Supermemory to control which TMs are searched. Fixed Trados bilingual DOCX round-trip issues (xml:space, language settings). Supermemory moved to Resources tab
- 🧠 **Supermemory Enhancements (v1.9.17)** - Complete domain management system for translation memories with domain categorization (Legal, Medical, Patents, etc.), multi-language filtering in search, integration with Superlookup for unified lookup, and TMX/CSV export. Color-coded domain tags, dynamic column headers showing actual languages, and professional search/filter interface
- 🖥️ **Local LLM Support - Ollama (v1.9.16)** - Run AI translation entirely on your computer with no API costs, complete privacy, and offline capability. New "Local LLM (Ollama)" provider option in Settings with automatic hardware detection and model recommendations. Supports qwen2.5 (3B/7B/14B), llama3.2, mistral, and gemma2 models. Built-in setup wizard guides installation and model downloads. See FAQ for setup instructions
- 📋 **Bilingual Table Export/Import (v1.9.15)** - New Supervertaler Bilingual Table format for review workflows. Export menu options: **"Bilingual Table - With Tags (DOCX)"** preserves Supervertaler formatting tags for re-import after review. **"Bilingual Table - Formatted (DOCX)"** applies formatting (bold/italic/underline, bullet markers) for client-ready output. Tables include segment number, source, target, status, and notes columns. **"Import Bilingual Table"** compares edited DOCX with current project, shows diff preview, and applies changes. Document title links to supervertaler.com
- 📤 **Improved DOCX Export & Keyboard Navigation (v1.9.14)** - Fixed DOCX export to properly handle formatting tags (`<b>`, `<i>`, `<u>`) and convert them to actual Word formatting. Export now handles multi-segment paragraphs with partial replacement. Added cleanup for Unicode replacement characters (U+FFFC). Ctrl+Home/End now properly navigate to first/last segment even when editing in grid cells
- 📄 **Document Preview & List Tags (v1.9.13)** - New Preview tab shows formatted document view with headings, paragraphs, and list formatting. Click any text to navigate to that segment. Distinct list tags: `<li-o>` for ordered/numbered lists (1. 2. 3.) and `<li-b>` for bullet points (•). DOCX import now properly detects bullet vs numbered lists from Word's numbering XML. Type column shows `¶` for continuation paragraphs instead of `#`
- 📊 **Progress Indicator Status Bar (v1.9.12)** - New permanent status bar showing real-time translation progress: Words translated (X/Y with percentage), Confirmed segments (X/Y with percentage), and Remaining segments count. Color-coded: red (<50%), orange (50-80%), green (>80%). Updates automatically as you work
- ⚡ **Navigation & Find/Replace Improvements (v1.9.11)** - Ctrl+Home/End to jump to first/last segment. Find/Replace dialog now pre-fills selected text from source or target grid. Ctrl+Q shortcut for instant term pair saving (remembers last-used termbase from Ctrl+E dialog)
- 🔧 **Non-Translatables: Case-Sensitive & Full-Word Matching (v1.9.11)** - Non-translatables matching is now case-sensitive by default and only matches full words (not partial words). Added LLM refusal detection with helpful error messages for batch translation. Fixed crash when closing project (missing stop_termbase_batch_worker). Fixed .svprompt files not showing in Prompt Library tree
- 🔧 **TM Search Fixes & Language Matching (v1.9.10)** - Fixed TM matches not appearing in Translation Results panel. Added flexible language matching ("Dutch", "nl", "nl-NL" all match). TM metadata manager now initializes with project load. Removed legacy Project TM/Big Mama hardcoding. Cleaned public database for new users. Non-Translatables: sortable columns, right-click delete, Delete key support
- 🎨 **memoQ-style Alternating Row Colors (v1.9.9)** - Grid now displays alternating row colors across all columns (ID, Type, Source, Target) like memoQ. User-configurable colors in Settings → View Settings with even/odd row color pickers. Colors are consistent across the entire row including QTextEdit widgets
- 🔄 **CafeTran Integration & Editor Shortcuts (v1.9.8)** - Full CafeTran bilingual DOCX support with pipe symbol formatting. New Ctrl+Shift+S copies source to target. Ctrl+, inserts pipe symbols for CafeTran. Pipes highlighted in red/bold. Sortable keyboard shortcuts table. Batch size default changed to 20
- 🔄 **CafeTran Bilingual DOCX Support (v1.9.7)** - Full import/export support for CafeTran bilingual DOCX files. Import preserves pipe symbol formatting markers. Export writes translations back with formatting preserved. Round-trip workflow for CafeTran users
- 📁 **Custom File Extensions & Monolingual Export (v1.9.6)** - New branded file extensions: `.svproj` (projects), `.svprompt` (prompts), `.svntl` (non-translatables). All formats maintain backward compatibility. Monolingual DOCX import now prompts for language pair. New "Target Only (DOCX)" export preserves original document structure (tables, formatting). Original DOCX path saved in project files for reliable exports
- 📤 **Send Segments to TM & memoQ Tag Shortcuts (v1.9.5)** - Bulk send translated segments to TMs via Edit > Bulk Operations. Filter by status (Translated, Reviewed, etc.) and scope. New Ctrl+, shortcut inserts memoQ tags pairs or wraps selection. Tab renamed to "Resources"
- 🏷️ **Tag-Based Formatting System (v1.9.4)** - Complete inline formatting support for memoQ bilingual files. Import preserves bold/italic/underline as `<b>`, `<i>`, `<u>` tags. Toggle between WYSIWYG and Tag view with Ctrl+Alt+T. Ctrl+B/I/U shortcuts to apply formatting. AI translation preserves tags. Export converts tags back to Word formatting
- 📋 **Session Log Tab & TM Defaults Fix (v1.9.3)** - Added Session Log tab to bottom panel for easy access to log messages. Fixed TM Read/Write checkbox defaults to respect project.json settings
- ⚙️ **Superlookup Settings UI (v1.9.2)** - Redesigned Settings tab with sub-tabs for TM/Termbase/MT/Web resources. Proper 18x18px checkboxes with green background and white checkmarks matching standard Supervertaler style. Each resource type has dedicated full-height space for easy selection
- ↩️ **Undo/Redo for Grid Edits (v1.9.1)** - Full undo/redo support for grid editing operations with Ctrl+Z/Ctrl+Y. Tracks target text changes, status changes, and find/replace operations with 100-level history
- 🔍 **Termview - Inline Terminology (v1.9.0)** - Visual inline terminology display showing source words with translations underneath, inspired by RYS Trados plugin. Supports multi-word terms, click-to-insert, hover tooltips, and terms with punctuation like "gew.%"
- 🎨 **UI Refinements - Tab Styling (v1.8.0)** - Refined selected tab appearance with subtle 1px blue underline and light background highlighting for cleaner visual design
- ✅ **Simplified TM/Termbase System (v1.6.6)** - Redesigned with Read/Write checkboxes, auto-priority system, removed complex Active/Project concepts for clearer workflow
- 🔍 **Find/Replace & TM Enhancements (v1.7.9)** - Fixed highlighting, disabled TM saves during navigation, added bidirectional TM search with language variant matching
- 🔍 **Filter Highlighting Fix (v1.7.8)** - Fixed search term highlighting in source/target filter boxes using widget-internal highlighting
- 🎯 **Termbase Display Customization (v1.7.7)** - User-configurable termbase match sorting and filtering for cleaner translation results
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

## [1.9.41] - December 16, 2025

### 🌙 Dark Mode - Complete Theme Implementation

**Full dark theme support across the entire application:**
- 🎨 **Compare Boxes**: Translation Results panel now properly displays dark backgrounds for Current Source, TM Source, and TM Target boxes in dark mode
- 📝 **Termview Visibility**: All words in Termview pane now visible in dark mode - not just terms with matches. Non-matched words use light text color on dark background
- 🔄 **Theme Consistency**: Fixed Qt styling issues where hidden widgets weren't receiving theme updates. Theme colors now applied when widgets become visible
- ⚡ **Reliable Styling**: Uses both stylesheet and QPalette approaches for maximum compatibility across different Qt rendering scenarios

**Technical improvements:**
- Added `_apply_compare_box_theme()` method for reliable theme application on visibility
- Theme-aware `TermBlock` and `NTBlock` classes in Termview widget
- Proper color inheritance for all UI components in dark mode

**Access Dark Mode:** View → Theme Editor → Select "Dark" theme

---

## [1.9.40] - December 12, 2025

### 🔍 Superlookup Unified Concordance System

**Major consolidation - Ctrl+K now opens Superlookup instead of separate dialog:**
- 🔗 **Unified Lookup Hub**: All concordance searches now go through Superlookup - one place for TM, Termbase, Supermemory, MT, and Web Resources
- ⌨️ **Ctrl+K Integration**: Pressing Ctrl+K in Project Editor navigates to Tools → Superlookup and auto-searches selected text
- 📝 **Selected Text Auto-Fill**: Any text selected in source/target automatically populates the search field

**Dual-view toggle for TM Matches tab:**
- 📊 **Horizontal (Table)**: Source | Target columns side-by-side - compact and scannable
- 📜 **Vertical (List)**: Dutch: ... / English: ... stacked format - traditional concordance layout with more detail
- 🔄 **Radio Button Toggle**: Switch between views instantly, results update in both views

**UI/Tab reorganization:**
- 📚 **"Resources" → "Project Resources"**: Clearer naming for the resources tab
- 🔀 **Tab Reorder**: Project Resources now comes BEFORE Prompt Manager (more logical flow)
- 🧹 **Removed Redundant Tabs**: Translation Memories no longer has Concordance or Import/Export tabs (functionality in Superlookup and TM List)
- 📦 **Compact Source Text**: Superlookup source text box shrunk from 100px to 50px
- 📚 **"Termbase Terms" → "Termbase Matches"**: Consistent naming

**FTS5 Full-Text Search optimization:**
- ⚡ **Concordance now uses FTS5**: `concordance_search()` now uses SQLite FTS5 MATCH instead of slow LIKE queries
- 🚀 **100-1000x faster** on large databases with millions of segments
- 🔄 **Auto-sync**: FTS5 index automatically rebuilt if out of sync with main table
- 🔧 **Manual rebuild**: New `rebuild_fts_index()` method available for maintenance

**ChromaDB stability fix:**
- 🐛 **Fixed Rust backend crashes**: Removed all `collection.count()` calls that caused native crashes in ChromaDB 1.3.x
- 📊 **Uses metadata count**: Stats now derived from SQLite metadata instead of ChromaDB collection queries
- ✅ **ChromaDB 0.6.3**: Stable version with Python backend, compatible with tokenizers 0.22.0

---

## [1.9.39] - December 11, 2025

### 🔍 Superlookup Multilingual Search

**Multilingual language filtering for TM and termbase searches:**
- 🌍 **From/To Language Dropdowns**: New filter dropdowns in Superlookup search bar to filter by source/target language pair
- 🔄 **Swap Button**: Quick ↔ button to swap From and To language selections
- 📚 **Auto-Population**: Languages auto-populate from your TMs and termbases when tab is first viewed
- 🔤 **Smart Sorting**: Languages alphabetically sorted with family grouping (all Dutch variants together, all English variants together, etc.)
- 🏷️ **Clear Display**: Format shows "English (en)", "Dutch (nl-BE)" for clarity and uniqueness

**Search direction controls:**
- ↔️ **Both**: Bidirectional search (searches source and target columns)
- → **Source only**: Search only in source text
- ← **Target only**: Search only in target text

**UI improvements:**
- 🟡 **Yellow Highlighting**: Search terms now highlighted in yellow in TM and termbase results
- 📏 **Compact Display**: Results use word wrap with 60px max row height, tooltips show full text on hover
- 🔢 **Hidden Row Numbers**: Cleaner display without row number column
- 🧹 **Removed Manual Capture**: Button was redundant (just paste text manually)
- 🧹 **Removed Operating Modes**: Dropdown was pointless (only Universal mode was used)

---

## [1.9.38] - December 11, 2025

### 📁 Project File & UX Improvements

**Reorganized .svproj file structure for human readability:**
- 📄 **Metadata First**: Project name, languages, dates, ID now at the top of the file
- ⚙️ **Settings Next**: Prompt, TM, termbase, spellcheck settings follow metadata
- 📂 **Paths Then**: Source file paths (DOCX, memoQ, Trados, etc.) before segments
- 📝 **Segments Last**: Translation content at the end for easy scrolling in text editors

**Improved batch translate warning for memoQ files:**
- 💡 Added tip: "You can clear all targets without re-importing" with instructions to use Select All + Clear Target from right-click menu
- Saves users from having to go back to memoQ to clean the file

---

## [1.9.37] - December 11, 2025

### 🔤 User-Configurable Grid Fonts

**New font customization options in Settings → View Settings:**
- 🔤 **Font Family Dropdown**: Choose from 10 popular fonts: Calibri, Segoe UI, Arial, Consolas, Verdana, Times New Roman, Georgia, Courier New, Tahoma, Trebuchet MS
- 👁️ **Live Preview**: Real-time preview showing sample source/target text with tags, updates instantly as you change font settings
- 💾 **Font Persistence**: Font family now saved to preferences and restored on startup (previously only font size was saved)
- 🎯 **Improved Spinbox**: Fixed font size spinner up/down arrows with better click targets
- 📝 **Contact Note**: Info text now includes "If your favourite font is missing, contact the developer!"

---

## [1.9.36] - December 10, 2025

### 🎨 Universal Tag Coloring

**All CAT tool tags now highlighted in pink in the translation grid:**
- 🏷️ **memoQ Tags**: `{1}`, `[2}`, `{3]`, `[4]` - all variations now colored pink
- 🏷️ **Trados Tags**: `<1>`, `</1>` - numeric tags now colored pink
- 🏷️ **Phrase Tags**: `{1}`, `{2}` - same as memoQ, now colored pink
- 🏷️ **HTML Tags**: `<b>`, `<i>`, `<u>`, `<li-o>` - already worked, still works

**CafeTran Pipe Symbol Fix:**
- 🐛 **Bug Fix**: Pipe symbols (`|`) were incorrectly highlighted red in ALL project types
- ✅ **Fixed**: Pipes now only red in CafeTran projects (as intended)
- 🔧 **Implementation**: Added `TagHighlighter._is_cafetran_project` class flag

---

## [1.9.35] - December 10, 2025

### 🎨 formatting
- **memoQ Red Tags**: Fixed issue where red formatting tags (e.g. `{1}`) in memoQ bilingual files were being exported as black text.
- **Smart Color Transfer**: Export now dynamically reads the source column color and applies it to the corresponding text in the target column.

## [1.9.34] - December 10, 2025

### 🎨 UI Fixes

**Checkmark Radio Buttons:**
- 🎨 **Global Update**: Replaced all standard `QRadioButton` instances across the application with the custom green `CheckmarkRadioButton`.
- ✅ **Updated Areas**: Find & Replace, Advanced Filters, Row Locking, Termbase Import, AutoFingers, and TM Import dialogs.
- 💅 **Visual Consistency**: Ensures a uniform look and feel across all green-themed UI elements.

---

## [1.9.32] - December 10, 2025

### 📦 Trados SDLRPX Status Fix

**Critical Bug Fix for Trados Return Packages:**
- 🔧 **Status Update Fix**: SDLRPX export now correctly updates segment confirmation status from "Draft" to "Translated"
- ✅ **Proper Trados Recognition**: Trados Studio now recognizes segments as translated, not machine translation drafts
- 📤 **Client Deliverables**: Return packages display correctly in Trados when client opens them
- 🏷️ **conf Attribute**: Fixed missing update of `conf` attribute in SDLXLIFF `<sdl:seg>` elements

**Technical Details:**
- Added `_update_segment_status()` method to `sdlppx_handler.py`
- Updates `conf` attribute in `sdl:seg-defs` section during export
- Maps internal status ('translated', 'approved') to SDL status ('Translated', 'ApprovedTranslation')
- Proper namespace handling for SDL elements in ElementTree

---

---

## [1.9.33] - December 10, 2025

### 🐛 Spellcheck Update Fix

**Fixed Spellcheck Highlighting Update:**
- 🔧 **Global Refresh**: Adding a word to custom dictionary or ignoring it now immediately updates all occurrences in the grid
- ✅ **No More False Positives**: Red wavy underlines vanish instantly across the entire document when you whitelist a word
- 🖱️ **Context Menu Fix**: Right-click "Add to Dictionary" and "Ignore Word" actions now trigger full grid refresh

---

## [1.9.31] - December 10, 2025

### 🔤 Spellcheck Language Fix

**Spellcheck Now Uses Project Target Language:**
- 🎯 **Automatic Language Detection**: Spellcheck initializes with project's target language instead of defaulting to English
- 🌐 **Language Dropdown**: Added language selector in Spellcheck Info dialog
- 🔄 **Immediate Effect**: Language changes take effect immediately with highlighting refresh
- 📝 **Fixed Initialization**: `_toggle_spellcheck()` now uses `self.current_project.target_lang`

---

## [1.9.30] - December 10, 2025

### 🐛 Critical LLM Fix

**Fixed OpenAI/LLM Translation Error:**
- 🔧 **File Path Error**: Fixed "No such file or directory: 'openai_debug.txt'" error that broke all LLM translations
- 📁 **Debug Path**: Removed hardcoded debug file path that only worked in development directory
- ✅ **Production Ready**: Translations now work when running from any directory

---

## [1.9.29] - December 10, 2025

### 📝 Spellcheck Integration

**Built-in Spellchecking for Target Language:**
- 📝 **Spellcheck Button**: Toggle in filter bar enables/disables spellchecking
- 〰️ **Red Wavy Underlines**: Misspelled words highlighted with red wavy underline
- 💬 **Right-Click Suggestions**: Click misspelled word for spelling suggestions
- ➕ **Add to Dictionary**: Add words to custom dictionary (persistent)
- 🔇 **Ignore Word**: Ignore word for current session only
- 📖 **Custom Dictionary**: Manage custom words from dropdown menu
- ℹ️ **Spellcheck Info**: View backend, language, and dictionary status

**Language Support:**
- 🇬🇧 English, 🇳🇱 Dutch, 🇩🇪 German, 🇫🇷 French, 🇪🇸 Spanish, 🇵🇹 Portuguese, 🇮🇹 Italian, 🇷🇺 Russian
- 🐍 **Built-in Backend**: Uses pyspellchecker with bundled dictionaries - works out of the box!
- 📚 **Hunspell Backend**: Optional .dic/.aff files for additional languages or improved accuracy
- Auto-matches project target language

**Settings & Persistence:**
- 💾 **Project-Level Settings**: Spellcheck state saved in .svproj files
- 🔄 **Session Persistence**: Button state remembered across restarts
- ℹ️ **Info Dialog**: Explains dual-backend system with dictionary download links

**Technical Details:**
- New module: `modules/spellcheck_manager.py` - Complete spellcheck handling
- Custom dictionary stored in `user_data/dictionaries/custom_words.txt`
- TagHighlighter extended for spell underline formatting
- Spellcheck only applied to target column (not source)
- Settings persisted in `ui_preferences.json` and `.svproj` files

---

## [1.9.28] - December 9, 2025

### 📄 Phrase (Memsource) Bilingual DOCX Support

**Full Round-Trip Workflow:**
- 📥 **Import Phrase Bilingual DOCX**: File → Import → Phrase (Memsource) Bilingual (DOCX)
- 📤 **Export Back to Phrase**: File → Export → Phrase (Memsource) Bilingual - Translated (DOCX)
- 🏷️ **Inline Tag Preservation**: Tags like `{1}`, `{1>text<1}` preserved for round-trip
- 🔍 **Auto-Detection**: Detects Phrase format (7-column tables, segment IDs with `:`)
- 💾 **Project Persistence**: Phrase source path saved in .svproj for future sessions

**Implementation:**
- New module: `modules/phrase_docx_handler.py` - Complete Phrase DOCX handling
- Language pair selection dialog for imported files
- Segment ID and status preserved in notes field
- Export updates only Column 5 (target text) as Phrase expects

### 👁️ Show Invisibles Feature

**Display Invisible Characters:**
- 🔘 **Dropdown Menu**: Show Invisibles button with granular control
- ·  **Spaces**: Displayed as middle dot (·)
- →  **Tabs**: Displayed as right arrow (→)
- °  **Non-Breaking Spaces**: Displayed as degree symbol (°)
- ¶  **Line Breaks**: Displayed as pilcrow (¶)
- 🎯 **Toggle All**: Quick on/off for all invisible types

**Smart Handling:**
- 📋 **Clipboard Safety**: Ctrl+C copies original characters, not symbols
- 🖱️ **Double-Click Selection**: Properly selects words when invisibles shown
- ⌨️ **Ctrl+Arrow Navigation**: Word-by-word navigation works correctly
- 🎨 **Configurable Color**: Symbol color in Settings → View Settings (default: light gray)
- ✅ **Zero-Width Space Technique**: Uses U+200B for line-break opportunities without breaking word boundaries

**Technical Details:**
- Replacements applied only at display time (segment data never modified)
- Automatic reversal when text is saved or edited
- TagHighlighter extended to color invisible symbols

### 🔧 TM Pre-Translation Fix

**Batch Translate with TM:**
- 🐛 **Fixed TM-Only Mode**: Batch Translate dialog now properly handles TM as a translation provider
- 📖 **TM Provider Support**: Select "Translation Memory" in provider dropdown for TM-only batch translation
- 🎯 **Respects Activated TMs**: Uses project's activated TMs for matching
- 📊 **Match Threshold**: Accepts matches 70% and above for pre-translation

---

## [1.9.26] - December 8, 2025

### 🔄 Automatic Model Version Checker

**Smart Model Updates:**
- 🆕 **Auto-detect New LLM Models**: Automatically checks for new models from OpenAI, Anthropic, and Google
- 📅 **Daily Checks**: Runs once per 24 hours on startup (configurable)
- 🔔 **Smart Notifications**: Popup dialog only when new models are detected
- ✅ **Easy Selection**: Click to select which models to add to Supervertaler
- 💾 **Intelligent Caching**: Remembers last check to avoid unnecessary API calls
- ⚙️ **Fully Configurable**: Enable/disable auto-check in Settings → AI Settings
- 🔍 **Manual Check**: "Check for New Models Now" button for on-demand checking

**Implementation:**
- New module: `modules/model_version_checker.py` - Core checking logic with 24-hour throttling
- New module: `modules/model_update_dialog.py` - User-friendly PyQt6 dialogs
- Settings integration: New "Model Version Checker" section in AI Settings
- Cache system: Stores results in `user_data/model_version_cache.json`
- Provider support: OpenAI (models.list API), Claude (pattern testing), Gemini (models API)

**User Experience:**
- Silent operation: No interruption if no new models found
- Error handling: Graceful degradation if APIs unavailable
- Documentation: Complete UI standards guide to maintain consistency

### 🎨 UI Polish & Standardization

**Checkbox Consistency:**
- ✅ **Standardized All Checkboxes**: Replaced 3 blue QCheckBox instances with green CheckmarkCheckBox
- 📏 **Refined Size**: Reduced checkbox size from 18x18px to 16x16px for cleaner appearance
- 📚 **Documentation**: Created UI_STANDARDS.md to prevent future inconsistencies
- 🎯 **Visual Consistency**: All checkboxes now use custom green style with white checkmarks

**Fixed Checkboxes:**
- "Enable LLM (AI) matching on segment selection"
- "Auto-generate markdown for imported documents"
- "Enable automatic model checking (once per day on startup)"

---

## [1.9.25] - December 8, 2025

### 🐧 Linux Compatibility Release

**Platform Support:**
- ✅ **Full Linux Compatibility**: Supervertaler now runs perfectly on Ubuntu and other Linux distributions
- ✅ **Removed Legacy Dependencies**: Eliminated tkinter imports from TMX editor module
- ✅ **Complete requirements.txt**: All dependencies now properly documented and installable
- ✅ **Graceful Platform Detection**: AutoFingers shows helpful message on Linux (Windows/memoQ-specific feature)

**Installation Improvements:**
- 📦 **One-Command Setup**: `pip install -r requirements.txt` installs all dependencies
- 📝 **Added Missing Dependencies**:
  - `pyyaml` - YAML support for Non-Translatables manager
  - `PyMuPDF` - PDF processing for PDF Rescue module
  - `sentence-transformers` - Semantic search for Supermemory
  - `keyboard` - Keyboard control for AutoFingers
  - `lxml` - XML processing for Trados DOCX handler
- 🛠️ **Platform-Specific Notes**: Clear documentation for Linux, Windows, and macOS compatibility
- 🔧 **Optional Dependencies**: Voice dictation and automation features clearly marked as optional

**Bug Fixes:**
- 🐛 **Fixed AutoFingers Import**: Made `pyautogui` import optional with graceful fallback for Linux
- 🐛 **Fixed TMX Editor**: Removed unnecessary tkinter dependency from core module
- 🐛 **Fixed Import Errors**: Proper error handling for platform-specific features

**Technical Changes:**
- 🔄 **AutoFingers Engine**: Added `HAS_PYAUTOGUI` flag for cross-platform compatibility
- 🔄 **Import Guards**: Platform-specific features now detect availability at runtime
- 📚 **Documentation**: Enhanced requirements.txt with feature descriptions and platform notes

**For Users:**
- 🎯 **Fresh Installation**: Works out-of-the-box on fresh Ubuntu installations
- 🎯 **Virtual Environment**: Full support for Python venv isolated installations
- 🎯 **Cross-Platform**: Same codebase works on Windows, Linux, and macOS

---

## [1.9.24] - December 7, 2025

### ✨ Smart Word Selection
- **Intelligent Text Selection**: Selecting part of a word automatically expands to the full word
  - Makes word selection faster and less stressful during translation
  - Works in both source (read-only) and target (editable) columns
  - Supports compound words with hyphens (e.g., "self-contained")
  - Supports contractions with apostrophes (e.g., "don't", "l'homme")
  - Threshold-based: Only expands selections under 50 characters (prevents interference with multi-word selections)
- **Settings Toggle**: New "Enable smart word selection" checkbox in Settings → General → Editor Settings
  - Enabled by default
  - Helpful tooltip explains the feature with examples
  - Can be disabled if user prefers traditional selection behavior
- **Implementation**:
  - Added `mouseReleaseEvent()` to both `ReadOnlyGridTextEditor` and `EditableGridTextEditor`
  - Word character detection includes alphanumeric, underscore, hyphen, and apostrophe
  - Boundary detection ensures expansion only occurs when selection is partial
  - Respects settings toggle across the application
- **Documentation**: Complete feature documentation in `SMART_WORD_SELECTION.md`
  - Implementation details, testing checklist, known limitations, future enhancements

### 🛡️ Supermemory Error Handling Improvements
- **Better DLL Error Messages**: Enhanced PyTorch DLL loading failure handling
  - `modules/supermemory.py` now catches `OSError` and `Exception` (not just `ImportError`)
  - Windows-specific DLL errors are properly caught and handled
  - Stores error message in `SENTENCE_TRANSFORMERS_ERROR` for debugging
- **Helpful Instructions**: Auto-detects DLL errors and provides actionable solutions
  - Detects "DLL", "c10.dll", or "torch" in error messages
  - Provides 3 specific fixes with direct links and exact commands:
    1. Install Visual C++ Redistributables (https://aka.ms/vs/17/release/vc_redist.x64.exe)
    2. Reinstall PyTorch with exact pip commands
    3. Disable Supermemory auto-init in Settings as fallback
  - Instructions appear automatically in the log when error occurs
- **Technical Details**:
  - Modified `Supervertaler.py`: Lines 4116-4126 (error handler in `_auto_init_supermemory()`)
  - Modified `modules/supermemory.py`: Lines 45-51 (exception catching)

---

## [1.9.23] - December 7, 2025

### 📄 Bilingual Table Landscape Orientation
- **Improved Visualization**: Supervertaler Bilingual Table exports now use landscape orientation
  - Better visualization of long segments (source and target columns have more horizontal space)
  - Applies to both "With Tags" and "Formatted" export options
  - Page dimensions automatically swapped for landscape layout
  - Maintains 0.5-inch margins on all sides
- **Technical Details**:
  - Added `WD_ORIENT.LANDSCAPE` to document sections
  - Swapped page width/height for proper landscape rendering
  - Modified `Supervertaler.py`: Lines 7820-7832 (document setup)

---

## [1.9.22] - December 7, 2025

### 🤖 Gemini 3 Pro Preview Support
- **Latest Google AI Model**: Added support for Gemini 3 Pro Preview (November 2025 release)
  - New model option in Settings → LLM Settings → Gemini Models dropdown
  - Listed as "gemini-3-pro-preview (Latest - Superior Performance)"
  - Works in both single segment translation (Ctrl+T) and batch translation
  - Performance: 10-20% improvement on average, 6-20x better on reasoning/math tasks
  - Pricing: $2/$12 per million tokens (vs $1.25/$10 for Gemini 2.5 Pro)
- **LLM Client Update**: Added all current Gemini models to supported list
  - `gemini-2.5-flash-lite` (Fastest & Most Economical)
  - `gemini-2.5-pro` (Premium - Complex Reasoning)
  - `gemini-3-pro-preview` (Latest - Superior Performance)
  - Updated module documentation to reflect Gemini 3 support
- **Files Modified**:
  - `Supervertaler.py`: Lines 10889-10902 (model dropdown and tooltip)
  - `modules/llm_clients.py`: Lines 8-11 (docs), 220-229 (supported models)

---

## [1.9.21] - December 6, 2025

### 🐛 Critical SDLPPX Handler Bug Fix
- **Fixed SDLRPX Export Failure After Project Reload**: Fixed "'str' object is not callable" error when exporting SDLRPX return packages after reopening a saved project
  - Root cause: Handler was initialized with path string instead of log_callback parameter
  - The path was incorrectly assigned to `self.log`, causing export to fail when trying to call log function
  - Now correctly initializes handler with `TradosPackageHandler(log_callback=self.log)` and calls `load_package(path)` separately
  - Also fixed missing `self.sdlppx_source_file` assignment during handler restoration
  - Full SDLPPX workflow now works correctly: import package → translate → save project → close → reopen → export SDLRPX ✓
- **Impact**: This bug prevented translators from exporting return packages after reopening saved SDLPPX projects, breaking the workflow for Trados Studio package handling

---

## [1.9.20] - December 5, 2025

### 📦 SDLPPX Project Persistence
- **Project Save/Restore**: SDLPPX package path now saved in .svproj files
  - Added `sdlppx_source_path` field to Project dataclass
  - Serialized in `to_dict()`, deserialized in `from_dict()`
  - Full round-trip workflow now persists across sessions
- **Handler Restoration**: SDLPPX handler automatically restored on project load
  - When opening a .svproj from an SDLPPX import, handler is recreated
  - SDLRPX export available immediately without reimporting
  - Log message confirms: "✓ Restored Trados package handler"
- **Export Bug Fix**: Fixed SDLRPX export showing "0 translations updated"
  - Export now reads from segment objects instead of table widget items
  - Notes column was never populated as QTableWidgetItem - data is in segment.notes
  - Verified translations correctly written to return package

---

## [1.9.19] - December 4, 2025

### 📦 Trados Studio Package Support
- **SDLPPX Import**: Import Trados Studio project packages directly
  - File → Import → Trados Studio → Package (SDLPPX)
  - Parses SDLXLIFF files within the package
  - Shows package info dialog with file list and segment counts
  - Preserves SDL-specific markup and segment IDs
  - Automatic language detection from package metadata
- **SDLRPX Export**: Create return packages for delivery
  - File → Export → Trados Studio → Return Package (SDLRPX)
  - Writes translations back to SDLXLIFF files
  - Creates properly formatted return package
  - Round-trip workflow for freelance translators
- **Menu Reorganization**: Grouped all Trados import/export options
  - New "Trados Studio" submenu under Import and Export
  - Contains both bilingual review DOCX and package options
- **New Module**: `modules/sdlppx_handler.py` (767 lines)
  - `TradosPackageHandler` class for package management
  - `SDLXLIFFParser` for parsing SDL-extended XLIFF files
  - Handles `<g>`, `<x/>`, `<mrk mtype="seg">` tags
  - Preserves SDL namespaces and attributes

---

## [1.9.18] - December 4, 2025

### 🔍 Supermemory Concordance Integration
- Concordance Search (Ctrl+K) now includes Supermemory semantic search
- Two-tab interface: TM Matches tab for exact text, Supermemory tab for meaning
- Active checkbox column in Supermemory to control which TMs are searched
- Fixed Trados bilingual DOCX round-trip issues (xml:space, language settings)
- Supermemory moved from Tools tab to Resources tab

---

## [1.9.17] - December 3, 2025

### 🧠 Supermemory Enhancements - Domain Management & Superlookup Integration

**Major upgrade to the vector-indexed translation memory system:**

**Domain Management System:**
- Added **Domain dataclass** with name, description, color, and active status
- New database schema: `domains` table and `domain` column in `indexed_tms`
- **8 default domains:** General, Patents, Medical, Legal, Technical, Marketing, Financial, Software
- **DomainManagerDialog:** Full CRUD interface with color pickers and active toggles
- Assign domains during TMX import with intuitive dropdown selector
- Color-coded domain tags in search results for visual categorization

**Enhanced Search & Filtering:**
- **Language pair filter:** Dropdown to filter by source-target language combination
- **Multi-domain filter:** Select multiple active domains to search within
- **Dynamic column headers:** Results table shows actual language codes (e.g., "Source (EN)", "Target (NL)")
- Search respects both language pair and domain filters simultaneously

**Superlookup Integration:**
- **New "Supermemory" tab** in Superlookup for unified terminology/TM lookup
- Semantic search results appear alongside TM, termbase, and MT matches
- Click to insert matches directly into target segment
- Seamless integration with existing Superlookup workflow

**Export Functionality:**
- **Export to TMX:** Full TMX export with language headers and segment metadata
- **Export to CSV:** Simple source-target pairs for spreadsheet workflows
- Export dialog lets you choose format before exporting

### Consolidated AI Settings

- Merged Gemini and Mistral settings into unified **"AI Settings"** tab
- Cleaner Settings panel with fewer tabs
- All API keys and model selections in one place

---

## [1.9.18] - December 4, 2025

### 🔍 Supermemory Concordance Integration & Trados Fixes

**Concordance Search now includes Supermemory semantic search:**

**Concordance Search Enhancements:**
- **Two-tab interface:** "TM Matches" (exact text) and "Supermemory" (semantic/meaning-based)
- Semantic search finds translations by meaning, not just exact words
- Tab headers show result counts (e.g., "📋 TM Matches (9)" and "🧠 Supermemory (25)")
- Results display similarity scores with color-coded High/Medium/Low indicators
- Window remembers position and size across sessions (saved to project)

**Supermemory UI Improvements:**
- **Moved to Resources tab** - now under Resources → Supermemory (was Tools)
- **Active checkbox column** in TM table - toggle which TMs are searched
- Only active TMs are included in Concordance semantic search
- Checkbox state persists in database

**Trados Bilingual DOCX Fixes:**
- Fixed `xml:space="preserve"` attribute on text elements for proper whitespace handling
- Fixed target language settings - runs now inherit from paragraph (was incorrectly setting nl-NL)
- Added language selection dialog on import (Trados files don't specify languages)
- Source file path now persisted in project for reliable re-export
- "Source File Not Found" now offers to browse for file in new location

**Other Improvements:**
- Renamed export menu items to "Supervertaler Bilingual Table" for clarity
- memoQ and CafeTran source paths also persisted in project
- Fixed Concordance accessing Supermemory engine (was checking wrong attribute)

---

## [1.9.16] - December 1, 2025

### 🖥️ Local LLM Support - Ollama Integration

**Run AI translation entirely on your computer with no API costs, complete privacy, and offline capability:**

**New Provider Option:**
- Added **"Local LLM (Ollama)"** as new provider in Settings → LLM Provider tab
- Appears alongside OpenAI, Anthropic, Google, etc. with familiar radio button selection
- Works with single translation, batch translation, and AI Assistant chat

**Intelligent Hardware Detection:**
- Automatically detects system RAM and GPU capabilities
- Recommends optimal model based on your hardware:
  - **4GB RAM:** qwen2.5:3b (2.5GB download) - Basic functionality
  - **8GB RAM:** qwen2.5:7b (5.5GB download) - Recommended default
  - **16GB+ RAM:** qwen2.5:14b (10GB download) - Premium quality
- GPU detection for NVIDIA, AMD, and Apple Silicon

**Built-in Setup Wizard:**
- One-click access via "Setup Local LLM..." button in Settings
- Guides users through complete Ollama installation
- Platform-specific instructions (Windows, macOS, Linux)
- Real-time connection testing to verify Ollama is running
- Model download with progress tracking and cancellation

**Recommended Models for Translation:**
- **qwen2.5** (3B/7B/14B) - Excellent multilingual capabilities, recommended for translation
- **llama3.2** (3B/7B) - Strong general purpose, good European languages
- **mistral:7b** - Fast inference, good quality/speed balance
- **gemma2:9b** - Google's efficient model, good multilingual

**Status Widget in Settings:**
- Shows real-time Ollama connection status
- Displays currently selected model
- Quick-access button to Setup dialog
- Hardware specification summary

**Technical Implementation:**
- `modules/local_llm_setup.py` (NEW) - Complete setup module with:
  - `LocalLLMSetupDialog` - Full wizard UI with model recommendations
  - `LocalLLMStatusWidget` - Compact status widget for Settings panel
  - `detect_system_specs()` - RAM and GPU detection
  - `get_model_recommendations()` - Hardware-based model suggestions
  - `ModelDownloadWorker` - Background download with progress
  - `ConnectionTestWorker` - Async connection verification
- `modules/llm_clients.py` - Extended with Ollama support:
  - `OLLAMA_MODELS` dict with 7 supported models
  - `check_ollama_status()` - Connection and model detection
  - `_call_ollama()` - REST API integration (OpenAI-compatible)
  - `translate()` routes to Ollama when selected

**Privacy & Cost Benefits:**
- All translation processing stays on your computer
- No data sent to external servers
- No API key required
- No per-token costs - unlimited translations
- Works completely offline after model download

---

## [1.9.15] - November 30, 2025

### 📋 Supervertaler Bilingual Table Export/Import

**New bilingual table format for proofreading and review workflows:**

**Export Options (File → Export):**
- **"Bilingual Table - With Tags (DOCX)"**: Exports 5-column table (Segment #, Source, Target, Status, Notes) with raw Supervertaler tags preserved. Intended for proofreaders to review and edit - can be re-imported after editing
- **"Bilingual Table - Formatted (DOCX)"**: Same structure but applies formatting: `<b>` becomes actual bold, `<i>` becomes italic, `<u>` becomes underline, list tags become visible markers (• for bullets, ◦ for nested). For client delivery or archiving - cannot be re-imported

**Import Option (File → Import):**
- **"Bilingual Table (DOCX) - Update Project"**: Re-imports edited bilingual table, compares with current project by segment number, shows preview of all changes (old vs new target), applies approved changes with status reset to "Not Started"

**Document Format:**
- Header with "Supervertaler Bilingual Table" title linking to Supervertaler.com
- Language names in column headers (e.g., "English", "Dutch" instead of "Source", "Target")
- Pink highlighting for tags in the With Tags version
- Footer with Supervertaler.com branding
- Decorative underlines for professional appearance

**Technical Implementation:**
- `export_review_table_with_tags()` - Wrapper for tag-visible export
- `export_review_table_formatted()` - Wrapper for formatted export with warning dialog
- `_export_review_table(apply_formatting)` - Core export logic with python-docx
- `_add_hyperlink_to_paragraph()` - Helper for Word hyperlinks via XML manipulation
- `import_review_table()` - Import logic with change detection and diff preview

---

## [1.9.14] - November 30, 2025

### 📤 Improved DOCX Export & Keyboard Navigation

**DOCX Export Improvements:**
- **Formatting Preservation:** Export now properly converts `<b>`, `<i>`, `<u>`, `<bi>` tags to actual Word formatting (bold, italic, underline)
- **Multi-Segment Paragraphs:** Export handles paragraphs containing multiple segments with partial replacement
- **Unicode Cleanup:** Removes problematic characters like U+FFFC (Object Replacement Character)
- **Tag Stripping:** Properly strips all list tags (`<li-o>`, `<li-b>`, `<li>`) while preserving formatting tags

**Keyboard Navigation Fix:**
- Ctrl+Home now properly navigates to first segment even when editing inside a grid cell
- Ctrl+End now properly navigates to last segment even when editing inside a grid cell
- Added `_get_main_window()` helper to both `EditableGridTextEditor` and `ReadOnlyGridTextEditor`

**Technical Changes:**
- `export_target_only_docx()`: Added `apply_formatted_text_to_paragraph()` for parsing tags into Word runs
- `export_target_only_docx()`: Added `replace_segments_in_text()` for partial segment replacement
- `export_target_only_docx()`: Added `clean_special_chars()` to remove Unicode replacement characters
- `EditableGridTextEditor.keyPressEvent()`: Added Ctrl+Home/End handlers
- `ReadOnlyGridTextEditor.event()`: Added Ctrl+Home/End handlers

---

## [1.9.13] - November 30, 2025

### 📄 Document Preview & List Formatting Tags

**New Preview tab shows formatted document view:**

**Preview Tab Features:**
- New "Preview" tab alongside Source/Target views in the main panel
- Shows formatted document with headings (H1-H6 with proper sizing), paragraphs, and lists
- List items display with correct prefix: numbers (1. 2. 3.) for ordered lists, bullets (•) for bullet points
- Click any text in preview to instantly navigate to that segment in the grid
- Read-only view for document context during translation

**List Type Detection from DOCX:**
- New `_get_list_type()` method in docx_handler.py examines Word's numPr XML structure
- Properly distinguishes numbered lists from bullet points by analyzing abstractNum definitions
- Looks for "bullet" in numFmt value or bullet characters (•, ○, ●, ■) in lvlText
- Caches list type lookups for performance

**New List Tags:**
- `<li-o>` - Ordered list items (numbered: 1. 2. 3.)
- `<li-b>` - Bullet list items (•)
- Both tags are colored with the tag highlighter
- Both work with Ctrl+, shortcut for quick insertion

**Type Column Improvements:**
- Type column now shows `#1`, `#2`, `#3` for ordered list items (numbered)
- Shows `•` for bullet list items
- Shows `¶` (paragraph mark) for continuation paragraphs instead of `#`
- Provides clearer visual distinction between list types

**Technical Implementation:**
- Added `_setup_preview_tab()` for Preview tab creation
- Added `_render_preview()` method with formatted text rendering
- Added `_render_formatted_text()` helper for styled QTextEdit output
- Updated tag regex pattern to support hyphenated tags: `[a-zA-Z][a-zA-Z0-9-]*`
- Preview connects to `_preview_navigation_requested()` for click-to-navigate

---

## [1.9.12] - November 28, 2025

### 📊 Progress Indicator Status Bar

**New permanent status bar showing real-time translation progress:**

**Progress Display:**
- **Words translated**: Shows X/Y words with percentage (counts words in segments that have translations)
- **Confirmed segments**: Shows X/Y segments with percentage (confirmed, tr_confirmed, proofread, approved statuses)
- **Remaining segments**: Count of segments still needing work (not_started, pretranslated, rejected statuses)

**Color Coding:**
- **Red** (<50%): Low progress - needs attention
- **Orange** (50-80%): Making progress - keep going
- **Green** (>80%): Almost done - near completion

**Auto-Updates:**
- Updates when project is loaded
- Updates when segment is confirmed (Ctrl+Enter)
- Updates after AI translation completes
- Updates after user finishes typing (debounced)
- Resets to "--" when project is closed

**Technical Implementation:**
- Added `_setup_progress_indicators()` method for status bar widget setup
- Added `update_progress_stats()` method for calculating and updating progress
- Added `_get_progress_color()` helper for color-based progress feedback
- Progress widgets are permanent status bar items (right-aligned)

---

## [1.9.11] - November 28, 2025

### 🔧 Non-Translatables: Case-Sensitive & Full-Word Matching

**Improved non-translatables matching to prevent false positives:**

**Matching Improvements:**
- Non-translatables matching is now **case-sensitive by default**
- Only matches **full words** (not partial words like "Product" inside "ProductName")
- Uses word boundary detection (`\b`) for accurate term matching
- Smart fallback for special characters like ® and ™ that don't work with word boundaries
- Prevents unwanted replacements in the middle of compound terms

**Bug Fixes:**
- Fixed crash when closing project: added missing `stop_termbase_batch_worker()` method
- Fixed `.svprompt` files not showing in Prompt Library tree (added extension to both library and manager)
- Added LLM refusal detection for batch translation with helpful error messages when AI refuses content

**Technical Details:**
- Changed `case_sensitive` default to `True` in `NonTranslatablesManager.matches()`
- Rewrote matching logic to use regex word boundaries for full-word matching
- Added proper error handling for OpenAI content policy refusals during batch translation

---

## [1.9.10] - November 28, 2025

### 🔧 TM Search Fixes & Flexible Language Matching

**Fixed TM matches not appearing in Translation Results panel:**

**Root Cause Analysis:**
- `tm_metadata_mgr` was only initialized when user opened TM List tab, but TM search runs immediately on segment navigation
- Database had mixed language formats ("Dutch", "nl", "nl-NL") but search only looked for ISO codes
- Legacy hardcoded `enabled_only=True` filter would search only 'project' and 'big_mama' TMs that don't exist

**Fixes Applied:**
- **Early initialization:** `tm_metadata_mgr` now initializes in `initialize_tm_database()` when project loads
- **Flexible language matching:** New `get_lang_match_variants()` function returns both ISO codes and full language names
- **Bypass legacy filter:** Added `enabled_only=False` to all `search_all()` calls
- **Fallback search:** When no TMs are explicitly activated, search now falls back to all TMs

**Database Improvements:**
- Cleaned public database (`user_data/Translation_Resources/supervertaler.db`) for new GitHub users
- Removed sample data that had orphaned TM entries without proper metadata
- Schema preserved - new users start with empty, properly structured database

**Code Cleanup:**
- Removed legacy `project` and `big_mama` TM hardcoding from `TMDatabase` class
- These were from the previous Supervertaler architecture and are no longer used
- All TMs now managed through `TMMetadataManager` with proper database storage

**Files Modified:**
- `Supervertaler.py` - TM metadata manager early init, enabled_only=False for searches
- `modules/translation_memory.py` - Removed legacy tm_metadata dict
- `modules/database_manager.py` - Flexible language matching in get_exact_match() and search_fuzzy_matches()
- `modules/tmx_generator.py` - Added get_lang_match_variants() and updated get_base_lang_code()

### 📊 Non-Translatables Entry Table Enhancements

**Sortable Columns:**
- Columns in the Non-Translatables entry table are now sortable by clicking on column headers
- Click on Pattern, Type, or other columns to sort alphabetically ascending/descending
- Default sort by Pattern column (ascending)
- Sorting is temporarily disabled during table refresh to prevent UI issues

**Delete Entries:**
- Right-click on selected entries to access context menu with delete option
- Press Delete key to remove selected entries
- Menu dynamically shows "Delete 1 entry" or "Delete N entries" based on selection
- Existing "🗑️ Remove Selected" button also still available

---

## [1.9.9] - November 27, 2025

### 🎨 memoQ-style Alternating Row Colors

**CafeTran Formatting Support:**
- Pipe symbols (|) now highlighted in red/bold in grid editor (like CafeTran)
- Ctrl+, inserts pipe symbols for CafeTran formatting (or wraps selection)
- Ctrl+Shift+S copies source text to target cell

**Keyboard Shortcuts Improvements:**
- Keyboard shortcuts table now sortable by clicking column headers
- Removed "Save Project As" shortcut (Ctrl+Shift+S now dedicated to copy source)

**Settings Changes:**
- Batch size default changed from 100 to 20 segments per API call

---

## [1.9.7] - November 27, 2025

### 🔄 CafeTran Bilingual DOCX Support

**Full import/export support for CafeTran bilingual table format:**

**CafeTran Import:**
- New **Import > CafeTran Bilingual Table (DOCX)...** menu option
- Validates CafeTran bilingual format (ID | Source | Target | Notes table)
- Extracts segments with pipe symbol formatting markers preserved
- Converts to internal segment format for translation
- Stores handler for round-trip export

**CafeTran Export:**
- New **Export > CafeTran Bilingual Table - Translated (DOCX)...** menu option
- Writes translations back to Target column
- Preserves pipe symbol formatting (bold/underline markers)
- Maintains original table structure
- File can be imported back into CafeTran

**Technical Implementation:**
- Uses `modules/cafetran_docx_handler.py` module
- `CafeTranDOCXHandler` class handles file I/O
- `FormattedSegment` class preserves pipe symbol markers
- Red/bold formatting for pipe symbols in export

---

## [1.9.4] - November 26, 2025

### 🏷️ Tag-Based Formatting System for memoQ Bilingual Files

**Complete inline formatting support for professional translation workflows with memoQ bilingual DOCX files.**

**Phase 1 - Import & Display:**
- Import memoQ bilingual DOCX preserves bold, italic, underline as `<b>`, `<i>`, `<u>` HTML-style tags
- New "🏷️ Tags ON/OFF" toggle button in grid toolbar
- WYSIWYG mode: Shows formatted text (bold appears bold)
- Tag mode: Shows raw tags like `<b>bold</b>` for precise editing
- Keyboard shortcut: **Ctrl+Alt+T** to toggle between modes
- Tags auto-enabled after import when formatting detected
- TagHighlighter colorizes tags with pink background for visibility

**Phase 2 - Export with Formatting:**
- Export converts `<b>`, `<i>`, `<u>` tags back to actual Word formatting
- New `tagged_text_to_runs()` function parses tags into Word runs
- Round-trip fidelity: Import → Edit → Export preserves formatting
- Handles nested tags correctly (e.g., `<b><i>bold italic</i></b>`)

**Phase 3 - AI Translation with Tags:**
- Updated default system prompt with inline formatting tag instructions
- AI translates text while preserving and repositioning tags intelligently
- Example: "Click the `<b>`Save`</b>` button" → "Klik op de knop `<b>`Opslaan`</b>`"
- Tags placed around corresponding translated words, not just same position

**Formatting Shortcuts in Target Editor:**
- **Ctrl+B** - Apply/toggle bold tags on selected text
- **Ctrl+I** - Apply/toggle italic tags on selected text
- **Ctrl+U** - Apply/toggle underline tags on selected text

**Helper Functions Added:**
- `runs_to_tagged_text()` - Convert Word runs to tagged text on import
- `tagged_text_to_runs()` - Parse tags back to Word runs on export
- `strip_formatting_tags()` - Remove tags for plain text
- `has_formatting_tags()` - Check if text contains formatting tags
- `get_formatted_html_display()` - Convert tags to HTML for WYSIWYG display

---

## [1.9.6] - November 27, 2025

### 📁 Custom File Extensions & Monolingual Export

**New Branded File Extensions:**
- **Projects:** `.svproj` (was `.json`) - Supervertaler Project files
- **Prompts:** `.svprompt` (was `.md`/`.json`) - Supervertaler Prompt files  
- **Non-Translatables:** `.svntl` (was `.ntl`) - Supervertaler Non-Translatable lists
- All formats maintain full backward compatibility - opens legacy files seamlessly
- New files created with branded extensions for professional consistency
- Industry standards retained: `.tmx` for TM exports, `.srx` planned for segmentation

**Monolingual DOCX Import Improvements:**
- Language pair selection dialog when importing monolingual DOCX files
- Dropdown selectors for source and target language (12 languages supported)
- Prevents language detection issues - user explicitly sets translation direction
- Removed unreliable auto-detect language feature

**Target-Only DOCX Export:**
- New **Export > Target Only (DOCX)...** menu option for monolingual exports
- Preserves original document structure (tables, formatting, styles, headers)
- Copies original DOCX as template before replacing text
- Replaces text in both paragraphs and table cells
- Falls back gracefully if original document unavailable

**Project Persistence:**
- Original DOCX path now saved in project files (`original_docx_path`)
- Path restored when reopening projects for reliable exports
- Enables structure-preserving exports even after closing and reopening

**Documentation Updates:**
- New modular documentation: QUICK_START.md, KEYBOARD_SHORTCUTS.md, CAT_WORKFLOW.md
- Archived legacy USER_GUIDE.md and INSTALLATION.md
- FAQ.md copied to repository root (fixes dead link)

---

## [1.9.5] - November 27, 2025

### 📤 Send Segments to TM & memoQ Tag Shortcuts

**Send Segments to TM (Bulk Operation):**
- New dialog under **Edit > Bulk Operations > Send Segments to TM**
- Send translated segments directly to selected Translation Memories
- **Scope filters:** All segments, Current selection, or specific row range
- **Status filters:** Filter by Translated, Reviewed, Approved, Needs Review, or Final status
- Select multiple TMs to write to simultaneously
- Shows count of segments that will be sent before execution
- Progress feedback with success/failure counts

**memoQ Tag Insertion Shortcut:**
- **Ctrl+,** (Ctrl+Comma) - Insert next memoQ tag pair or wrap selection
- Smart tag insertion: Analyzes source segment for memoQ tags (`[1}`, `{1]`, `[3]`, etc.)
- With selection: Wraps selected text with next unused tag pair
- Without selection: Inserts next available tag pair at cursor
- Works with paired tags (`[1}...{1]`) and standalone tags (`[3]`)
- Respects tag order from source segment for consistency

**UI Improvements:**
- Renamed "Translation Resources" tab to "Resources" for cleaner UI
- Resources tab contains TM, Termbase, and MT/Web resources sub-tabs

---

## [1.9.3] - November 26, 2025

### 📋 Session Log Tab & TM/Termbase Defaults Fix

**Session Log Tab:**
- Added Session Log tab to bottom panel alongside Comments and Termview
- Real-time log display with timestamps in monospace font
- Easy access to log messages without detaching window
- Read-only display with automatic scrolling to latest entries

**TM/Termbase Checkbox Defaults Fixed:**
- Read checkboxes now default to unchecked (inactive) when no project loaded
- Read checkboxes default to unchecked when no activation record exists
- Write checkboxes default to unchecked (read-only) by default
- All settings properly restored from project.json when project is loaded
- Fixed `is_tm_active()` in tm_metadata_manager.py to return False by default

**Quick Actions for Bulk Selection:**
- Added "Select All Read" and "Select All Write" checkboxes above TM table
- Added "Select All Read" and "Select All Write" checkboxes above Termbase table
- Green checkbox for Read, blue checkbox for Write matching table style
- Quickly activate/deactivate all resources with single click

---

## [1.9.2] - November 25, 2025

### ⚙️ Superlookup Settings UI Redesign

**Improved Resource Selection Interface:**
- Redesigned Settings tab with sub-tabs for TM, Termbase, MT, and Web Resources
- Each resource type now has dedicated full-height space in its own sub-tab
- Replaced cramped single-page layout with spacious tabbed interface

**Proper Checkbox Styling:**
- Replaced tiny multi-selection indicators with standard Supervertaler checkboxes
- 18x18px checkbox size with green (#4CAF50) background when checked
- White checkmark (✓) drawn on checked items matching AutoFingers style
- QScrollArea + CheckmarkCheckBox widgets instead of QListWidget
- Hover effects and proper visual feedback

**Technical Implementation:**
- `create_settings_tab()`: Creates QTabWidget with 4 sub-tabs
- `create_tm_settings_subtab()`: Full-height TM selection with checkboxes
- `create_termbase_settings_subtab()`: Full-height termbase selection
- `create_mt_settings_subtab()`: Placeholder for future MT integration
- `create_web_settings_subtab()`: Placeholder for future web resources
- CheckmarkCheckBox widgets in QScrollArea provide proper green checkboxes
- Fixed `cursor()` → `cursor` property access for database queries

**Bug Fixes:**
- Fixed Translation Memories list loading (was showing empty due to cursor() call error)
- Fixed termbase loading timing (lazy loading when Settings tab viewed)
- Proper checkbox state tracking with `setProperty()` and `property()` methods
- Select All/Clear All buttons now work with checkbox widgets instead of selection

**User Experience:**
- Much more spacious and easier to read
- Clear visual separation between resource types
- Checkboxes are now clearly visible and clickable
- Consistent styling across entire application

---

## [1.9.1] - November 24, 2025

### ↩️ Undo/Redo for Grid Edits

**New Feature: Complete Undo/Redo System**
- Full undo/redo support for all grid editing operations
- Keyboard shortcuts: Ctrl+Z (Undo), Ctrl+Y/Ctrl+Shift+Z (Redo)
- Edit menu actions with dynamic enabled/disabled states
- 100-level undo history to prevent memory issues

**What's Tracked:**
- Target text changes as you type
- Status changes (Not Started → Translated → Confirmed)
- Ctrl+Enter confirmations
- Find/Replace batch operations
- Document view edits

**Technical Implementation:**
- Dual stack system (undo_stack + redo_stack) tracks segment changes
- Records: segment_id, old_target, new_target, old_status, new_status
- Smart recording: Only captures actual changes, ignores no-ops
- Automatic redo stack clearing on new edits (standard undo behavior)
- Stack trimming to max 100 levels for memory efficiency
- Updates both segment data and grid display simultaneously

**Integration Points:**
- `on_target_text_changed()`: Text editing in grid cells
- `update_status_icon()`: Status changes via toolbar/ribbon
- `on_doc_status_change()`: Document view status changes
- `replace_all_matches()`: Batch find/replace operations
- Ctrl+Enter confirmation handler

**User Experience:**
- Menu actions show enabled/disabled state based on stack contents
- Seamless integration with existing editing workflow
- No performance impact on grid operations
- Professional CAT tool behavior (like memoQ/Trados)

---

## [1.9.0] - November 24, 2025

### 🔍 Termview - RYS-Style Inline Terminology Display

**New Feature: Visual Inline Terminology**
- Added "🔍 Termview" tab in bottom panel showing inline terminology like RYS Trados plugin
- Source text displayed as flowing words with translations appearing underneath matched terms
- Compact 8pt font with colored 2px top borders (pink for project termbase, blue for background)
- Text wrapping with FlowLayout to adapt to window width
- Click any translation to insert it into target segment
- Hover tooltips show full term details and metadata

**Technical Implementation:**
- `modules/termview_widget.py`: New widget with FlowLayout, TermBlock classes for visual display
- RYS-style tokenization preserves multi-word terms (e.g., "De uitvinding heeft betrekking op een werkwijze")
- Direct integration with Translation Results termbase cache for instant updates
- Smart refresh: Updates immediately after termbase search completes

**Termbase Search Enhancements:**
- Fixed punctuation handling: Terms like "gew.%" now matched correctly
- Changed from `strip()` to `rstrip()/lstrip()` to preserve internal punctuation
- Use lookaround word boundaries `(?<!\w)(?!\w)` for terms with punctuation
- Standard `\b` boundaries for regular words

**Bug Fixes:**
- Fixed data format mismatch between termbase cache dict and Termview list format
- Fixed timing issue where Termview updated before termbase search completed
- Fixed tokenization regex to capture terms with special characters
- Removed debug logging after successful implementation

### 🎯 Priority & Visual Improvements
- Project termbases (#1 priority) display with pink border for instant recognition
- Background termbases display with blue border
- Clean, minimal design with 1px padding and compact spacing

---

## [1.8.0] - November 23, 2025

### UI/UX Improvements
- **Tab Styling Refinement**: Reduced selected tab border-bottom from 3px to 1px for a more subtle, professional appearance
- **Visual Consistency**: Maintained light blue background highlighting (rgba(33, 150, 243, 0.08)) with thinner accent line
- **Applied Across Application**: Updated styling for all tab widgets including Resources, Modules, TM, Settings, Domain, Import, Results, and Prompt Manager tabs
- **Theme Manager Update**: Global tab styling now uses refined 1px border-bottom for consistent appearance

### Technical Changes
- Updated border-bottom styling in 12 locations across main application and modules
- Modified theme_manager.py for global tab appearance consistency
- Maintained focus removal and outline suppression for cleaner tab interactions

---

## [1.6.6] - November 23, 2025

### ✅ Simplified TM/Termbase Management System

**Major Redesign:**

- 🎯 **Simple Read/Write Checkbox System**
  - Removed confusing "Active" checkbox and "Project TM/Termbase" concepts
  - **Translation Memories:** Simple Read (green ✓) and Write (blue ✓) checkboxes
  - **Termbases:** Simple Read (green ✓) and Write (blue ✓) checkboxes  
  - All TMs and termbases start completely unchecked by default
  - Users explicitly check Read to use for matching, Write to allow updates
  
- 📊 **Auto-Priority System for Termbases**
  - Priorities 1-N automatically assigned to Read-enabled termbases
  - Priority #1 = Project Termbase (pink highlighting, highest priority)
  - Priority #2, #3, etc. = Background termbases (lower priorities)
  - No manual project termbase designation needed - just check Read boxes
  - Priority based on activation order (ranking in database)

- 🎨 **Cleaner Column Layout**
  - **TMs:** `TM Name | Languages | Entries | Read | Write | Last Modified | Description`
  - **Termbases:** `Type | Name | Languages | Terms | Read | Write | Priority`
  - Removed redundant columns and confusing labels
  - Type auto-shows "📌 Project" for priority #1, "Background" for others

- 🔒 **Read-Only Database Defaults**
  - New TMs created with `read_only=1` (Write unchecked by default)
  - New termbases created with `read_only=1` (Write unchecked by default)
  - Prevents accidental updates to reference memories
  - User must explicitly enable Write for TMs/termbases they want to update

**Benefits:**
- Much simpler mental model: Read = use for matching, Write = allow updates
- No more confusion about "Active" vs "Project" vs "Background"
- Project termbase is simply the highest priority (first activated)
- Clear visual feedback with color-coded checkboxes (green Read, blue Write)
- Safer defaults prevent accidental corruption of reference resources

---

## [1.7.9] - November 22, 2025

### 🔍 Find/Replace & TM Enhancements

**Fixed:**

- ✨ **Find/Replace Highlighting System** - Complete rewrite using consistent QTextCursor approach
  - "Find Next" now correctly highlights matches with yellow background
  - "Highlight All" button now actually highlights all matches in the grid
  - Font size no longer changes during navigation (previously shrunk with each find)
  - Switched from QLabel+HTML (which replaced widgets) to QTextCursor+QTextCharFormat (preserves existing widgets)
  - Matches same highlighting system used by filter boxes
  - Supports case-sensitive/insensitive, whole words, and entire segment modes

- ✨ **No More TM Saves During Find/Replace** - Eliminated slowdowns during search navigation
  - Added `find_replace_active` flag to disable background TM saves
  - Prevents segments from being saved to TM on every "Find Next" click
  - Re-enables TM saves when dialog closes
  - Also disables expensive TM/MT/LLM lookups during find/replace operations
  - Results in much faster navigation through search results

**Added:**

- 🌍 **Bidirectional TM Search** - TMs now search in both directions automatically
  - When translating nl→en, also searches en→nl TMs for reverse matches
  - Example: English source text can match Dutch source in reverse TM
  - Reverse matches clearly marked with "Reverse" indicator
  - Improves TM utilization by ~2x without any user action required

- 🌍 **Language Variant Matching** - Base language codes match all regional variants
  - "en" matches "en-US", "en-GB", "en-AU" automatically
  - "nl" matches "nl-NL", "nl-BE" automatically  
  - TMX import now handles language variants gracefully
  - User can choose to strip variants or preserve them during import
  - Supports bidirectional matching with variants (e.g., nl-BE → en-US works both ways)

- 💾 **Activated TM Persistence** - Projects remember which TMs are active
  - Activated TMs saved to `project.json` in `tm_settings.activated_tm_ids`
  - Automatically restored when project is reopened
  - No more manually re-activating TMs for each project session
  - Works per-project (different projects can have different active TMs)

- 📝 **TM Pre-Check in Batch Translation** - Saves API costs by checking TM first
  - Before making expensive API calls, checks if 100% TM matches exist
  - Auto-inserts TM matches and skips API translation for those segments
  - Shows clear log of how many API calls were saved
  - Can save significant costs on projects with high TM leverage
  - Controlled by "Check TM before API call" setting (enabled by default)

- 🎨 **Language Display Normalization** - Consistent language variant format
  - All language variants displayed as lowercase-UPPERCASE (e.g., nl-NL, en-US)
  - Previously: inconsistent formats like "nl-nl", "EN-us", "NL-BE"
  - Now: standardized as "nl-NL", "en-US", "nl-BE"
  - Applied in TM manager UI, TMX import dialogs, and all TM displays

**Technical Details:**

- **Find/Replace Highlighting:**
  - `highlight_search_term()` rewritten to use `QTextCursor` and `QTextCharFormat`
  - `highlight_all_matches()` rewritten to actually highlight instead of just filtering
  - Added `processEvents()` after grid load to ensure widgets exist before highlighting
  - Files: `Supervertaler.py` lines 15726-15792, 15982-16008

- **TM Save Prevention:**
  - Added `find_replace_active` flag check in `_handle_target_text_debounced_by_id()` (line 13660)
  - Added same check in `update_status_icon()` (line 13703)
  - Added check in `on_cell_selected()` to skip TM/MT/LLM lookups (line 14050)
  - Files: `Supervertaler.py` lines 13657-13664, 13699-13709, 14044-14051

- **Bidirectional Search:**
  - `get_exact_match()` now searches reverse direction if no forward match found
  - `search_fuzzy_matches()` includes reverse direction results
  - Results marked with `reverse_match: True` metadata
  - Files: `modules/database_manager.py` lines 635-732, 744-810

- **Language Variant Matching:**
  - Added `get_base_lang_code()` to extract base from variants (en-US → en)
  - Added `normalize_lang_variant()` for consistent display formatting
  - Added `languages_are_compatible()` for base code comparison
  - Database queries use LIKE pattern: `(source_lang = 'en' OR source_lang LIKE 'en-%')`
  - Files: `modules/tmx_generator.py` lines 119-156, `modules/database_manager.py` lines 652-676

- **TMX Import with Variants:**
  - `detect_tmx_languages()` reads all language codes from TMX
  - `check_language_compatibility()` analyzes variant mismatches
  - `_load_tmx_into_db()` accepts `strip_variants` parameter
  - User dialog offers "Import with variant stripping" vs "Create new TM"
  - Files: `modules/translation_memory.py` lines 408-557, `Supervertaler.py` lines 4807-4903

- **TM Persistence:**
  - Added `tm_settings` field to `Project` class (line 223)
  - `save_project_to_file()` saves activated TM IDs (lines 11442-11449)
  - `load_project()` restores activated TMs (lines 10797-10816)
  - Files: `Supervertaler.py` lines 220-285, 10794-10816, 11439-11449

**User Experience:**

- Find/Replace dialog now fast and responsive with proper highlighting
- "Highlight All" button finally works as expected
- No font size changes during search navigation
- TMs work across language variants automatically (no manual configuration)
- Projects remember your TM activation choices
- Batch translation saves money by checking TM first
- Clear visual feedback for all TM operations

---

## [1.7.8] - November 22, 2025

### 🔍 Filter Highlighting Fix

**Fixed:**

- ✨ **Filter Search Term Highlighting** - Fixed highlighting of search terms in filtered segments
  - Source and target filter boxes now correctly highlight matching terms in yellow
  - Previously used delegate-based highlighting which was bypassed by cell widgets
  - New implementation uses widget-internal highlighting with QTextCursor + QTextCharFormat
  - Case-insensitive matching: "test", "TEST", "TeSt" all match "test"
  - Multiple matches per cell are highlighted correctly
  - Highlights automatically clear when filters are removed

**Technical Details:**

- **Root Cause:** Source/target cells use `setCellWidget()` with QTextEdit widgets, which completely bypass `QStyledItemDelegate.paint()` method
- **Solution:** Created `_highlight_text_in_widget()` method that applies highlighting directly within QTextEdit widgets
- **Implementation:**
  - Uses `QTextCursor` to find all occurrences of search term in widget's document
  - Applies `QTextCharFormat` with yellow background (#FFFF00) to each match
  - Clears previous highlights before applying new ones
  - Modified `apply_filters()` to call widget highlighting instead of delegate approach
  - `clear_filters()` automatically clears highlights by reloading grid
- **Files Modified:**
  - `Supervertaler.py` (lines ~15765-15810): New `_highlight_text_in_widget()` method
  - `Supervertaler.py` (lines ~15779-15860): Modified `apply_filters()` to use widget highlighting
- **Documentation Added:**
  - `docs/FILTER_HIGHLIGHTING_FIX.md` - Complete technical explanation of the fix

**User Experience:**

- Filter boxes now work as expected with visible yellow highlighting
- Improves searchability and visual feedback when filtering segments
- No performance impact with large segment counts (tested with 219 segments)

---

## [1.7.7] - November 21, 2025

### 🎯 Termbase Display Customization

**Added:**

- ✨ **User-Configurable Termbase Sorting** - Control how termbase matches are displayed
  - Three sorting options available in Settings → General:
    - **Order of appearance in source text** (default) - Matches appear as they occur in the segment
    - **Alphabetical (A-Z)** - Matches sorted by source term alphabetically
    - **By length (longest first)** - Longer multi-word terms prioritized over shorter ones
  - Sorting preference persists across sessions
  - Only affects termbase matches; TM, MT, and LLM results maintain their existing order

- ✨ **Smart Substring Filtering** - Reduces termbase match clutter
  - Optional "Hide shorter termbase matches" checkbox in Settings → General
  - Automatically filters out shorter terms that are fully contained within longer matched terms
  - Example: If both "cooling" and "cooling system" match, only "cooling system" is shown
  - Helps focus on the most relevant multi-word terminology
  - Can be toggled on/off without restarting the application

**Enhanced:**

- 🔧 **Bold Font for Project Resources** - Project termbases and TMs now display with bold provider codes (TB, TM) instead of asterisks for cleaner visual distinction
- 🎨 **Translation Results Panel** - Added parent app reference for accessing user settings dynamically

**Technical Details:**

- Settings stored in `ui_preferences.json` under `general_settings`
- `TranslationResultsPanel` now accepts `parent_app` parameter for settings access
- New methods: `_sort_termbase_matches()` and `_filter_shorter_matches()` in `translation_results_panel.py`
- Sorting uses case-insensitive comparison for alphabetical mode
- Filtering uses substring detection with length comparison
- Files Modified:
  - `Supervertaler.py` (lines 2391-2393, 7377-7406, 8316-8360, 8930, 9548, 12604-12606)
  - `modules/translation_results_panel.py` (lines 626-628, 1201-1276, 1324-1329)

**User Experience:**

- Settings are immediately accessible via Settings → General → TM/Termbase Options
- Tooltips explain each option clearly
- Changes apply to all subsequent segment matches
- No performance impact on match retrieval

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
- **🔍 Detachable Superlookup:** Multi-screen support for Superlookup module
  - Detach button on Home tab to open Superlookup in separate window
  - Perfect for multi-monitor workflows - move lookup to second screen while translating
  - Proper window positioning and multi-monitor detection
  - Reattach functionality to return to embedded mode

### Improved
- **🏠 Home Tab Enhancements:**
  - Integrated About section directly into header with improved visibility
  - Better text styling with purple gradient for subtitle and version (larger, bold)
  - Reorganized layout: About in header, Resources & Support next, Projects at bottom
  - Projects section with distinct background color for visual separation
  - Superlookup prominently featured on right side of Home tab

### Fixed
- **Multi-Monitor Support:** Fixed window positioning for detached Superlookup
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
  - Embedded Superlookup for instant translations
  - Clean, modern design with proper visual hierarchy
  
- **Major UI Reorganization:** Complete restructuring of main interface
  - **Tab Order Redesigned:** 
    1. 🏠 Home (NEW - welcome screen)
    2. 💡 Prompt Manager (moved up from #5)
    3. 📝 Editor (renamed from "Project Editor")
    4. �️ Resources (organized nested tabs)
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
- Superlookup tab → Shows Translation ribbon
- Project Editor tab → Shows Home ribbon
- Intelligent tab selection for better workflow

**2. ✅ Quick Access Toolbar (QAT)**
- Mini toolbar above ribbon with most-used commands
- **Actions**: New 📄, Open 📂, Save 💾, Superlookup 🔍, Translate 🤖
- **Minimize Ribbon toggle** ⌃ - Collapse ribbon to tabs-only
- Always visible for quick access to favorites
- Icon-only buttons for compact display

**3. ✅ Quick Access Sidebar** (NEW)
- memoQ-style left navigation panel
- **Collapsible sections**:
  - **Quick Actions**: New, Open, Save
  - **Translation Tools**: Superlookup, AutoFingers, TM Manager
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
  - **Translation**: Translate, Batch Translate, TM Manager, Superlookup
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
  - Superlookup - Dictionary/search tool
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

