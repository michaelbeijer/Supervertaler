# Supervertaler - AI Agent Documentation

> **This is the single source of truth for AI coding assistants working on this project.**
> **Last Updated:** January 21, 2026 | **Version:** v1.9.146

---

## 🎯 Project Overview

**Supervertaler** is a professional desktop translation application built with Python and PyQt6. It serves as a companion tool for translators, integrating AI-powered translation with traditional CAT (Computer-Assisted Translation) tool workflows.

| Property | Value |
|----------|-------|
| **Name** | Supervertaler |
| **Version** | v1.9.146 (January 2026) |
| **Framework** | PyQt6 (Qt for Python) |
| **Language** | Python 3.10+ |
| **Platform** | Windows (primary), Linux compatible |
| **Repository** | https://github.com/michaelbeijer/Supervertaler |
| **Website** | https://supervertaler.com |
| **Main File** | `Supervertaler.py` (~38,000+ lines) |
| **Modules** | 60+ specialized modules in `modules/` directory |

### Key Capabilities

- **Multi-LLM AI Translation**: OpenAI GPT-4, Anthropic Claude, Google Gemini, Local Ollama
- **CAT Tool Integration**: Trados SDLPPX/SDLRPX, memoQ XLIFF, Phrase/Memsource DOCX, CafeTran DOCX, Déjà Vu X3 RTF
- **Translation Memory**: Fuzzy matching TM with TMX import/export + Supermemory (ChromaDB vector search)
- **Terminology Management**: SQLite-based termbases with priority highlighting and automatic extraction
- **Document Handling**: DOCX, bilingual DOCX, PDF (via OCR), simple TXT, **Multi-file folder import**
- **Quality Assurance**: Spellcheck, tag validation, consistency checking
- **Superlookup**: Unified concordance hub with TM, Termbase, Supermemory, MT, and Web Resources
- **Batteries Included**: Default install includes all major features and dependencies, except heavy optional components (Supermemory + offline Local Whisper)

---

## 📦 Installation (Simplified)

Supervertaler uses a batteries-included *core* install: `pip install supervertaler` pulls in everything needed for the major features, while keeping heavy optional components out of the default install.

**Note:** Offline dictation via Local Whisper is optional because it pulls in very large dependencies (PyTorch). The default/recommended voice path uses the OpenAI Whisper API.

**Legacy note:** older “extras” (e.g. `supervertaler[all]`) are still accepted for backward compatibility, but they no longer change what gets installed.

### Installation Options

| Command | Notes |
|---------|-------|
| `pip install supervertaler` | Recommended core install (excludes heavy optional Local Whisper) |
| `pip install supervertaler[local-whisper]` | Adds offline Local Whisper (heavy; pulls PyTorch) |
| `pip install supervertaler[all]` | Legacy alias (no-op; kept for compatibility) |

### Feature Modules

| Module | Included by default | Size | Description |
|--------|----------------------|------|-------------|
| **Supervoice** | ✅ | ~150 MB | Voice dictation & commands (OpenAI Whisper API recommended) |
| **Web Browser** | ✅ | ~100 MB | Built-in browser for Superlookup |
| **PDF Rescue** | ✅ | ~30 MB | PDF text extraction/OCR |
| **MT Providers** | ✅ | ~30 MB | DeepL, Amazon Translate |
| **Hunspell** | ✅ | ~20 MB | Advanced spellcheck |
| **AutoFingers** | ✅ (Windows) | ~10 MB | Windows automation |

### Settings → Features Tab

Users can enable/disable features in **Settings → 📦 Features**.

### Feature Manager Module

The `modules/feature_manager.py` provides:
- `FeatureManager` class for checking feature availability
- `FEATURE_MODULES` dict defining all optional features
- `lazy_import_*()` functions for conditional imports
- `check_feature(id)` quick availability check

---

## 🪟 Windows EXE Releases (CORE + FULL)

Supervertaler Windows releases are published as **two separate ZIP assets** on the same GitHub Release:

1) **CORE** (recommended for most users)
- Smaller download
- Does **not** bundle the heavy ML stack (Supermemory + offline Local Whisper)

2) **FULL** ("batteries included")
- Larger download
- Bundles **Supermemory** + **offline Local Whisper** (PyTorch / sentence-transformers / ChromaDB)

### Key Rule (PyInstaller one-folder builds)

The EXE must be run from the extracted distribution folder. Do **not** separate `Supervertaler.exe` from `_internal/`.

If users see an error like missing `python312.dll`, they are almost always:
- running the wrong EXE (from an intermediate build folder), or
- moving the EXE away from `_internal/`.

### How to Build (recommended)

Use the automated build script:

```powershell
# Build BOTH core + full and create both ZIP assets
powershell -NoProfile -ExecutionPolicy Bypass -File .\build_windows_release.ps1

# Build only core
powershell -NoProfile -ExecutionPolicy Bypass -File .\build_windows_release.ps1 -CoreOnly

# Build only full
powershell -NoProfile -ExecutionPolicy Bypass -File .\build_windows_release.ps1 -FullOnly

# Clean build venvs + rebuild (keeps dist/ so multi-flavor builds can coexist)
powershell -NoProfile -ExecutionPolicy Bypass -File .\build_windows_release.ps1 -Clean
```

What it does:
- Uses two isolated build environments: `.venv-build-core` and `.venv-build-full`
- Runs PyInstaller with the corresponding spec:
  - `Supervertaler.core.spec` → `dist\Supervertaler-core\...`
  - `Supervertaler.full.spec` → `dist\Supervertaler-full\...`
- Zips each output using `create_release_zip.py` and writes a `README_FIRST.txt` into each dist folder.

### Output Files

After a successful run, you should have:
- `dist\Supervertaler-v<version>-Windows-CORE.zip`
- `dist\Supervertaler-v<version>-Windows-FULL.zip`

### GitHub Release Posting

Attach **both** ZIP files to the same GitHub Release tag.

### VS Code Tasks

There are build tasks wired up in `.vscode/tasks.json`:
- "Build Windows EXE (core)"
- "Build Windows EXE (full)"
- "Build Windows EXE (core + full)"

---

## 📁 Project Structure

```
Supervertaler/
├── Supervertaler.py          # Main application (~38,000+ lines)
├── modules/                   # 60+ specialized modules
│   ├── feature_manager.py    # Modular feature management (NEW)
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
│   └── ...                   # See module list below
├── user_data/                 # User content (gitignored)
│   ├── prompts/              # .svprompt files
│   ├── termbases/            # .db termbase files
│   ├── translation_memories/ # .db TM files
│   ├── dictionaries/         # Custom spellcheck words
│   └── supermemory/          # ChromaDB vector database
├── assets/                    # Icons, images
├── docs/                      # Documentation site
├── beijerterm/                # 🔗 GIT SUBMODULE - Beijerterm glossary website
├── tests/                     # Test files
└── legacy_versions/           # Historical Tkinter version
```

---

## 🔗 Beijerterm Website Submodule (IMPORTANT FOR AI AGENTS)

The `beijerterm/` folder is a **Git submodule** - a separate repository embedded inside Supervertaler.

### What is a Submodule?

- It's a **pointer** to a specific commit in another repository
- Regular `git clone` does NOT download submodule contents (saves ~15 MB)
- The submodule has its own `.git` and tracks `michaelbeijer/beijerterm` separately

### Two Separate Projects

| Project | Location | Purpose |
|---------|----------|---------|
| **Supervertaler** | Root folder | PyQt6 translation app |
| **Beijerterm** | `beijerterm/` subfolder | Static glossary website (beijerterm.com) |

**Note**: The "Superlookup" name refers to the in-app lookup panel inside Supervertaler - don't confuse it with the Beijerterm website!

### Working with the Submodule

**To make changes to Beijerterm website:**
```bash
cd beijerterm/
# Edit files...
git add .
git commit -m "your message"
git push origin main          # Pushes to michaelbeijer/beijerterm
```

**Then update the parent reference:**
```bash
cd ..                          # Back to Supervertaler root
git add beijerterm             # Stage the new submodule commit pointer
git commit -m "chore: Update beijerterm submodule"
git push origin main           # Pushes to michaelbeijer/Supervertaler
```

### ⚠️ Common Pitfalls

1. **Commits in submodule aren't automatically tracked** - After committing inside `beijerterm/`, you must also commit in the parent repo to update the pointer.

2. **Changelogs are separate** - Beijerterm website changes go in `beijerterm/CHANGELOG.md`, Supervertaler changes go in `CHANGELOG.md` at root.

3. **Features in the wrong repo** - The "Superlookup" panel inside Supervertaler.py is part of **Supervertaler**, not the Beijerterm website. Don't confuse them!

4. **Building the website** - Run `python scripts/build_site.py` from inside `beijerterm/`, not from root.

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

### Key Classes

