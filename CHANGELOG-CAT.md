# Supervertaler CAT Edition - Changelog

**Version Line**: v3.x.x-beta (Segment-based CAT Editor Architecture)

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

