# CAT Editor Prototype - Changelog

## [0.4.1] - 2025-10-03

### Changed
- **Precise Search Term Highlighting in Document View**
  - Search terms now highlighted individually in bright yellow (not entire segments)
  - Multiple occurrences in same segment all highlighted
  - Bold font applied to highlighted terms for better visibility
  - Works in both paragraphs and table cells
  - Much cleaner and more precise visual feedback
  - Easier to see exactly what matched the filter

### Improved
- Better readability in Document View when using filters
- Context around search terms remains visible
- Status colors still visible (highlights layer on top)

## [0.4.0] - 2025-10-03

### Added
- **Filter Panel in Document View**
  - Complete filter UI matching Grid and List views
  - Mode toggle (Filter/Highlight), source/target/status filters
  - Apply and Clear buttons
  - Results counter showing match statistics
  
- **Dual-Mode Filtering System**
  - **Filter Mode (🔍)**: Shows only matching segments
  - **Highlight Mode (💡)**: Shows all segments, highlights matches
  - Radio-style buttons for clear mode indication
  - Real-time results counter
  - Works consistently across all three views
  
- **Keyboard Shortcuts for Filtering**
  - `Ctrl+M` - Toggle between Filter and Highlight modes
  - `Ctrl+Shift+A` - Apply filters
  - `Ctrl+Shift+F` - Focus source filter field
  - `Enter` in filter fields - Apply filters
  
- **Filter Preferences Saved to Projects**
  - Filter mode (Filter/Highlight) saved
  - Source and target filter text saved
  - Status selection saved
  - Active state saved
  - Filters automatically restored when loading project
  - 100% backward compatible with old project files
  
- **Button-Triggered Filtering**
  - Filters now manual (click Apply or press Enter)
  - No more real-time filtering while typing
  - Better performance and user control
  - Status dropdown still auto-applies (standard UX)

- **Document View** - Revolutionary new view mode showing translations in natural document flow
  - Natural text flow with paragraphs appearing as they would in the original document
  - Clickable segments with editor panel below for easy editing
  - Smart placeholder system:
    - Shows target translation when available
    - Shows `[empty - click to edit]` when user clears target
    - Shows source text when not yet translated (for context)
  - Status color coding (red=untranslated, yellow=draft, green=translated, blue=approved)
  - Hover effects on segments (brighten and raise on mouseover)
  - Style support with visual formatting (headings in appropriate sizes and colors)
  - Keyboard shortcut: `Ctrl+3` to switch to Document View
  
- **Table Rendering in Document View**
  - Tables now render as actual table structures (not flowing text)
  - Proper grid layout with rows and columns
  - Tables appear in correct document position (not at end)
  - Each cell is individually clickable and editable
  - Equal column widths with proper spacing
  - Cell borders visible for clear structure
  
- **Document Position Tracking**
  - Added `document_position` field to `Segment` class
  - Added `document_position` field to `ParagraphInfo` class
  - Rewrote `docx_handler.py` import to process elements in document order
  - Now iterates through `document.element.body` for proper element ordering
  - Tables and paragraphs interleaved correctly based on source document structure
  
- **View Switching with State Preservation**
  - Current segment selection preserved when switching between views
  - Auto-scroll to selected segment in new view
  - Works across all view modes: Grid, List, Document
  - Keyboard shortcuts for all views:
    - `Ctrl+1` - Grid View
    - `Ctrl+2` - List View
    - `Ctrl+3` - Document View

- **List View** - Tree-based view with compact list interface
  - Six-column treeview: ID, Type, Style, Status, Source, Target
  - Text truncation for list density
  - Compact editor panel below
  - Perfect for quick navigation and overview
  - Full keyboard support with same shortcuts as other views
  - Status color coding for visual progress tracking
  - Keyboard shortcut: `Ctrl+3` to switch to Compact View

