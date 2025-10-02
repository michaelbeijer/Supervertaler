# CAT Editor Prototype - Release Notes

## Version 0.3.1 (October 2, 2025) - Style Visibility Release 🎨

### New Features
- **✨ Style Column** - Segment grid now shows Word style (Title, H 1, H 2, H 3, Normal, etc.)
- **🎨 Visual Style Formatting** - Headings display with distinct colors and fonts:
  - Heading 1: Bold, dark blue
  - Heading 2: Bold, medium blue
  - Heading 3: Bold, light blue
  - Title: Bold, larger, purple
  - Subtitle: Italic, purple
  - Normal: Regular text

### Enhancements
- **Better Translator Context** - Instantly see if segment is heading vs body text
- **Enhanced Data Model** - Segment class includes style attribute
- **Style Statistics** - Import shows breakdown of styles in document
- **Backward Compatible** - Old projects load with "Normal" default style

### Use Cases
Perfect for documents with structure:
- Legal documents (section headings, subsections)
- Technical manuals (chapter titles, sections)
- Business reports (executive summaries, headers)
- Contracts (article headers, clauses)
- Academic papers (titles, abstracts)

### Technical Details
- **Files Modified**: `cat_editor_prototype.py` (~60 lines)
- **Style Detection**: Already captured, now displayed
- **Visual Tags**: heading1, heading2, heading3, title, subtitle
- **Test Document**: `test_document_with_styles.docx` (46 segments, 7 different styles)

### Benefits
- ✅ **Immediate visual feedback** - See heading hierarchy at a glance
- ✅ **Better translations** - Apply appropriate tone based on style
- ✅ **Document structure** - Understand organization
- ✅ **Quality control** - Verify headings translated correctly

---

## Version 0.3.0 (October 2, 2025) - Table Support Release 🎉

### New Features
- **✨ Table Cell Segmentation** - Documents with tables are now fully supported!
  - Each table cell is treated as a separate translatable segment
  - Table structure is preserved on export
  - Visual indicators show which segments are table cells vs paragraphs
  - Type column displays: "Para" for paragraphs, "T#R#C#" for table cells

### Enhancements
- **Enhanced Data Model**
  - `Segment` class now tracks table metadata
  - `ParagraphInfo` includes table cell coordinates
  - Serialization updated for project save/load

- **Improved Import/Export**
  - DOCX import extracts both paragraphs and table cells
  - Export maintains original document structure
  - Statistics show breakdown: paragraphs vs table cells

- **Better Visual Feedback**
  - Table cells displayed in blue italic font
  - Type column shows segment origin clearly
  - Status colors apply to both paragraphs and tables

### Use Cases
Perfect for translating:
- Contracts with party information tables
- Invoices with line item tables
- Technical specifications with feature tables
- Forms with field/value pairs
- Reports with data tables

### Technical Details
- **Files Modified**: `docx_handler.py`, `cat_editor_prototype.py`
- **Lines Added**: ~120 lines
- **Backward Compatible**: Yes - paragraph-only documents work as before
- **Test Coverage**: Sample document with 2 tables, 18 cells, 8 paragraphs

### Testing
- ✅ Import test document with tables
- ✅ Verify table cell identification
- ✅ Export with translations
- ✅ Structure preservation validated
- ✅ Inline formatting maintained

---

## Version 0.2.0 (October 2, 2025) - Inline Formatting Release

### New Features
- **✨ Inline Formatting Preservation**
  - Bold, italic, underline, and combined styles preserved
  - Formatting converted to inline tags during import
  - Tags converted back to proper formatting on export
  - Visual tag rendering in source/target editors

### Enhancements
- **Tag Management System**
  - `TagManager` class for formatting extraction/application
  - Run-based text processing
  - Tag validation and cleaning

- **Editor Improvements**
  - Source editor shows tags in gray
  - Target editor shows tags in gray
  - Tag syntax highlighting
  - Formatting guides

### Technical Details
- **New Module**: `tag_manager.py` (290 lines)
- **Files Modified**: `docx_handler.py`, `cat_editor_prototype.py`
- **Tag Format**: `<b>bold</b>`, `<i>italic</i>`, `<u>underline</u>`, `<bi>bold-italic</bi>`

---

## Version 0.1.0 (Initial Release)

### Core Features
- **DOCX Import/Export**
  - Import Word documents
  - Automatic sentence segmentation
  - Export with original structure

- **Segment Management**
  - Treeview grid for segment display
  - Source/target editing
  - Status tracking (untranslated, draft, translated, approved)

- **Project Management**
  - Save/load projects as JSON
  - Project metadata tracking
  - Progress indicators

- **UI Components**
  - Menu bar with keyboard shortcuts
  - Toolbar with quick actions
  - Status bar with statistics
  - Log viewer

### Segmentation
- Sentence-level segmentation
- Abbreviation handling
- Paragraph tracking

### Export Options
- Translated DOCX
- Bilingual DOCX (review format)
- Original structure preservation

---

## Roadmap

### Phase 0.2: Testing & Refinement
- Real-world document testing
- Edge case handling (nested tables, merged cells)
- Performance optimization
- Bug fixes

### Future Enhancements (Post-Integration)
- Translation Memory integration
- Terminology management
- Quality checks
- Advanced filtering
- Batch processing
- Plugin system

---

## Known Limitations

### Current Version (0.3.0):
- Nested tables not explicitly tested
- Merged cells treated as single segments
- No visual table preview in editor

### By Design:
- Sentence-level segmentation only (no phrase-level)
- DOCX format only (no DOC, ODT, etc.)
- Single-file operations (no batch processing yet)

---

## Installation & Requirements

### Dependencies:
```bash
pip install python-docx
```

### Python Version:
- Python 3.7+
- Tkinter (usually included)

### Files Needed:
- `cat_editor_prototype.py` - Main application
- `docx_handler.py` - DOCX import/export
- `simple_segmenter.py` - Text segmentation
- `tag_manager.py` - Formatting preservation

### Optional:
- `test_table_support.py` - Testing utilities
- `test_document_with_tables.docx` - Sample document

---

## Credits

Developed as part of the **Supervertaler** project for integration into v2.5.0.

**Development Timeline:**
- v0.1.0: Basic CAT functionality
- v0.2.0: Inline formatting tags
- v0.3.0: Table cell segmentation

**Next**: Integration into main Supervertaler application (see `FULL_INTEGRATION_PLAN.md`)
