# CAT Editor Prototype v0.4.0

**A standalone Computer-Aided Translation (CAT) Editor for Supervertaler**

## 🎯 Features

### Core Features
- ✅ **DOCX Import** - Import Microsoft Word documents with full formatting
- ✅ **Automatic Segmentation** - Split text into translatable segments
- ✅ **Table Support** - Import and translate table cells as individual segments
- ✅ **Style Support** - Visual display and preservation of Word styles (Heading 1-3, Title, etc.)
- ✅ **Multiple View Modes** - Grid View, Split View, Compact View, and Document View
- ✅ **Document View** - See translations in natural document flow with tables rendered properly
- ✅ **Editable Grid** - Excel-like interface with 6 columns (ID, Type, Style, Status, Source, Target)
- ✅ **DOCX Export** - Export with full formatting and style preservation
- ✅ **Bilingual Export** - Create side-by-side review documents
- ✅ **TSV Export** - Export to tab-separated format
- ✅ **Find/Replace** - Search and replace across segments
- ✅ **Status Tracking** - Track translation progress (Untranslated, Draft, Translated, Approved)
- ✅ **Project Save/Load** - Save work and resume later
- ✅ **Inline Formatting** - Preserve bold, italic, underline with XML-like tags

### Advanced Features
- ✅ **Table Cell Segmentation** - Each table cell is a separate translatable segment
- ✅ **Table Rendering in Document View** - Tables appear as actual table structures in correct position
- ✅ **Style Visibility** - Color-coded headings (H1=dark blue, H2=medium blue, H3=light blue)
- ✅ **Style Preservation on Export** - Exported documents maintain original styles
- ✅ **Type Column** - Shows "Para" for paragraphs, "T#R#C#" for table cells
- ✅ **Tag Management** - Insert, validate, and manage inline formatting tags
- ✅ **Real-time Tag Validation** - Instant feedback on tag errors
- ✅ **View Switching** - Seamlessly switch between views with selection preserved

## 📋 Requirements

### Python Version
- Python 3.7 or higher

### Required Libraries
```bash
pip install python-docx
```

### Optional Libraries (for future features)
```bash
pip install lxml      # For SRX segmentation
pip install regex     # For advanced pattern matching
```

## 🚀 Quick Start

### 1. Install Dependencies

Open PowerShell and run:
```powershell
pip install python-docx
```

### 2. Run the Prototype

Navigate to the prototype folder:
```powershell
cd "c:\Users\pc\My Drive\Software\Python\Supervertaler\cat_tool_prototype"
python cat_editor_prototype.py
```

### 3. Import a Document

1. Click **"📁 Import DOCX"** or use `File > Import DOCX...`
2. Select a Word document (.docx file)
3. The document will be automatically segmented into sentences

### 4. Translate

- Double-click a segment or press Enter to start editing
- Type your translation in the "Target" field
- Press `Ctrl+Enter` to save and move to next segment
- Use the Status dropdown to mark progress

### 5. Export

- **Export to DOCX** - Creates translated Word document with original formatting
- **Export to Bilingual DOCX** - Creates review document with source and target side-by-side
- **Export to TSV** - Creates spreadsheet-compatible file

## 💡 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Import DOCX |
| `Ctrl+S` | Save project |
| `Ctrl+L` | Load project |
| `Ctrl+F` | Find/Replace |
| `Ctrl+D` | Copy source to target |
| `Ctrl+Enter` | Save segment and move to next |
| `Enter` | Edit selected segment |
| `↑` `↓` | Navigate segments |
| `Ctrl+1` | Switch to Grid View |
| `Ctrl+2` | Switch to Split View |
| `Ctrl+3` | Switch to Compact View |
| `Ctrl+4` | Switch to Document View |

## 🎨 View Modes

### Grid View (Ctrl+1)
Excel-like table with all segments visible. Best for bulk editing and getting an overview.

### Split View (Ctrl+2)
Traditional CAT tool layout with segment list on left and editor on right. Best for focused translation work.

### Compact View (Ctrl+3)
Minimalist 3-column view (placeholder - coming soon).

### Document View (Ctrl+4) ⭐ NEW
Natural document flow showing text and tables as they appear in the original document. Best for reviewing context and final output. Features:
- Text flows naturally like a Word document
- Tables rendered in proper position with correct structure
- Clickable segments with editor panel below
- Color-coded by status (red=untranslated, yellow=draft, green=translated, blue=approved)
- Smart placeholders show source when not translated, target when complete

