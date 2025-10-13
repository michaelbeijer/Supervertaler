# Supervertaler CAT Edition - Changelog

**Version Line**: v3.x.x-beta (Segment-based CAT Editor Architecture)

---

## [3.5.0-beta] - 2025-10-14 📊 DATA FORMAT STANDARDIZATION

> **Major Feature**: Unified Supervertaler Project Data Format (DOCX/TSV) for import/export workflows

### 🆕 NEW FEATURES

**Supervertaler Project Data Format** 📊
- **Unified Export Format**: Single format in two file types (DOCX table or TSV spreadsheet)
  * **6 Columns**: ID, Status, Source, Target, Paragraph, Notes
  * **Complete Metadata**: Full preservation of translation state
  * **Round-trip Ready**: Designed for reimport (planned for v3.6.0)
  * Menu: Export > Supervertaler project data (DOCX/TSV)...
- **Format Selection Dialog**: Custom dialog with proper buttons
  * Green "DOCX (Word table)" button - For review/printing in Word
  * Blue "TSV (Spreadsheet)" button - For Excel analysis/scripting
  * Clear message explaining both formats contain identical data
  * Replaces confusing Yes/No dialog
- **True Format Equivalence**: Both formats now export ALL 6 columns
  * DOCX: Full table with ID, Status, Source, Target, Paragraph, Notes
  * TSV: Tab-separated with same 6 columns
  * Previous DOCX only had 3 columns (ID, Source, Target)
- **Professional Table Styling**: DOCX uses "Light Grid Accent 1" with bold headers

**Export Menu Refinement** 🎯
- **"Translated document (DOCX/TXT)"**: Choose output format
  * DOCX - Preserves formatting for final delivery
  * TXT - Plain text for copyediting/review
- **Descriptive Labels**: All export options now clearly state purpose
  * "Translation memory (TMX)" instead of just "TMX"
  * "Manual copy/paste translation workflow (TXT)" instead of "Bilingual data for reimport"
- **Workflow Pairing**: Import/Export options with identical names
  * Import: "Manual copy/paste translation workflow (TXT)"
  * Export: "Manual copy/paste translation workflow (TXT)"
  * Perfect round-trip clarity

**Plain Text Export** 📝
- **New Export Option**: Export target text only (TXT format)
  * One segment per line
  * No formatting, no metadata
  * Perfect for plain text delivery or copyediting
  * Called by "Translated document (DOCX/TXT)" when TXT selected

### 🏗️ ARCHITECTURE IMPROVEMENTS

**Export Methods** 📦
- **New Method**: `export_translated_document()` - Format choice wrapper
  * Shows dialog: DOCX or TXT?
  * Routes to appropriate export method
  * Clean separation of concerns
- **New Method**: `export_txt_translated()` - Plain text export
  * Exports target text only
  * One segment per line
  * UTF-8 encoding
- **New Method**: `export_supervertaler_data()` - Unified format wrapper
  * Shows custom format selection dialog
  * Routes to DOCX or TSV export
  * Explains both formats contain same data
- **New Method**: `export_bilingual_docx_full()` - Complete DOCX export
  * Creates 6-column table (was 3 columns)
  * Uses python-docx directly (bypasses docx_handler module)
  * Matches TSV format exactly
  * Bold headers, professional styling

**Format Specification Document** 📋
- **New File**: `SUPERVERTALER_DATA_FORMAT.md` (comprehensive specification)
  * Complete format documentation
  * Column structure definition
  * Future extensions planned (proofreading, glossary, QA, collaboration)
  * Version evolution roadmap
  * Use case descriptions
  * Design principles

### 🐛 BUG FIXES

**Export Dialog UX** 🔧
- Fixed counterintuitive Yes/No dialog for format selection
  * OLD: "Yes = DOCX, No = TSV, Cancel = Cancel" (confusing!)
  * NEW: Custom dialog with clear "DOCX (Word table)" and "TSV (Spreadsheet)" buttons
  * Much better user experience

**DOCX Export Completeness** 🔧
- Fixed incomplete DOCX export in Supervertaler format
  * OLD: Only 3 columns (ID, Source, Target) - not equivalent to TSV
  * NEW: All 6 columns (ID, Status, Source, Target, Paragraph, Notes)
  * True format equivalence achieved