```python
@dataclass
class Project:
    segments: List[Segment]
    source_lang: str
    target_lang: str
    original_docx_path: Optional[str] = None
    memoq_source_path: Optional[str] = None
    sdlppx_source_path: Optional[str] = None
    phrase_source_path: Optional[str] = None
    original_txt_path: Optional[str] = None
    # ... 20+ fields total

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

## 🔌 Complete Module List

### AI & LLM (`modules/`)
- `llm_clients.py` - OpenAI, Anthropic Claude, Google Gemini, Ollama integration
- `model_version_checker.py` - Auto-detect new LLM models from providers
- `model_update_dialog.py` - UI for selecting new models
- `prompt_library.py` - Prompt management and favorites
- `prompt_assistant.py` - AI-powered prompt generation
- `unified_prompt_library.py` - Unified prompt system
- `unified_prompt_manager_qt.py` - Prompt manager UI
- `voice_dictation.py` - Whisper-based voice input
- `voice_commands.py` - Talon-style voice command system (NEW)
- `ai_actions.py` - AI action system for prompt library
- `ai_attachment_manager.py` - File attachment persistence
- `ai_file_viewer_dialog.py` - File viewing dialog

### Translation Memory & Terminology
- `translation_memory.py` - Fuzzy matching TM system
- `supermemory.py` - ChromaDB vector semantic search (2100+ lines)
- `termbase_manager.py` - SQLite-based terminology
- `term_extractor.py` - Automatic term extraction
- `termbase_entry_editor.py` - Term editing UI
- `termbase_import_export.py` - TMX/TBX import/export
- `tm_manager_qt.py` - TM management UI
- `tm_metadata_manager.py` - TM metadata handling
- `tm_editor_dialog.py` - TM editing dialog
- `tmx_editor.py` / `tmx_editor_qt.py` - TMX file editing
- `tmx_generator.py` - TMX file generation

### File Handlers
- `docx_handler.py` - Standard DOCX import/export
- `sdlppx_handler.py` - Trados Studio SDLPPX/SDLRPX packages (767+ lines)
- `phrase_docx_handler.py` - Phrase/Memsource bilingual DOCX
- `cafetran_docx_handler.py` - CafeTran bilingual DOCX
- `trados_docx_handler.py` - Trados bilingual review DOCX
- `dejavurtf_handler.py` - Déjà Vu X3 bilingual RTF (NEW in v1.9.91)
- `mqxliff_handler.py` - memoQ XLIFF files
- `simple_segmenter.py` - Text segmentation

### Spellcheck & QA
- `spellcheck_manager.py` - Dual-backend spellcheck (pyspellchecker + Hunspell)
- `non_translatables_manager.py` - Non-translatable term management
- `tag_cleaner.py` - CAT tool tag removal
- `tag_manager.py` - Tag handling

### UI Components
- `ribbon_widget.py` - Ribbon-style toolbar
- `translation_results_panel.py` - Match display panel
- `termview_widget.py` - Inline term display
- `superlookup.py` - Unified lookup window
- `superbrowser.py` - Multi-chat AI browser
- `quick_access_sidebar.py` - Quick access panel
- `keyboard_shortcuts_widget.py` - Shortcut management
- `project_home_panel.py` - Project home UI

### Utilities
- `database_manager.py` - SQLite database operations
- `database_migrations.py` - Database schema migrations
- `config_manager.py` - Settings management
- `file_dialog_helper.py` - File dialog utilities
- `find_replace.py` - Find and replace functionality
- `shortcut_manager.py` - Keyboard shortcut handling
- `theme_manager.py` - UI theme management
- `statuses.py` - Segment status definitions

### Specialized Tools
- `pdf_rescue_Qt.py` - AI OCR for PDF extraction
- `image_extractor.py` - Extract images from DOCX
- `figure_context_manager.py` - Image context for AI
- `document_analyzer.py` - Document analysis
- `encoding_repair.py` / `encoding_repair_Qt.py` - Fix encoding issues
- `autofingers_engine.py` - memoQ AutoFingers automation
- `tracked_changes.py` - Track changes analysis
- `supercleaner.py` / `supercleaner_ui.py` - Text cleaning

### Benchmarking
- `llm_leaderboard.py` - LLM quality benchmarking
- `superbench_ui.py` - Benchmark UI
- `local_llm_setup.py` - Ollama setup wizard

---

## 🏗️ Architecture Patterns

### UI Pattern
- PyQt6 with custom styled widgets
- Consistent styling:
  - Checkboxes: `CheckmarkCheckBox` (Standard), `PinkCheckmarkCheckBox` (Project), `BlueCheckmarkCheckBox` (Global)
  - Radio Buttons: `CheckmarkRadioButton` (Standard Green)
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
1. `AGENTS.md` - Add dated entry to development history
2. `CHANGELOG.md` - Add version entry
3. `README.md` - Update version badge if needed

### Commit Messages
Use semantic prefixes:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `refactor:` - Code restructuring
- `style:` - Formatting

---

## ⚠️ Common Pitfalls

1. **ElementTree namespaces** - Always use namespace dict when working with SDLXLIFF:
   ```python
   NAMESPACES = {'sdl': 'http://sdl.com/FileTypes/SdlXliff/1.0'}
   element.find('.//sdl:seg', NAMESPACES)
   ```

2. **Grid widget access** - Use `table.cellWidget()` for QTextEdit, `table.item()` for QTableWidgetItem

3. **File paths** - Store absolute paths, use `os.path.exists()` before accessing

4. **Status updates** - Remember to update both internal data and grid display

5. **Signal blocking** - When setting text programmatically, use `blockSignals(True/False)` to prevent cascading events

6. **Qt event queue** - Be aware that `setPlainText()` queues events even when signals are blocked

7. **Hidden widget styling** - Qt may not apply stylesheets to hidden widgets. If theme colors aren't appearing, apply styles when the widget becomes visible, not just at creation time

8. **Race conditions & timing** - When debugging UI issues, consider whether the problem might be timing-related:
   - Widgets created before theme manager is initialized
   - Styles applied while widgets are hidden
   - Signals firing before handlers are connected
   - Use `QTimer.singleShot()` for deferred initialization when needed

---

## 📋 Planned Features & Refactoring

### 🔧 Configuration File Consolidation (PRIORITY - Scheduled)

**Identified:** January 9, 2026  
**Status:** Documented, not yet implemented  
**Complexity:** Medium (30-40 file edits + migration script)

**Current Problem: Configuration File Sprawl**

Settings are currently scattered across multiple JSON files in `user_data/`:
- `general_settings.json` - General application preferences
- `ui_preferences.json` - Window geometry, button states (DEPRECATED, migrated to general_settings.json)
- `themes.json` - Theme definitions
- `recent_projects.json` - Recent project list
- `feature_settings.json` - Optional feature toggles
- `find_replace_history.json` - Find & Replace history
- `superlookup_history.json` - Superlookup search history
- `voice_commands.json` - Voice command library
- Plus module-specific configs...

**Issues:**
1. **Scattered settings** - Hard to find where a setting is stored
2. **Code complexity** - Multiple file read/write operations throughout codebase
3. **Inconsistent structure** - Each file has different patterns (nested vs flat, etc.)
4. **Migration headaches** - Changing structure requires updating multiple files
5. **User confusion** - Manual editing requires knowing which file to look in
6. **Backup/restore complexity** - Must backup multiple files to preserve all settings

**Proposed Solution: Single `config.json`**

Consolidate all settings into one well-structured file:

```json
{
  "config_version": "1.0.0",
  "general": {
    "restore_last_project": false,
    "auto_propagate_exact_matches": true,
    "auto_center_active_segment": true,
    "auto_insert_100_percent_matches": true,
    "auto_confirm_100_percent_matches": false,
    "tm_save_mode": "latest",
    "enable_smart_word_selection": true,
    "enable_auto_backup": true,
    "backup_interval_minutes": 5
  },
  "ui": {
    "theme": "light",
    "window_geometry": {
      "x": 100,
      "y": 100,
      "width": 1200,
      "height": 800
    },
    "fonts": {
      "grid_family": "Segoe UI",
      "grid_size": 11,
      "results_match_size": 9,
      "results_compare_size": 9,
      "termview_family": "Segoe UI",
      "termview_size": 10,
      "termview_bold": false
    },
    "colors": {
      "tag_color": "#7f0001",
      "focus_border_color": "#2196F3",
      "focus_border_thickness": 2,
      "badge_text_color": "#333333",
      "invisible_char_color": "#999999",
      "even_row_color": "#FFFFFF",
      "odd_row_color": "#F0F0F0"
    },
    "layout": {
      "tabs_above_grid": false,
      "enable_alternating_row_colors": true,
      "show_invisibles": false
    }
  },
  "features": {
    "supermemory_enabled": true,
    "supermemory_auto_init": false,
    "voice_enabled": false,
    "web_browser_enabled": true,
    "pdf_rescue_enabled": true,
    "autofingers_enabled": false
  },
  "match_limits": {
    "LLM": 3,
    "MT": 5,
    "TM": 10,
    "Termbases": 10
  },
  "termbase": {
    "enable_grid_highlighting": true,
    "highlight_style": "semibold",
    "display_order": "appearance",
    "hide_shorter_matches": false,
    "dotted_color": "#808080"
  },
  "precision_scroll": {
    "divisor": 3
  },
  "recent_projects": [
    "/path/to/project1.svproj",
    "/path/to/project2.svproj",
    "/path/to/project3.svproj"
  ],
  "custom_themes": [
    {
      "name": "Dark Blue",
      "is_dark": true,
      "colors": {
        "background": "#1e1e1e",
        "foreground": "#d4d4d4",
        ...
      }
    }
  ],
  "history": {
    "find_replace": [
      {"find": "example", "replace": "sample"}
    ],
    "superlookup_searches": [
      "translation memory",
      "terminology"
    ]
  },
  "voice_commands": {
    "enabled": false,
    "recognition_engine": "openai_whisper",
    "custom_commands": [
      {
        "phrase": "next segment",
        "aliases": ["go next", "move forward"],
        "action_type": "internal",
        "action": "next_segment"
      }
    ]
  },
  "ollama": {
    "keepwarm": false
  },
  "autohotkey": {
    "path": "C:\\Program Files\\AutoHotkey\\v2\\AutoHotkey64.exe"
  }
}
```

**Benefits:**
- ✅ **Single source of truth** - All settings in one place
- ✅ **Clear hierarchy** - Logical grouping by functionality
- ✅ **Easy to read/edit** - Clear structure for manual editing
- ✅ **Atomic saves** - All settings updated together (no partial updates)
- ✅ **Simple backup/restore** - One file to backup
- ✅ **Version tracking** - `config_version` field for migrations
- ✅ **Better defaults** - Easy to see all default values at once

**Implementation Plan:**

1. **Create `modules/config_manager_v2.py`** (new unified config manager):
   - `ConfigManager` class with section accessors
   - `get(section, key, default)` method
   - `set(section, key, value)` method
   - `save()` method (atomic write)
   - `load()` method with validation

2. **Migration script** (`scripts/migrate_config.py`):
   - Read all existing JSON files
   - Map to new structure
   - Write `config.json`
   - Backup old files to `user_data/config_backup/`
   - Run automatically on first startup after update

3. **Update all load/save calls** (~30-40 locations):
   - Replace `_load_general_settings_from_file()` → `config_manager.get('general', key)`
   - Replace `save_general_settings()` → `config_manager.set('general', key, value)` + `config_manager.save()`
   - Update theme manager
   - Update recent projects
   - Update find/replace history
   - Update voice command loader

4. **Backward compatibility**:
   - Keep old loaders as fallback for 1-2 versions
   - Log migration warnings
   - Auto-migrate on first run

5. **Testing checklist**:
   - [ ] Fresh install (no config files)
   - [ ] Migration from old files
   - [ ] Settings persist correctly
   - [ ] All features still work
   - [ ] No performance regression

**Files to modify:**
- `Supervertaler.py` - Replace all config load/save calls
- `modules/config_manager_v2.py` - NEW unified config manager
- `modules/theme_manager.py` - Use new config manager
- `modules/voice_commands.py` - Use new config manager
- `modules/find_replace_qt.py` - Use new config manager
- `scripts/migrate_config.py` - NEW migration script

**Estimated effort:** 3-4 hours (careful testing needed)

**Priority:** High (improves maintainability significantly)

---

## � Future Investigation: TMX Tag Export Format


**Issue discovered December 22, 2025**: Our TMX Editor stores formatting tags (like `<b>`, `<i>`) as escaped text (`&lt;b&gt;`) in the `<seg>` element. This is valid XML but may not be the optimal approach.

**Three approaches exist:**

| Approach | Example in TMX file | Pros | Cons |
|----------|---------------------|------|------|
| **Escaped text** | `<seg>&lt;b&gt;text&lt;/b&gt;</seg>` | Simple, valid XML | Tags treated as plain text, lost semantic meaning |
| **TMX inline elements** | `<seg><bpt i="1" type="bold">&lt;b&gt;</bpt>text<ept i="1">&lt;/b&gt;</ept></seg>` | TMX 1.4 compliant, preserves tag semantics | More complex to implement |
| **Raw XML** (invalid) | `<seg><b>text</b></seg>` | Human readable | Invalid XML unless DTD defines `<b>` |

**What other tools do:**
- **memoQ**: Uses TMX inline elements (`<bpt>`, `<ept>`) for proper tag preservation
- **Trados Studio**: Similar, uses inline elements with type attributes
- **OmegaT**: Generally uses escaped text for simplicity
- **Many web tools**: Just escape everything

**Recommendation for future**: Consider implementing proper TMX inline elements (`<bpt>`, `<ept>`, `<ph>`) when exporting. This would:
1. Maintain compatibility with professional CAT tools
2. Preserve tag type information (bold, italic, etc.)
3. Allow round-tripping without tag loss

**Files to modify**: `modules/tmx_editor.py` - `TmxParser.save_file()` method

---

## �💡 Problem-Solving Tips for AI Agents

When stuck on a difficult bug, consider these approaches:

1. **Think about timing**: Is this a race condition? Are things happening in the wrong order?
   - Widget creation vs. theme application timing
   - Signal connections vs. signal emissions
   - Hidden vs. visible widget state changes

2. **Think outside the box**: The obvious solution may not work
   - If stylesheets aren't applying, try QPalette as an alternative
   - If a method isn't being called, check if the widget is even visible
   - If changes aren't reflected, check if there's caching involved

3. **Add debug output**: When behavior is mysterious, add logging to trace execution flow
   - Print method entry/exit with timestamps
   - Log parameter values and state
   - Write to a debug file if console output is too fast

4. **Question assumptions**: What do you THINK is happening vs. what is ACTUALLY happening?
   - The code might be running but not having the expected effect
   - A different code path might be executing
   - Something else might be overriding your changes

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
- [ ] Spellcheck toggles correctly
- [ ] SDLPPX import/export round-trip

---

## 🔑 API Keys

**Unified Loading System with Dev-First Priority:**

The app now uses a **dual-path** API key loading system:

1. **Priority 1**: `user_data_private/api_keys.txt` (Dev mode - gitignored, never synced)
2. **Priority 2**: `user_data/api_keys.txt` (User mode - ships with app)

**For Developers (running from source):**
- Store keys in: `user_data_private/api_keys.txt`
- This location is fully gitignored and will **never** be uploaded to GitHub
- All features (translation, AI Assistant, tests) will find keys here

**For End Users (pip install or .exe):**
- Store keys in: `user_data/api_keys.txt`
- The app auto-creates this location on first run

**Format:**
```
openai=sk-...
claude=sk-ant-...
google=AI...
deepl=...
```

**Implementation Details:**
- `Supervertaler.py` line ~39407: `load_api_keys()` method checks dev path first
- `modules/unified_prompt_manager_qt.py` line ~2824: AI Assistant uses parent app's loader
- All API key loading now unified through main app's method

---

## 🔄 Recent Development History

### January 21, 2026 - Glossary Bug Fixes & Compare Panel Enhancement (v1.9.141-145)

**🐛 Glossary/Termview Bug Fixes**

Fixed chain of bugs related to glossary management after Alt+Down term addition:

| Version | Issue | Fix |
|---------|-------|-----|
| **v1.9.141** | Termview goes blank after adding term ("list index out of range") | Fixed dict key mismatch: `source_term`→`source`, `target_term`→`translation` in `_refresh_termbase_display_for_current_segment()` |
| **v1.9.142** | Edit glossary entry error ("on_cell_selected() missing 2 required positional arguments") | Simplified `_refresh_current_segment_matches()` to use `_refresh_termbase_display_for_current_segment()` instead of calling `on_cell_selected()` |
| **v1.9.143** | Delete glossary entry error ("'DatabaseManager' object has no attribute 'get_connection'") | Changed to use `self.termbase_mgr.delete_term(term_id)` instead of non-existent database method |

**Key Method - Data Structure:**
- `find_termbase_matches_in_source()` returns dict with keys: `source`, `translation`, `termbase_name`, `priority`, etc.
- NOT `source_term` / `target_term` as previously assumed

**🎨 Compare Panel memoQ-Style Diff (v1.9.144-145)**

Enhanced `_set_compare_panel_text_with_diff()` to show word-level differences like memoQ's "Track changes view":

| Element | Style |
|---------|-------|
| **Deletions** | Red text (#CC0000) with strikethrough |
| **Insertions** | Red text (#CC0000) with underline |
| **Unchanged** | Normal text |

**Implementation:**
- Uses `difflib.SequenceMatcher` for word-level diffing
- Words split by whitespace for readable diffs
- Applied to both TM Source and TM Target compare boxes
- Matches professional CAT tool behavior

**Files Modified:**
- `Supervertaler.py` - All bug fixes and Compare Panel enhancement
- `CHANGELOG.md` - Added v1.9.141-145 entries

---

### January 20, 2026 - Context Placeholders & Auto-Center Fix (v1.9.130)

**📝 Three Context Placeholders for QuickMenu**

Split `{{DOCUMENT_CONTEXT}}` into specialized variants:

| Placeholder | Mode | Use Case |
|-------------|------|----------|
| `{{SOURCE+TARGET_CONTEXT}}` | `mode="both"` | Proofreading (needs both to verify) |
| `{{SOURCE_CONTEXT}}` | `mode="source"` | Translation questions (source only) |
| `{{TARGET_CONTEXT}}` | `mode="target"` | Consistency/style analysis |

**Implementation:**
- `_build_quickmenu_document_context(mode)` now accepts "both", "source", or "target"
- `_quickmenu_build_custom_prompt()` detects and handles all three placeholders
- `modules/unified_prompt_manager_qt.py` Placeholders tab updated

**🎯 Auto-Center Active Segment Fix**

Fixed "Keep Active Segment Centered" using Qt's built-in `scrollTo()` with `PositionAtCenter`:

```python
index = self.table.model().index(row, 0)
self.table.scrollTo(index, QAbstractItemView.ScrollHint.PositionAtCenter)
```

- Added `QAbstractItemView` to imports
- Replaced unreliable manual viewport calculations
- Works consistently across all screen sizes

**⌨️ Double-Tap Shift Context Menu (AutoHotkey)**

- `superlookup_hotkey.ahk` → `supervertaler_hotkeys.ahk`
- Added double-tap Shift detection for context menu (Supervertaler window only)
- Uses `Shift+F10` (Qt's native context menu trigger)

**Files Modified:**
- `Supervertaler.py` - Context placeholders, auto-center, AHK references
- `modules/unified_prompt_manager_qt.py` - Placeholders tab
- `modules/shortcut_manager.py` - Double-shift shortcut docs
- `supervertaler_hotkeys.ahk` - Combined hotkey script (renamed)

---

### January 19, 2026 - Prompt System Improvements (v1.9.126)

**🔄 Field Rename: `quickmenu_quickmenu` → `sv_quickmenu`**

Renamed redundant field throughout the codebase for cleaner API:

**What Changed:**
- All internal code now uses `sv_quickmenu` (Supervertaler QuickMenu)
- Updated in both `unified_prompt_library.py` and `unified_prompt_manager_qt.py`
- 18+ occurrences renamed across parsing, saving, display, and toggle methods
- Backward compatibility: Old .svprompt files still load correctly
- Legacy `quick_run` field kept in sync for compatibility

**Files Modified:**
- `modules/unified_prompt_library.py` - Parse, save, toggle methods
- `modules/unified_prompt_manager_qt.py` - Editor, creation, display code
- `Supervertaler.py` - Version bump to 1.9.126
- `CHANGELOG.md` - Added v1.9.126 entry

**📝 Placeholders Reference Tab**

Added dedicated reference tab in Prompt Manager showing all available placeholders:

**Features:**
- Table format: Placeholder | Description | Example
- All 5 placeholders documented:
  * `{{SELECTION}}` - Selected text in grid
  * `{{SOURCE_TEXT}}` - Full source segment
  * `{{SOURCE_LANGUAGE}}` - Project source language
  * `{{TARGET_LANGUAGE}}` - Project target language
  * `{{DOCUMENT_CONTEXT}}` - Project segments (configurable %)
- Usage tips section with best practices
- Located after AI Assistant tab

**Implementation:**
- New `_create_placeholders_tab()` method (~120 lines)
- Added as Tab 3 in Prompt Manager sub-tabs
- Uses QTableWidget with 3 columns and 5 rows
- Monospace font for placeholders and examples
- Adjustable column widths for readability

**Files Modified:**
- `modules/unified_prompt_manager_qt.py` - New tab method, added to sub-tabs

---

### January 19, 2026 - QuickMenu Document Context (v1.9.124)

---

### January 19, 2026 - Prompt Manager UI Fixes (v1.9.127)

**🔧 Save Button Fix**

Fixed issue where Save button remained greyed out after creating new prompts:

- **Problem**: User creates new prompt → editor loads content → Save button stays disabled
- **Root Cause**: `_new_prompt_in_folder()` called `_load_prompt_in_editor()` which should enable button, but timing issue prevented it
- **Solution**: Added explicit `btn_save_prompt.setEnabled(True)` call immediately after loading prompt in editor
- **Result**: Save button now properly enabled for all new prompts

**📝 Label Rename for Clarity**

Renamed QuickMenu checkbox label:
- **Before**: "Show in QuickMenu"
- **After**: "Show in Supervertaler QuickMenu"
- **Reason**: Distinguishes app-level QuickMenu from Grid right-click QuickMenu

**Files Modified:**
- `modules/unified_prompt_manager_qt.py` - Save button enable, checkbox label

---

### January 19, 2026 - Prompt System Improvements (v1.9.126)

**🔄 Field Rename: `quickmenu_quickmenu` → `sv_quickmenu`**

Renamed redundant field throughout the codebase for cleaner API:

**What Changed:**
- All internal code now uses `sv_quickmenu` (Supervertaler QuickMenu)
- Updated in both `unified_prompt_library.py` and `unified_prompt_manager_qt.py`
- 18+ occurrences renamed across parsing, saving, display, and toggle methods
- Backward compatibility: Old .svprompt files still load correctly
- Legacy `quick_run` field kept in sync for compatibility

**Files Modified:**
- `modules/unified_prompt_library.py` - Parse, save, toggle methods
- `modules/unified_prompt_manager_qt.py` - Editor, creation, display code
- `Supervertaler.py` - Version bump to 1.9.126
- `CHANGELOG.md` - Added v1.9.126 entry

**📝 Placeholders Reference Tab**

Added dedicated reference tab in Prompt Manager showing all available placeholders:

**Features:**
- Table format: Placeholder | Description | Example
- All 5 placeholders documented:
  * `{{SELECTION}}` - Selected text in grid
  * `{{SOURCE_TEXT}}` - Full source segment
  * `{{SOURCE_LANGUAGE}}` - Project source language
  * `{{TARGET_LANGUAGE}}` - Project target language
  * `{{DOCUMENT_CONTEXT}}` - Project segments (configurable %)
- Usage tips section with best practices
- Located after AI Assistant tab

**Implementation:**
- New `_create_placeholders_tab()` method (~120 lines)
- Added as Tab 3 in Prompt Manager sub-tabs
- Uses QTableWidget with 3 columns and 5 rows
- Monospace font for placeholders and examples
- Adjustable column widths for readability

**Files Modified:**
- `modules/unified_prompt_manager_qt.py` - New tab method, added to sub-tabs

---

### January 19, 2026 - QuickMenu Document Context (v1.9.124)

**📄 Context-Aware AI Suggestions**

Implemented major enhancement allowing QuickMenu prompts to access full project context for better AI suggestions:

**The Feature:**
- New `{{DOCUMENT_CONTEXT}}` placeholder for QuickMenu prompts
- Configurable percentage slider (0-100%, default 50%) in Settings → AI Settings
- Safety limit: Maximum 100 segments to prevent token overload
- Format: `[ID] source\n    → target\n\n` with header showing segment count/percentage

**Implementation:**
- `_build_quickmenu_document_context()` - Builds formatted segment list
- Enhanced `_quickmenu_build_custom_prompt()` - Replaces placeholder with context
- Settings UI: Horizontal slider with dynamic value label
- Pattern reuse: Adapted from batch translation "surrounding segments" feature

**Example Use Case:**
```
{{DOCUMENT_CONTEXT}}