- **UX Improvements**
  - `Ctrl+D` (Copy Source to Target) now works in Grid View
  - Double-click source column opens popup with full text
  - Source text popup includes "Copy to Clipboard" and "Copy to Target" buttons
  - Source text is selectable and copyable
  - Escape key closes source popup

### Changed
- **Grid View Layout Buttons** - Visual indication of active view mode
- **docx_handler.py** - Complete rewrite of import logic for proper element ordering
  - Lines 28-38: Added `document_position` to ParagraphInfo
  - Lines 75-160: Rewrote to process document.element.body in order
  - Tables and paragraphs now extracted in document order (not all paragraphs first)

### Fixed
- **Table Position Bug** - Tables no longer appear at end of document
  - Root cause: Import was processing all paragraphs first, then all tables
  - Solution: Process elements in document order and track position
  - Result: Perfect document structure preservation
  
- **Text Wrapping in Document View** - Proper height calculation
  - Uses `dlineinfo()` to count actual wrapped display lines
  - Paragraphs now show full content without vertical clipping

### Technical Details
- **Files Modified**:
  - `cat_editor_prototype.py`:
    - Added `LayoutMode.DOCUMENT` constant
    - Added `document_position` parameter to Segment class (line ~50)
    - Implemented `create_document_layout()` (lines 467-555)
    - Implemented `load_segments_to_document()` (lines 557-612)
    - Implemented `render_paragraph()` (lines 614-751)
    - Implemented `render_table()` (lines 753-838)
    - Implemented `on_doc_segment_click()` (lines 840-877)
    - Implemented `save_doc_segment()` (lines 961-1026)
    - Implemented `create_compact_layout()` (lines 463-590)
    - Implemented `load_segments_to_compact()` (lines 592-610)
    - Updated `switch_layout()` for view preservation (lines 1220-1300)
    - Updated `import_docx()` to pass document_position (line ~2336)
  - `docx_handler.py`:
    - Added `document_position` to ParagraphInfo (line ~35)
    - Rewrote `import_docx()` to process in document order (lines 75-160)

### Documentation
- Created `DOCUMENT_VIEW_v0.4.0.md` - Complete Document View documentation
- Created `COMPACT_VIEW_v0.4.0.md` - Complete Compact View documentation
- Updated `UX_IMPROVEMENTS_v0.4.0.md` - Grid View improvements
- Updated `README.md` with v0.4.0 information and view modes section
- Updated `VERSION_SUMMARY.md` with current version

### Performance
- Dynamic height calculation using `dlineinfo()` - tested up to 500 segments
- Canvas scrolling performs well for typical documents
- Consider pagination for documents > 1000 segments

### Impact
- ✅ Professional document preview mode
- ✅ Better context for translators  
- ✅ Natural reading flow for reviewers
- ✅ Proper table structure visualization
- ✅ Complete view mode ecosystem (Grid, Split, Compact, Document)
- ✅ Maximum efficiency interface for speed translation
- ✅ Flexible workflow - choose the right view for each task

---

## [0.3.2] - 2025-10-02

### Added
- **Style Preservation on Export** (Phase B)
  - Modified `_replace_paragraph_text()` to accept and apply `original_style` parameter
  - Modified `_replace_paragraph_with_formatting()` to accept and apply styles
  - Updated `export_docx()` to pass original styles for both regular paragraphs and table cells
  - All paragraph styles now preserved: Title, Subtitle, Heading 1-3, Normal, custom styles
  - Graceful error handling when style doesn't exist in document template
  - Works for both regular paragraphs and table cell content

### Fixed
- **Missing Subtitle Bug** (Critical)
  - Changed table paragraph filtering from `id(para._element)` to storing actual paragraph objects
  - Fixed Python object ID reuse issue causing false positives
  - Subtitle and other paragraphs no longer incorrectly identified as table paragraphs
  - Reliable object identity comparison prevents memory address reuse issues
  - All paragraphs now imported correctly (no silent data loss)