### 📚 DOCUMENTATION

**New Documentation Files**
- `SUPERVERTALER_DATA_FORMAT.md` - Complete format specification
  * Current implementation details
  * Planned extensions (v3.6.0-v4.0.0)
  * Proofreading workflow design
  * Glossary integration plan
  * QA workflow concepts
  * Collaborative translation ideas
  * Version comparison features

**Updated Documentation**
- `TERMINOLOGY_UPDATE_SUMMARY.md` - Import/Export terminology guide
- `EXPORT_MENU_UPDATE.md` - Comprehensive export menu documentation
- `CHANGELOG-CAT.md` - Complete v3.5.0-beta changes
- `README.md` - Updated feature list and version number

### 🎯 DESIGN PRINCIPLES

**User Experience Focus**
- **Clear Labels**: Descriptive menu items ("Translation memory (TMX)" not "TMX")
- **Purpose-Driven**: Labels explain what export does ("for reimport", "with metadata")
- **Workflow Pairing**: Identical names for Import/Export round-trips
- **Format Flexibility**: Single menu item, multiple format choices
- **Professional Appearance**: Matches modern CAT tool standards

**Technical Excellence**
- **Format Equivalence**: DOCX and TSV contain identical data
- **Extensible Architecture**: Ready for future enhancements (import, proofreading, glossary)
- **Clean Code**: New methods with clear responsibilities
- **Comprehensive Documentation**: Complete specifications for developers

### 🚀 FUTURE ROADMAP

**Planned Features** (Using Supervertaler Project Data Format)
- **v3.6.0**: Import Supervertaler project data (DOCX/TSV) - Proofreading workflow
- **v3.7.0**: Glossary import/export using same format
- **v3.8.0**: QA workflow with review status tracking
- **v3.9.0**: Collaborative translation (split/merge segments)
- **v4.0.0**: Version comparison and change tracking

---

## [3.4.0-beta] - 2025-10-13 🖼️ FIGURE CONTEXT & UI POLISH

> **Major Feature**: Multimodal AI support with figure context for technical translations + Complete UI standardization

### 🆕 NEW FEATURES

**Figure Context (Visual Context for Technical Translations)** 🖼️
- **Multimodal AI Integration**: Automatically include images when translating segments with figure references
  * Auto-detection: Scans text for "Figure 1", "fig. 2A", "Figuur 3b" patterns
  * Smart matching: Maps detected references to loaded images
  * Transparent routing: Switches to multimodal API when figures detected
- **Three Provider Support**:
  * OpenAI: Base64-encoded PNG via data URLs
  * Claude: Structured base64 content blocks
  * Gemini: Direct PIL.Image support
- **Images Tab UI**: Fully functional display in assistant panel
  * Live thumbnail preview (200px max width)
  * Image dimensions display
  * Folder name and image count
  * Load/Clear buttons
- **Status Indicators**: Figure count shown in context status bar
  * "Context: ... | 🖼️ 3 figures" when images loaded
- **Project Persistence**: Figure context folder saved with projects
  * Auto-reload: Images restored when reopening project
- **Supported Formats**: PNG, JPG, JPEG, GIF, BMP, TIFF
- **Filename Patterns**: "Figure 1.png", "Figure 2A.jpg", "fig3b.png"

**Menu Standardization (British Sentence Case)** 📝
- **Consistent Capitalization**: All menu items now use sentence case
  * Before: "Save Project", "Clear All Targets", "Grid View"
  * After: "Save project", "Clear all targets", "Grid view"
- **Improved Readability**: Matches modern UI conventions (VS Code, memoQ, CafeTran)
- **90+ Items Updated**: Project, File, Edit, View, Resources, Help menus

**Monolingual TXT Import (Auto-Segmentation)** 📄
- **New Feature**: Import plain text documents and auto-segment into sentences
  * Perfect for articles, essays, books, blog posts, reports
  * Uses `SimpleSegmenter` module for intelligent sentence detection
  * No manual preparation needed - just import and translate
  * Menu: File > Import > Monolingual document (TXT)...
- **Smart Segmentation**:
  * Handles abbreviations correctly (Dr., Inc., etc.)
  * Preserves sentence boundaries
  * Works with multiple paragraph formats