Suggest the best possible translation of "{{SELECTION}}" from {{SOURCE_LANGUAGE}} to {{TARGET_LANGUAGE}} within the context of the current project shown above.
```

**Benefits:**
- ✅ AI understands project domain and terminology
- ✅ Consistent translations across the document  
- ✅ Better handling of ambiguous terms
- ✅ Context-aware suggestions for specialized fields

**Files Modified:**
- `Supervertaler.py` - New method, enhanced prompt builder, settings UI, save wiring

---

### January 19, 2026 - QuickMenu Generic AI Support (v1.9.123)

**🤖 Fixed QuickMenu Translation Mode Lock**

Fixed critical bug where QuickMenu prompts were being forced into translation mode:

**The Problem:**
- QuickMenu was calling `client.translate(text=input_text, ...)` which forced translation behavior
- Generic prompts like "Explain this", "Define the selection" would fail
- The AI would translate the prompt itself instead of executing it

**The Fix:**
- Changed to use generic AI completion: `client.translate(text="", custom_prompt=...)`
- Simplified prompt builder - removed translation-specific wrappers
- QuickMenu now supports ANY AI task (explain, define, suggest, analyze)

**Placeholders Available:**
- `{{SELECTION}}` - Selected text
- `{{SOURCE_TEXT}}` - Full source segment
- `{{SOURCE_LANGUAGE}}` - Project source language
- `{{TARGET_LANGUAGE}}` - Project target language
- `{{DOCUMENT_CONTEXT}}` - Full project context (v1.9.124)

**Files Modified:**
- `Supervertaler.py` - `run_grid_quickmenu_prompt()`, `_quickmenu_build_custom_prompt()`

---

### January 19, 2026 - Ctrl+N for Quick Notes (v1.9.122)

**⌨️ Shortcut Repurposed for Note-Taking**

Repurposed Ctrl+N from "New Project" (rarely used) to "Focus Segment Note tab":

**The Feature:**
- Press Ctrl+N to instantly jump to Segment Note tab
- Cursor placed in notes field, ready to type
- Perfect for quick proofreading notes, context reminders, translation decisions

**Implementation:**
- `modules/shortcut_manager.py` - Changed `file_new` default to "" (empty), added `editor_focus_notes` with Ctrl+N
- `Supervertaler.py` - New `focus_segment_notes()` method switches to tab index 1, focuses `bottom_notes_edit`

---

### January 19, 2026 - API Key Loading System Unified (v1.9.113)

**🔐 Unified API Key Loading with Dev-First Priority**

Consolidated the confusing multi-path API key loading system into a single, clear dual-path approach:

**The Problem:**
- Three different API key file locations existed (root, user_data, user_data_private)
- Two different loading mechanisms (`Supervertaler.load_api_keys()` vs `llm_clients.load_api_keys()`)
- Conflicting instructions in example files
- AI Assistant bug (#107): Keys worked for translation but failed for AI Assistant

**The Solution:**
- **Unified loading in main app**: `load_api_keys()` now checks TWO locations with clear priority
  1. `user_data_private/api_keys.txt` (Dev mode - gitignored, never uploaded to GitHub)
  2. `user_data/api_keys.txt` (User mode - ships with app)
- **AI Assistant fixed**: Now uses `parent_app.load_api_keys()` instead of module function
- **Example files updated**: Both example files now give consistent, clear instructions

**Developer Workflow:**
- Store keys in `user_data_private/api_keys.txt`
- Fully gitignored - safe from accidental commits
- All features find keys here (translation, AI Assistant, tests)

**User Workflow:**
- Keys go in `user_data/api_keys.txt`
- App auto-creates this location on first run
- Simple, single location

**Files Modified:**
- `Supervertaler.py` - `load_api_keys()` method now checks dev path first (line ~39407)
- `api_keys.example.txt` - Updated with dev/user instructions
- `user_data/api_keys.example.txt` - Updated with dev/user instructions
- `AGENTS.md` - Updated API Keys section with new dual-path documentation

**Result:**
- ✅ Developers: Keys safe in gitignored location
- ✅ Users: Simple single location
- ✅ AI Assistant: Now works with same keys as translation
- ✅ No more confusion about where to put keys

---

### January 19, 2026 - Version 1.9.112: Critical Bug Fixes

**🐛 Filter Pagination Bug Fixed**

Fixed critical bug where Filter Source/Target boxes only searched visible page instead of all segments:

- **The Problem**: When pagination was active (e.g., "50 per page"), filtering only searched through the currently visible rows in the table
- **Root Cause**: `apply_filters()` used `self.table.rowCount()` which could be limited by pagination state or previous filtering
- **The Fix**: Changed to `len(segments)` to always iterate through ALL segments in the project
- **User Impact**: Filtering now finds matches across the entire project regardless of which page you're viewing

**Technical Details:**
- Changed iteration from `for row in range(row_count)` where `row_count = self.table.rowCount()`
- To: `for row in range(total_segments)` where `total_segments = len(segments)`
- The filter builds a complete `matching_rows` set, then `_apply_pagination_to_grid()` handles combined visibility

**📝 Bilingual Table Export - Notes Column**

Fixed segment notes not being exported to Supervertaler Bilingual Table DOCX files:

- **The Problem**: Notes column was hardcoded to empty string: `cells[4].text = ''`
- **The Fix**: Now properly exports `seg.notes` from each segment
- **Formatting**: 8pt font to match Status column styling
- **Includes**: Proofreading notes (⚠️ PROOFREAD prefix), user notes, all segment annotations

**📏 Grid Column Width Optimization**

Reduced segment ID column width for more compact display:

- **Before**: 55px (unnecessarily wide even for 4-digit segment numbers)
- **After**: 40px (fits up to 3 digits comfortably, readable for 4+ digits)
- **Benefit**: More horizontal space available for Source/Target columns

**Files Modified:**
- `Supervertaler.py` - Fixed `apply_filters()` iteration logic, notes export in `_export_review_table()`, column width in grid initialization

---

### January 18, 2026 - TMX Language Pair Bug Fix (User Issue #105) - v1.9.109

**🔧 Fixed Critical TMX Import Language Reversal Bug**

**Issue ([#105](https://github.com/michaelbeijer/Supervertaler/issues/105)):** User reported that EN-GB → DE-DE TMX files were being imported as DE-DE → EN-GB, making it impossible to find matches for translated segments.

**Root Cause:**
- TMX import code incorrectly assumed the FIRST language in the TMX file was the source language and the SECOND was the target
- TMX files list languages in arbitrary order (often alphabetically), so this assumption was wrong
- Example: A file with languages listed as [de-DE, en-GB] would be imported as DE-DE → EN-GB even if the user wanted EN-GB → DE-DE

**Fix Implemented:**
- Added language pair selection dialog when importing TMX files
- User now explicitly selects which detected language should be source and which should be target
- Prevents accidental language reversal regardless of TMX file language order
- Applied to both "Create new TM from TMX" and "Add to existing TM" workflows

**User Workflow:**
1. Import TMX file via TM Manager
2. Dialog shows all detected languages (e.g., "de-DE, en-GB")
3. User selects: Source = en-GB, Target = de-DE
4. Import proceeds with correct language pair
5. TM matches now work correctly

**Implementation Details:**
- Added language selection dialog with two dropdowns (Source/Target)
- Validation ensures source ≠ target
- Dialog appears in two locations in `_import_tmx_as_tm()`:
  - When creating new TM from TMX (line ~12852)
  - When adding to existing TM with no languages set (line ~12957)

**Files Modified:**
- `Supervertaler.py` - Added language selection dialog in `_import_tmx_as_tm()` method (~110 lines added)
- `CHANGELOG.md` - Added v1.9.109 entry
- `README.md` - Version updated to v1.9.109

**GitHub:**
- Issue: https://github.com/michaelbeijer/Supervertaler/issues/105
- Response: `GitHub_Issue_105_Response.md`

---

### January 18, 2026 - memoQ XLIFF Import/Export Support (User Issue #106) - v1.9.108

**📥📤 Complete memoQ XLIFF (.mqxliff) Workflow**

Added full import/export support for memoQ XLIFF files - feature was implemented in module but never exposed in UI:

**User Issue:**
- User reported inability to import memoQ XLIFF files
- Slovak language support question (already supported but needed clarification)
- Handler module (`modules/mqxliff_handler.py`) existed but no menu items
- memoQ bilingual DOCX import had limited language detection (only 8 languages)

**Implementation:**

1. **Import Menu Item**: File → Import → memoQ XLIFF (.mqxliff)...
   - Opens file dialog for `.mqxliff` files
   - Automatically extracts source segments using `MQXLIFFHandler`
   - Converts ISO language codes to full names (`sk` → `Slovak`)
   - Stores handler and source path for round-trip export

2. **Export Menu Item**: File → Export → memoQ XLIFF - Translated (.mqxliff)...
   - Updates target segments in original XLIFF structure
   - Preserves formatting tags (bpt/ept pairs)
   - Saves translated file with proper namespace handling

3. **Language Code Normalization**:
   - New `_normalize_language_code()` method
   - Converts ISO 639-1/639-2 codes to full language names
   - Supports 30+ languages including Slovak (`sk`, `sk-SK`)

4. **memoQ Bilingual DOCX Language Detection**:
   - Expanded `lang_map` in `import_memoq_bilingual()` from 8 to 24 languages
   - Now includes Slovak, Czech, Hungarian, Romanian, Bulgarian, Greek, Russian, Ukrainian, Swedish, Danish, Finnish, Norwegian, Japanese, Chinese, Korean, Arabic, Turkish, Hebrew
   - Fixes bug where Slovak would default to EN→NL instead of being detected

5. **Project Persistence**:
   - Added `mqxliff_source_path` field to `Project` dataclass
   - Source path saved in `.svproj` files
   - Automatic handler restoration when loading projects

**Methods Added:**
- `import_memoq_xliff()` - Import XLIFF files (~90 lines)
- `export_memoq_xliff()` - Export with translations (~120 lines)  
- `_normalize_language_code()` - ISO code → full name converter (~60 lines)

**Round-Trip Workflow:**
1. Export from memoQ as XLIFF
2. Import into Supervertaler
3. Translate segments
4. Export back to XLIFF
5. Import into memoQ

**Files Modified:**
- `Supervertaler.py` - Import/export menu items, methods, language normalization
- `Supervertaler.py` - Project dataclass: added `mqxliff_source_path` field
- `Supervertaler.py` - Project save/load: persist mqxliff_source_path

**GitHub Discussion:**
- https://github.com/michaelbeijer/Supervertaler/discussions/106

---

### January 15, 2026 - Version 1.9.107: Prompt Library & Superlookup Fixes

**🔧 Prompt Library Improvements**

Unified filename and Name field throughout the prompt library:
- **Tree Display**: Now shows full filename with `.svprompt` extension (e.g., "prompt.svprompt")
- **Editor Name Field**: Shows full filename including extension (was previously metadata-only)
- **File Operations**: Name field now represents the actual filename - editing it renames the file on disk
- **New Prompt Dialog**: Asks for "filename with extension" and auto-appends `.svprompt` if missing
- **Result**: One unified concept where filename = what you see = what you edit everywhere

**Files Modified:**
- `modules/unified_prompt_manager_qt.py` - Tree display, editor field, save logic, new prompt dialog

**🔍 Superlookup Navigation Fixes**

Fixed two critical navigation bugs after Supermemory removal:

1. **Ctrl+K AttributeError Fixed**:
   - Removed orphaned Supermemory code from SuperlookupTab
   - `search_supermemory()` now gracefully returns 0 instead of trying to access removed engine
   - Removed unused methods: `create_supermemory_results_tab()`, `init_supermemory()`, `on_supermemory_result_double_click()`, `copy_selected_supermemory_target()`
   - ~140 lines of dead code removed

2. **Ctrl+K Tab Navigation Fixed**:
   - Updated `_go_to_superlookup()` to use correct tab index
   - After Prompt Manager tab was added, indices shifted: Tools moved from index 2 → 3
   - Ctrl+K was opening Prompt Manager instead of Superlookup
   - Now correctly navigates to Tools tab (index 3)

**Tab Order:**
- 0 = Grid
- 1 = Resources
- 2 = Prompt Manager
- 3 = Tools (Superlookup is here)
- 4 = Settings

**Files Modified:**
- `Supervertaler.py` - Removed Supermemory code, fixed tab navigation

---

### January 15, 2026 - 🗑️ Supermemory Removed (v1.9.105)

**Strategic Refactoring: Remove Supermemory Entirely**

After extensive attempts to package Supermemory (vector-indexed semantic search) in Windows EXE builds, made the decision to remove it entirely from the project:

**Problems Encountered:**
- PyTorch/sentence-transformers has complex native dependencies (CUDA libs, Intel MKL, OpenMP, etc.)
- Multiple Windows DLL loading failures (`vcomp142.dll`, `c10.dll`, etc.) even after comprehensive packaging
- 7+ packaging iterations failed to produce a working frozen build
- ~600 MB footprint for a feature that didn't work reliably

**Strategic Decision:**
- Focus development effort on the **SQLite-based Translation Memory** system instead
- SQLite TM is:
  - Faster and more reliable for professional translation workflows
  - Works perfectly in frozen builds
  - Easier to maintain and improve
  - Better suited for large TMX imports (thousands of entries)

**Removed:**
- `modules/supermemory.py` (2100+ lines deleted)
- Supermemory tab from Resources
- Auto-init and cleanup code in main application
- Dependencies: `sentence-transformers`, `chromadb`, `tokenizers`
- Pip extra: `supervertaler[supermemory]`
- Feature manager entry
- Build spec references

**Files Modified:**
- `Supervertaler.py` - Removed create_supermemory_tab(), _auto_init_supermemory(), _cleanup_supermemory(), UI tab
- `modules/feature_manager.py` - Removed supermemory from FEATURE_MODULES
- `pyproject.toml` - Removed supermemory extra and heavy dependencies
- `Supervertaler.core.spec` / `Supervertaler.full.spec` - Updated comments (FULL now just for Local Whisper)
- `CHANGELOG.md` - Documented removal in v1.9.105

**Result:**
- Cleaner codebase
- ~600 MB smaller default installation
- Focus on what works: SQLite TM, LLMs, termbases, voice commands
- No more Windows EXE packaging headaches with PyTorch

---

### January 18, 2026 - Version 1.9.111: Clean Slate Project Imports

**🔒 Automatic Resource Deactivation on New Project Import**

Implemented automatic deactivation of all resources (TMs, glossaries, NT lists) when importing new projects:

**The Problem:**
- When importing a new project, all previously activated resources remained active
- Users could end up with dozens of unrelated TMs/glossaries active across projects
- No clean separation between project contexts
- Difficult to tell which resources were actually relevant to current project

**The Solution:**
- Added `_deactivate_all_resources_for_new_project()` method
- Automatically called after import in all 5 handlers: DOCX, TXT, memoQ, CafeTran, Trados
- Deactivates all TMs via `tm_metadata_mgr.deactivate_tm()`
- Deactivates all glossaries via `termbase_mgr.deactivate_termbase()`
- Deactivates all NT lists via `nt_manager.set_list_active(False)`

**User Workflow:**
1. Import new project → All resources automatically deactivated
2. Go to Project Resources tab → Activate only needed TMs/glossaries
3. Work on project with clean, relevant resource set
4. Import next project → Clean slate again

**Benefits:**
- ✅ Fresh start for every project
- ✅ Prevents unintended resource pollution
- ✅ Users explicitly choose what's relevant
- ✅ Clearer project context separation
- ✅ Consistent behavior across all import types

**Files Modified:**
- `Supervertaler.py` - Added `_deactivate_all_resources_for_new_project()`, called in 5 import handlers

---

### January 15, 2026 - 🏗️ Windows EXE: CORE + FULL release pipeline (v1.9.104)

- Added/used dual build flavors: CORE (no heavy ML stack) and FULL (bundles Supermemory + heavy deps).
- Important runtime rule (PyInstaller one-folder): users must run `Supervertaler.exe` from the extracted folder next to `_internal/` (do not move the EXE).
- FULL launch crash mitigation notes: avoid importing heavy deps during startup/feature detection; disable UPX for FULL; exclude problematic `VCOMP140.DLL` from the bundle when it causes `0xc0000409` startup crashes.
- Supermemory-in-FULL packaging note: do not exclude `torch.cuda` Python modules (CPU use can still touch those imports); keep `triton` excluded if needed.
- **Critical:** Do NOT exclude `unittest` - it's a standard library module needed by sentence-transformers/tokenizers. The spec initially had it in excludes list which caused "No module named 'unittest'" error.
- **Critical:** Add `tiktoken` to the `collect_submodules()` package list - sentence-transformers needs `tiktoken140.dll` which won't be bundled otherwise.
- **Critical:** Use `collect_dynamic_libs()` for packages with native extensions - added explicit DLL collection for `tokenizers`, `safetensors`, and `torch` to ensure all `.dll`/`.pyd` files are bundled (sentence-transformers depends on native code from all three).
- **Critical:** Use `collect_data_files("torch")` to bundle ALL torch lib files, not just DLLs - PyTorch has complex directory structure with many dependent files.
- **Exit crash fix:** Added `_cleanup_supermemory()` method in closeEvent to explicitly shut down ChromaDB client and clear PyTorch references before exit, preventing "Python has stopped working" crash on Windows.
- Artifact hygiene: keep only the two intended release zips in `dist/` (`Supervertaler-v1.9.104-Windows-CORE.zip` + `...-FULL.zip`) to avoid uploading/testing stale builds.

### January 14, 2026 - 📦 Packaging: Lighter Default Install (v1.9.104)

- Made Supermemory an optional install extra again so `pip install supervertaler` no longer pulls the heavy ML stack by default.
- Install on demand with `pip install supervertaler[supermemory]`.

### January 14, 2026 - ✅ Filtered Ctrl+Enter + Website Screenshots (v1.9.103)

- Fixed Ctrl+Enter under active Filter Source/Target: confirm + advance stays within the filtered set (no more grid “unfiltering” while the filter text remains).
- Website: added new screenshots for Compare Panel + Termview and updated the Prompt Manager screenshot.

### January 14, 2026 - ⚡ QuickMenu (Prompt actions in Grid)

- Renamed main tab label: "📝 Project editor" → "📝 Grid"
- Introduced "QuickMenu" prompt metadata (replacing "Quick run menu" terminology):
  - `quickmenu_label` (menu display label)
  - `quickmenu_grid` (show in Grid right-click QuickMenu)
  - `quickmenu_quickmenu` (show in future app-level QuickMenu; legacy-synced with `quick_run`)
- Prompt Manager UI now exposes QuickMenu label + both inclusion toggles
- Grid right-click menus (Source + Target) now include a "⚡ QuickMenu" submenu:
  - Run selected prompt and show response dialog
  - Run selected prompt and replace selection/target

### January 13, 2026 - 📝 Update Checker Investigation (Work in Progress)

**Goal:** Add a Help → “🔄 Check for Updates…” action that tells users whether they’re on the latest release.

**Implementation Attempt (PyQt6/QtNetwork):**
- Implemented an async update-check flow against GitHub:
  - API: `https://api.github.com/repos/michaelbeijer/Supervertaler/releases/latest`
  - Fallback: `https://github.com/michaelbeijer/Supervertaler/releases/latest`
- Hardened against common Qt pitfalls:
  - Avoided `QProgressDialog` auto-close/auto-reset surprises
  - Added request-id guarding to ignore stale replies
  - Prevented double-cleanup (double `finish()` calls)
  - Added logging for network/SSL errors

**What we observed on the developer machine:**
- QtNetwork consistently returns `Unknown error` (no usable error string) for both API and fallback URLs.
- The dialog could hang far longer than intended due to overlapping timeout/fallback paths.
- This appears to be an environment-dependent Qt SSL/TLS backend issue (Windows).

**Temporary Decision (to avoid UX pain):**
- `Help → Check for Updates…` currently just opens the GitHub Releases page:
  - `https://github.com/michaelbeijer/Supervertaler/releases/latest`
- This avoids hangs/crashes while we revisit a robust implementation later.

**Future direction (when revisiting):**
- Prefer a Python HTTPS-based check (`urllib`/`requests`) in a worker thread, or a tiny lightweight update endpoint.
- If keeping QtNetwork, validate Qt SSL backend availability and provide clear guidance when SSL is missing.

### January 13, 2026 - 🌐 New Website Planning: `michaelbeijer.co.uk` (NEW repo)

**Context / Goal:**
Build a new professional personal website for Michael Beijer (Dutch/English patent + technical translator & terminologist). Current site is MediaWiki-based at `https://michaelbeijer.co.uk/`; the goal is to replace it with a modern static site once complete.

**Brand / Domain strategy (agreed):**
- Keep the *personal* brand on `michaelbeijer.co.uk` (and keep email on that domain: `info@michaelbeijer.co.uk`).
- Keep product/project brands on their own domains:
  - `https://supervertaler.com` (CAT tool)
  - `https://beijerterm.com` (open-source multilingual terminology database)
- Optional: `beijer.uk` can exist as a vanity domain and 301-redirect to `michaelbeijer.co.uk` (recommended rather than migrating the main domain).

**Aesthetic / Inspiration:**
- The user wants a crisp, black-and-white, content-first aesthetic similar to Pagefind docs:
  - Reference: `https://pagefind.app/docs/multilingual/`
- Strongly avoid garish colors; typography + whitespace + hairline borders.

**Key identity & contact details (provided by user):**
- Michael Beijer — Dutch/English translator & terminologist — Hastings, United Kingdom
- Tel: `+44 7475 771720`
- Email: `info@michaelbeijer.co.uk`
- Websites:
  - Main: `michaelbeijer.co.uk`
  - Terminology DB: `beijerterm.com`
  - CAT tool: `supervertaler.com`
- Profiles:
  - ProZ: profile + testimonials source (Feedback Card): `https://www.proz.com/feedback-card/652138`
  - LinkedIn: `michaelbeijer`

**Single-page vs multi-page decision:**
- Recommended: a minimal multi-page site (still “docs-like” and simple), because Michael has multiple distinct offerings (patents/translation, copywriting, CAT consulting) + products (Supervertaler, Beijerterm).

**Information Architecture (proposed):**
- Home (positioning + proof + CTA)
- Patents (primary specialization: process, QA, confidentiality, what clients should send)
- Services (technical translation, editing/proofreading, copywriting, CAT/terminology consulting)
- Work (case studies)
- Testimonials (ProZ + selected quotes)
- Tools (side projects): Supervertaler, Beijerterm
- Blog (wanted; current blog exists at `https://michaelbeijer.co.uk/blog`)
- Contact (email-first CTA)

**CTA (agreed):**
- Primary CTA is email (not booking link): “Email me” with a short checklist (word count, deadline, source format, subject/domain).

**Case studies + testimonials: how to combine (agreed approach):**
- Use “Proof” as an umbrella concept:
  - *Case studies* = structured “problem → approach → outcome” writeups.
  - *Testimonials* = short curated quotes (primarily from ProZ) + link back to ProZ.
- Patents often involve NDAs; case studies should generally be anonymized:
  - No client names/logos unless explicit permission.
  - Avoid application/publication identifiers unless already public and acceptable.
  - Keep focus on domain, constraints, workflow, QA strategy, measurable outcomes.

**ProZ testimonials handling (important):**
- Do NOT auto-scrape ProZ.
- Curate a small selection manually (short excerpts) and include a prominent link to the ProZ feedback card.
- Store testimonials as local data (YAML/JSON) so they can be reused on Home + Testimonials pages.

**Recommended tech stack for the new repo:**
- Astro (static site generation, component-based)
- Tailwind CSS (consistent type/spacing, minimal custom CSS)
- Markdown/MDX for Blog + Case studies
- Optional later: Pagefind for fully static site search (fits the desired “docs” vibe)

**Repo plan:**
- New GitHub repo name: `michaelbeijer.co.uk`.
- During development, the site can be “parked” locally/in a separate folder; once finished, point `michaelbeijer.co.uk` DNS to GitHub Pages (or another static host).
- Prefer keeping this separate from the Supervertaler repo and separate from the `beijerterm/` submodule.

