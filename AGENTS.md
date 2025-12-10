# Instructions for AI Agents (AGENTS.md)

> **This file provides comprehensive project documentation for AI coding assistants.**
> **Also see:** `CLAUDE.md` (identical), `PROJECT_CONTEXT.md` (detailed development history)

---

## 🎯 Project Overview

**Supervertaler** is a professional desktop translation application built with Python and PyQt6. It's designed as a companion tool for translators, integrating AI-powered translation with traditional CAT (Computer-Assisted Translation) tool workflows.

| Property | Value |
|----------|-------|
| **Name** | Supervertaler |
| **Version** | v1.9.32 (December 2025) |
| **Framework** | PyQt6 (Qt for Python) |
| **Language** | Python 3.10+ |
| **Platform** | Windows (primary), Linux compatible |
| **Repository** | https://github.com/michaelbeijer/Supervertaler |
| **Website** | https://supervertaler.com |

---

## 📁 Project Structure

```
Supervertaler/
├── Supervertaler.py          # Main application (~32,000+ lines)
├── modules/                   # 60+ specialized modules
│   ├── llm_clients.py        # OpenAI, Anthropic, Google Gemini, Ollama
│   ├── translation_memory.py # TM matching and storage
│   ├── termbase_manager.py   # Terminology management
│   ├── docx_handler.py       # DOCX import/export
│   ├── sdlppx_handler.py     # Trados Studio packages
│   ├── phrase_docx_handler.py# Phrase/Memsource bilingual
│   ├── cafetran_docx_handler.py # CafeTran bilingual
│   ├── supermemory.py        # Vector-indexed semantic TM (ChromaDB)
│   ├── spellcheck_manager.py # Spellcheck with pyspellchecker/Hunspell
│   ├── prompt_library.py     # AI prompt management
│   └── ...                   # See full list below
├── user_data/                 # User content (gitignored)
│   ├── prompts/              # .svprompt files
│   ├── termbases/            # .db termbase files
│   ├── translation_memories/ # .db TM files
│   ├── dictionaries/         # Custom spellcheck words
│   └── supermemory/          # ChromaDB vector database
├── assets/                    # Icons, images
├── docs/                      # Documentation site
├── tests/                     # Test files
└── legacy_versions/           # Historical Tkinter version
```

---

## 🔧 Key Technical Details

### Main Application (`Supervertaler.py`)

The main file is a large monolithic PyQt6 application. Key sections:

| Line Range | Purpose |
|------------|---------|
| 1-700 | Imports, constants, Project dataclass |
| 700-2000 | Custom widgets (grid editors, checkboxes) |
| 2000-4500 | MainWindow initialization, UI setup |
| 4500-8000 | Menu actions, file operations |
| 8000-12000 | Settings dialogs |
| 12000-18000 | Grid operations, navigation |
| 18000-25000 | Import/Export handlers |
| 25000-32000 | AI translation, batch operations |

### Project Class (Dataclass)

```python
@dataclass
class Project:
    segments: List[Segment]
    source_lang: str
    target_lang: str
    original_docx_path: Optional[str] = None
    memoq_source_path: Optional[str] = None
    sdlppx_source_path: Optional[str] = None
    # ... many more fields
```

### Segment Class (Dataclass)

```python
@dataclass
class Segment:
    source: str
    target: str = ""
    status: str = "Not Started"
    notes: str = ""
    segment_type: str = "text"
    # ... additional fields
```

### File Extensions

| Extension | Purpose |
|-----------|---------|
| `.svproj` | Supervertaler project files (JSON) |
| `.svprompt` | Prompt files (JSON) |
| `.svntl` | Non-translatables lists (JSON) |

---

## 🔌 Module Overview

### AI & LLM
- `llm_clients.py` - OpenAI, Anthropic Claude, Google Gemini, Ollama integration
- `model_version_checker.py` - Auto-detect new LLM models
- `prompt_library.py` - Prompt management and favorites
- `voice_dictation.py` - Whisper-based voice input

### Translation Memory & Terminology
- `translation_memory.py` - Fuzzy matching TM system
- `supermemory.py` - ChromaDB vector semantic search
- `termbase_manager.py` - SQLite-based terminology
- `term_extractor.py` - Automatic term extraction

