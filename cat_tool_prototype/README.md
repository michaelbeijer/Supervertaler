# CAT Editor Prototype v0.1

**A standalone Computer-Aided Translation (CAT) Editor for Supervertaler**

## 🎯 Features

- ✅ **DOCX Import** - Import Microsoft Word documents
- ✅ **Automatic Segmentation** - Split text into translatable segments
- ✅ **Editable Grid** - Excel-like interface for translation
- ✅ **DOCX Export** - Export with formatting preservation
- ✅ **Bilingual Export** - Create side-by-side review documents
- ✅ **TSV Export** - Export to tab-separated format
- ✅ **Find/Replace** - Search and replace across segments
- ✅ **Status Tracking** - Track translation progress
- ✅ **Project Save/Load** - Save work and resume later

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

## 📁 File Structure

```
cat_tool_prototype/
├── cat_editor_prototype.py    # Main application
├── simple_segmenter.py         # Sentence segmentation
├── docx_handler.py             # DOCX import/export
└── README.md                   # This file
```

## 🎨 User Interface

### Main Window

```
┌─────────────────────────────────────────────────────────┐
│  Supervertaler CAT Editor - Prototype v0.1              │
├─────────────────────────────────────────────────────────┤
│ [Import] [Save] [Export] │ [Find/Replace]  Progress: 50%│
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

## 🐛 Known Limitations (v0.1)

- ❌ No SRX-based segmentation yet (simple regex only)
- ❌ Limited formatting preservation (paragraph-level only)
- ❌ No inline tag handling for bold/italic within segments
- ❌ No table support during segmentation
- ❌ No translation memory integration
- ❌ No AI translation integration

## 🚧 Planned Features (Future Versions)

- [ ] SRX rule-based segmentation
- [ ] Advanced formatting preservation (run-level)
- [ ] Inline tag handling
- [ ] Table cell segmentation
- [ ] Translation memory matching
- [ ] Integration with Supervertaler AI agents
- [ ] Quality assurance checks
- [ ] Concordance search
- [ ] Segment splitting/merging
- [ ] Auto-propagation of translations

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
