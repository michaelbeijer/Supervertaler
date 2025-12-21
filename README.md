# 🚀 Supervertaler v1.9.54

[![PyPI version](https://badge.fury.io/py/supervertaler.svg)](https://pypi.org/project/Supervertaler/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

🎯 **The Ultimate Translation Workbench** — Context-aware AI with intuitive 2-Layer Prompt Architecture, AI Assistant, project glossary system with automatic extraction, and specialized modules.

**Current Version:** v1.9.54 (December 22, 2025)
**Framework:** PyQt6
**Status:** Active Development

---

## 📚 Documentation

| Guide | Description |
|-------|-------------|
| **[Quick Start](docs/guides/QUICK_START.md)** | Get translating in 5 minutes |
| **[CAT Workflow](docs/guides/CAT_WORKFLOW.md)** | memoQ, Trados, CafeTran integration |
| **[Keyboard Shortcuts](docs/guides/KEYBOARD_SHORTCUTS.md)** | Complete shortcut reference |
| **[FAQ](FAQ.md)** | Common questions answered |
| **[Changelog](CHANGELOG.md)** | Version history and recent features |

### Additional Resources
- **[Project Context](PROJECT_CONTEXT.md)** — Complete project reference
- **[Architecture](docs/ARCHITECTURE.md)** — System design
- **[Legacy Versions](legacy_versions/LEGACY_VERSIONS.md)** — Historical information
- **[Similar Apps](docs/SIMILAR_APPS.md)** — CotranslatorAI, TWAS Suite, and other translation tools
- **[Stargazers](https://github.com/michaelbeijer/Supervertaler/stargazers)** — A page that lists all the users who have starred this repository
  
---

## 🚀 Installation & Running

### Option 1: Install from PyPI (Recommended)

```bash
pip install supervertaler
supervertaler
```

### Option 2: Run from Source

```bash
git clone https://github.com/michaelbeijer/Supervertaler.git
cd Supervertaler
pip install -r requirements.txt
python Supervertaler.py
```

**PyPI Package:** https://pypi.org/project/Supervertaler/

### NEW in v1.9.54 - User-Facing Terminology Rename 📝
*   **Termbase → Glossary**: All user-facing UI now uses "Glossary" instead of "Termbase"
*   **TM Matches → TMs**: Tab renamed for consistency
*   **Superlookup UX**: Enter triggers search, Edit in Glossary navigation fixed, fuzzy search filter improved
*   **TM Source Column**: New column shows which TM each match came from
*   **Internal code unchanged**: Database and project files maintain backward compatibility

### v1.9.53 - Superlookup Glossary Enhancements 📋
*   **Metadata Columns**: Glossary name, Domain, Notes columns in results
*   **Import Progress Dialog**: Real-time progress with statistics and scrolling log
*   **Tooltips**: Hover to see full content for long entries

### v1.9.52 - Superlookup Web Resources 🌐
*   **14 Web Resources**: IATE, Linguee, ProZ, Reverso, Google, Google Patents, Wikipedia (Source/Target), Juremy, michaelbeijer.co.uk, AcronymFinder, BabelNet, Wiktionary (Source/Target)
*   **Persistent Login Sessions**: Cookies stored in `user_data/web_cache/` - stay logged in to ProZ, Linguee, etc.
*   **Auto Language Selection**: Language pair auto-fills from current project
*   **Compact Search Layout**: Single-line search with direction controls
*   **Customizable Sidebar**: Settings checkboxes control which resource buttons appear

### v1.9.51 - Superlookup MT Integration 🔍
*   **All MT Providers Working**: Google Translate, Amazon Translate, DeepL, Microsoft Translator, ModernMT, MyMemory
*   **Provider Status Panel**: Shows ✅ active, ⏸️ disabled, ❌ missing API keys
*   **Error Display**: Errors shown in red with full details (no more silent failures)
*   **Language Mapping Fix**: "Dutch" → "nl", "English" → "en" for all MT APIs
*   **Settings Link**: "⚙️ Configure in Settings" navigates to Settings → MT Settings
*   **Termbases Tab**: Search filter + split-view with editable terms grid

### v1.9.50 - Voice Commands System 🎤
*   **Hands-Free Translation**: Say "next segment", "confirm", "source to target", "translate" and more
*   **Always-On Listening**: VAD-based continuous listening - no need to press F9 twice
*   **Dual Recognition**: OpenAI Whisper API (recommended) or local Whisper model
*   **Grid Toggle Button**: 🎧 Voice ON/OFF button in toolbar for easy access
*   **Status Indicators**: Status bar shows 🟢 Listening → 🔴 Recording → ⏳ Processing
*   **AutoHotkey Integration**: Control external apps (memoQ, Trados, Word) by voice
*   **Custom Commands**: Add your own voice commands with fuzzy matching
*   **Configure**: Tools → Supervoice tab

### v1.9.41 - Dark Mode 🌙
*   **Complete Dark Theme**: Full dark mode support with consistent styling across the entire application
*   **Compare Boxes**: Translation Results panel properly displays dark backgrounds in dark mode
*   **Termview Visibility**: All words visible in dark mode, not just terms with matches
*   **Access**: View → Theme Editor → Select "Dark" theme

### v1.9.40 - Superlookup Unified Concordance System
*   **Ctrl+K Now Opens Superlookup**: All concordance searches consolidated into Superlookup - one hub for TM, Termbase, Supermemory, MT, and Web Resources
*   **Dual-View Toggle**: Switch between Horizontal (table) and Vertical (list) layouts for TM results
*   **Tab Reorganization**: "Project Resources" tab now before "Prompt Manager", removed redundant Concordance and Import/Export tabs
*   **FTS5 Full-Text Search**: Concordance now uses SQLite FTS5 for 100-1000x faster search on large databases

### v1.9.39 - Superlookup Multilingual Search
*   **Language Filtering**: From/To dropdowns filter TM and termbase searches by language pair
*   **Search Direction**: Both/Source only/Target only radio buttons for precise concordance
*   **Yellow Highlighting**: Search terms highlighted in results with compact display and tooltips

**v1.9.32 - Trados SDLRPX Status Fix:**
- 📦 **Trados SDLRPX Status Fix** - Fixed critical bug where exported SDLRPX return packages kept segments in "Draft" status instead of updating to "Translated".

**v1.9.30 - Critical LLM Fix:**
- 🐛 **Fixed OpenAI Translation** - Removed hardcoded debug path that caused "No such file or directory" errors
- 📝 **Spellcheck Integration** - Built-in spellcheck with 8 languages bundled (EN, NL, DE, FR, ES, PT, IT, RU)
- 📚 **Optional Hunspell** - Add more languages with .dic/.aff dictionary files
- 💬 **Right-Click Menu** - Spelling suggestions, Add to Dictionary, Ignore
- 💾 **Project Settings** - Spellcheck state saved per-project in .svproj files

**v1.9.28 - Phrase DOCX Support & Show Invisibles:**
- 📄 **Phrase (Memsource) Bilingual DOCX** - Full round-trip support for Phrase TMS files
- 👁️ **Show Invisibles** - Display spaces (·), tabs (→), NBSPs (°), line breaks (¶) in the grid
- 🎨 **Smart Handling** - Copy/paste, word selection, and navigation work correctly with invisibles shown

**v1.9.27 - Simple Text File Import/Export:**
- 📄 **Simple TXT Import** - Import plain text files where each line becomes a source segment
- 📤 **Simple TXT Export** - Export translations as matching text file with target text
- 🌐 **Encoding Support** - UTF-8, Latin-1, Windows-1252 with automatic detection
- 📝 **Line-by-Line** - Perfect for translating simple text content

**v1.9.26 - Automatic Model Version Checker:**
- 🔄 **Auto Model Detection** - Automatically checks for new LLM models from OpenAI, Anthropic, and Google
- 📅 **Daily Checks** - Runs once per 24 hours on startup (configurable)
- 🎨 **UI Standardization** - All 68 checkboxes now use consistent green (16x16px) design

**v1.9.25 - Linux Compatibility:**
- 🐧 **Full Linux Support** - Works perfectly on Ubuntu and other Linux distributions
- 📦 **Complete Dependencies** - One-command installation with requirements.txt

**v1.9.20 - Trados Studio Package Support:**
- 📦 **SDLPPX Import** - Import Trados Studio project packages directly
- 📤 **SDLRPX Export** - Create return packages for delivery back to Trados users
- 💾 **Project Persistence** - Save/restore SDLPPX projects across sessions

**v1.9.18 - Supermemory Concordance Integration:**
- 🔍 **Semantic Concordance** - Concordance Search (Ctrl+K) now includes Supermemory tab
- 🧠 **Two-Tab Interface** - TM Matches (exact) and Supermemory (meaning-based)

**v1.9.17 - Supermemory Enhancements:**
- 🧠 **Domain Management** - Categorize TMs by domain (Legal, Medical, Patents, Technical, etc.)
- 🔍 **Semantic Search** - Find translations by meaning using AI embeddings
- 🌐 **Language Filtering** - Filter by language pairs with dynamic column headers
- 🔗 **Superlookup Integration** - New Supermemory tab for unified lookup
- 📤 **Export Options** - Export to TMX or CSV format

**v1.9.16 - Local LLM Support (Ollama):**
- 🖥️ **Offline AI** - Run translation entirely on your computer with no API costs
- 🔧 **Hardware Detection** - Automatic model recommendations based on RAM/GPU
- 📦 **Setup Wizard** - One-click Ollama installation and model downloads

**v1.9.15 - Bilingual Table Export/Import:**
- 📋 **With Tags Export** - Export bilingual table with Supervertaler tags for proofreading (can be re-imported)
- 📄 **Formatted Export** - Export bilingual table with applied formatting for clients/archives
- 🔄 **Import Changes** - Re-import edited bilingual table to update translations with diff preview
- 📊 **5-Column Table** - Segment #, Source, Target, Status, Notes - perfect for review workflow

**v1.9.14 - DOCX Export & Keyboard Navigation:**
- 📤 **Formatting Preservation** - Export properly converts `<b>`, `<i>`, `<u>` tags to Word formatting
- ⌨️ **Ctrl+Home/End** - Navigate to first/last segment even when editing in grid cells

**v1.9.13 - Document Preview & List Formatting Tags:**
- 📄 **Preview Tab** - New Preview tab shows formatted document with headings, paragraphs, and lists
- 🔢 **List Type Detection** - DOCX import properly detects bullet vs numbered lists from Word XML
- 🏷️ **Short List Tags** - `<li-o>` for ordered/numbered lists (1. 2. 3.), `<li-b>` for bullet points (•)

**v1.9.12 - Progress Indicator Status Bar:**
- 📊 **Words Translated** - Shows X/Y words with percentage
- ✅ **Confirmed Segments** - Shows X/Y segments with percentage
- 🔢 **Remaining Count** - Segments still needing work
- 🎨 **Color Coding** - Red (<50%), Orange (50-80%), Green (>80%)

**v1.9.11 - Navigation & Find/Replace Improvements:**
- ⚡ **Quick Navigation** - Ctrl+Home/End to jump to first/last segment
- 🔍 **Smart Pre-fill** - Find/Replace dialog pre-fills selected text
- ⌨️ **Ctrl+Q Shortcut** - Instant term pair saving (remembers last-used termbase)

**v1.9.6 - Custom File Extensions & Monolingual Export:**
- 📁 **Branded Extensions** - `.svproj` (projects), `.svprompt` (prompts), `.svntl` (non-translatables)
- 🌐 **Language Selection** - Monolingual DOCX import now prompts for source/target languages
- 📤 **Target-Only Export** - Export translated content preserving original document structure
- 💾 **Project Persistence** - Original DOCX path saved for reliable exports
- 📊 **Preview & Configure** - Review extracted terms, adjust parameters (frequency, n-gram, language)
- 🎯 **Visual Distinction** - Project=pink, Forbidden=black, Background=priority-based blue
- ⚡ **One-Click Extraction** - Extract Terms button in Termbases tab (enabled when project loaded)

**v1.6.0 - Complete Termbase System:**
- 📚 **Professional Terminology Management** - SQLite-based termbase system rivaling commercial CAT tools
- 🎨 **Priority-Based Highlighting** - Terms highlighted in source with color intensity matching priority (1-99)
- 💡 **Hover Tooltips** - Mouse over highlighted terms to see translation, priority, and forbidden status
- 🖱️ **Double-Click Insertion** - Click any highlighted term to insert translation at cursor
- ⚫ **Forbidden Term Marking** - Forbidden terms highlighted in black for maximum visibility
- 🔍 **Real-Time Matching** - Automatic detection and display in Translation Results panel
- 🗂️ **Multi-Termbase Support** - Create, activate/deactivate, and manage multiple termbases
- ⌨️ **Fast Term Entry** - Select source → Tab → select target → Ctrl+E to add term
- ✏️ **Full Management** - Edit priority, forbidden flag, definition, domain in dedicated UI

**v1.5.1 - Source/Target Tab Cycling:**
- 🔄 **Tab Key Cycling** - Press `Tab` to jump between source and target cells
- ⌨️ **Termbase Workflow** - Select term in source → `Tab` → select translation in target
- 🔠 **Ctrl+Tab** - Insert actual tab character when needed

**v1.5.0 - Translation Results Enhancement + Match Insertion:**
- 🎯 **Progressive Match Loading** - All match types now accumulate (termbase + TM + MT + LLM)
- ⌨️ **Match Shortcuts** - `Ctrl+1-9` for quick insert, `Ctrl+Up/Down` to navigate, `Ctrl+Space` to insert
- 🏷️ **Tag Display Control** - Optional show/hide HTML/XML tags in results
- 📊 **Smart Status** - Manual edits reset status requiring confirmation

**v1.4.0 - Supervoice Voice Dictation + Detachable Log:**
- 🎤 **Supervoice Voice Dictation** - AI-powered hands-free translation input
- 🌍 **100+ Languages** - OpenAI Whisper supports virtually any language
- ⌨️ **F9 Global Hotkey** - Press-to-start, press-to-stop recording anywhere
- 🎚️ **5 Model Sizes** - Tiny to Large (balance speed vs accuracy)
- 🚀 **Future Voice Commands** - Planned parallel dictation for workflow automation
- 🪟 **Detachable Log Window** - Multi-monitor support with synchronized auto-scroll

**Previous Features:**
- 🤖 **AI Assistant Enhanced Prompts** - ChatGPT-quality translation prompts (v1.3.4)
- 📊 **Superbench** - LLM translation quality benchmarking with adaptive project sampling (v1.4.1, formerly LLM Leaderboard v1.3.3)

**v1.3.1 Features - AI Assistant File Attachment Persistence:**
- 📎 **Persistent File Attachments** - Attached files saved to disk across sessions
- 👁️ **File Viewer Dialog** - View attached content with markdown preview
- 🗂️ **Expandable Files Panel** - Collapsible UI with view/remove buttons

**v1.3.0 Features - AI Assistant + 2-Layer Architecture:**
- 🤖 **AI Assistant with Chat Interface** - Conversational prompt generation and document analysis
- 🎯 **2-Layer Prompt Architecture** - Simplified from 4-layer to intuitive 2-layer system
  - **Layer 1: System Prompts** - Infrastructure (CAT tags, formatting, core instructions)
  - **Layer 2: Custom Prompts** - Domain + Project + Style Guide (unified, flexible)
- ✨ **Markdown Chat Formatting** - Beautiful chat bubbles with **bold**, *italic*, `code`, and bullets
- 🧹 **TagCleaner Module** - Clean memoQ index tags from AutoFingers translations
- 🎨 **Perfect Chat Rendering** - Custom Qt delegates for professional chat UI

**v1.2.4 Features - TagCleaner Module & AutoFingers Enhancement:**
- ✅ **TagCleaner Module** - Standalone module for cleaning CAT tool tags
- ✅ **AutoFingers Integration** - Tag cleaning integrated with AutoFingers engine
- ✅ **Status Column Improvements** - Semantic icons and better visual design

**v1.2.2-1.2.3 Features:**
- ✅ **Translation Results Panels** - All match types display correctly
- ✅ **Document View Formatting** - Renders bold, italic, underline, list items
- ✅ **Enhanced Type Column** - H1-H4, Title, Sub, li, ¶ with color coding
- ✅ **Tabbed Panel Interface** - Translation Results | Segment Editor | Notes
- ✅ **Complete Match Chaining** - Termbase + TM + MT + LLM together

**Core Features:**
- 🎯 **2-Layer Prompt Architecture** - System Prompts + Custom Prompts with AI Assistant
- 🤖 **AI Assistant** - Conversational interface for document analysis and prompt generation
- 🧠 **Context-aware AI** - Leverages full document context, images, TM, and termbases
- 🤖 **Multiple AI Providers** - OpenAI GPT-4o/5, Claude 3.5 Sonnet, Google Gemini 2.0
- 🖥️ **Local LLM (Ollama)** - Run AI translation offline, no API keys needed, complete privacy
- 🌐 **Machine Translation** - Google Cloud Translation API integration
- 🎨 **Translation Results Panel** - All match types (Termbase, TM, MT, LLM) in one view
- 🔄 **CAT Tool Integration** - Import/export with memoQ, Trados, CafeTran
- 📊 **Bilingual Review Interface** - Grid, List, and Document views
- 🔍 **Superlookup** - System-wide search with global hotkey (Ctrl+Alt+L)
- 📝 **TMX Editor** - Professional translation memory editor with database support
- 🧹 **AutoFingers** - Automated translation pasting for memoQ with tag cleaning
- 🔧 **PDF Rescue** - AI-powered OCR for poorly formatted PDFs
- 🔧 **Encoding Repair Tool** - Detect and fix text encoding corruption (mojibake)
- 💾 **Translation Memory** - Fuzzy matching with TMX import/export
- 📚 **Multiple Termbases** - Glossary support per project

---

## 📋 System Requirements

- **Python:** 3.8+
- **PyQt6** - Modern GUI framework
- **OS:** Windows, macOS, Linux
- **Database:** SQLite (built-in)

---

## 💡 Repository Philosophy

This repository follows a **lean structure** optimized for efficiency:
- ✅ Only essential source code included
- ✅ Current documentation in `docs/`
- ✅ Historical documentation archived in `docs/archive/`
- ✅ Smaller repo = faster AI processing = lower costs

---

## 📖 Learn More

For comprehensive project information, see [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md).

---

**Last Updated:** October 30, 2025  
**Latest Version:** v1.0.2-Qt (October 31, 2025)

---

## 📦 Two Editions Available

### 🆕 Qt Edition (Modern) - **Recommended**
**File**: `Supervertaler_Qt.py`  
**Current Version**: v1.0.0 Phase 5 (October 29, 2025)

**Latest Features**:
- 🔍 **Superlookup** - Search TM from anywhere (Ctrl+Alt+L)
- 🎨 **Modern UI** - PyQt6 with 6 built-in themes + custom theme editor
- ⚡ **Better Performance** - Faster, more responsive
- 🎯 **Superlookup** - System-wide translation memory search
- 🤖 **AutoFingers** - Automated translation pasting for memoQ
- 📋 **memoQ Integration** - Bilingual DOCX import/export
- 💾 **Translation Memory** - SQLite-based with FTS5 search
- 📝 **TMX Editor** - Professional TM editing

### 🔧 Tkinter Edition (Classic) - **Stable**
**File**: `Supervertaler_tkinter.py`  
**Current Version**: v3.7.7 (October 27, 2025)

**Features**:
- 🤖 **LLM Integration** - OpenAI GPT-4/5, Anthropic Claude, Google Gemini
- 🎯 **Context-aware Translation** - Full document understanding
- 📚 **Unified Prompt Library** - System Prompts + Custom Instructions
- 🆘 **PDF Rescue** - AI-powered OCR for badly-formatted PDFs
- ✅ **CAT Features** - Segment editing, grid pagination, dual selection
- 📝 **TMX Editor** - Professional translation memory editor
- 🔗 **CAT Tool Integration** - memoQ, CafeTran, Trados Studio
- 📊 **Smart Auto-export** - TMX, TSV, XLIFF, Excel

---

##  Quick Start

**Download Latest**:
- **Qt Edition**: `Supervertaler_Qt.py` (Modern, recommended)
- **Tkinter Edition**: `Supervertaler_tkinter.py` (Classic, stable)

**Previous Versions**: See `previous_versions/` folder for archived releases

---

## ✨ What is Supervertaler?

Supervertaler is a **professional Computer-Aided Translation (CAT) editor** designed by a 30-year veteran translator for translators.

Built with PyQt6, Supervertaler offers modern UI, advanced AI integration, complete termbase system, and specialized modules for every translation challenge.

---

## 🎯 Core Features

**Complete Termbase System** (v1.6.0):
- 📚 **Professional Terminology Management** - SQLite-based with FTS5 search
- 🎨 **Priority-Based Highlighting** - Terms highlighted with color intensity (1-99 scale)
- 💡 **Hover Tooltips** - See translation, priority, forbidden status on hover
- 🖱️ **Double-Click Insertion** - Insert translations at cursor with one click
- ⚫ **Forbidden Term Marking** - Black highlighting for do-not-use terms
- 🔍 **Real-Time Matching** - Automatic detection in Translation Results panel
- 🗂️ **Multi-Termbase Support** - Create, activate/deactivate multiple termbases

**AI & Translation**

- 🤖 **Multiple AI Providers** - OpenAI GPT-4o/5, Claude 3.5 Sonnet, Google Gemini 2.0
- 🎯 **2-Layer Prompt Architecture** - System Prompts + Custom Prompts with AI Assistant
- 🤖 **AI Assistant** - Conversational interface for document analysis and prompt generation
- 🧠 **Context-aware Translation** - Full document context, images, TM, and termbases
- 🌐 **Machine Translation** - Google Cloud Translation API integration
- 🎨 **Translation Results Panel** - All match types (Termbase, TM, MT, LLM) in one view

**Professional CAT Editor**:
- 📊 **Bilingual Grid Interface** - Source/target cells with inline editing
- 🔄 **Tab Key Cycling** - Jump between source and target cells
- ⌨️ **Match Shortcuts** - Ctrl+1-9 for quick insert, Ctrl+Up/Down to navigate
- 📝 **Document View** - Full document layout with formatting
- 🏷️ **Tag Display Control** - Optional show/hide HTML/XML tags
- 🔍 **Find/Replace** - Search across segments with regex support

**Translation Memory**:
- 💾 **SQLite Backend** - Fast, reliable database storage with FTS5 search
- 🔍 **Fuzzy Matching** - Find similar segments with match percentages
- 📝 **TMX Editor** - Professional TM editor handles massive 1GB+ files
- 📥 **Import/Export** - TMX, XLIFF, bilingual DOCX formats
- 🔄 **Auto-propagation** - Repeat translations automatically

**Voice & Accessibility**:
- 🎤 **Supervoice** - AI voice dictation with OpenAI Whisper (100+ languages)
- ⌨️ **F9 Global Hotkey** - Press-to-start, press-to-stop recording
- 🎚️ **5 Model Sizes** - Tiny to Large (balance speed vs accuracy)
- 🪟 **Detachable Windows** - Multi-monitor support for log and panels

**Specialized Modules**:
- 📄 **PDF Rescue** - AI OCR with GPT-4 Vision for locked PDFs
- 🧹 **AutoFingers** - Automated translation pasting for memoQ with tag cleaning
- 📊 **Superbench** - LLM translation quality benchmarking with chrF++ scoring
- 🔧 **Encoding Repair** - Detect and fix text encoding corruption (mojibake)
- 🔍 **Superlookup** - System-wide TM search with global hotkey (Ctrl+Alt+L)

**CAT Tool Integration**:
- 📊 **memoQ** - Bilingual DOCX import/export with perfect alignment
- 🏢 **Trados** - XLIFF import/export with tag preservation
- ☕ **CafeTran** - Bilingual DOCX support
- 💾 **Export Formats** - DOCX, TSV, JSON, XLIFF, TMX, Excel, HTML, Markdown

---

## 🔧 Getting Started

### Installation

```bash
# Clone repository
git clone https://github.com/michaelbeijer/Supervertaler.git
cd Supervertaler

# Install dependencies
pip install -r requirements.txt

# Run application
python Supervertaler.py
```

---

### First Steps

1.  **Configure API Keys**: Set up OpenAI, Claude, or Gemini credentials
2.  **Explore System Prompts** (Ctrl+P) - Browse domain-specific specialist prompts
3.  **Create Custom Instructions** - Define your translation preferences
4.  **Open a Document** - Import DOCX, create segments
5.  **Start Translating** - Use System Prompts or custom instructions
6.  **Export Results** - Session reports, TMX, auto-export to CAT tools

---

## 📖 Documentation

- **Changelog**: [CHANGELOG.md](CHANGELOG.md) - Complete version history
- **Legacy Versions**: [legacy_versions/LEGACY_VERSIONS.md](legacy_versions/LEGACY_VERSIONS.md) - Historical information
- **Project Context**: [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) - Complete project reference
- **Website**: [michaelbeijer.github.io/Supervertaler](https://michaelbeijer.github.io/Supervertaler)

---

## 🎯 Why Supervertaler?

### For Professional Translators
- ✅ Built by a professional translator (30 years experience)
- ✅ Designed for real translation workflows, not generic AI
- ✅ Integrates with your existing CAT tools
- ✅ Context-aware for better accuracy
- ✅ Fully open source - no vendor lock-in

### For Translation Agencies (LSPs)
- ✅ Improve translator productivity (20-40% gains documented)
- ✅ Consistent quality across your translator pool
- ✅ Works with your existing CAT tool infrastructure
- ✅ Open source means you own your workflow
- ✅ Custom training and consulting available

### Why Open Source?
- 🔓 **Full transparency** - See exactly what the AI is doing
- 🔓 **No vendor lock-in** - Own your translation workflow
- 🔓 **Community-driven** - Contribute features, report bugs
- 🔓 **Sustainable** - Supported through consulting and training

---

## 🚀 Features Overview

### AI Translation Engine
- **Multiple providers** - OpenAI, Anthropic, Google Gemini
- **Multimodal support** - GPT-4 Vision for figures and context
- **Batch processing** - Translate entire documents at once
- **Context preservation** - Full document analysis before translation

### Professional Prompts
- **19 System Prompts** - Domain specialists (Legal, Medical, Patent, Tech, etc.)
- **8 Custom Instructions** - User-defined preferences
- **Prompt Assistant** - Generate custom prompts from document analysis
- **Markdown format** - Human-readable, easy to edit

### Translation Memory
- **Fuzzy matching** - Find similar segments
- **Context display** - See source alongside match
- **Segment history** - Learn from previous translations
- **TMX export** - Industry-standard format

### Professional Export
- **Auto-reports** - Session reports in HTML and Markdown
- **CAT tool export** - Direct memoQ and CafeTran DOCX
- **Format preservation** - Bold, italic, formatting maintained
- **Tag safety** - XLIFF tags completely preserved

---

## 📊 Performance

- ⚡ **Grid pagination** - 10x faster loading (50 segments/page)
- ⚡ **Smart caching** - Reduce API calls with TM fuzzy matching
- ⚡ **Batch translation** - Process 100+ segments simultaneously
- ⚡ **Responsive UI** - Stays responsive during large operations

---

## 🤝 Community & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/michaelbeijer/Supervertaler/issues)
- **GitHub Discussions**: [Community chat and questions](https://github.com/michaelbeijer/Supervertaler/discussions)
- **Website**: [supervertaler.com](https://supervertaler.com)
- **Professional Website**: [michaelbeijer.co.uk](https://michaelbeijer.co.uk)

---

## 💡 Use Cases

### Individual Translators
- Enhance personal productivity with AI
- Maintain consistent terminology
- Work faster without sacrificing quality
- Leverage domain-specific prompts

### Translation Agencies
- Train all translators with same prompts
- Maintain company-wide consistency
- Increase productivity across the team
- Reduce review/QA time
- Custom LSP consulting available

### Translation Students
- Learn professional translation workflows
- Understand CAT tool integration
- Practice with real-world tools
- Open source to study and modify

---

## 🔐 Privacy & Security

- **No data collection** - Your translations stay on your computer
- **Local processing** - Translations processed locally by default
- **API keys encrypted** - Credentials stored securely
- **Open source** - Full audit trail, no hidden code
- **GDPR compliant** - User data never leaves your system

---

## 📄 License

**MIT License** - Fully open source and free

This software is provided as-is for both personal and commercial use.

---

## 👤 About

**Supervertaler** is maintained by Michael Beijer, a professional translator with 30 years of experience in technical and patent translation. The project represents a personal passion for building tools that make translators' lives easier.

- 🌐 **Website**: [michaelbeijer.co.uk](https://michaelbeijer.co.uk)
- 💼 **Professional**: [ProZ Profile](https://www.proz.com/profile/652138)
- 🔗 **LinkedIn**: [linkedin.com/in/michaelbeijer](https://www.linkedin.com/in/michaelbeijer/)

---

**Last Updated:** November 16, 2025  
**Current Version:** v1.6.6

## 🎯 Roadmap

### Planned Features (v3.8+)
- Enhanced Prompt Assistant with auto-refinement
- Glossary management UI improvements
- Advanced TM features (penalty weights, leverage scoring)
- Integration marketplace (partner CAT tools)
- Professional cloud hosting option (optional)

### Community Contributions Welcome
We're looking for:
- 🐛 Bug reports and feature requests
- 💡 Prompt contributions (System Prompts, Custom Instructions)
- 📖 Documentation improvements
- 🌍 Translations and localization
- 🤝 Code contributions

---

## 📞 Questions?

Check out:
1. **README.md** (this file) - Overview
2. **[CHANGELOG.md](CHANGELOG.md)** - Complete version history
3. **[PROJECT_CONTEXT.md](PROJECT_CONTEXT.md)** - Complete project reference
4. **[GitHub Discussions](https://github.com/michaelbeijer/Supervertaler/discussions)** - Ask questions & share ideas
5. **[Website Documentation](https://supervertaler.com)** - Guides and tutorials
6. **[GitHub Issues](https://github.com/michaelbeijer/Supervertaler/issues)** - Bug reports & feature requests

---

## 💡 Contributing & Feedback

We welcome contributions and feedback from the community!

### Feature Requests & Ideas
Have an idea for a new module or feature? We'd love to hear from you!

- **💬 [Start a Discussion](https://github.com/michaelbeijer/Supervertaler/discussions)** - Share ideas, ask questions, discuss features
  - Perfect for brainstorming new modules
  - Exploring "what if" scenarios
  - Getting community feedback
  - Discussing implementation approaches

### Bug Reports
Found a problem? Help us improve!

- **🐛 [Report a Bug](https://github.com/michaelbeijer/Supervertaler/issues)** - Submit detailed bug reports
  - Include steps to reproduce
  - Specify your environment (OS, Python version)
  - Attach screenshots if relevant

### Workflow
1. **💭 Idea** → Start in [Discussions](https://github.com/michaelbeijer/Supervertaler/discussions)
2. **✅ Approved** → Converted to [Issue](https://github.com/michaelbeijer/Supervertaler/issues) for tracking
3. **🚀 Implemented** → Linked to commits and released

---

**Last Updated**: October 31, 2025  
**Version**: v1.1.0 (Qt Edition)  
**Status**: Active Development  
**License**: MIT (Open Source)  
**Security Status**: Current - Security patches applied

---

> 🎯 **Supervertaler**: Empowering professional translators with intelligent, context-aware AI tools. Built by translators, for translators.