### Technical Details
- **File**: `docx_handler.py`
  - Lines 75-95: Changed `table_paragraph_ids` (IDs) to `table_paragraphs` (objects)
  - Lines 258-316: Enhanced `_replace_paragraph_text()` with style parameter
  - Lines 318-382: Enhanced `_replace_paragraph_with_formatting()` with style parameter
  - Lines 197-215: Updated regular paragraph export to pass style
  - Lines 227-241: Updated table cell export to pass style

### Documentation
- Created `PHASE_B_STYLE_PRESERVATION.md` - Complete feature documentation
- Created `BUGFIX_MISSING_SUBTITLE.md` - Detailed bug analysis and fix
- Updated `README.md` with v0.3.2 information

### Impact
- ✅ Professional exported documents with preserved styles
- ✅ No manual reformatting needed after translation
- ✅ Headings maintain proper hierarchy and formatting
- ✅ All content imported correctly (no data loss)

---

## [0.3.1] - 2025-10-02

### Added
- **Style Visibility** (Phase A)
  - New "Style" column in grid showing Word paragraph styles
  - Visual color coding for heading styles:
    - Heading 1: Dark blue (bold)
    - Heading 2: Medium blue
    - Heading 3: Light blue
    - Title: Purple (bold)
    - Subtitle: Purple (italic)
  - Helper methods: `_format_style_name()` and `_get_style_tag()`
  - Style information captured during import in `ParagraphInfo`
  - Grid now has 6 columns: ID, Type, Style, Status, Source, Target

### Fixed
- **Column Misalignment Bug** (Critical)
  - `update_segment_in_grid()` was passing only 4 values to 6-column grid
  - Now correctly passes all 6 values: id, type, style, status, source, target
  - Column widths adjusted with `minwidth` and `stretch` properties
  - Fixed columns (ID, Type, Style, Status) don't stretch
  - Content columns (Source, Target) stretch to fill space

### Technical Details
- **File**: `cat_editor_prototype.py`
  - Lines ~37-56: Added `style` parameter to Segment class
  - Lines ~186-203: Treeview configured for 6 columns
  - Lines ~218-223: Visual tags created for heading styles
  - Lines ~318-347: Import captures style from para_info
  - Lines ~377-401: Load displays all 6 columns
  - Lines ~413-440: Helper methods for style formatting
  - Lines ~508-533: Update fixed to pass all 6 values

### Documentation
- Created `PHASE_A_COMPLETE.md` - Complete feature documentation
- Created `BUGFIX_COLUMN_MISALIGNMENT.md` - Bug analysis and fix
- Created `STYLE_SUPPORT_VISUAL_GUIDE.md` - Visual reference
- Created `test_style_support.py` - Test script with 44 segments

### Impact
- ✅ Visual indication of document structure in grid
- ✅ Color-coded headings improve readability
- ✅ Easier to maintain document hierarchy
- ✅ Grid updates correctly after translation

---

## [0.3.0] - 2025-10-02

### Added
- **Table Support** (Phase 0.1)
  - Table cells imported as individual segments
  - Each table cell gets unique identifier: T{table}R{row}C{col}
  - "Type" column in grid showing "Para" or "T#R#C#"
  - Table cells can be translated independently
  - Export reconstructs tables with translations
  - Enhanced `ParagraphInfo` with table metadata:
    - `is_table_cell`: Boolean flag
    - `table_index`: Table number (0-based)
    - `row_index`: Row position
    - `cell_index`: Column position
  - Grid now has 5 columns: ID, Type, Status, Source, Target

### Fixed
- **Table Cell Duplication Bug** (Critical)
  - python-docx `document.paragraphs` includes table cell paragraphs
  - Created `table_paragraph_ids` set to track table paragraphs
  - Filter out table paragraphs when processing regular paragraphs
  - Then process table cells separately
  - No more duplicate segments in grid