**Terminology Clarity (Import/Export Menus)** 🏷️
- **Improved Menu Organization**: Clear distinction between workflows
  * **Monolingual documents (DOCX/TXT)** - Regular files to translate
  * **Bilingual tables (DOCX)** - memoQ/CafeTran/Trados exported tables
  * **Manual copy/paste workflow (TXT)** - For pasted CAT tool columns
- **Menu Grouping**: Separators added for visual organization
- **Export Menu Updates**:
  * **"Translated document (DOCX/TXT)"** - Choose format (DOCX preserves formatting, TXT is plain text)
  * **"Supervertaler bilingual table (DOCX)"** - Can be reimported for proofreading workflow
  * **"Translation memory (TMX)"** - Standard TM format
  * **"Bilingual data for reimport (TXT)"** - Tab-delimited for reimport
  * **"Full data with metadata (TSV)"** - Complete export with status, notes, etc.
  * **CAT tool exports** renamed: "memoQ/CafeTran/Trados bilingual table - Translated (DOCX)"
- **Docstring Updates**: All import/export methods updated with clear descriptions

### 🏗️ ARCHITECTURE IMPROVEMENTS

**Modularization - Figure Context Manager** 📦
- **New Module**: `modules/figure_context_manager.py` (~400 lines)
  * `FigureContextManager` class with clean API
  * `normalize_figure_ref()` helper function
  * `pil_image_to_base64_png()` encoding utility
- **Code Reduction**: Main file reduced by ~200 lines (14,957 → 14,751)
- **Better Maintainability**: All figure context logic in one place
- **Testable**: Module can be unit tested independently
- **Reusable**: Can be used in other translation tools

**Multimodal API Methods** 🤖
- `call_openai_api_with_images(prompt, images)` - GPT-4 Vision support
- `call_claude_api_with_images(prompt, images)` - Claude Vision support  
- `call_gemini_api_with_images(prompt, images)` - Gemini Vision support
- Auto-detection in `translate_current_segment()` switches to multimodal when needed

### 🐛 BUG FIXES

**TXT Import Crash Fix** 🔧
- Fixed crash when importing TXT files: `'Supervertaler' object has no attribute 'grid_inner_frame'`
  * Removed duplicate `load_segments_to_grid()` call
  * Ensured `switch_from_start_to_grid()` happens before loading segments
  * Proper UI initialization order

**Import Fixes**
- Added missing `ImageTk` import from PIL (fixes thumbnail display error)
- Module imports now include figure context manager

**Code Cleanup**
- Removed duplicate `normalize_figure_ref()` functions (2 copies consolidated)
- Removed duplicate `pil_image_to_base64_png()` function
- Removed duplicate `detect_figure_references()` function

### 🎨 UI/UX IMPROVEMENTS (from previous v3.4.0 release)