**Design rules-of-thumb (to match the desired vibe):**
- Grayscale palette; at most one subtle accent for links.
- Narrow reading column (target ~70–80 characters) + generous whitespace.
- Hairline borders instead of heavy cards/shadows.
- Minimal nav, fast scanning; let headings + spacing do the work.

**Open questions (next agent can confirm if needed):**
- Initial blog migration: import which posts from the current MediaWiki blog, and in what format (manual copy vs export).
- Whether any named clients/published patents can be referenced explicitly (if yes, add a “Selected clients / published work” section).

### January 13, 2026 - ✅ FIXED: Ctrl+Return Not Working in Source Cell

**Issue:** Ctrl+Enter (main keyboard Return key) does not trigger `confirm_selected_or_next()` when cursor is in source cell (`ReadOnlyGridTextEditor`).

**Key Finding:** Ctrl+Enter on **numpad** (Key_Enter) WORKS, but main keyboard Return (Key_Return) does NOT.

**What We Observed:**
1. ✅ Global QShortcut IS registered: `key=Ctrl+Enter, enabled=True, context=ApplicationShortcut`
2. ❌ Widget's `keyPressEvent()` is NEVER called for main keyboard Return
3. ❌ Widget's `event()` override is NEVER called for main keyboard Return
4. ❌ Debug print statements produce NO output when pressing Ctrl+Return

**Likely Root Cause:**
On Windows/Qt, `Ctrl+Return` (Key_Return) can be swallowed before it reaches the cell widget, and the `QShortcut(QKeySequence("Ctrl+Return"))` path appears to effectively only catch numpad Enter (Key_Enter) in this scenario.

**Suspected Areas:**
- QTableWidget default key handling (line 18352: `setEditTriggers(DoubleClicked)`)
- Possible event filter on table or viewport
- Qt's internal focus/key event routing for QTextEdit inside QTableWidget cells
- Possible conflict with recent "Auto Resize Rows" feature

**Fix Implemented:**
- Added an application-level event filter that catches `Ctrl+Return` and `Ctrl+Enter` *before* Qt/table routing can swallow it, but only when focus is inside the grid.
- The filter calls `confirm_selected_or_next()` and returns `True` to stop further handling.
- Expanded the same handling so it also works when focus is in the **Filter Source** / **Filter Target** boxes.

**Implementation Notes:**
- `Supervertaler.py`: new `_CtrlReturnEventFilter(QObject)` near the grid editor classes.
- `Supervertaler.py`: installed via `QApplication.instance().installEventFilter(...)` in `setup_global_shortcuts()`.
- Kept `QShortcut` binding for `editor_save_and_next`, but the event filter ensures main-keyboard Return also works.

**Workaround (no longer needed):** Previously: use numpad Enter key instead of main keyboard Return.

---

### January 12, 2026 - Version 1.9.99: Compare Panel Shortcuts + Sound Effects

- **Compare Panel quick insert**: Added `Alt+0` (MT) and `Alt+0,0` (TM Target) insertion; replaces entire target segment in one undo step.
- **Compare Panel navigation**: Added `Ctrl+Alt+Left/Right` for MT and `Ctrl+Alt+Up/Down` for TM match navigation.
- **Context-aware shortcuts**: Match navigation/insertion now respects active panel (Compare Panel vs Translation Results).
- **Minimalist sound effects**: Per-event Windows sound mapping (beeps or Windows `.wav`) with sound effects OFF by default.
- **Glossary add feedback**: Status-bar “information bar” messages for add/duplicate/error outcomes.
- **Less TM log spam**: Collapsed repeated “Saved segment to TM(s)” messages into a single debounced `(xN)` log line.

### January 11, 2026 - Docs: Contributing Guide & Code of Conduct

- Added `CONTRIBUTING.md` with guidance for bug reports, feature requests, PRs, dev setup, and coding standards
- Added `CODE_OF_CONDUCT.md` using Contributor Covenant v2.1 (with required CC BY attribution)
- Updated `README.md` to link the new docs and clarify MIT vs CC BY scope

### January 11, 2026 - Version 1.9.98: Glossary Notes in Tooltips

**📝 Fixed Glossary Entry Notes Not Appearing in Tooltips**

Fixed bug where glossary entry notes were not appearing in tooltips despite being saved correctly to the database.

**The Problem:**
- Notes were saved correctly to `termbase_terms.notes` database column
- When converting termbase matches from dict to list format for display, `notes` field was dropped in 5 places
- TermView and source cell tooltips never received notes data

**The Fix:**
Fixed 5 locations where glossary notes were being lost:
1. Cached termbase matches conversion (~lines 26753-26768)
2. Fresh termbase matches conversion (~lines 26835-26850)
3. Refresh current segment conversion (~lines 30420-30438)
4. TranslationMatch metadata (~lines 30469-30485)

**Also in this release:**
- **WebEngineView cleanup**: Fixed "Release of profile requested" terminal warnings
- **FAQ update**: Added embedded browser password/cookie security documentation

**Files Modified:**
- `Supervertaler.py` - Fixed notes field in 4 dict-to-list conversions + 1 TranslationMatch metadata
- `docs/superdocs/reference/faq.md` - Added FAQ about embedded browser security

---

### January 11, 2026 - Version 1.9.97: All MT Providers in Translation Results

**🌐 Multiple Machine Translation Providers Now Displayed**

The Translation Results panel now shows translations from **all configured MT providers**, not just Google Translate.

**Previously:**
- Only Google Translate was called when navigating to a segment
- DeepL, Amazon Translate, and MyMemory were only available in Batch Translate

**Now:**
- All enabled MT providers are called and displayed progressively
- Each provider's translation appears as it completes
- Provider codes: GT (Google), DL (DeepL), AT (Amazon), MM (MyMemory)

**Supported Providers:**
| Provider | Key Name | Notes |
|----------|----------|-------|
| Google Translate | `google_translate` | Requires API key |
| DeepL | `deepl` | Requires API key |
| Amazon Translate | `amazon_translate` + `amazon_translate_secret` | AWS credentials |
| MyMemory | `mymemory` | Free; email as key for higher limits |

**Files Modified:**
- `Supervertaler.py` - Expanded `_add_mt_and_llm_matches_progressive()` to call all MT providers

---

### January 11, 2026 - Version 1.9.96: Thread-Safe Logging

**🛡️ Fixed Crash When Adding Terms via Alt+Down**

Fixed critical crash caused by Qt threading violation when background workers called the `log()` method.

**The Problem:**
- `log()` method was called from background threads (termbase batch processor)
- Qt widgets (`status_bar`, `session_log_text`) were being accessed from non-main threads
- This caused: `QObject::killTimer: Timers cannot be stopped from another thread`

**The Fix:**
- Added `_log_signal = pyqtSignal(str)` to `SupervertalerQt` class
- Background threads now emit signal instead of directly updating UI
- Signal automatically queues to main thread's event loop
- New `_log_to_ui()` internal method handles actual widget updates

**Files Modified:**
- `Supervertaler.py` - Added `_log_signal`, `_log_to_ui()`, made `log()` thread-safe

---

### January 11, 2026 - Version 1.9.95: TM Fuzzy Matching Fix

**🔍 Improved Translation Memory Fuzzy Matching for Long Segments**

Fixed critical issue where highly similar TM entries were not being found for long segments (especially in patent/technical documents).

**The Problem:**
- FTS5 full-text search uses BM25 ranking which prioritizes entries matching MORE search terms
- For long segments with many technical compound words, BM25 pushed truly similar entries below the candidate limit
- Example: Two sentences 92% similar weren't matching because other entries matched more individual words

**The Fix:**
- Increased FTS5 candidate pool from 100 to 500 entries
- Changed `max(50, max_results * 10)` to `max(500, max_results * 50)` in `search_fuzzy_matches()`

**Technical Details:**
- FTS5 BM25 is great for keyword relevance but needs a larger pool for similarity-based reranking
- SequenceMatcher then correctly scores the candidates by actual text similarity
- More candidates = better chance of finding truly similar matches

**Files Modified:**
- `modules/database_manager.py` - `search_fuzzy_matches()` candidate limit increase

---

### January 11, 2026 - Version 1.9.94: TermView Quick-Insert Shortcuts

**🎯 TermView Quick-Insert Shortcuts**

**Note (updated in v1.9.99):** `Alt+0` / `Alt+0,0` are reserved for the Compare Panel. TermView shortcuts start at `Alt+1`.

Implemented a novel 20-term quick-insert system using Alt key shortcuts — a feature unique to Supervertaler:

- **Alt+1 through Alt+9**: Insert terms 1-9 instantly (no delay)
- **Double-tap Alt+N,N**: Insert terms 10-18 (displayed as 11, 22, ..., 99)
- **Smart double-tap detection**: First tap inserts immediately; if same key pressed within 300ms, undoes and inserts the double-digit term
- **Visual badges**: Blue circular badges (14px for single digit, 20px for double) show shortcut numbers

**Badge Mapping:**
| Badge | Shortcut | Internal Index |
|-------|----------|----------------|
| 1-9 | Alt+1 to Alt+9 | 0-8 |
| 11, 22, ..., 99 | Alt+1,1 to Alt+9,9 | 9-17 |

**Visual Improvements:**
- Background color now extends across entire term block (text + badge unified)
- Hover effect applies to whole container
- Rounded corners (3px border-radius) on term blocks
- Tooltips show exact shortcut instructions

**Implementation Details:**

*modules/termview_widget.py:*
- `TermBlock.__init__()`: Accepts `shortcut_number` parameter (0-19)
- `TermBlock.init_ui()`: Creates badge with dynamic width and proper styling
- `update_with_matches()`: Assigns shortcut numbers 0-19 to first 20 unique terms
- `insert_term_by_number()`: Inserts term by internal index, logs with badge text
- `shortcut_terms` dict: Maps internal index to target text

*Supervertaler.py:*
- `_termview_last_key` / `_termview_last_time`: Track double-tap state
- `_handle_termview_shortcut()`: Double-tap detection with undo + replace logic
- `_get_current_target_widget()`: Helper to get current target cell for undo
- `insert_termview_term_by_number()`: Delegates to TermView widget

*modules/shortcut_manager.py:*
- Added `termview_insert_0` through `termview_insert_9` definitions
- Category: "TermView Insertion"
- Descriptions explain double-tap behavior

**Files Modified:**
- `modules/termview_widget.py` - Badge display, shortcut tracking, insertion logic
- `Supervertaler.py` - Double-tap handler, shortcuts setup
- `modules/shortcut_manager.py` - Shortcut definitions for Alt+0-9

---

### January 11, 2026 - Version 1.9.93: Keyboard Shortcuts & Quick Glossary Add

**⚡ Quick Add to Priority Glossary**

- **Alt+Shift+Up**: Add selected term pair to glossary with Priority #1
- **Alt+Shift+Down**: Add selected term pair to glossary with Priority #2
- Uses database `termbase_activation` table for priority lookup
- No dialog required — instant term addition

**🔧 Shortcut Enable/Disable Feature**

- New "Enabled" checkbox column in Settings → Keyboard Shortcuts
- Disabled shortcuts fully release their key combinations
- Settings persist between sessions

**Bug Fixes:**
- Fixed Ctrl+Enter not working in target editor cells
- Fixed "Save & Next" button not confirming segments
- Renamed button to "✓ Confirm & Next"

---

### January 9, 2026 - Version 1.9.87: Auto-Confirm & Tab Layout

**⚡ Auto-Confirm 100% TM Matches Feature**

Implemented intelligent auto-confirmation system for perfect TM matches during Ctrl+Enter navigation:

- **Core Feature**: Automatically inserts, confirms, and skips segments with 100% TM matches
- **Recursive Logic**: Continues processing multiple consecutive 100% matches until finding segment needing manual work
- **Safety Check**: Only auto-confirms segments with empty targets (won't overwrite existing translations)
- **Hash-Based Lookup**: Uses `get_exact_match()` for instant O(1) MD5 hash-based matching
- **TM Integration**: Auto-confirmed segments automatically saved to activated Translation Memories
- **Pagination Handling**: Correctly switches pages when auto-skipping across page boundaries

**Implementation Journey** (5 iterations):
1. Initial implementation with fuzzy search
2. Fixed AttributeError: get_activated_tms() doesn't exist → use tm_settings
3. Fixed TypeError: limit parameter → changed to max_results
4. Switched from fuzzy to exact match (fuzzy returned 0 for 100% matches)
5. Added empty target check for safety

**Code Locations:**
- `Supervertaler.py` line 4747: Instance variable initialization
- `Supervertaler.py` lines 13468-13477: UI checkbox in General Settings
- `Supervertaler.py` lines 16243-16245: Save/load settings
- `Supervertaler.py` lines 31250-31438: Complete navigation logic with recursion

**📐 Tab Layout Customization Feature**

Added optional setting to move Termview and Session Log tabs above or below the grid:

- **New Setting**: "Show Termview/Session Log tabs above grid" checkbox in View Settings → Tab Layout
- **Persistence**: Setting saved to general_settings.json and restored on app start  
- **Layout Logic**: Conditional widget ordering in `create_main_layout()` based on `self.tabs_above_grid` flag
- **Splitter Sizes**: Adjusted proportions for both layouts (200/600 for tabs above, 600/200 for tabs below)

**Code Locations:**
- `Supervertaler.py` line 4751: Instance variable `self.tabs_above_grid`
- `Supervertaler.py` lines 14287-14306: UI checkbox in View Settings
- `Supervertaler.py` lines 16243-16245, 24693-24694: Save/load
- `Supervertaler.py` lines 17016-17027: Conditional layout creation

**🎨 UI Polish & Bug Fixes**

- **Segment Column Width**: Increased from 35px to 55px (fits 4-digit segment numbers)
- **Auto-Center Persistence**: Fixed "Keep Active Segment Centered" not saving between sessions
- **Badge Text Color**: Changed from black to dark gray (#333333) for better appearance
- **Color Customization**: Added badge text color picker with 8 preset colors
- **Settings Rename**: "View/Display" → "View Settings" for clarity

**Files Modified:**
- `Supervertaler.py` - All implementations above

---

### January 9, 2026 - Version 1.9.89: Critical Bug Fixes

**🔧 Translation Results Zoom Persistence Fix**

Fixed critical bug where Translation Results pane font size settings were not being restored when loading projects:

- **Root Cause**: Method name typo in `load_project()` at line 18492: `set_compare_font_size()` instead of `set_compare_box_font_size()`
- **Impact**: Users complained "zoom settings are constantly being forgotten during a project and across projects"
- **Solution**: Changed method call to correct name `set_compare_box_font_size()`
- **Result**: Font sizes now properly persist across projects and sessions

**🎨 Border Thickness Spinbox Fix**

Fixed Target Cell Focus Border thickness control arrows not appearing:

- **Root Cause**: Complex stylesheet was hiding the spinbox arrow buttons completely
- **Previous State**: Users saw no arrows, couldn't click to adjust border thickness
- **Solution**: 
  - Removed problematic stylesheet that hid buttons
  - Added explicit `setButtonSymbols(QSpinBox.ButtonSymbols.UpDownArrows)`
  - Increased maximum thickness from 5px to 10px
  - Made spinbox wider (90px) for better visibility
- **Result**: Arrows now visible and fully functional

**🌍 Language Pair Memory Fix**

Fixed DOCX import always defaulting to EN→NL instead of remembering user's language pair:

- **User Report**: "Whatever I do before importing a NL-ES table, the language is detected always as EN-NL!!!"
- **Root Cause**: Import dialog hardcoded to `source_combo.setCurrentIndex(0)` (English) and `target_combo.setCurrentIndex(1)` (Dutch)
- **Solution**:
  - Added `last_import_source_lang` and `last_import_target_lang` to general_settings.json
  - Load last used languages from settings on dialog open
  - Fall back to current project languages if available
  - Save selected languages to settings when user clicks Import
- **Result**: Language pair now persists across sessions and imports

**Code Locations:**
- `Supervertaler.py` line 18492: Fixed `set_compare_font_size` → `set_compare_box_font_size`
- `Supervertaler.py` lines 14363-14375: Fixed border thickness spinbox
- `Supervertaler.py` lines 19589-19625: Load last language pair from settings
- `Supervertaler.py` lines 19670-19677: Save language pair to settings

**Files Modified:**
- `Supervertaler.py` - All bug fixes implemented

---

### January 9, 2026 - Version 1.9.86: Glossary Duplicate Prevention & Priority Filtering

**🚫 Duplicate Term Prevention**

Implemented comprehensive duplicate prevention when adding terms to glossaries:

- **Case-Insensitive Check**: Added duplicate detection in `termbase_manager.py` before inserting terms
- **User Feedback**: Clear warning dialog when attempting to add duplicate: "This term already exists in [glossary]. Duplicate terms are not allowed."
- **Graceful Handling**: `add_term()` returns `None` if duplicate found (no exception raised)
- **Database Query**: Uses `LOWER()` SQL function for case-insensitive comparison

**🎯 Priority-Based Duplicate Filtering**

Enhanced glossary match display to show only highest priority match when duplicates exist:

- **Filtering at Source**: `find_termbase_matches_in_source()` filters duplicates before caching
- **Priority Logic**: When same source→target exists in multiple glossaries, keeps only lowest ranking number (highest priority)
- **Comprehensive Coverage**: Filtering applies to grid highlighting, Translation Results panel, TermView, and Superlookup
- **Performance**: Duplicate filtering adds negligible overhead (single pass through matches)

**⚖️ TermView Font Normalization**

Fixed font size inconsistency in TermView widget:

- **Before**: Source text 10pt, target text 8pt (2pt smaller)
- **After**: Both source and target use same font size
- **Benefit**: Improved readability and visual consistency

**Implementation Details:**
- `modules/termbase_manager.py` (lines 620-680): Added duplicate check query before INSERT
- `Supervertaler.py` (lines 27680-27707): Added duplicate filtering logic with seen_pairs dict
- `Supervertaler.py` (lines 38420-38430): Show warning dialog when duplicate detected
- `modules/termview_widget.py` (line 219): Changed target font size from `self.font_size - 2` to `self.font_size`

**Files Modified:**
- `modules/termbase_manager.py` - Duplicate check in `add_term()`
- `Supervertaler.py` - Duplicate filtering in `find_termbase_matches_in_source()`, warning dialog in `show_add_term_dialog()`
- `modules/termview_widget.py` - Font size normalization in `TermBlock.init_ui()`

---

### January 9, 2026 - Bug Fix: QTextCursor Scope Error

**🐛 Fixed Navigation Crash**

Resolved critical UnboundLocalError that occurred during segment navigation (Alt+Up/Alt+Down):

- **Root Cause**: `QTextCursor` imported inside if block but used in else block (classic Python scope error)
- **Solution**: Moved import to top of both `go_to_next_segment()` and `go_to_previous_segment()` methods
- **Impact**: Prevented crashes during normal workflow navigation

**Files Modified:**
- `Supervertaler.py` - Fixed QTextCursor import scope in navigation methods

---

### January 9, 2026 - Beijerterm: Splitpen Image Resize

**🖼️ Image Size Optimization**

Reduced oversized first image on splitpen term page:

- **Before**: Full-width display (~1200px)
- **After**: 300px width using HTML `<img>` tag
- **Conversion**: Changed from Markdown `![Image](url)` to `<img src="url" width="300">`

**Files Modified:**
- `beijerterm/content/terms/splitpen.md` - First image now uses HTML with width attribute

---

### January 7, 2026 - Version 1.9.85: AI Proofreading System

**✅ Intelligent Translation Quality Verification**

Complete proofreading system for AI-powered translation quality checking:

- **Batch Proofreading Feature**: LLM analyzes translations for errors, inconsistencies, and quality issues
  - Processes segments in batches of 20 for efficient API usage
  - Issues stored in Notes field with `⚠️ PROOFREAD:` prefix for easy identification
  - Real-time progress dialog shows statistics during operation
  
- **Results Management**:
  - Proofreading Results dialog shows all segments with issues in a table
  - Double-click any result to navigate directly to that segment
  - Orange highlight on status icons for segments with proofreading notes
  
- **Filter Integration**: New "Has proofreading issues" option in Advanced Filters
  - Quickly isolate segments that need attention
  - Works alongside existing status/text filters
  
- **Clear Operations**:
  - Bulk clear: Remove all proofreading notes from entire project
  - Individual clear: Right-click segment to clear proofreading notes
  
**Access Points:**
- Edit → Batch Operations → ✅ Proofread Translation...
- View → ✅ Proofreading Results...
- Right-click → ✅ Clear Proofreading Notes

**Implementation Details:**
- `Supervertaler.py` (lines ~25732-26131): Proofreading methods
  - `show_proofread_dialog()`: Configuration and execution
  - `_run_proofreading()`: Batch processing with LLM
  - `show_proofreading_results_dialog()`: Results table UI
  - `_clear_all_proofreading_notes()`: Bulk clear operation
- Orange status icon highlighting when `segment.notes` contains proofreading data
- Advanced Filters updated with proofreading checkbox

**Files Modified:**
- `Supervertaler.py` - Proofreading system implementation

---

### January 7, 2026 - Version 1.9.84: Subscript & Superscript Support

**📐 New Formatting Tags**

Added support for subscript and superscript formatting throughout the entire pipeline:

- **Import**: DOCX files with subscript/superscript text now preserve formatting as `<sub>` and `<sup>` tags
- **Display**: Tags shown in grid cells (e.g., `P<sub>totaal</sub>`, `m<sup>2</sup>`)
- **Export**: Tags converted back to real Word subscript/superscript formatting
- **Preview**: Document Preview renders actual subscript/superscript positioning

**Technical Implementation:**
- `modules/tag_manager.py`:
  - `FormattingRun` dataclass: Added `subscript: bool` and `superscript: bool` fields
  - `TAG_PATTERN`: Extended to `r'<(/?)([biu]|bi|li|sub|sup)>'`
  - `tag_colors`: Added `'sub': '#666600'` and `'sup': '#006666'`
  - `extract_runs()`: Now captures `run.font.subscript` and `run.font.superscript`
  - `runs_to_tagged_text()`: Generates `<sub>` and `<sup>` tags
  - `tagged_text_to_runs()`: Parses `<sub>` and `<sup>` tags

- `modules/docx_handler.py`:
  - Formatting check includes `<sub>` and `<sup>` tag detection
  - Fallback mode strips `<sub>` and `<sup>` tags
  - `_replace_paragraph_with_formatting()`: Applies `run.font.subscript = True` and `run.font.superscript = True`

- `Supervertaler.py`:
  - `_render_formatted_text()`: Handles `<sub>` and `<sup>` tags using `QTextCharFormat.VerticalAlignment.AlignSubScript/AlignSuperScript`

**Files Modified:**
- `modules/tag_manager.py` - FormattingRun, TAG_PATTERN, tag_colors, extract_runs, runs_to_tagged_text, tagged_text_to_runs
- `modules/docx_handler.py` - Format detection, tag stripping, formatting application
- `Supervertaler.py` - Preview rendering with actual sub/superscript

---

### January 6, 2026 - Version 1.9.83: Notes Tab & Status Indicator

**📝 Notes Tab in Translation Results Panel**

Translation Results panel now has tabbed interface for TM Info and Notes:

- **TM Info Tab**: Shows TM match details when a match is selected
- **Notes Tab**: Add/edit notes for each segment with auto-save
- **Persistence**: Notes saved to .svproj project file
- **Removed Comments Tab**: Redundant tab under grid removed (Notes tab replaces it)

**🟠 Notes Indicator on Status Icon**

Clean visual indicator for segments with notes:

- **Orange Background**: Status icon (✓/✗) gets subtle orange highlight when segment has notes
- **Compact Design**: No separate icon cluttering the status cell
- **Tooltip**: Hover over status cell to see notes preview
- **Narrower Column**: Status column reduced from 120px to 70px

**Files Modified:**
- `Supervertaler.py` - Notes saving/loading, status icon highlighting, removed Comments tab
- `modules/translation_results_panel.py` - Added TM Info + Notes tabs interface

---

### January 5, 2026 - Version 1.9.82: Export for AI

**🤖 AI-Readable Export Format**

New export option for segments in a format optimized for AI systems:

- **Menu Location**: File → Export → 🤖 AI-Readable Format (TXT)...
- **Output Format**: `[SEGMENT 0001]` with language-labeled source/target
- **Auto Language Codes**: Detects project languages and converts to short codes (NL, EN, DE, etc.)

**Configurable Options:**
- **Language Codes**: Editable source/target codes (auto-filled from project)
- **Numbering**: Start number and zero padding (1-8 digits)
- **Content Modes**: Bilingual (source+target), Source only, Target only
- **Segment Filters**: All, Untranslated only, Translated only
- **Live Preview**: Shows format preview before export

**Use Cases:**
- Export source-only for AI translation (ChatGPT, Claude, Gemini)
- Export bilingual for AI quality review
- Simple format for automated processing and re-import

**Files Modified:**
- `Supervertaler.py` - Added `export_for_ai()` method, menu item in Export submenu

---

### January 4, 2026 - Version 1.9.81: Superlookup UX Improvements

**🔍 Search History Dropdown**

Superlookup search box now remembers last 20 searches:

- **HistoryComboBox**: Replaced QTextEdit with editable combo box showing search history
- **Persistent**: Saved to `user_data/superlookup_history.json`
- **Most Recent First**: New searches added to top of dropdown

**↔️ Resizable Sidebar**

Web Resources sidebar now resizable:

- **QSplitter**: Allows resizing between 120-250px
- **No Text Cutoff**: Resource buttons properly visible at all widths

**🎨 UI Polish**

- **Focus Rectangles Removed**: Global stylesheet removes ugly focus outlines from all buttons
- **Styled Radio Buttons**: 5 plain QRadioButton instances replaced with CheckmarkRadioButton
- **External Mode Fix**: External browser mode now correctly triggers web search

**Files Modified:**
- `Supervertaler.py` - HistoryComboBox, QSplitter, global stylesheet, radio buttons, external mode

---

### January 4, 2026 - Version 1.9.80: GitHub Code Search (Beijerterm)

**💻 GitHub Code Search for Beijerterm**

Added dedicated GitHub Code search for Beijerterm repository:

- **New Resource**: "💻 GitHub Code (Beijerterm)" button in Superlookup's Web Resources
- **Search URL**: `https://github.com/search?q={query}+repo:michaelbeijer/beijerterm&type=code`
- **Search Source Files**: Query YAML glossary files and Markdown documentation
- **Renamed**: "GitHub Code" → "GitHub Code (all)" for clarity

**Files Modified:**
- `Supervertaler.py` - Added `github_beijerterm` resource, renamed `github_code` to "GitHub Code (all)"

---

### January 4, 2026 - Version 1.9.79: Beijerterm Integration in Superlookup

**📚 Beijerterm Web Resource**

Added Beijerterm to Superlookup's Web Resources tab:

- **Updated Resource**: Replaced old `michaelbeijer.co.uk` wiki with new Beijerterm static site
- **Search URL**: `https://michaelbeijer.github.io/beijerterm/?q={query}`
- **500k+ Terms**: Dutch-English terminology database with 583,000+ term entries
- **URL Search**: Beijerterm now supports `?q=searchterm` for programmatic search integration

**Files Modified:**
- `Supervertaler.py` - Updated `beijerterm` resource in `self.web_resources` list

---

### January 9, 2026 - Version 1.9.88: Context Menu Enhancement

**🔍 Superlookup Integration in Context Menus**

Implemented quick concordance search via right-click context menu:

- **New Context Menu Item**: "🔍 Search in Superlookup (Ctrl+K)" appears when text is selected
- **Both Editor Types**: Added to ReadOnlyGridTextEditor (source) and EditableGridTextEditor (target)
- **Smart Workflow**: Select text → Right-click → Instant search in Superlookup
- **Auto-Navigation**: Opens Superlookup tab and triggers search automatically
- **Language-Aware**: Passes project source/target language pair to search
- **Vertical View**: Uses traditional concordance list layout
- **Unified Search**: Searches TM, glossaries, Supermemory, MT, and web resources

**Implementation Details:**
- `_handle_superlookup_search()` method added to both editor classes
- Gets selected text from `textCursor().selectedText()`
- Calls `_go_to_superlookup()` for navigation
- Calls `lookup_tab.search_with_query()` with full parameters
- Menu item positioned after Paste, before Add to Glossary

**Code Locations:**
- `Supervertaler.py` lines 1885-1895: ReadOnlyGridTextEditor context menu
- `Supervertaler.py` lines 1670-1702: ReadOnlyGridTextEditor handler method
- `Supervertaler.py` lines 2412-2422: EditableGridTextEditor context menu
- `Supervertaler.py` lines 2360-2392: EditableGridTextEditor handler method

**Files Modified:**
- `Supervertaler.py` - Added menu items and handler methods to both editor classes

---

### January 4, 2026 - Version 1.9.78: Find & Replace History & Batch Sets

**🔍 Find & Replace History**

Enhanced Find & Replace dialog (Ctrl+F / Ctrl+H) with history dropdowns and batch operations:

- **History Dropdowns**: Find and Replace fields now have dropdown arrows showing last 20 searches
- **Persistent History**: Search/replace terms saved to `user_data/find_replace_history.json`
- **F&R Sets Panel**: Collapsible panel for creating and managing batch replace operations
- **Batch Operations**: Run multiple find/replace operations with a single click
- **Import/Export**: Save F&R sets as `.svfr` files for sharing or backup

**New Module: `modules/find_replace_qt.py`**
- `FindReplaceHistory` - Manages and persists recent search/replace terms
- `FindReplaceOperation` - Dataclass for single F&R operation
- `FindReplaceSet` - Collection of operations that can be saved/loaded
- `FindReplaceSetsManager` - QWidget UI for managing F&R sets
- `HistoryComboBox` - Editable combo box with history dropdown

**UI Changes:**
- Find/Replace inputs changed from QLineEdit to HistoryComboBox
- Added "F&R Sets (Batch Operations)" collapsible panel below main dialog
- Added "+ Add to Set" button to save current operation to selected set
- Added "▶ Run All" button to execute all enabled operations in a set
- Double-click operation in table loads it into the dialog fields

**Files Created:**
- `modules/find_replace_qt.py` - New F&R support module (~400 lines)

**Files Modified:**
- `Supervertaler.py` - Added import, `fr_history` instance, rewrote `show_find_replace_dialog()`, added helper methods

---

### January 4, 2026 - Version 1.9.77: GitHub Code Search in Superlookup

**💻 GitHub Code Search**

Added GitHub Code Search to Superlookup's Web Resources tab:

- **New Resource**: "💻 GitHub Code" button in the web resources sidebar
- **Search URL**: `https://github.com/search?q={query}&type=code`
- **Use Case**: Search for terms/code across all public GitHub repositories
- **Great for**: Finding how technical terms are used in real code, locating terminology in open-source projects

**Files Modified:**
- `Supervertaler.py` - Added `github_code` resource to `self.web_resources` list

---

### January 3, 2025 - Version 1.9.76: Onboarding, Spellcheck & Project Info

**🎉 First-Run Welcome for New Users**

New users now get a welcoming introduction to the modular architecture:

- **Welcome Dialog**: Shows on first launch explaining modular pip extras
- **Auto-Navigate**: Opens Settings → Features tab automatically
- **Don't Show Again**: Checkbox to skip on future launches (uses CheckmarkCheckBox)
- **Bug Fix**: First-run flag now saves to correct file (ui_preferences.json)

**💰 Free vs Paid LLM Info Box**

Added clear pricing information to Settings → AI Settings:

- **Google Gemini**: FREE tier (15 req/min, 1M tokens/day)
- **Ollama**: 100% FREE (runs locally)
- **OpenAI/Claude**: Paid API only
- **Important Note**: Clarifies that ChatGPT Plus and Claude Pro web subscriptions do NOT include API access

**🔤 Spylls Spellcheck (Windows Fix)**

Fixed Hunspell spellcheck on Windows by switching to `spylls`:

- **Problem**: `cyhunspell` fails to compile on Python 3.12+ / Windows
- **Solution**: Replaced with `spylls` - pure Python Hunspell implementation
- **Benefit**: Supports regional variants (en-US vs en-GB distinguish "colour/color")
- **Backend Priority**: hunspell → spylls → pyspellchecker (graceful degradation)

**🌍 Language Variant Support**

Spellcheck now supports regional language variants:

- **Dropdown shows variants**: "English (US)", "English (GB)", "Portuguese (BR)", etc.
- **Subdirectory search**: Finds dictionaries in `dictionaries/en/en_GB.dic` subfolders
- **Added en_ZA**: South African English variant mapping
- **Regional spelling works**: "colour" correct in en_GB, incorrect in en_US

**📋 Improved Spellcheck Info Dialog**

Enhanced Spellcheck Info dialog with better documentation:

- **Three backend display**: Shows Hunspell, Spylls, pyspellchecker status separately
- **Active backend highlighting**: Current backend highlighted in green
- **Bundled dict info**: Explains Spylls includes EN, RU, SV dictionaries
- **Project links section**: Links to pyspellchecker, spylls, Hunspell GitHub pages
- **Add More Dictionaries**: Renamed section with clearer instructions

**📋 Project Info Dialog (NEW)**

New dialog to view comprehensive project information:

- **Menu**: File → 📋 Project Info...
- **Overview section**: Name, file path, languages, created/modified dates, project ID
- **Statistics section**: Segment counts, word counts, character counts, progress %
- **Source Files section**: Shows original DOCX, memoQ, CafeTran, Trados paths
- **Resources section**: Active prompt, TMs, glossaries, spellcheck settings

**Files Modified:**
- `Supervertaler.py` - Added `_show_first_run_welcome()`, `show_project_info_dialog()`, free/paid info box, spellcheck dialog improvements
- `modules/feature_manager.py` - Changed hunspell check_import from `cyhunspell` to `spylls`
- `modules/spellcheck_manager.py` - Added spylls backend, language variants, subdirectory search, CODE_TO_DISPLAY mapping
- `pyproject.toml` - Replaced `cyhunspell>=2.0.0` with `spylls>=0.1.7`
- `requirements.txt` - Updated hunspell dependency to spylls

---

### January 2, 2025 - Version 1.9.75: Modular Architecture

**📦 Modular Installation System**

Major new feature allowing users to install only the features they need, significantly reducing disk space requirements:

- **Feature Manager Module**: New `modules/feature_manager.py` provides centralized feature detection and management
- **pip Extras**: Install specific features with `pip install supervertaler[supermemory,voice,web]`
- **Settings → Features Tab**: New UI showing installed/missing features with size estimates and install commands
- **Lazy Loading Helpers**: Functions like `lazy_import_supermemory()` for conditional imports

**Installation Options:**
- `pip install supervertaler` - Core only (~300 MB)
- `pip install supervertaler[supermemory]` - Add semantic search (+600 MB)
- `pip install supervertaler[voice]` - Add voice commands (+150 MB)
- `pip install supervertaler[all]` - Everything (~1.2 GB)

**Feature Modules:**
| Module | pip Extra | Size |
|--------|-----------|------|
| Supermemory | `supermemory` | ~600 MB |
| Supervoice | `voice` | ~150 MB |
| Web Browser | `web` | ~100 MB |
| PDF Rescue | `pdf` | ~30 MB |
| MT Providers | `mt` | ~30 MB |
| Hunspell | `hunspell` | ~20 MB |
| AutoFingers | `windows` | ~10 MB |

**Files Created:**
- `modules/feature_manager.py` - FeatureManager class, FEATURE_MODULES dict, lazy import helpers

**Files Modified:**
- `Supervertaler.py` - Added `_create_features_settings_tab()`, version bump to 1.9.75
- `pyproject.toml` - Reorganized dependencies into core vs optional extras
- `requirements.txt` - Updated with modular structure documentation
- `AGENTS.md` - Added modular installation documentation

---

### January 2, 2026 - Docs: Superdocs link sanity sweep

- Fixed a broken internal Superdocs link in the TMX Editor page (Related → Translation memory).
- Re-ran SUMMARY.md and internal markdown link checks to confirm clean navigation.

**Files Modified:**
- `docs/superdocs/tools/tmx-editor.md`

### January 1, 2026 - Docs: Superdocs FAQ integration & Sv website icon

- Integrated the full legacy repository FAQ into Superdocs (GitBook source) so the FAQ lives inside the online help center.
- Updated the in-app Help → FAQ link to open the Superdocs FAQ page.
- Updated the website navbar to use the Sv icon in the top-left brand slot.

**Files Modified:**
- `docs/superdocs/reference/faq.md`
- `Supervertaler.py`
- `docs/index.html`
- `docs/sv-icon.svg`
- `docs/superdocs/.gitbook/assets/sv-icon.svg`

### January 1, 2026 - Docs: Tools pages expanded

- Rewrote the Superdocs Tools pages for accuracy against the current PyQt6 UI.
- Expanded documentation for TMX Editor, AutoFingers, Supervoice (voice commands), and Image Extractor.

**Files Modified:**
- `docs/superdocs/tools/tmx-editor.md`
- `docs/superdocs/tools/autofingers.md`
- `docs/superdocs/tools/voice-commands.md`
- `docs/superdocs/tools/image-extractor.md`

### January 1, 2026 - Docs: Superlookup pages expanded

- Expanded the Superdocs Superlookup pages (TM Search, Glossary Search, Machine Translation, Web Resources) to match current UI and behavior.
- Updated the Superlookup overview page to align entry points (Ctrl+K / Ctrl+Alt+L), language/direction filters, and the actual Web Resources list.
- Fixed Superlookup copy/insert behavior for TM and Glossary results (table items were missing under rich cell widgets).

**Files Modified:**
- `docs/superdocs/superlookup/overview.md`
- `docs/superdocs/superlookup/tm-search.md`
- `docs/superdocs/superlookup/glossary-search.md`
- `docs/superdocs/superlookup/mt.md`
- `docs/superdocs/superlookup/web-resources.md`
- `Supervertaler.py`

### December 31, 2025 - Version 1.9.73: External Prompt Editor Display

**📝 External Prompts Now Display in Editor**

When loading an external prompt file (not in the library), it now displays in the Prompt Editor panel:

- **Editor display**: External prompts show in the editor with name, description, and content fields
- **Read/write support**: External prompts can be edited and saved back to the original file
- **Format detection**: `.svprompt` files parsed as JSON to extract name, description, and content
- **Plain text support**: `.txt` and `.md` files displayed as raw content
- **Visual indicator**: Editor label shows "📁 External: {name}" to distinguish from library prompts
- **Save functionality**: Changes can be saved back to external files (JSON for .svprompt, plain text for others)
- **Project load fix**: Prompts stored in project files now display in editor when project is loaded (both external and library prompts)

**Files Modified:**
- `modules/unified_prompt_manager_qt.py` - Added `_display_external_prompt_in_editor()`, `_save_external_prompt()`, updated `_load_external_primary_prompt()`, `_save_current_prompt()`, and `_set_primary_prompt()`
- `Supervertaler.py` - Added call to `_display_external_prompt_in_editor()` in project load code

---

### December 30, 2025 - Version 1.9.67: memoQ Tag Highlighting & Batch Retry Fix

**🏷️ memoQ Content Tag Highlighting**

Fixed and improved tag highlighting for memoQ bilingual DOCX files:

- **Mixed bracket tags now highlighted**: `[uicontrol id="..."}`, `{uicontrol]`, `[image cid="..." href="..."]`
- **Closing tags**: `{tagname}` like `{MQ}`, `{tspan}` now properly pink
- **No false positives**: `[Company]`, `[Bedrijf]` placeholders stay black (only tags with attributes or mixed brackets highlighted)
- **Regex patterns fixed**: Patterns now exclude unwanted characters to prevent greedy matching across multiple tags

**Final Tag Patterns:**
```python
r'\[[^}\]]+\}'        # memoQ mixed: [anything}
r'\{[^\[\]]+\]'       # memoQ mixed: {anything]
r'\[[a-zA-Z][^}\]]*\s[^}\]]*\]'  # memoQ content: [tag attr...]
r'\{[a-zA-Z][a-zA-Z0-9_-]*\}'    # memoQ closing: {tagname}
```

**🔄 Batch Translate Retry Fix**

Fixed `UnboundLocalError: cannot access local variable 'provider_dialog'` when retry pass starts:

- **Root Cause**: Retry passes skipped the dialog but code still tried to use dialog variables
- **Fix**: Properly wrapped entire dialog section in `if not is_retry_pass:` block (~200 lines)
- **Retry passes**: Now correctly use stored settings and skip directly to progress dialog

**📄 Pagination After Clear Filters**

Fixed pagination resetting when clearing filters:

- **Previously**: Clear Filters showed ALL segments, ignoring per-page setting
- **Now**: After clearing filters, `_apply_pagination_to_grid()` is called to maintain pagination

**🎨 Tag Color Setting Visibility**

Improved discoverability of tag color setting:

- **Group renamed**: "Translation Results Pane Font Size" → "Translation Results Pane & Tag Colors"
- **Tooltip updated**: Now explains the color applies to "CAT tool tags in the grid and results pane"

**Files Modified:**
- `Supervertaler.py` - TagHighlighter patterns, batch translate retry logic, clear_filters pagination, view settings labels

---

### December 30, 2025 - Version 1.9.68: memoQ Tag Color as Default

**🎨 Default Tag Color Changed to memoQ Dark Red**

Changed the default tag highlight color from light pink (`#FFB6C1`) to memoQ's actual dark red (`#7f0001`):

- **Color picked from memoQ**: The exact color memoQ uses for inline tags (`#7f0001` / RGB 127,0,1)
- **Updated everywhere**: Grid cells, Translation Results panel, Settings defaults
- **Preset colors**: Added 8 preset colors to the color picker (memoQ red, memoQ orange, Trados blue/purple, etc.)
- **Reset button**: Now resets to memoQ red with updated tooltip

**Tag Color Behavior:**
- **memoQ exports**: Preserve original memoQ colors from source file ✅
- **Trados exports**: Preserve original Trados colors from source file ✅
- **Phrase exports**: Preserve original Phrase colors from source file ✅
- **CafeTran exports**: Preserve original CafeTran colors from source file ✅
- **Supervertaler Bilingual Table**: Uses memoQ red (`RGBColor(127, 0, 1)`) ✅

**Files Modified:**
- `Supervertaler.py` - Default tag colors, preset colors, reset button, bilingual table export
- `modules/translation_results_panel.py` - Default tag color

---

### December 30, 2025 - Version 1.9.69: Page Up/Down Pagination Navigation

**📄 Page Up/Down Shortcuts for Pagination**

Added Page Up and Page Down keyboard shortcuts for navigating through pagination pages:

- **Page Up**: Go to previous page in pagination
- **Page Down**: Go to next page in pagination
- **Added to Settings**: Shortcuts now appear in Settings → Keyboard Shortcuts under "Grid Navigation" category

**Files Modified:**
- `Supervertaler.py` - Added `shortcut_page_up` and `shortcut_page_down` QShortcuts
- `modules/shortcut_manager.py` - Added `page_prev` and `page_next` shortcut definitions

---

### December 30, 2025 - Version 1.9.71: Go to Segment Dialog (Ctrl+G)

**⌨️ Improved Go to Segment Dialog**

Enhanced the Go to Segment feature with a streamlined dialog:

- **Global shortcut**: Ctrl+G now works from anywhere in the application (added as QShortcut)
- **Minimal dialog**: Small, focused dialog with just a text field
- **Type and Enter**: Just type the segment number and press Enter - no need to click buttons
- **Input validation**: Only accepts valid segment numbers within range
- **Shows current position**: Placeholder shows current segment number
- **Pagination-aware**: Automatically switches to the correct page when jumping to segments on other pages
- **Cursor placement**: Target cell is focused and cursor placed at end, ready to edit
- **Shortcut conflict fix**: Removed duplicate Ctrl+G assignment (was on both QShortcut and menu action)

**Already in Settings**: The shortcut was already listed in Settings → Keyboard Shortcuts under "Edit" category

**Files Modified:**
- `Supervertaler.py` - Added `shortcut_goto` QShortcut, redesigned `show_goto_dialog()` with pagination support, cursor focus, removed duplicate shortcut

---

### December 30, 2025 - Version 1.9.67: memoQ Tag Highlighting & Batch Retry Fix

**📚 Documentation Consolidation**

Merged two separate guides into a single comprehensive manual:

- **Previous**: `QUICK_START.md` + `CAT_WORKFLOW.md` (separate files)
- **Now**: `MANUAL.md` - Supervertaler Manual (consolidated into online Superdocs)
- **Contents**: Installation, API setup, CAT tool workflows (memoQ, Trados, CafeTran, Phrase), keyboard shortcuts, formatting, troubleshooting
- **Location**: `docs/guides/MANUAL.md` (archived); primary docs now hosted at https://supervertaler.gitbook.io/superdocs/

**⬆️⬇️ memoQ-Style Arrow Key Navigation**

Implemented intuitive segment navigation using Up/Down arrow keys:

- **Up Arrow at top line**: Moves to previous segment, positions cursor at last line
- **Down Arrow at bottom line**: Moves to next segment, positions cursor at first line
- **Cursor column preserved**: When moving between segments, cursor stays at same column position (or end of line if shorter)
- **Works in both Source and Target cells**: Navigation works whether you're in the read-only source cell or editable target cell
- **Normal behavior within cell**: Arrow keys work normally when cursor is NOT at first/last line

**New Methods in `EditableGridTextEditor`:**
- `_position_cursor_at_end_of_segment()` - Position cursor at last line of cell
- `_position_cursor_at_start_of_segment()` - Position cursor at first line of cell

**Also Added to `ReadOnlyGridTextEditor`:**
- Same Up/Down arrow key navigation
- Tab key now cycles to target cell (column 3)

**🔢 Grammar Fix**

Fixed "Batch Translate 1 Segments" → "Batch Translate 1 Segment" (proper singular/plural)

**Files Modified:**
- `Supervertaler.py` - Arrow key navigation in both editor classes, grammar fix
- `docs/guides/MANUAL.md` - New consolidated manual (now archived; primary docs live in Superdocs)
- Deleted: `docs/guides/QUICK_START.md`, `docs/guides/CAT_WORKFLOW.md`

---

### December 29, 2025 - Version 1.9.64: Grid Pagination & Batch Translate Retry

**📄 Working Grid Pagination**

The pagination controls now actually filter the displayed segments:

- **Previously**: Pagination UI existed but all segments were always shown
- **Now**: When you select "50 per page", only 50 segments are displayed at a time
- **Navigation**: First/Prev/Next/Last buttons or type a page number
- **Efficient**: Uses show/hide rows approach without reloading the grid

**New Pagination Methods:**
- `_get_total_pages()` - Calculate total pages based on segments and page size
- `_update_pagination_ui()` - Update labels and enable/disable buttons
- `_apply_pagination_to_grid()` - Show/hide rows for current page
- Updated `go_to_first_page()`, `go_to_prev_page()`, `go_to_next_page()`, `go_to_last_page()`, `go_to_page()`, `on_page_size_changed()`

**🔄 Batch Translate Retry Until Complete**

New option to automatically retry translating empty segments:

- **Checkbox**: "🔄 Retry until all segments are translated (recommended)" in batch translate dialog
- **Default**: Enabled by default
- **Behavior**: After first pass completes, checks for segments that are still empty. If any found, automatically starts another pass with just those segments.
- **Max Retries**: 5 passes maximum to prevent infinite loops
- **LLM Only**: Only works with LLM provider (not TM or MT modes)

**Instance Variables for Retry:**
- `_batch_retry_enabled` - Whether retry is enabled
- `_batch_retry_pass` - Current retry pass number (0 = first pass)
- `_batch_provider_type`, `_batch_provider_name`, `_batch_model` - Stored settings for retry passes

**🤖 Prompt Manager Tab Rename**

- "Prompts" tab renamed to "Prompt manager" in Project resources

**📁 External Prompt Restoration Fix**

Fixed external prompts not being restored when loading a project:

- External prompts are saved with `[EXTERNAL] /path/to/file.svprompt` prefix
- On load, detects `[EXTERNAL]` prefix and calls `library.set_external_primary_prompt()`
- Updates UI label with 📁 icon and prompt name
- Shows warning if external file no longer exists

**Files Modified:**
- `Supervertaler.py` - Pagination methods, batch translate retry, prompt restoration, tab rename
- `modules/unified_prompt_library.py` - (no changes, existing method used)

---

### December 30, 2025 - Version 1.9.66: Performance Boost & Cache Fix

**⚡ Termbase Cache Fix**

Fixed critical bug where termbase cache wasn't working - same segments were being re-searched repeatedly:

- **Root Cause**: Cache check was looking at whether `stored_matches` was empty, not whether the segment was in the cache. Empty results (`{}`) were never cached, causing repeated slow searches for segments with no termbase matches.

- **Fix**: Changed to proper membership check using `segment_id in self.termbase_cache`:
  - Uses `cache_checked` boolean flag to track if cache was consulted
  - Stores results in cache EVEN IF EMPTY so segments without matches are remembered
  - Removed duplicate cache-checking code blocks

**🔇 Reduced Logging Overhead**

Removed verbose logging that was contributing to navigation slowness:

- Removed per-word termbase search logging (was logging each of 50+ words per segment)
- Removed per-match termbase result logging
- Removed prefetch worker progress logging (every 10 segments)
- Removed MT/LLM scheduling/execution debug logging
- Removed TM search debug logging (project ID, activated TMs, match counts)
- Removed termbase highlighting debug logging
- Kept only error logs and essential status messages

**Result**: Navigation between segments should feel significantly faster, especially for segments with no termbase matches (which were being re-searched every time).

**Files Modified:**
- `Supervertaler.py` - Cache logic fix (~lines 24260-24290), removed verbose logging throughout

---

### December 29, 2025 - Version 1.9.63: Linux Memory Access Violation Fix

**🐧 Linux Stability Improvements**

Fixed memory access violations (segfaults) that could occur on Linux when clicking in the grid after importing a Trados package:

**Root Cause**: Native code libraries (Hunspell spellcheck, ChromaDB, Sentence-Transformers) can crash with segfaults on Linux, especially when:
- Hunspell dictionaries are not properly installed for the target language
- ChromaDB's Rust backend has thread safety issues
- Tokenizers library uses parallel processing

**Fixes Applied:**

1. **Safer Hunspell Initialization** (`modules/spellcheck_manager.py`):
   - Added test spell check call during initialization to catch crashes early
   - Added `_crash_detected` flag to disable spellcheck permanently if it crashes
   - If spellcheck crashes mid-session, it's automatically disabled

2. **Protected Spellcheck Highlighting** (`Supervertaler.py`):
   - Added safety checks in `TagHighlighter._highlight_misspelled_words()`
   - Wrapped spellcheck loop in try/except to catch any errors
   - If errors occur, spellcheck is disabled for the session

3. **Skip AutoHotkey on Linux/Mac** (`Supervertaler.py`):
   - AutoHotkey registration now skipped entirely on non-Windows platforms
   - No more "AutoHotkey not found" warnings on Linux/Mac
   - Settings and menu items already hidden via `os.name == 'nt'` checks

**User Guidance for Linux:**
- If crashes persist, disable spellcheck in Settings → View Settings
- Ensure Hunspell dictionaries are installed: `sudo apt install hunspell-pl` (for Polish)
- Disable Supermemory auto-init if using ChromaDB causes issues

**Files Modified:**
- `modules/spellcheck_manager.py` - `_try_hunspell()`, `check_word()`, added `_crash_detected` flag
- `Supervertaler.py` - `_highlight_misspelled_words()`, `main()` Linux env vars

---

### December 22, 2025 - Version 1.9.61: DOCX Export Tag Fix & TagHighlighter Accuracy

**📄 DOCX Export List Tag Stripping**

Fixed `<li-o>` and `<li-b>` tags appearing in exported Word documents:

- Added `re.sub(r'</?li-[ob]>', '', text)` to both `_replace_paragraph_text()` and `_replace_paragraph_with_formatting()` in docx_handler.py
- These list item tags are now stripped during DOCX export, not passed through to the document

**Files Modified:**
- `modules/docx_handler.py` - `_replace_paragraph_text()`, `_replace_paragraph_with_formatting()`

**🎨 TagHighlighter - Fixed False Positives for Bracket Text**

Fixed `[Bedrijf]`, `[Company]` and other square-bracketed placeholder text being incorrectly highlighted in pink (tag color):

- **Root Cause**: The TagHighlighter patterns were too broad:
  - `r'\[[a-zA-Z][^}\]]*\]'` matched ANY `[text]` starting with a letter
  - `r'\{[a-zA-Z][^}\]]*\}'` matched ANY `{text}` starting with a letter
  
- **Fix**: Removed these overly broad patterns. Now only highlights:
  - HTML/XML tags: `<tag>`, `</tag>`, `<tag/>`
  - Trados numeric: `<1>`, `</1>`
  - memoQ numeric: `[1}`, `{1]`, `[1]`, `{1}` (numbers only, not arbitrary text)

- **Result**: `[Bedrijf]`, `[Company]`, `{placeholder}` etc. are no longer colored pink - only actual CAT tool tags get highlighted

**Files Modified:**
- `Supervertaler.py` - `TagHighlighter.highlightBlock()` - removed overly broad bracket patterns

---

### December 23, 2025 - Version 1.9.62: Dead Code Cleanup & Code Quality

**🧹 Dead Code Removal (~230+ lines)**

Removed deprecated and unused methods from the codebase:

- `toggle_sidebar()` - Quick Access sidebar removed long ago
- `update_sidebar_recent_files()` - Quick Access sidebar removed
- `handle_ribbon_action()` - Ribbon UI removed, replaced by menu bar
- `create_toolbar()` - Toolbar removed, replaced by ribbon (then menu)
- `_create_llm_settings_tab()` - Deprecated redirect, never called
- `_render_paragraph()` - Explicitly marked "no longer used"
- `_handle_target_text_debounced()` - Superseded by `_by_id` version
- `update_for_segment()` (termview) - Deprecated, use `update_with_matches()`
- `tokenize_source()` (termview) - Deprecated, use `tokenize_with_multiword_terms()`

**📋 Project Dataclass Cleanup**

- Added missing `spellcheck_settings: Dict[str, Any]` field to Project dataclass
- Added initialization in `__post_init__`
- Removed unnecessary `hasattr()` checks throughout codebase (fields now properly declared)

**🔇 Debug Logging Cleanup**

- Removed verbose TERMVIEW debug print statements from `termview_widget.py`
- Removed "💾💾💾 FINAL DEBUG" logging from project save
- Removed excessive "🔍 TERMVIEW:" log messages from main app

**🤖 AutoFingers UI Simplification**

- Removed unnecessary QTabWidget wrapper (was single tab "🎮 Control Panel")
- Control panel now displays directly without tab overhead

**Files Modified:**
- `Supervertaler.py` - Removed deprecated methods, added dataclass field, cleaned debug logs
- `modules/termview_widget.py` - Removed deprecated methods and debug prints

---

### December 22, 2025 - Version 1.9.60: Tag-Aware TM Matching & AutoFingers Cleanup

**🔍 Tag-Aware TM Matching**

Translation Memory fuzzy matching now works regardless of whether segments contain formatting tags:

- **Dual Search Strategy**: Searches both with original text (including tags) AND with tags stripped
  - `<b><u>Technisch mankement</u></b>` generates search terms: `['Technisch', 'mankement']`
  - Also includes any tag-derived terms (in case TM was indexed with tags)
  - Single FTS query with combined terms - negligible performance impact

- **Tag-Stripped Similarity Calculation**: `calculate_similarity()` now strips HTML/XML tags before comparing
  - `<b>Hello</b>` vs `Hello` now gives 100% match instead of ~70%
  - More accurate fuzzy match percentages

- **Benefits**:
  - TMs imported with tags now match segments without tags (and vice versa)
  - Similarity scores based on actual text content, not tag presence
  - Debug output shows combined search terms

**Files Modified:**
- `modules/database_manager.py` - `search_fuzzy_matches()` dual search, `calculate_similarity()` tag stripping

**🧹 TMX Tag Cleaner - Additional Tags**

- Added `<li-b></li-b>` (bullet list item) and `<li-o></li-o>` (ordered list item) tags to Formatting category
- Both enabled by default

**Files Modified:**
- `modules/tmx_editor_qt.py` - Added list item tags to `DEFAULT_TAG_PATTERNS`

**🤖 AutoFingers Cleanup**

- Removed TMX Manager tab (unused features)
- Added "📥 Import from TM" button to Control Panel's TMX File group
- Simplified TMX status display: now shows "✓ X TUs loaded" instead of verbose multi-line stats
- Removed unused `create_tmx_tab()` method

**Files Modified:**
- `Supervertaler.py` - AutoFingers UI cleanup, removed tab, added button

---

### December 22, 2025 - Version 1.9.59: TMX Tag Cleaner & UX Improvements

**🧹 TMX Tag Cleaner - Complete Implementation**

Tag cleaning functionality in both TMX Editor and main application:

- **TMX Editor Access**: 
  - Toolbar button: "🧹 Clean Tags"
  - Edit menu: Edit → Bulk Operations → 🧹 Clean Tags...
  - Tools menu: Tools → 🧹 Clean Tags...

- **Main App Access**:
  - Edit menu: Edit → Bulk Operations → 🧹 Clean Tags...
  - Cleans tags from currently loaded project segments

- **Tag Selection Dialog**:
  - User can select/deselect individual tag patterns to clean
  - Tags grouped by category: Formatting, TMX/XLIFF, memoQ, Trados, Generic
  - Quick select buttons: "Select All", "Select None", "Select Formatting Only"
  
- **Supported Tag Types**:
  - **Formatting**: `<b>`, `<i>`, `<u>`, `<bi>`, `<sub>`, `<sup>`
  - **TMX/XLIFF**: `<bpt>`, `<ept>`, `<ph>`, `<it>`, `<hi>`, `<ut>`
  - **memoQ**: `{1}`, `[2}`, `{3]` index tags
  - **Trados**: `<1>`, `</1>` numbered tags, `{1}`, `{/1}` curly tags
  - **Generic**: All XML-style tags

- **Replacement Options**:
  - Remove tags completely (no replacement)
  - Replace tags with a space

- **Scope Options**:
  - Clean both source and target segments
  - Clean source segments only
  - Clean target segments only

- **Implementation**:
  - Works in both RAM mode and database mode
  - Progress dialog with cancel option
  - Shows statistics on completion (TUs modified, tags removed)
  - Automatically refreshes grid after cleaning

**New Class:**
- `TmxTagCleanerDialog` - Configuration dialog with checkboxes for each tag pattern

**Files Modified:**
- `modules/tmx_editor_qt.py` - Added `TmxTagCleanerDialog`, `show_clean_tags_dialog()`, `clean_tags()`, toolbar button, menu items

---

### December 22, 2025 - Version 1.9.57: Flattened Tab Structure

**🏠 Simplified Main Navigation**

Reorganized the main tab structure from nested to flat hierarchy:

- **Before**: Workspace (containing Editor + Resources subtabs) → Tools → Settings
- **After**: Project editor → Project resources → Tools → Settings

**Changes Made:**
- Removed nested `project_home_tabs` QTabWidget
- Grid widget now added directly to `main_tabs` as "📝 Project editor"
- Resources tab added directly to `main_tabs` as "🗂️ Project resources"
- Updated all tab index references throughout codebase (Tools is now index 2, Settings is now index 3)
- Updated View → Navigate To menu items
- Updated keyboard shortcut action mappings
- Updated all navigation methods: `_go_to_superlookup()`, `_open_superdocs_tab()`, `show_autofingers()`, `show_image_extractor_from_tools()`, `_open_mt_settings()`, `_navigate_to_termbase_entry()`

**Capitalization Style:**
- Tab names use lowercase for subtabs: "Project editor", "Project resources" (NOT "Project Editor", "Project Resources")
- Tools and Settings remain capitalized as they are top-level concepts

**Files Modified:**
- `Supervertaler.py` - `create_main_layout()`, navigation menu, shortcut actions, all navigation methods

---

### December 22, 2025 - Version 1.9.56: Glossary Renaming Feature

**✏️ Glossary Renaming via Right-Click**

Fixed the glossary (termbase) renaming functionality:

- **Problem**: Editing the glossary name directly in the table appeared to work but changes were never saved to the database
- **Root Cause**: `QTableWidgetItem` in the Name column was editable by default, but no handler saved the edited value
- **Solution Implemented**:
  - Added right-click context menu to glossary table with "✏️ Rename Glossary" and "🗑️ Delete Glossary" options
  - New `rename_termbase()` method in `TermbaseManager` class updates the name in the database
  - New `_show_termbase_context_menu()` method shows context menu at right-click position
  - New `_rename_termbase_dialog()` method shows QInputDialog for entering new name
  - Disabled inline editing with `setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)`

**Files Modified:**
- `modules/termbase_manager.py` - Added `rename_termbase()` method
- `Supervertaler.py` - Added context menu, rename dialog, disabled inline editing

---

### December 22, 2025 - Version 1.9.54: Superlookup UX Improvements & Terminology Rename

**🔍 Superlookup Enhancements**

Several usability fixes for the Superlookup unified lookup window:

- **Enter Key Behavior**: Pressing Enter in search box now triggers search (Shift+Enter for newline)
- **Edit in Glossary Navigation**: Right-click "Edit in Glossary" now correctly selects the glossary in the Resources tab
- **Fuzzy Search Filter**: Minimum term length filter prevents single-letter terms from matching long search queries (e.g., "A" no longer matches "Machine Fingerprint")
- **TM Source Column**: Added new "TM" column to TM results showing which Translation Memory the match came from

**📝 User-Facing Terminology Rename: Termbase → Glossary**

Comprehensive rename of user-facing terminology throughout the application:

- **Tab Names**: "Termbase Matches" → "Glossaries", "TM Matches" → "TMs"
- **Dialog Titles**: "Create New Termbase" → "Create New Glossary", "Import Termbase" → "Import Glossary"
- **Settings Labels**: "TM/Termbase lookup delay" → "TM/Glossary lookup delay", "Termbase Highlight Style" → "Glossary Highlight Style"
- **Button Text**: "Add to Termbase" → "Add to Glossary", "TM/Termbase ON" → "TM/Glossary ON"
- **Tooltips**: All termbase-related tooltips updated to use "glossary"
- **Context Menus**: "Add to Termbase" → "Add to Glossary", "Edit in Termbase" → "Edit in Glossary"
- **Warning Messages**: All QMessageBox dialogs updated to use "glossary" terminology
- **Checkboxes**: "Enable TM & Termbase Matching" → "Enable TM & Glossary Matching"

**Technical Notes:**
- Internal code (variable names, method names, database columns) remains unchanged for backward compatibility
- Only user-visible strings were modified
- Project files (.svproj) still use `termbase_settings` key for compatibility

**Files Modified:**
- `Supervertaler.py` - Comprehensive UI string updates throughout

---

### December 21, 2025 - Version 1.9.55: Lightning-Fast Filtering

**⚡ Optimized Filter Performance**

Major performance optimization for filter operations (Ctrl+Shift+F):

- **Before**: ~12 seconds to apply or clear a filter
- **After**: Instant (typically <200ms)

**Root Cause**: Filter operations were calling `load_segments_to_grid()` which recreates all QTextEdit widgets for every segment. With 500+ segments, this took ~12 seconds.

**Solution Implemented**:
- `apply_filters()` now uses `setUpdatesEnabled(False)` to batch UI changes, only shows/hides rows and applies yellow highlights without recreating widgets
- `clear_filters()` now clears only yellow filter highlights (preserves termbase/tag formatting) and unhides rows in place
- New `_clear_filter_highlights_in_widget()` method surgically removes only yellow (#FFFF00) highlights while preserving green termbase highlights and pink tag colors

**🔄 Ctrl+Shift+F Toggle Behavior**

The filter shortcut now works as a true toggle:
- **First press** (with text selected): Filters on selected text
- **Second press** (with filter active): Clears the filter immediately

**📋 Keyboard Shortcuts Update**

Added "Clear filter" entry in keyboard shortcuts (same Ctrl+Shift+F shortcut) for discoverability. Updated shortcut description to reflect toggle behavior.

**Files Modified:**
- `Supervertaler.py` - `apply_filters()`, `clear_filters()`, `_highlight_text_in_widget()`, `_clear_filter_highlights_in_widget()` (new), `filter_on_selected_text()`
- `modules/shortcut_manager.py` - Added `clear_filter` shortcut entry, updated descriptions

---

### December 21, 2025 - Version 1.9.53: Superlookup Termbase Enhancements

**📋 Improved Termbase Matches Tab**

Enhanced the Superlookup Termbase Matches tab with additional metadata columns:

- **Renamed Column Headers**: "Term (Source)" → "Source", "Translation (Target)" → "Target"
- **New Columns Added**: Termbase (source name), Domain, Notes
- **Full Metadata in Results**: Each termbase match now includes domain, notes, priority, project, client, forbidden status
- **Tooltips**: Hover over cells to see full content (especially useful for long notes)

**📥 Termbase Import Progress Dialog**

New real-time progress dialog when importing termbases from TSV files:

- **Visual Progress Bar**: Shows percentage and entry count (e.g., "245/500 (49%)")
- **Live Statistics**: Running counters for imported (✅), skipped (⏭️), and errors (❌)
- **Scrolling Log Window**: Dark-themed console showing each entry as it's processed
  - ✅ Imported: source → target
  - ⏭️ Skipped duplicate: source
  - 🔄 Updated: source → target (when update mode selected)
  - ❌ Line X: error message
- **Auto-Refresh**: Termbase table automatically updates term counts after import

**Files Modified:**
- `Supervertaler.py` - `create_termbase_results_tab()`, `display_termbase_results()`, `search_termbases()`, `_import_termbase()`, `_refresh_termbase_table()`
- `modules/termbase_import_export.py` - `import_tsv()` now accepts `progress_callback` parameter

---

### December 20, 2025 - Version 1.9.52: Superlookup Web Resources

**🌐 Expanded Web Resources Tab**

Complete overhaul of the Superlookup Web Resources tab with 14 reference sites and persistent sessions:

- **New Web Resources (6 added)**:
  - Juremy (ISO 639-3 language codes)
  - michaelbeijer.co.uk (translator's personal site)
  - AcronymFinder (uppercase language codes)
  - BabelNet (multilingual knowledge graph)
  - Wiktionary Source & Target (separate dictionary for each language)

- **Persistent Login Sessions**:
  - QWebEngineProfile with `ForcePersistentCookies` policy
  - Cookies stored in `user_data/web_cache/`
  - Stay logged in to ProZ, Linguee, IATE, etc.

- **Auto Language Selection**:
  - `set_project_languages()` method sets Superlookup dropdowns from project
  - Called automatically on project load
  - Language pair auto-fills when opening Superlookup

- **Compact UI Layout**:
  - Single-line search bar with direction controls
  - "Search" label replaced with 🔍 icon
  - Simplified direction labels: "Both", "Source", "Target"
  - Settings checkboxes control sidebar button visibility

- **Language Code Formats**:
  - iso2, iso3, iso639_3, full_lower, iso2_upper
  - `_get_web_lang_code()` handles all format conversions
  - `_build_web_search_url()` with sl_upper/tl_upper placeholders

**Files Modified:**
- `Supervertaler.py` - Web resources tab, language handling, persistent profile, UI layout

---

### December 20, 2025 - Version 1.9.51: Superlookup MT Integration

**🔍 Complete Machine Translation in Superlookup**

Full MT integration with multiple providers and improved error handling:

- **MT Provider Status Display**: New compact status panel in Machine Translation tab
  - Shows active providers (✅), disabled providers (⏸️), and missing API keys (❌)
  - "⚙️ Configure in Settings" link navigates directly to Settings → MT Settings

- **All MT Providers Now Working**:
  - Google Translate, Amazon Translate, DeepL, Microsoft Translator, ModernMT, MyMemory
  - Error messages now displayed in red with full details (no more silent failures)
  - Successful translations shown in blue with copy button

- **Language Name Mapping Fix**: Critical fix for all MT providers
  - App stores languages as full names ("Dutch", "English")
  - MT APIs require ISO codes ("nl", "en")
  - Added `lang_name_to_code` mapping dictionary to Google Translate, Amazon Translate, MyMemory
  - Supports 24+ languages including European, Asian, and Middle Eastern

- **Dependencies**: Added `boto3` and `deepl` to requirements.txt

- **Termbases Tab Improvements**:
  - Search filter now functional (filters termbase list as you type)
  - New split-view with editable terms grid on right side
  - All term columns visible: Source, Target, Priority, Domain, Notes, Project, Client, Forbidden

- **Cleanup**:
  - Removed debug print spam (ROW COLOR DEBUG messages)
  - Removed redundant MT sub-tab from Superlookup Settings (MT config now in main Settings → MT Settings)

**Files Modified:**
- `Supervertaler.py` - MT provider calls, language mapping, Superlookup MT tab, Termbases split view
- `requirements.txt` - Added boto3, deepl

---

### December 18, 2025 - Version 1.9.50: Voice Commands Complete

**🎤 Voice Commands System - Final Polish**

Complete hands-free translation system with all features working:

- **OpenAI Whisper API Integration**: Added dual recognition engine support
  - OpenAI Whisper API (recommended): Fast, accurate, works great for short voice commands
  - Local Whisper model (fallback): Works offline but less accurate for short clips
  - Recognition engine dropdown in Supervoice settings

- **Grid Toolbar Button**: New 🎧 Voice ON/OFF toggle button in the grid toolbar
  - Shows current state: 🎧 Voice ON (green), 🔴 REC (red), ⏳ Processing (orange)
  - Click to toggle always-on listening without going to settings

- **Status Bar Indicator**: Always-on indicator in status bar (bottom-right)
  - 🎤 VOICE ON / 🔴 REC / ⏳ ... 
  - Clickable to toggle on/off

- **Bug Fixes**:
  - Fixed `copy_source_to_grid_target()` not working - was using wrong column (1 instead of 3) and wrong method (`table.item()` instead of `table.cellWidget()`)
  - Fixed `clear_grid_target()` same issue
  - Fixed `get_api_key()` AttributeError - changed to `load_api_keys()` which returns dict

**Files Modified:**
- `Supervertaler.py` - Grid toolbar button, status bar indicator, API key loading fix, copy/clear target fixes
- `modules/voice_commands.py` - OpenAI Whisper API transcription path

---

### December 18, 2025 - Version 1.9.49: Always-On Voice Listening

**🎧 Always-On Listening Mode**

New VAD-based (Voice Activity Detection) continuous listening mode that eliminates the need to press F9 twice:

- **How it works:**
  1. Continuously monitors microphone audio levels
  2. When speech detected (RMS above threshold) → starts recording
  3. When silence detected (0.8s of quiet) → stops and transcribes
  4. Processes result as command or dictation
  5. Repeats automatically

- **Settings UI:** Settings → 🎤 Supervoice → "🎧 Always-On Listening Mode" section:
  - Start/Stop toggle button with status indicator
  - Visual feedback: 🟢 Listening → 🔴 Recording → ⏳ Processing
  - Microphone sensitivity: Low/Medium/High (for different environments)

- **F9 Behavior Update:**
  - If always-on is active: F9 stops it
  - If always-on is inactive: F9 works as push-to-talk (original behavior)

- **Technical Details:**
  - VAD uses amplitude-based speech detection (RMS threshold)
  - Minimum speech duration: 0.3s (ignores short sounds)
  - Maximum recording: 15s (prevents runaway recordings)
  - Silence timeout: 0.8s (adjustable via sensitivity)
  - Model loaded once, cached for fast subsequent transcriptions

**Classes Added/Modified:**
- `ContinuousVoiceListener` - Complete rewrite with VAD
- `_VADListenerThread` - New background thread with proper VAD loop
- Settings persistence for sensitivity level

**Files Modified:**
- `modules/voice_commands.py` - ContinuousVoiceListener, _VADListenerThread
- `Supervertaler.py` - Import, initialization, toggle function, UI, signal handlers

---

### December 18, 2025 - Version 1.9.48: Voice Commands System (Talon-style)

**🎤 Voice Command System**

New Talon-style voice command system that lets users control Supervertaler and other applications by voice:

- **3-Tier Architecture:**
  - **Tier 1: Internal Commands** - Control Supervertaler (confirm segment, navigate, translate, etc.)
  - **Tier 2: System Commands** - AutoHotkey integration for controlling other apps (memoQ, Trados, Word)
  - **Tier 3: Dictation Fallback** - If no command matches, insert as text

- **Built-in Commands:**
  - Navigation: "next segment", "previous", "first segment", "last segment"
  - Editing: "confirm", "copy source", "clear target", "undo", "redo"
  - Translation: "translate", "translate all"
  - Lookup: "lookup", "concordance"
  - memoQ: "glossary" (Alt+Down), "tag next" (multi-key sequence)
  - Trados: "confirm trados" (Ctrl+Enter)

- **Settings UI:** Settings → 🎤 Supervoice tab now includes:
  - Enable/disable voice commands toggle
  - Voice commands table with all phrases, aliases, actions
  - Add/Edit/Remove custom commands
  - Reset to defaults button
  - AutoHotkey status indicator

- **Custom Command Support:**
  - Phrase + aliases (fuzzy matching)
  - Action types: internal, keystroke, AHK inline code, AHK script file
  - Categories for organization
  - User commands stored in `user_data/voice_commands.json`

**New Files:**
- `modules/voice_commands.py` - VoiceCommandManager, VoiceCommand dataclass, fuzzy matching
- `voice_commands.ahk` - AutoHotkey v2 bridge script for system-level automation
- `user_data/voice_commands.json` - User command library (auto-created)

**Files Modified:**
- `Supervertaler.py` - Added VoiceCommandManager, VoiceCommandEditDialog, enhanced Supervoice settings

---

### December 18, 2025 - Version 1.9.46: Workspace UI Redesign

**🏠 New Tab Hierarchy**

Cleaner, more intuitive tab structure:

- **Main tabs**: 🏠 Workspace → 🛠️ Tools → ⚙️ Settings
- **Workspace subtabs**: 📝 Editor (the grid) + 🗂️ Resources (TM, Termbases, Prompts, etc.)
- Removed Document View (unused feature)
- Simplified View menu (removed Grid/Document view switcher)

**Naming Philosophy:**
- "Workspace" - generic term that works for translation, localization, and copywriting
- "Editor" - describes what you do (edit content), not the UI (grid)
- "Resources" - all project resources in one place

**🐛 Critical Bug Fix: Termbase Activation**

Fixed termbase matches showing terms from non-activated termbases:
- Added `AND (ta.is_active = 1 OR tb.is_project_termbase = 1)` filter to `search_termbases()` query
- Now only returns terms from termbases with Read checkbox enabled

**Files Modified:**
- `Supervertaler.py` - `create_main_layout()`, navigation menu, view menu
- `modules/database_manager.py` - `search_termbases()` activation filter

---

### December 18, 2025 - Version 1.9.47: Code Cleanup

**🧹 Dead Document View Code Removed**

Removed ~811 lines of unused Document View code. The Document View feature was never used in production - the Grid View (Editor) is the primary and only workflow.

**Removed Items:**
- `LayoutMode` class (GRID/DOCUMENT enum)
- `create_editor_widget()` - View switcher with Grid/List/Document buttons
- `create_home_tab()`, `create_projects_manager_tab()` - Deprecated wrappers
- `create_editor_tab()`, `switch_view_mode()` - View switching logic
- `switch_home_view_mode()` - Home tab view switching
- `create_document_view_widget()`, `create_document_view_widget_for_home()` - Document view creation
- `refresh_document_view()` - ~300 lines of document rendering code
- `_find_document_container()`, `_register_document_container()`, `_set_active_document_host()`, `_get_document_container()`, `_locate_document_container()` - Container helpers
- `_find_widget_by_object_name()` - Widget search helper
- Document View Methods section (on_doc_segment_clicked, on_doc_status_change, etc.)
- Document view state variables (doc_segment_widgets, doc_current_segment_id, document_containers, active_document_host, current_view_mode)

**Result:**
- File reduced from 35,249 to 34,438 lines
- Cleaner codebase, easier to maintain
- No functional changes - Grid View (Editor) is unaffected

---

### December 17, 2025 - Version 1.9.45: Termbase Highlight Styles & Spellcheck Auto-Language

**🏷️ Configurable Termbase Highlight Styles**

Three visual styles for termbase term highlighting in the translation grid:

- **Background (Default)**: Pastel green shades based on priority (existing behavior)
- **Dotted Underline**: DotLine underline with priority-based colors
  - Priority 1: Red
  - Priority 2-3: Gray shades  
  - Priority 4+: User-configurable color (default dark green)
  - Reset button to restore default color
- **Semibold**: DemiBold font weight with tinted green foreground colors

**Settings UI:**
- New "🏷️ Termbase Highlight Style" section in Settings → View Settings
- Radio button selection for style type
- Color picker for dotted underline (Priority 4+)
- Reset button to restore default color

**🔤 Spellcheck Auto-Language Initialization**

Fixed spellcheck not using project's target language:

- **All Import Handlers**: DOCX, TXT, memoQ, CafeTran, Trados bilingual, SDLPPX, Phrase now initialize spellcheck for target language
- **Project Load**: Always sets spellcheck to project target language (ignores old saved language)
- **Short Code Support**: Added `SHORT_CODE_MAP` in spellcheck_manager.py to handle "nl" → "nl_NL", "de" → "de_DE", etc.

**Bug Fixes:**
- Fixed NT list crash (`lst.active` → `lst.is_active`)
- Fixed NonTranslatable attributes (`pattern` → `text`, `description` → `notes`)
- Fixed Ctrl+K going to Settings instead of Superlookup (tab index 3 → 2)
- Renamed Grid/Document tabs to "Grid View"/"Document View"

**Files Modified:**
- `Supervertaler.py` - `highlight_termbase_matches()`, `_create_view_settings_tab()`, `_save_view_settings_from_ui()`, all import handlers, `load_project()`
- `modules/spellcheck_manager.py` - Added `SHORT_CODE_MAP`, updated `set_language()` to handle short codes

---

### December 16, 2025 - Version 1.9.41: Dark Mode Complete Implementation

**🌙 Full Dark Theme Support**

Completed comprehensive dark mode implementation after extensive debugging session:

- **Compare Boxes Fixed**: Translation Results panel compare boxes (Current Source, TM Source, TM Target) now properly dark in dark mode
- **Termview Visibility**: All words in Termview pane now visible - non-matched words use light text color
- **Root Cause Discovery**: Qt doesn't reliably apply stylesheets to hidden widgets
- **Solution**: Added `_apply_compare_box_theme()` method called when compare frame becomes visible

**Technical Changes:**
- `modules/translation_results_panel.py` - Added `_apply_compare_box_theme()`, uses both stylesheet AND QPalette for reliability
- `modules/termview_widget.py` - Made `TermBlock` and `NTBlock` theme-aware with `theme_manager` parameter

**Key Lesson Learned:**
When Qt stylesheets aren't visually applying despite the code running correctly, consider:
1. Widget visibility state at time of styling
2. Using QPalette as an alternative/supplement to stylesheets
3. Re-applying styles when widget becomes visible

---

### December 17, 2025 - Version 1.9.42: Multi-File Project Support

**📁 Import Folder (Multiple Files)**

Major new feature allowing users to import entire folders of files as a single multi-file project:

- **New Menu Item**: File → Import → Folder (Multiple Files)...
- **Supported Formats**: DOCX and TXT files in selected folder
- **File Selection Dialog**: Preview files with size, select/deselect individual files
- **Language Pair Selection**: Set source/target language for all files
- **Progress Dialog**: Shows import progress with per-file segment counts

**🗂️ Per-File Progress Tracking**

- **File Progress Dialog**: View → File Progress... (or click on status bar)
- **Per-File Statistics**: Segments, words, translated, confirmed, progress bar for each file
- **Status Indicators**: ✅ Complete, 📝 Translated, 🔄 In Progress, ⬜ Not Started
- **Navigation**: Double-click file to jump to its first segment

**📊 Status Bar Enhancement**

- **Files Indicator**: Shows "📁 Files: X/Y" for multi-file projects (completed/total)
- **Clickable**: Click the files indicator to open File Progress dialog
- **Tooltip**: Hover for file count and completion summary

**🔍 File Filter Dropdown**

- **New Dropdown**: Appears in filter panel for multi-file projects
- **Filter by File**: Select a specific file to show only its segments
- **All Files**: Default option to show all segments from all files

**Data Model Changes:**
- `Segment` dataclass: Added `file_id` (int) and `file_name` (str) fields
- `Project` dataclass: Added `files` (list of file metadata) and `is_multifile` (bool) fields
- Backward compatible: Single-file projects work unchanged

**📤 Export Folder (Multiple Files)**

- **New Menu Item**: File → Export → Folder (Multiple Files)...
- **Format Options**: TXT (plain text), DOCX (formatted), Bilingual (Source/Target table)
- **File Preview**: Shows all files with format, segment count, and status
- **Progress Dialog**: Shows export progress with per-file updates

**New Methods in Supervertaler.py:**
- `import_folder_multifile()` - Folder import dialog
- `_import_multifile_project()` - Import multiple files into single project
- `export_folder_multifile()` - Folder export dialog
- `_export_multifile_to_folder()` - Export multiple files to folder
- `_export_file_as_txt()` - Export single file as plain text
- `_export_file_as_docx()` - Export single file as formatted DOCX
- `_export_file_as_bilingual()` - Export single file as bilingual DOCX table
- `show_file_progress_dialog()` - Per-file progress dialog
- `_add_overall_progress_section()` - Overall progress stats
- `_on_file_filter_changed()` - File filter dropdown handler
- `_update_file_filter_combo()` - Populate file filter dropdown

**🔧 Source File Backup & Recovery (added later)**

- **Automatic Backup**: Source files now copied to `_source_files/` folder inside project directory during import
- **Relocate Source Folder**: File → Relocate Source Folder... menu item to fix broken paths when source files are moved
- **Export Warning**: Shows helpful message when source files are missing, suggests using Relocate feature

**🔍 Superlookup Fixes**

- **Class Renamed**: `UniversalLookupTab` → `SuperlookupTab` for consistency
- **Theme Support**: Added `theme_manager` attribute for theme-aware search term highlighting
- **Fixed Error**: Resolved `'UniversalLookupTab' object has no attribute 'theme_manager'` error

**📋 Spellcheck Info Dialog Redesign**

- **Compact Layout**: Completely redesigned to fit on screen without scrolling off the bottom
- **Horizontal Top Row**: Status, language dropdown, and backend indicator on one line
- **Collapsible Troubleshooting**: Diagnostics section collapsed by default (click to expand)
- **Inline Links**: Download links for Hunspell dictionaries in horizontal row with separators
- **Max Height**: Dialog limited to 500px to prevent overflow

---

### December 12, 2025 - Trados Bilingual DOCX Workflow Documentation

**📚 Comprehensive Trados Workflow Documentation**

Added critical workflow documentation for Trados Bilingual Review DOCX format:

- **Import dialog warning**: `import_trados_bilingual()` now shows detailed ⚠️ CRITICAL WORKFLOW warning explaining the required preparation steps
- **CAT_WORKFLOW.md**: Updated Trados Studio section with both SDLPPX (recommended) and Bilingual DOCX (workaround) workflows
- **QUICK_START.md**: Added warning note directing users to full documentation

**The Critical Workflow:**
The Trados Bilingual Review format is designed for **review only**, not translation - it doesn't export empty target segments! ([RWS Community reference](https://community.rws.com/product-groups/trados-portfolio/trados-studio/f/studio/34874/export-for-bilingual-review-exports-only-source-text))

Required workaround:
1. In Trados: Copy source to target (fills empty segments)
2. Export as Bilingual Review DOCX
3. In Word: Delete all target text (cells exist but are empty)
4. Import into Supervertaler, translate, export
5. Reimport into Trados Studio

**Files Modified:**
- `Supervertaler.py` - `import_trados_bilingual()` warning dialog (line ~18562)
- `docs/guides/CAT_WORKFLOW.md` - Comprehensive Trados section with both workflows
- `docs/guides/QUICK_START.md` - Warning note with link to full documentation

---

### December 12, 2025 - Version 1.9.40: Superlookup Unified Concordance System

**🔍 Ctrl+K Now Opens Superlookup**

- Major consolidation: Concordance search now uses Superlookup instead of separate dialog
- All lookup resources in one place: TM, Termbase, Supermemory, MT, Web Resources
- Selected text in source/target automatically populates search field
- `show_concordance_search()` now calls `_go_to_superlookup()` and triggers search

**📊 Dual-View Toggle for TM Matches**

- Horizontal (Table): Source | Target columns side-by-side - compact, scannable
- Vertical (List): Dutch: ... / English: ... stacked - traditional concordance layout
- Radio button toggle in TM Matches tab
- Both views stay in sync with search results
- `toggle_tm_view_mode()` and `display_tm_results()` updated for dual display

**🗂️ Tab Reorganization**

- "Resources" renamed to "Project Resources"
- Tab order changed: Project Editor → Project Resources → Prompt Manager → Tools → Settings
- Removed "Concordance" and "Import/Export" tabs from Translation Memories (redundant)
- Source text box in Superlookup shrunk from 100px to 50px
- "Termbase Terms" renamed to "Termbase Matches"

**⚡ FTS5 Full-Text Search Optimization**

- `concordance_search()` in database_manager.py now uses FTS5 MATCH queries
- 100-1000x faster than previous LIKE queries on large databases
- Auto-sync: FTS5 index rebuilt on connect if out of sync
- New methods: `rebuild_fts_index()`, `check_fts_index()`

**🐛 ChromaDB Stability Fix**

- Removed all `collection.count()` calls that caused native Rust crashes
- Stats now use SQLite metadata count instead of ChromaDB collection queries
- ChromaDB 0.6.3 with tokenizers 0.22.0 (stable combination)

**Files Modified:**
- `Supervertaler.py` - show_concordance_search(), create_tm_results_tab(), display_tm_results(), tab ordering
- `modules/database_manager.py` - concordance_search() FTS5, rebuild_fts_index(), check_fts_index()
- `modules/supermemory.py` - Removed collection.count() calls, uses metadata for stats

---

### December 11, 2025 - Version 1.9.39: Superlookup Multilingual Search

**🔍 Multilingual Language Filtering**

- Added From/To language dropdown filters in Superlookup search bar
- Filter TM and termbase searches by source/target language pair
- Languages auto-populate from TMs and termbases on first tab view
- Alphabetically sorted with language family grouping (all Dutch variants together, etc.)
- Display format: "English (en)", "Dutch (nl-BE)" for clarity

**↔️ Search Direction Controls**

- Radio buttons: Both (bidirectional), Source only, Target only
- Concordance search respects direction setting
- Termbase search also respects direction for bidirectional term lookup

**🎨 UI Improvements**

- Yellow highlighting of search terms in TM/termbase results
- Compact results display with word wrap and 60px max row height
- Tooltips show full text on hover
- Hidden row numbers for cleaner display
- Removed Manual Capture button (redundant with paste)
- Removed Operating Modes dropdown (only Universal mode used)

**Files Modified:**
- `Supervertaler.py` - UniversalLookupTab UI, language dropdowns, direction radio buttons, display methods
- `modules/superlookup.py` - search_tm() accepts direction and language parameters
- `modules/translation_memory.py` - concordance_search() accepts language filters
- `modules/database_manager.py` - concordance_search() filters by source_lang/target_lang

---

### December 11, 2025 - Version 1.9.38: Project File & UX Improvements

**📁 Reorganized .svproj File Structure**

- Metadata now at top of file (name, languages, dates, ID)
- Settings next (prompts, TM, termbases, spellcheck)
- Source paths follow (DOCX, memoQ, Trados, CafeTran, SDLPPX)
- Segments moved to END of file for easier human inspection

**💡 Improved Batch Translate Warning**

- Added tip about using Select All + Clear Target from right-click menu
- Users no longer need to re-import memoQ files just to clear targets

**Files Modified:**
- `Supervertaler.py` - `Project.to_dict()`, batch translate warning message

---

### December 11, 2025 - Version 1.9.37: User-Configurable Grid Fonts

**🔤 Font Customization in Settings → View Settings**

- Added font family dropdown with 10 popular fonts (Calibri, Segoe UI, Arial, Consolas, Verdana, Times New Roman, Georgia, Courier New, Tahoma, Trebuchet MS)
- Added live preview panel showing sample source/target text with tags - updates in real-time as you adjust settings
- Font family now persists between sessions (previously only font size was saved)
- Fixed font size spinbox up/down arrows with improved styling and click targets
- Added friendly note: "If your favourite font is missing, contact the developer!"

**Files Modified:**
- `Supervertaler.py` - `_create_view_settings_tab()`, `_save_view_settings_from_ui()`, `load_font_sizes_from_preferences()`, `save_current_font_sizes()`

---

### December 10, 2025 - Version 1.9.35: memoQ Red Tag Color Fix + Universal Tag Coloring

**🔴 memoQ Inline Tag Color Preservation (Export)**

Fixed critical issue where red/magenta inline tags (e.g., `{1}`, `[2}`) in memoQ bilingual exports were appearing as black text in the target column.

**Root Cause Discovery:**
- memoQ stores tag colors in **character styles** (e.g., `mqInternal`), not directly on the run
- The `mqInternal` style defines color `800000` (dark red) at the style level
- `python-docx` API (`run.font.color.rgb`) returns `None` for style-based colors

**Solution Implemented:**
- Added 3-tier color extraction method in `export_memoq_bilingual()`:
  1. Check `run.font.color.rgb` (direct color)
  2. Check XML `w:color` element in `rPr` (inline XML color)
  3. **NEW**: Check `w:rStyle` element, lookup character style, extract style's color

---

**🎨 Universal Tag Coloring in Grid (Display)**

Extended `TagHighlighter` to color ALL CAT tool tags with pink (`#FFB6C1`) in the translation grid:

| Format | Tag Examples | Status |
|--------|-------------|--------|
| HTML/XML | `<b>`, `<i>`, `<u>`, `<li-o>` | ✅ Already worked |
| memoQ | `{1}`, `[2}`, `{3]`, `[4]` | ✅ NEW |
| Trados | `<1>`, `</1>` | ✅ NEW |
| Phrase | `{1}`, `{2}` | ✅ NEW |

**CafeTran Pipe Fix:**
- Pipe symbols (`|`) now only highlighted red in **CafeTran projects**
- Previously, pipes were red in ALL project types (bug)
- Added `TagHighlighter._is_cafetran_project` class flag

**Files Modified:**
- `Supervertaler.py` - `TagHighlighter.highlightBlock()`, CafeTran import function

### December 10, 2025 - Version 1.9.34: UI Fixes

**🎨 Global UI Standardization**
- Replaced standard OS radio buttons with custom green `CheckmarkRadioButton`.
- Unified design across Filters, Import, AutoFingers, and Find/Replace dialogs.
- Replaced default radio buttons in Import TMX dialogue with standard `CheckmarkRadioButton` widgets
- Ensures consistency with application's green UI theme

---

### December 10, 2025 - Version 1.9.32: Trados SDLRPX Status Fix

**📦 Fixed Critical SDLRPX Export Bug**
- Fixed segments staying in "Draft" status instead of being updated to "Translated" in exported SDLRPX packages
- Trados Studio now correctly recognizes translated segments when client opens return package
- Added `_update_segment_status()` method to `modules/sdlppx_handler.py`
- Updates `conf` attribute in `sdl:seg-defs` section of SDLXLIFF files

**Root Cause:**
- The `_update_xliff_tree()` function was updating target text but not updating the `conf` attribute
- SDL/Trados uses `conf="Draft"` vs `conf="Translated"` in `<sdl:seg>` elements

---

### December 10, 2025 - Version 1.9.33: Spellcheck Update Fix

**🐛 Fixed Spellcheck Highlighting Bug**
- Fixed issue where adding/ignoring words only removed underline in the current cell
- Now triggers global refresh of all highlighters
- Modified `_add_to_dictionary` and `_ignore_word` in `EditableGridTextEditor`

---

### December 10, 2025 - Version 1.9.31: Spellcheck Language Fix

- Spellcheck now correctly uses the project's target language instead of defaulting to English
- Added language dropdown in Spellcheck Info dialog

---

### December 10, 2025 - Version 1.9.30: Critical LLM Fix

- Removed hardcoded debug file path that caused "No such file or directory" errors

---

### December 10, 2025 - Version 1.9.29: Spellcheck Integration

- Red wavy underlines for misspelled words
- Right-click context menu with suggestions
- Add to Dictionary, Ignore Word
- New module: `modules/spellcheck_manager.py`

---

### December 9, 2025 - Version 1.9.28: Phrase DOCX & Show Invisibles

- Phrase (Memsource) bilingual DOCX support
- Show Invisibles feature (spaces, tabs, line breaks)

---

### December 9, 2025 - Version 1.9.27: Simple Text Import/Export

- Import text files (each line = segment)
- Export translations as text

---

### December 8, 2025 - Version 1.9.26: Model Version Checker

- Auto-detect new LLM models from OpenAI, Anthropic, Google

---

### December 7, 2025 - Version 1.9.24: Smart Word Selection

- Selecting part of word expands to full word

---

### December 5, 2025 - Version 1.9.20: SDLPPX Persistence

- Package path saved in .svproj files

---

### December 4, 2025 - Version 1.9.19: Trados Package Support

- Import SDLPPX, export SDLRPX
- New module: `modules/sdlppx_handler.py`

---

### December 3-4, 2025 - Version 1.9.17-18: Supermemory

- Domain management, filtering, Superlookup integration
- Concordance Search with semantic tab

---

### December 2, 2025 - Supermemory: Vector TM

- ChromaDB + Sentence-Transformers
- Semantic search across TMs
- Module: `modules/supermemory.py` (2100+ lines)

---

### December 1, 2025 - Version 1.9.16: Ollama Support

- Local LLM translation with Ollama

---

### November 30, 2025 - Versions 1.9.13-15

- Document Preview tab
- Bilingual Table export/import

---

### November 27-28, 2025 - Versions 1.9.8-11

- CafeTran integration
- Navigation improvements

---

### November 8-9, 2025 - Unified Prompt System

- 2-layer prompt architecture
- AI Assistant for prompt generation

---

### November 7, 2025 - TagCleaner

- CAT tool tag removal module

---

### November 6, 2025 - LLM Integration Complete

- Multi-LLM support operational

---

## 🗄️ Database Schema (SQLite)

### Core Tables
- **translation_units** - TM entries
- **termbases** - Termbase definitions
- **termbase_terms** - Individual terms
- **termbase_activation** - Project termbase tracking
- **non_translatables** - Locked terms
- **projects** - Translation projects

### Naming Conventions
- ✅ Use "Termbase" (one word)
- ❌ Never use "Glossary" or "glossary_terms"

---

## � Planned Features

### ✅ AI Proofreading System (IMPLEMENTED - January 7, 2026)

> **STATUS:** Fully implemented in v1.9.85

**Overview:**
An intelligent proofreading system that uses LLMs to verify translation quality. Issues are stored in the Notes field with ⚠️ PROOFREAD prefix.

**Access Points:**
- Edit → Batch Operations → ✅ Proofread Translation...
- View → ✅ Proofreading Results...
- Advanced Filters → "Has proofreading issues"
- Right-click → ✅ Clear Proofreading Notes

**Features:**
- Batch processing (20 segments per API call)
- Progress dialog with real-time stats
- Results table with navigation to segments
- Bulk and individual clear operations
- Orange indicator on status icons
- Filter for segments with issues

**Files Modified:**
- `Supervertaler.py` - All implementation

---

## 📚 Additional Resources

| File | Purpose |
|------|---------|
| `CHANGELOG.md` | Complete version history |
| `README.md` | User-facing documentation |
| `FAQ.md` | Common questions |
| `docs/guides/` | User guides |

---

*This file replaces the previous CLAUDE.md and PROJECT_CONTEXT.md files.*
*Last updated: January 21, 2026 - v1.9.146*