### Technical Details
- **File**: `docx_handler.py`
  - Lines 70-140: Enhanced import to extract table cells
  - Lines 82-88: Build set of table paragraph IDs
  - Lines 119-147: Process table cells with position tracking
  - Lines 220-241: Export reconstructs tables
  - Lines 247-261: Helper methods for table cell lookup
- **File**: `cat_editor_prototype.py`
  - Lines ~186-203: Grid configured for 5 columns
  - Lines ~377-401: Display type labels (Para/T#R#C#)
  - Type column shows segment origin clearly

### Documentation
- Created `PHASE_0.1_COMPLETE.md` - Complete feature documentation
- Created `BUGFIX_TABLE_DUPLICATION.md` - Bug analysis and fix
- Created `TABLE_SUPPORT_IMPLEMENTATION.md` - Technical details
- Created `TABLE_SUPPORT_VISUAL_GUIDE.md` - Visual reference
- Created `test_table_support.py` - Test script with 26 segments

### Impact
- ✅ Professional documents with tables can be translated
- ✅ Each table cell is independent segment
- ✅ Table structure preserved on export
- ✅ Clear indication of segment type in grid

---

## [0.2.0] - 2025-10-01

### Added
- **Inline Formatting Tags** - Full support for bold, italic, and underline preservation
  - Automatic extraction of run-level formatting from DOCX import
  - XML-like tags display in editor (`<b>`, `<i>`, `<u>`, `<bi>` for bold+italic)
  - Real-time tag validation with error messages
  - Tag insertion buttons (Bold, Italic, Underline) with selection wrapping
  - "Copy Source Tags" feature to match source formatting structure
  - "Strip Tags" button to remove all formatting from target
  - Visual tag indicators (color-coded by type)
  - Automatic tag reconstruction on DOCX export
  - Proper formatting run creation with bold/italic/underline applied

### Technical Details
- **New Module**: `tag_manager.py` - Complete inline tag handling system (290+ lines)
  - `FormattingRun` dataclass for run representation
  - `TagManager` class with extraction, conversion, and validation
  - Tag pattern matching with regex
  - Run-to-tags and tags-to-runs conversion
  - Nested tag validation
  - Color scheme for different tag types
- **Updated**: `docx_handler.py` - Enhanced with formatting support
  - `extract_runs()` method to extract formatting from paragraphs
  - `import_docx()` now has `extract_formatting` parameter (default True)
  - `_replace_paragraph_with_formatting()` method for tag reconstruction
  - Proper handling of multiple runs with different formatting
- **Updated**: `cat_editor_prototype.py` - Enhanced UI and tag features
  - Tag validation label showing real-time status
  - Tag insertion buttons with keyboard support
  - Copy source tags functionality
  - Strip tags functionality
  - Visual feedback for tag errors

### How It Works
```
IMPORT: Bold text in DOCX → <b>Bold text</b> in editor
EDIT:   Translator sees: "The <b>API key</b> is required"
        Translates to:    "La <b>clé API</b> est requise"
EXPORT: <b>clé API</b> → Bold formatting in DOCX
```

### Benefits
- ✅ Professional formatting preserved through translation workflow
- ✅ Visual indication of formatted regions in source/target
- ✅ No formatting lost during export
- ✅ Quality control with tag validation
- ✅ Efficient tag copying from source
- ✅ Works with patents, contracts, technical docs with formatting

---

## [0.1.1] - 2025-10-01

### Fixed
- **DOCX Export Issues** - Corrected paragraph matching and whitespace handling
  - Fixed source text appearing in exported DOCX when segments were untranslated
  - Fixed extra newlines/line breaks in exported documents
  - Improved paragraph index matching between import and export
  - Better run management to prevent empty runs causing spacing issues
  - Strip whitespace from translated text to prevent formatting problems
  - Export now correctly skips empty paragraphs (matching import logic)

### Technical Changes
- Updated `docx_handler.py` export logic to use `non_empty_para_index`
- Improved `_replace_paragraph_text()` to properly remove extra runs
- Added whitespace stripping to prevent trailing spaces/newlines

---

## [0.1.0] - 2025-10-01

### Added - Initial Release
- **CAT Editor Prototype** - Standalone Computer-Aided Translation editor
  - DOCX file import with automatic sentence segmentation
  - Interactive grid interface for segment-by-segment translation
  - Editable target column with status tracking (untranslated, draft, translated, approved)
  - DOCX export with formatting preservation
  - Bilingual DOCX export (source|target table format)
  - TSV export for spreadsheet compatibility
  - Find/Replace functionality across segments
  - Project save/load to JSON format
  - Progress tracking and completion percentage
  - Keyboard shortcuts for efficient translation workflow
  - Color-coded status indicators in grid
  - Segment editor panel with quick actions
  - Paragraph tracking for document reconstruction
  - Basic formatting preservation (paragraph-level)

### Technical Details
- **New Modules**:
  - `cat_editor_prototype.py` - Main application (800+ lines)
  - `simple_segmenter.py` - Sentence segmentation engine
  - `docx_handler.py` - DOCX import/export with formatting
  - `README.md` - Complete documentation
  - `QUICK_START.md` - Quick start guide
- **Dependencies**: python-docx, tkinter (built-in)
- **Architecture**: Standalone prototype for testing before main integration
- **Status**: Experimental - Testing phase before v2.5.0 integration

### Keyboard Shortcuts
- `Ctrl+O` - Import DOCX
- `Ctrl+S` - Save project
- `Ctrl+L` - Load project
- `Ctrl+F` - Find/Replace
- `Ctrl+D` - Copy source to target
- `Ctrl+Enter` - Save segment and move to next
- `Enter` - Edit selected segment
- `↑` `↓` - Navigate segments

### Features Summary
- ✅ Import Word documents
- ✅ Sentence segmentation
- ✅ Translation grid
- ✅ Status tracking
- ✅ Export to DOCX/TSV
- ✅ Project management
- ✅ Find/Replace
- ✅ Progress tracking

---

## Upcoming Features

### Planned for Future Versions
- [ ] SRX rule-based segmentation
- [ ] Translation memory integration
- [ ] AI translation integration (Supervertaler agents)
- [ ] Concordance search
- [ ] Segment splitting/merging
- [ ] Auto-propagation of translations
- [ ] Quality assurance checks
- [ ] Complex table support (merged cells, nested tables)
- [ ] Track changes preservation
- [ ] Comment preservation
- [ ] Integration with main Supervertaler v2.5.0

### Integration Roadmap
1. **Phase 0.2**: Real-world testing with complex documents
2. **Phase 1**: Foundation integration (data model, UI)
3. **Phase 2**: CAT features (TM, concordance)
4. **Phase 3**: AI integration (translation agents)
5. **Phase 4**: Quality & testing
6. **Release**: Supervertaler v2.5.0 with full CAT support

---

## Notes

### Development Timeline
- v0.1.0: October 1, 2025 - Initial release
- v0.1.1: October 1, 2025 - Export bug fixes
- v0.2.0: October 1, 2025 - Inline formatting tags
- v0.3.0: October 2, 2025 - Table support
- v0.3.1: October 2, 2025 - Style visibility
- v0.3.2: October 2, 2025 - Style preservation

### Bug Fixes Summary
1. **Export whitespace** (v0.1.1) - Fixed extra newlines
2. **Table duplication** (v0.3.0) - Fixed duplicate segments
3. **Column misalignment** (v0.3.1) - Fixed grid display
4. **Missing subtitle** (v0.3.2) - Fixed object ID reuse

### Documentation
- `README.md` - Main documentation
- `PHASE_*.md` - Feature implementation docs
- `BUGFIX_*.md` - Bug analysis and fixes
- `*_GUIDE.md` - User guides and references
- `test_*.py` - Test scripts for each feature

---

**Current Version**: 0.3.2  
**Status**: Stable prototype, ready for real-world testing  
**Next**: Phase 0.2 - Real-world document testing
