# TMX Editor Module

A professional, nimble TMX (Translation Memory eXchange) editor inspired by the legendary **Heartsome TMX Editor 8**.

## 🎯 Overview

The TMX Editor is a specialized module that can run both **standalone** and **integrated** within Supervertaler. It provides a fast, user-friendly interface for editing translation memory files.

## ✨ Features

### Core Functionality
- ✅ **Dual-language grid editor** - Edit source and target side-by-side
- ✅ **Unicode bold search highlighting** - Search terms displayed in true bold (𝐛𝐨𝐥𝐝 𝐭𝐞𝐱𝐭)
- ✅ **Dual highlighting system** - Light yellow row background + bold search terms
- ✅ **Resizable columns** - Drag column borders to adjust width
- ✅ **Fast pagination** - 50 TUs per page for smooth performance
- ✅ **Integrated edit panel** - Edit directly above grid (no popup dialogs)
- ✅ **Multi-language support** - View any language pair from your TMX
- ✅ **Advanced filtering** - Filter by source/target content with real-time highlighting
- ✅ **TMX validation** - Check file structure and find issues
- ✅ **Header editing** - Edit TMX metadata
- ✅ **Statistics** - Analyze TMX content (TU count, character averages)

### File Operations
- 📁 Create new TMX files
- 📂 Open existing TMX files
- 💾 Save / Save As
- ➕ Add translation units
- ❌ Delete translation units
- 📋 Copy source to target
- 🔄 Batch operations on multiple TUs

### Integration
- 🪟 **Standalone mode** - Run independently
- 📑 **Embedded in Supervertaler** - Assistant panel tab
- 🛠️ **Tools menu** - Quick access from main app

## 🚀 Usage

### Standalone Mode

Run the TMX Editor independently:

```bash
# Qt Edition (PyQt6) - Recommended
python modules/tmx_editor_qt.py

# Tkinter Edition (Legacy)
python modules/tmx_editor.py
```

### Within Supervertaler

**Option 1: Assistant Panel**
1. Open Supervertaler
2. Look for the "📝 TMX Editor" tab in the assistant panel
3. Click to access embedded editor

**Option 2: Tools Menu**
1. Click "Tools" in toolbar
2. Select "TMX Editor"
3. Opens in separate window

**Option 3: Quick Actions**
- In the TMX Editor tab, use "🪟 Open in Separate Window" for full-screen editing

## 📖 Keyboard Shortcuts

**Standalone Mode:**
- `Ctrl+N` - New TMX file
- `Ctrl+O` - Open TMX file
- `Ctrl+S` - Save TMX file
- `Enter` (in filter boxes) - Apply filter
- `Double-click` - Edit translation unit
- `Right-click` - Context menu

## 🏗️ Architecture

### Inspiration: Heartsome TMX Editor 8

The original Heartsome TMX Editor 8 was built with:
- **Language:** Java
- **Framework:** Eclipse RCP (Rich Client Platform)
- **UI:** SWT (Standard Widget Toolkit) + NatTable
- **XML Parser:** VTD-XML (Virtual Token Descriptor)
- **Features:** Large file support via file splitting

### Our Implementation

**Technology Stack:**
- **Language:** Python 3.12+
- **UI Framework:** Tkinter (built-in, no extra dependencies)
- **XML Parser:** ElementTree (standard library)
- **Data Model:** Dataclasses for clean structure

**Design Decisions:**
- ✅ **Standalone capability** - Can be extracted and used independently
- ✅ **No external dependencies** - Uses only Python standard library
- ✅ **Pagination** - Handles large TMX files efficiently (50 TUs/page)
- ✅ **Clean separation** - Module can be maintained separately from Supervertaler
- ✅ **TMX 1.4 standard** - Full compliance with TMX specification

### Data Model

```python
@dataclass
class TmxSegment:
    """Translation unit variant (one language)"""
    lang: str
    text: str
    creation_date: str
    change_date: str

@dataclass
class TmxTranslationUnit:
    """Translation unit (multiple language variants)"""
    tu_id: int
    segments: Dict[str, TmxSegment]
    creation_date: str
    change_date: str

@dataclass
class TmxHeader:
    """TMX file header metadata"""
    creation_tool: str
    creation_tool_version: str
    segtype: str
    srclang: str
    # ... more fields
```

### Class Structure

```
TmxEditorUI (main UI class)
├── TmxFile (data model)
│   ├── TmxHeader (metadata)
│   └── List[TmxTranslationUnit] (content)
└── TmxParser (I/O operations)
    ├── parse_file()
    └── save_file()
```