### File Handlers
- `docx_handler.py` - Standard DOCX import/export
- `sdlppx_handler.py` - Trados Studio SDLPPX/SDLRPX packages
- `phrase_docx_handler.py` - Phrase/Memsource bilingual DOCX
- `cafetran_docx_handler.py` - CafeTran bilingual DOCX
- `trados_docx_handler.py` - Trados bilingual review DOCX
- `mqxliff_handler.py` - memoQ XLIFF files

### Spellcheck
- `spellcheck_manager.py` - Dual-backend spellcheck (pyspellchecker + Hunspell)

### UI Components
- `ribbon_widget.py` - Ribbon-style toolbar
- `translation_results_panel.py` - Match display
- `termview_widget.py` - Inline term display
- `superlookup.py` - Unified lookup window

---

## 🏗️ Architecture Patterns

### UI Pattern
- PyQt6 with custom styled widgets
- Consistent checkbox styling (`CheckmarkCheckBox`, `PinkCheckmarkCheckBox`)
- Tag-based text formatting (`<b>`, `<i>`, `<u>`, `<li-o>`, `<li-b>`)
- Grid-based segment editor with source (read-only) and target (editable) columns

### Data Flow
1. Import file → Parse to segments → Display in grid
2. User translates/edits → Status updates → Grid refreshes
3. Export → Reconstruct original format with translations

### Settings Storage
- `user_data/general_settings.json` - App preferences
- `user_data/ui_preferences.json` - Window geometry, button states
- `.svproj` files - Per-project settings

---

## 📝 Development Guidelines

### When Editing Supervertaler.py
1. The file is large (~32K lines) - use line ranges when reading
2. Search for method names with `grep_search` before editing
3. Follow existing patterns for new features
4. Update `__version__` at the top when making changes

### When Adding New Modules
1. Create in `modules/` directory
2. Add import in main file where needed
3. Follow existing module patterns (docstrings, type hints)

### Documentation Updates
**Always update these files after changes:**
1. `PROJECT_CONTEXT.md` - Add dated entry with details
2. `CHANGELOG.md` - Add version entry
3. `README.md` - Update version badge

### Commit Messages
Use semantic prefixes:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `refactor:` - Code restructuring
- `style:` - Formatting

---

## 🧪 Testing

### Running Tests
```bash
pytest tests/
```

### Manual Testing Checklist
- [ ] Import DOCX, translate segment, export
- [ ] Save/load .svproj project
- [ ] TM matching works
- [ ] Termbase highlighting works
- [ ] AI translation (if API keys configured)

---

## 🔑 API Keys

Store in `api_keys.txt` (gitignored):
```
openai_api_key=sk-...
anthropic_api_key=sk-ant-...
google_api_key=AI...
```

---

## 📚 Additional Resources

| File | Purpose |
|------|---------|
| `PROJECT_CONTEXT.md` | Detailed development history and decisions |
| `CHANGELOG.md` | Complete version history |
| `README.md` | User-facing documentation |
| `FAQ.md` | Common questions |
| `docs/guides/` | User guides |
| `docs/technical/` | Technical documentation |

---

## ⚠️ Common Pitfalls

1. **ElementTree namespaces** - Always use namespace dict when working with SDLXLIFF
2. **Grid widget access** - Use `table.cellWidget()` for QTextEdit, `table.item()` for QTableWidgetItem
3. **File paths** - Store absolute paths, use `os.path.exists()` before accessing
4. **Status updates** - Remember to update both internal data and grid display

---

## 🔄 Recent Development Focus (v1.9.x)

- **v1.9.32** - Trados SDLRPX conf status fix
- **v1.9.31** - Spellcheck language initialization
- **v1.9.30** - LLM debug path fix
- **v1.9.29** - Spellcheck integration
- **v1.9.28** - Phrase DOCX, Show Invisibles
- **v1.9.27** - Simple TXT import/export
- **v1.9.26** - Auto model version checker
- **v1.9.19-20** - Trados SDLPPX/SDLRPX support

---

*Last updated: December 10, 2025 - v1.9.32*