## 📁 File Structure

```
cat_tool_prototype/
├── cat_editor_prototype.py    # Main application (1000+ lines)
├── simple_segmenter.py         # Sentence segmentation
├── docx_handler.py             # DOCX import/export with formatting (450+ lines)
├── tag_manager.py              # Inline formatting tag management (300+ lines)
├── README.md                   # This file
├── PHASE_0.1_COMPLETE.md       # Table support documentation
├── PHASE_A_COMPLETE.md         # Style visibility documentation
├── PHASE_B_STYLE_PRESERVATION.md  # Style preservation documentation
├── BUGFIX_*.md                 # Bug fix documentation
└── test_*.py                   # Test scripts
```

## 🎨 User Interface

### Main Window

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Supervertaler CAT Editor - Prototype v0.3.2                            │
├─────────────────────────────────────────────────────────────────────────┤
│ [Import] [Save] [Export] │ [Find/Replace]  Progress: 50%               │
├─────────────────────────────────────────────────────────────────────────┤
│  Translation Grid                                                        │
│  # │ Type │ Style    │ Status      │ Source             │ Target        │
├────┼──────┼──────────┼─────────────┼────────────────────┼───────────────┤
│  1 │ Para │ Heading 1│ Translated  │ First sentence.    │ Eerste zin.   │
│  2 │ Para │ Normal   │ Draft       │ Second sentence.   │ Tweede...     │
│  3 │ T1R1C1│ Normal  │ Untranslated│ Table cell text    │               │
├─────────────────────────────────────────────────────────────────────────┤
│  Segment Editor                                                          │
│  Segment #2 | Para | Normal          Status: [Draft ▼]                 │
│  Source: Second sentence.                                                │
│  Target: [Tweede zin.____________________________]                       │
│  [Copy Source → Target] [Clear]  [Save & Next]                         │
│  [📎 Bold] [📎 Italic] [📎 Underline] [Copy Tags] [Strip Tags]        │
│  Tags: ✓ Valid                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│  Log                                                                     │
│  [10:30:15] Imported: document.docx                                      │
│  [10:30:16] ✓ Loaded 50 segments (40 paragraphs + 10 table cells)      │
└─────────────────────────────────────────────────────────────────────────┘
```
├─────────────────────────────────────────────────────────┤
│  Translation Grid                                        │
│  # │ Status      │ Source             │ Target          │
├────┼─────────────┼────────────────────┼─────────────────┤
│  1 │ Translated  │ First sentence.    │ Eerste zin.     │
│  2 │ Draft       │ Second sentence.   │ Tweede...       │
│  3 │ Untranslated│ Third sentence.    │                 │
├─────────────────────────────────────────────────────────┤
│  Segment Editor                                          │
│  Segment #2 | Paragraph 1          Status: [Draft ▼]    │
│  Source: Second sentence.                                │
│  Target: [Tweede zin.____________________________]       │
│  [Copy Source → Target] [Clear]  [Save & Next]          │
├─────────────────────────────────────────────────────────┤
│  Log                                                     │
│  [10:30:15] Imported: document.docx                      │
│  [10:30:16] ✓ Loaded 50 segments from 10 paragraphs     │
└─────────────────────────────────────────────────────────┘
```

## 📊 Status Types

- **Untranslated** (red) - Not yet translated
- **Draft** (yellow) - Translation in progress
- **Translated** (green) - Translation complete
- **Approved** (blue) - Translation reviewed and approved

## 🔧 How It Works

### Import Process
1. Opens DOCX file using `python-docx` library
2. Extracts all paragraphs with formatting metadata
3. Segments each paragraph into sentences using regex
4. Creates editable segments in grid

### Export Process
1. Loads original DOCX as template
2. Walks through document structure
3. Replaces source text with target translations
4. Preserves original formatting (fonts, styles, colors)
5. Saves as new DOCX file

### Project Files
Projects are saved as JSON files containing:
- All segments (source, target, status)
- Original DOCX file path
- Metadata (creation date, paragraph IDs)

## 🎯 Use Cases

### Patent Translation
```
1. Import patent document (EN)
2. Translate segment by segment
3. Export to DOCX (NL)
4. Result: Fully translated patent with identical formatting
```

### Legal Documents
```
1. Import contract
2. Use status tracking for complex clauses
3. Add notes to segments
4. Export bilingual version for review
```