## 🎨 UI Features

### Main Grid
- **ID Column** - Translation unit ID
- **Source Column** - Source language text (configurable)
- **Target Column** - Target language text (configurable)

### Language Selector
- Choose any source/target pair from available languages
- "All Languages" view to see complete language list

### Filter Panel
- Filter by source text
- Filter by target text
- Real-time filtering with Enter key
- Clear filters with one click

### Pagination
- ⏮️ First page
- ◀️ Previous page
- ▶️ Next page
- ⏭️ Last page
- Shows: "Page X of Y (Z TUs)"

### Toolbar
- 📁 New - Create new TMX file
- 📂 Open - Open existing TMX file
- 💾 Save - Save current file
- ➕ Add TU - Add new translation unit
- ❌ Delete - Delete selected TUs
- ℹ️ Header - Edit TMX metadata
- 📊 Stats - View file statistics
- ✓ Validate - Check TMX structure

## 📋 Comparison: Heartsome vs. Our Editor

| Feature | Heartsome TMX Editor 8 | Supervertaler TMX Editor |
|---------|----------------------|--------------------------|
| **Platform** | Java/Eclipse RCP | Python/Tkinter |
| **Dependencies** | Eclipse, SWT, VTD-XML | None (std library only) |
| **Installation** | Complex (Java runtime, Eclipse) | Simple (Python only) |
| **File Size** | ~100MB+ (with runtime) | ~50KB (single file) |
| **Startup Time** | 5-10 seconds | < 1 second |
| **Large Files** | File splitting | Pagination |
| **Performance** | Very fast (VTD-XML) | Fast (ElementTree) |
| **UI** | Professional Eclipse | Clean Tkinter |
| **Extensibility** | Eclipse plugin system | Python module |
| **Learning Curve** | High (Eclipse/Java) | Low (Python/Tkinter) |
| **Portability** | Cross-platform (JVM) | Cross-platform (Python) |

## 🔧 API Usage

### Programmatic Access

```python
from modules.tmx_editor import TmxEditorUI, TmxParser, TmxFile

# Method 1: Open GUI
editor = TmxEditorUI(standalone=True)
editor.run()

# Method 2: Parse TMX programmatically
tmx_file = TmxParser.parse_file("my_memory.tmx")
print(f"Loaded {tmx_file.get_tu_count()} translation units")
print(f"Languages: {tmx_file.get_languages()}")

# Method 3: Create TMX from scratch
tmx = TmxFile()
tu = TmxTranslationUnit(tu_id=1)
tu.set_segment("en-US", "Hello world")
tu.set_segment("nl-NL", "Hallo wereld")
tmx.add_translation_unit(tu)
TmxParser.save_file(tmx, "output.tmx")
```

## 🐛 Known Limitations

1. **No VTD-XML** - Uses ElementTree instead (slower for very large files)
2. **No file splitting** - Uses pagination instead (fine for most use cases)
3. **Basic validation** - Checks structure, not all TMX edge cases
4. **No inline tags** - Simple text editing (no complex tag handling yet)

## 🚧 Future Enhancements

Planned features:
- [ ] Find/Replace functionality
- [ ] Export to other formats (Excel, CSV, bilingual DOCX)
- [ ] Import from other formats
- [ ] Advanced validation (DTD checking)
- [ ] Inline tag support (for complex segments)
- [ ] Term extraction
- [ ] Merge multiple TMX files
- [ ] Split TMX by language pairs
- [ ] Advanced search (regex support)

## 📜 License

MIT License - Free and open source

## 🙏 Credits

- **Inspired by:** Heartsome TMX Editor 8 (archived open-source project)
- **Original Heartsome Team:** Jason, Robert, and contributors
- **Reimplemented by:** Michael Beijer (Supervertaler project)
- **Original Heartsome Source:** https://github.com/heartsome/tmxeditor8

## 📚 Resources

- [TMX 1.4 Specification](http://www.lisa.org/tmx/tmx.htm)
- [Heartsome TMX Editor 8 (archived)](https://github.com/heartsome/tmxeditor8)
- [Translation Memory eXchange Format](https://en.wikipedia.org/wiki/Translation_Memory_eXchange)

---

**Designer:** Michael Beijer  
**Project:** Supervertaler v3.7.5+  
**Module:** TMX Editor  
**Status:** Production Ready  