**Status Icons** (memoQ-style visual indicators)
- **Status Column Redesign**: Text labels replaced with color-coded icons
  * ✗ (Red #F44336) - Untranslated segments
  * ~ (Orange #FF9800) - Draft segments
  * ✓ (Green #4CAF50) - Translated segments
  * ✓✓ (Dark Blue #1976D2) - Approved segments
  * 🔒 (Blue #2196F3) - Locked segments
- **Column Reordering**: Status moved to rightmost column (after Target)
  * Previous: # - Type - Style - Source - Status - Target
  * New: # - Type - Style - Source - Target - Status
- **Space Optimization**: Status column width reduced from 75px → 30px (45px reclaimed)
- **Fixed-width Container**: 30px Frame prevents text overflow
- **Visual Hierarchy**: 14pt bold icons for better visibility
- **Language Independence**: Icons replace text for universal understanding

**Multi-Selection System** (Ctrl/Shift modifiers)
- **Ctrl+Click**: Toggle individual segment selection (add/remove)
- **Shift+Click**: Range selection from last selected segment
- **Ctrl+A**: Select all visible segments
- **Visual Feedback**: 
  * Selected rows highlighted with blue background (#CCE5FF)
  * ID column clickable for selection
  * Selection counter in status bar
- **Bulk Operations**: All segment operations work on selected segments
  * Change Status (Ctrl+T)
  * Lock/Unlock Segments (Ctrl+L)
  * Clear Selection

**Selection Counter** (Status bar integration)
- **Display**: Shows "X segment(s) selected" in status bar
- **Log Messages**: Confirms selection changes
- **Real-time Updates**: Counter updates on every selection change

**Responsive Button Layout** (Grid Editor panel)
- **Compact Layout**: 55% vertical space reduction
  * Padding reduced: 10px → 5px
  * Font size: 10pt → 8-9pt
  * Widgets: 2-line → 1-line (dropdowns, entries)
- **Button Groups**: Organized with separators
  * Left: Navigation (segment controls)
  * Right: Actions (translate, save)
- **Visibility**: All buttons visible without scrolling

**Column Optimization**
- **Width Reduction**: 70px total saved
  * ID column: 50px → 35px
  * Type column: 60px → 50px
  * Style column: 80px → 70px
  * Status column: 75px → 30px (from status icons feature)
- **Resize Handles**: Drag column borders to adjust width (min 25px)
- **More Content Space**: Additional 115px for Source/Target columns

**Custom Tab Overflow** (Assistant panel)
- **Full Tab Names**: No truncation (was "Trans..." → "Translation Memory")
- **Dropdown Menu**: "More ▼" button for remaining tabs
- **Dynamic Layout**: Adapts to available width
- **🔄 Refresh Tabs Button**: Purple button to fix tab display issues
  * Toggles layout mode (stacked → tabbed) to force reflow
  * Fixes tab overflow problems without restart

**Start Screen Layout**
- **Horizontal Buttons**: Width reduced 25% (25 → 18 chars)
- **Compact Design**: Buttons arranged in row (was vertical stack)
- **Shorter Labels**: "Import Bilingual File" → "Import Bilingual"

### 🔧 TECHNICAL CHANGES

**Figure Context Integration**
- Auto-detection before every translation API call
- Logging at each stage: detection → matching → API selection
- Status updates when loading/clearing figures
- UI refresh after load/clear/project restore operations

**Grid Architecture** (from previous release)
- `selected_segments` Set for tracking selections
- `get_status_icon()` method for icon mapping
- `get_status_icon_color()` method for color coding
- `update_selection_counter()` for status bar updates
- Fixed-width Frame container for status column (30px with `pack_propagate(False)`)
- Status column packs `side='right'` before content expands `side='left'`

**Method Refactoring**
- Extracted status icon logic to separate methods
- Unified selection handling across grid operations
- Row update function uses icon methods (not text)

**Documentation**
- `.dev/docs/MULTI_SELECTION_IMPLEMENTATION.md`
- `.dev/docs/SELECTION_COUNTER_UI.md`
- `.dev/docs/RESPONSIVE_BUTTON_LAYOUT.md`
- `.dev/docs/GRID_EDITOR_COMPACT_FIX.md`
- `.dev/docs/CUSTOM_TAB_OVERFLOW_SYSTEM.md`
- `.dev/docs/UI_IMPROVEMENTS_TABS_AND_COLUMNS.md`

**Version & Compatibility**
- Version bump: v3.3.0-beta → v3.4.0-beta
- ~500 lines modified/added
- 100% backward compatible (no breaking changes)
- All existing functionality preserved

---

## [3.3.0-beta] - 2025-10-12 🎨 UI/UX REDESIGN + PROJECT START SCREEN

> **Major Interface Overhaul**: Cleaner toolbar, reorganized menus, semantic colors, professional Start Screen

### 🎨 UI/UX IMPROVEMENTS

**Start Screen** (NEW - Professional Welcome Interface)
- **BEFORE**: Empty grid view when launching program (no document loaded)
- **AFTER**: Professional Start Screen with tabbed interface
  * **Projects Tab**: Quick actions + Recent projects list (last 20 projects, sorted by date)
    - Quick action buttons: Open DOCX, Open Project, Import Bilingual, Import TXT
    - Recent projects listbox with double-click to open
  * **File Explorer Tab**: Browse and open files directly
    - Tree view with Name, Size, Modified columns
    - Folder navigation with ".." parent directory access
    - Smart file type detection (auto-detect memoQ/CafeTran files)
    - Icons for file types (📁 folders, 📄 DOCX, ⚙ JSON, 💾 TMX, 📝 TXT)
  * **Settings Tab**: Quick overview and configuration access
    - Current API provider/model display
    - Current language pair display
    - Active TM count display
    - Quick access buttons to all settings dialogs
- **Automatic Transition**: Start Screen → Grid View when document is loaded
- **Consistent Layout**: Assistant panel stays on right, Log stays at bottom

**Toolbar Reorganization** (55% space reduction)
- **BEFORE**: 12 individual buttons (Import DOCX, Import TXT, Import memoQ, Import CafeTran, Save, Export, Grid, List, Document, Find/Replace)
- **AFTER**: 4 dropdown menus + 3 toggle buttons + 1 save button
  * Import ▼ (DOCX, TXT, memoQ, CafeTran, Trados Studio)
  * Export ▼ (DOCX, TMX, TSV, memoQ, CafeTran, Trados Studio, Session Report)
  * Save (frequently used, remains standalone)
  * View toggles: Grid | List | Document (neutral gray)
  * Tools ▼ (Find/Replace, Prompt Library, API Settings, Language Settings)

**Menu Bar Restructure**
- **REMOVED**: "Translate" menu (distributed to Edit/Resources)
- **REMOVED**: "Prompt Library" menu (merged into Resources)
- **ADDED**: "Project" menu (Save/Load/API/Language settings)
- **ADDED**: "Resources" menu (TM, Prompts, Tracked Changes, Images, Glossaries)
- **ADDED**: "Help" menu (User Guide, Changelog, About)
- **ENHANCED**: "View" menu now controls Assistant panel layout options

**Color Scheme** (Semantic coding)
- Green (#4CAF50): Import operations
- Orange (#FF9800): Export operations
- Blue (#2196F3): Save operations
- Gray (#e0e0e0 / #f5f5f5): View toggles (neutral, less visually demanding)

**Terminology Changes**
- "Translation Workspace" → **"Assistant panel"** (more accurate descriptor)

**Tab Reordering** (Assistant panel)
- **BEFORE**: ...Non-trans | Settings | Changes | Log
- **AFTER**: ...Non-trans | Changes | Settings | Log
- Rationale: Data analysis → Configuration → System log

### 🆕 NEW FEATURES

**Start Screen**
- Projects tab with recent projects and quick actions
- File Explorer tab with tree view navigation
- Settings tab with overview and quick access
- Automatic transition to Grid View when document loaded

**Help Menu**
- User Guide (opens USER_GUIDE.md)
- Changelog (opens CHANGELOG-CAT.md)
- About dialog (version info, features, license)

### � BILINGUAL FORMAT SUPPORT

**Trados Studio DOCX** (NEW - Third major CAT tool format)
- **Import**: Trados Studio bilingual DOCX files (4-column table format)
  * Automatic format detection (Segment ID, Segment status, Source segment, Target segment)
  * Status mapping: "Not Translated (0%)", "Draft (X%)", "Translated (100%)", "Approved Sign-off"
  * UUID-based segment IDs preserved for export
  * Formatting preservation (bold, italic, underline via <b>, <i>, <u> tags)
- **Export**: Export segments to Trados Studio bilingual DOCX format
  * Reconstructs 4-column table with proper headers
  * Preserves original segment UUIDs if available
  * Maps Supervertaler statuses back to Trados format
  * Formatting tags converted to Word formatting
- **UI Integration**: 
  * File → Import → "Trados Studio DOCX (Bilingual)..."
  * File → Export → "Trados Studio DOCX..."
  * Toolbar Import/Export dropdowns include Trados options
  * Start Screen Import Bilingual menu includes Trados
  * File Explorer smart detection (filename contains "trados")
- **Module**: `modules/trados_docx_handler.py` (300+ lines)
  * `is_trados_bilingual_docx()` - Format detection
  * `extract_segments()` - Import with formatting
  * `create_bilingual_docx()` - Export with formatting
  * `map_trados_status_to_supervertaler()` - Status conversion

**Trados Studio Re-Import Compatibility** ✅ **VERIFIED WORKING**
- **Tag Style Preservation**: Formatting tags now use exact "Tag" character style (italic, pink FF0066)
  * Auto-detection of "Tag" style in original document
  * Automatic application to all Trados tags (<NUMBER>, </NUMBER>, <NUMBER/>)
  * Fallback to manual formatting if style doesn't exist
- **XML Declaration Fix**: Post-processing to match Trados exact format
  * From: `<?xml version='1.0' encoding='UTF-8' standalone='yes'?>`
  * To: `<?xml version="1.0" encoding="utf-8"?>` (matches Trados output exactly)
  * Applied to all critical XML files (document.xml, styles.xml, settings.xml)
- **Format Preservation**: Original file structure maintained
  * Table style preserved
  * Custom XML metadata preserved (segment hashes)
  * Comments.xml preserved
  * Settings.xml preserved
- **Testing Results** (October 12, 2025):
  * ✅ Trados accepts re-import of Supervertaler-exported files
  * ✅ Segments updated correctly
  * ✅ Tags maintain proper styling
  * ✅ No data loss
  * ✅ Full round-trip workflow confirmed working
- **Critical Behavior Note**: 
  * Trados **only imports changes to pre-translated segments**
  * Empty/untranslated segments at export → Changes ignored on re-import
  * Solution: Pre-translate in Trados first (MT/TM), then edit in Supervertaler
  * See [USER_GUIDE.md - Trados Studio Re-Import](#trados-studio-re-import-critical-information) for full workflow
- **Implementation**: 
  * `_fix_xml_declarations_for_trados()` - Post-process DOCX after save
  * `_add_text_with_tag_styles()` - Apply "Tag" style to formatting tags
  * `update_bilingual_docx()` - Preserve original file structure

**Complete CAT Tool Trio** ✅
- memoQ XLIFF (v3.0.0-beta)
- CafeTran DOCX (v3.1.0-beta)
- Trados Studio DOCX (v3.3.0-beta) ← NEW

### �📊 TRACKED CHANGES UPDATES

**Report Enhancements**
- Title now includes version: "Tracked Changes Analysis Report ([Supervertaler](https://github.com/michaelbeijer/Supervertaler) 3.3.0-beta)"
- Footer includes clickable GitHub link
- Both title and footer link to repository

**Dialog Improvements**
- Batch size configuration dialog height: 240px → 280px (OK button now fully visible)

### 🔧 TECHNICAL CHANGES

- Version bump: v3.2.0-beta → v3.3.0-beta
- ~250 lines modified/added
- 100% backward compatible (no breaking changes)
- All keyboard shortcuts preserved

### 💡 BENEFITS

- 55% reduction in toolbar width (more content space)
- Reduced cognitive load (fewer buttons to scan)
- Logical grouping by function (import/export/save/view/tools)
- Professional CAT tool aesthetic (memoQ/Trados-style)
- Improved discoverability (related features grouped)

---

## [3.2.0-beta] - 2025-10-12 🎯 POST-TRANSLATION ANALYSIS

> **📊 Major Feature Port**: AI-powered Tracked Changes Analysis from v2.5.0-CLASSIC

### ✨ NEW FEATURES

**Bulk Operations Suite** - Comprehensive Segment Management

- **Multi-Selection System** (Trados/memoQ-style):
  * **Click** to select single segment (blue highlight)
  * **Ctrl+Click** to toggle individual segments in/out of selection
  * **Shift+Click** to select range from last selected to current
  * **Blue row highlighting** (#CCE5FF) for selected segments - no checkbox clutter
  * **Selection persists across pages** (ID-based storage)
  * **Selection counter** shows total selected segments in log
  * **Professional CAT tool aesthetics** matching Trados/memoQ design patterns

- **New "Bulk Operations" Submenu** in Edit menu with powerful batch editing tools

- **Select All Segments** (Ctrl+A):
  * Select all visible segments (respects current filter)
  * Applies blue highlighting to all visible rows
  * Shows count and available bulk operations
  * Filter-aware: selects only filtered segments when filter active
  
- **Clear All Targets**:
  * Remove target text from all segments at once
  * Shows count of segments with targets before clearing
  * Confirmation dialog with undo warning
  * Sets status back to "untranslated"
  
- **Change Status (All/Filtered)**:
  * Change status for all segments or filtered segments only
  * Radio button dialog: Untranslated | Translated | Approved | Draft
  * Filtered mode respects active filters (source/target/status)
  * Shows count of segments that will be changed
  
- **Lock/Unlock Segments** - NEW segment lock status:
  * Lock All / Unlock All - applies to entire project
  * Lock/Unlock Filtered - applies only to visible segments
  * Lock/Unlock Current Segment - in Segment submenu
  * **Locked status** saved in project JSON
  * Prevents accidental edits to reviewed segments
  * Visual indication of lock status (future enhancement)
  
- **Segment Lock Feature**:
  * New `locked` boolean field added to Segment class
  * Serialized/deserialized in project save/load
  * Foundation for edit protection (enforcement in next update)
  
- **Filter Integration**:
  * Filtered operations work with existing Filter functionality
  * "Change Status (Filtered)" respects source/target/status filters
  * Lock/Unlock Filtered only affects visible segments
  * Clear distinction between "All" vs "Filtered" operations

**Copy Source to Target (All Segments)** - Cost-Saving CAT Tool Workflow

- **Edit Menu**: New "Copy Source to Target (All Segments)" command
- **Purpose**: Prepare files for Trados/memoQ/CafeTran re-import without paying for MT
- **Workflow**:
  1. Export bilingual file with empty targets from CAT tool
  2. Import into Supervertaler
  3. Copy source → target for all segments (Edit menu)
  4. Translate with AI (using your own API keys)
  5. Export and re-import to CAT tool
- **Cost Savings**: 80-90% cheaper than commercial MT (€2-5 vs €20-40 per 1M chars)
- **Why It Works**: CAT tools only accept changes to segments with existing targets
- **Dialog Confirmation**: Shows tip about workflow and next steps
- **Documentation**: Added comprehensive guide in USER_GUIDE.md with cost comparison table

**TrackedChangesBrowser Class** - Complete GUI for tracked changes review

- **AI-Powered Analysis Export**:
  - Export markdown reports with AI-generated change summaries
  - Batch processing (1-100 segments per request, configurable via slider)
  - Supports Claude, Gemini, and OpenAI
  - ~90% faster than sequential processing (25-segment batches)
  
- **Interactive Browser Window**:
  - Searchable treeview of all tracked changes
  - Filter by exact match or partial text
  - Shows: Segment #, Original (AI), Final (Edited)
  - Copy to clipboard functionality
  
- **Export to Markdown Report**:
  - Configurable batch size (1-100 via slider)
  - Real-time estimate of API calls needed
  - Precision AI prompts detect subtle changes:
    * Curly vs straight quotes (" vs ")
    * Apostrophes (' vs ')
    * Dashes (- vs – vs —)
  - Paragraph format (one segment per section)
  - Includes full AI prompt template in header

### 🔧 ENHANCED METHODS

**browse_tracked_changes()**:
- **CHANGED**: Now uses TrackedChangesBrowser class (was inline implementation)
- **ADDED**: parent_app reference for AI provider/model access
- **ADDED**: Export button "📊 Export Report (MD)"

**Tracked Changes Integration**:
- Maintains compatibility with existing load/clear methods
- Works seamlessly with v3's menu structure (Translate menu)

### 📊 EXPORT REPORT FORMAT

```markdown
# Tracked Changes Analysis Report

## What is this report?
This report analyzes differences between AI-generated translations 
and your final edited versions...

**Generated:** [timestamp]
**Total Changes:** [count]
**AI Analysis:** Enabled

### AI Analysis Configuration
**Provider:** Claude/Gemini/OpenAI
**Model:** [model-name]
**Prompt Template Used:** [full prompt]

---

### Segment 1
**Target (Original):** [AI baseline]
**Target (Revised):** [Your edits]
**Change Summary:** [AI-powered precise analysis]
```

### 🎯 USE CASE

1. Complete translation project in v3 CAT editor
2. Export tracked changes (already supported)
3. Click "Translate → Browse Tracked Changes"
4. Click "📊 Export Report (MD)"
5. Configure batch size (1-100 segments)
6. Review comprehensive AI-powered analysis

### ⚡ PERFORMANCE

- **Batch processing**: 33 changes in ~10 seconds (vs ~90 seconds sequential)
- **Configurable batches**: Balance speed vs token usage
- **Progress window**: Real-time feedback during processing

### 🔗 COMPATIBILITY

- ✅ **Ported from v2.5.0-CLASSIC**: Feature parity achieved
- ✅ **Integrated with v3 architecture**: Uses v3's AI provider system
- ✅ **Maintains existing functionality**: Load/clear methods unchanged

---