### Technical Documentation
```
1. Import manual
2. Use Find/Replace for terminology consistency
3. Export to TSV for glossary extraction
```

## 🐛 Known Limitations (v0.3.2)

- ❌ No SRX-based segmentation yet (simple regex only)
- ❌ No translation memory integration
- ❌ No AI translation integration
- ❌ No concordance search
- ⚠️ Complex nested tables may need testing
- ⚠️ Very large documents (1000+ segments) may be slow

## 🚧 Planned Features (Future Versions)

- [ ] SRX rule-based segmentation
- [ ] Translation memory matching
- [ ] Integration with Supervertaler AI agents
- [ ] Quality assurance checks
- [ ] Concordance search
- [ ] Segment splitting/merging
- [ ] Auto-propagation of translations
- [ ] Complex table support (merged cells, nested tables)
- [ ] Track changes preservation

## 🔍 Testing

### Test with Sample Document

Create a test document in Word with:
```
Title: Test Document

This is the first sentence. This is the second sentence.

This is a new paragraph. It contains multiple sentences! 
Does it work correctly?

Final paragraph with some text.
```

Import it and verify:
1. Correct sentence segmentation
2. Paragraph tracking
3. Translation workflow
4. Export preserves structure

## 💡 Tips & Tricks

### Efficient Translation
- Use `Ctrl+D` to copy source when translation is identical
- Use `Ctrl+Enter` to quickly move through segments
- Change status to "Draft" while working, "Translated" when done

### Quality Control
- Export to Bilingual DOCX for review
- Use Find/Replace to ensure terminology consistency
- Check progress counter regularly

### Project Management
- Save frequently (Ctrl+S)
- Use descriptive project filenames
- Keep original DOCX files with project

## 🆘 Troubleshooting

### Import Error: "python-docx not installed"
```powershell
pip install python-docx
```

### Export Error: "Original DOCX file not found"
- Make sure the original DOCX file hasn't been moved or deleted
- The prototype needs the original file as a template for export

### Segmentation Issues
- Very long sentences might not segment properly
- Abbreviations might cause incorrect splits
- Custom SRX rules will be added in future versions

### Performance with Large Documents
- Documents with 1000+ segments may load slowly
- Consider splitting very large documents
- Future versions will have performance optimizations

## 📞 Support

For issues or questions:
- Check the main implementation plan: `CAT_TOOL_IMPLEMENTATION_PLAN.md`
- Review the Supervertaler documentation
- Test with small documents first

## 📝 Version History

### v0.3.2 (October 2, 2025)
- ✅ **Style Preservation on Export** - All Word styles maintained (Heading 1-3, Title, Subtitle, Normal)
- 🐛 **Bug Fix**: Missing Subtitle paragraph (object identity comparison fix)
- ✅ Style preservation for regular paragraphs AND table cells
- ✅ Graceful handling of missing styles

### v0.3.1 (October 2, 2025)
- ✅ **Style Visibility** - Display Word styles in Style column
- ✅ Color-coded headings (H1, H2, H3, Title, Subtitle)
- ✅ Style column added to grid (6 columns total)
- 🐛 **Bug Fix**: Column misalignment when saving translations

### v0.3.0 (October 2, 2025)
- ✅ **Table Support** - Import and translate table cells
- ✅ Type column showing "Para" or "T#R#C#" format
- ✅ Table cells as individual segments
- 🐛 **Bug Fix**: Table cell duplication (filter table paragraphs)

### v0.2.0 (October 1, 2025)
- ✅ **Inline Formatting Tags** - Bold, italic, underline preservation
- ✅ Tag validation and visual feedback
- ✅ Tag insertion buttons and keyboard shortcuts
- ✅ Copy source tags functionality

### v0.1.1 (October 1, 2025)
- 🐛 **Bug Fix**: DOCX export whitespace and paragraph matching

### v0.1 (October 1, 2025)
- ✅ Initial prototype release
- ✅ Basic DOCX import/export
- ✅ Simple segmentation
- ✅ Editable grid interface
- ✅ Find/Replace functionality
- ✅ Status tracking
- ✅ Project save/load

## 🎓 Next Steps

After testing this prototype:

1. **Provide Feedback** - What works? What needs improvement?
2. **Test with Real Documents** - Try your actual translation files
3. **Request Features** - What features are most important?
4. **Integration Planning** - Decide how to integrate with main Supervertaler

---

**Ready to translate! 🚀**
