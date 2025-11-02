# Supervertaler Qt Edition - Changelog

All notable changes to the **Qt Edition** of Supervertaler are documented in this file.

The Qt Edition is the **primary version** for active development and new features. See [CHANGELOG_Tkinter.md](CHANGELOG_Tkinter.md) for the legacy Classic edition.

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
