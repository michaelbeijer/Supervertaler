# Supervertaler CAT Edition - Changelog

**Version Branch**: v3.x.x-beta (Experimental CAT Editor)

This changelog tracks changes specific to the **CAT Edition** of Supervertaler - the experimental segment-based CAT editor with advanced features.

For the Classic Edition changelog, see [CHANGELOG-CLASSIC.md](CHANGELOG-CLASSIC.md).  
For the unified changelog, see [CHANGELOG.md](CHANGELOG.md).

---

## [3.6.0-beta] - 2025-01-16 📄 PDF RESCUE + DOCUMENTATION UPDATE

> **🎉 Major Release**: PDF Rescue fully documented and production-ready! Complete documentation overhaul across README, CHANGELOG, FAQ, website, and dedicated user guide.

### ✨ WHAT'S NEW

**Comprehensive Documentation**:
- **NEW: `docs/guides/PDF_RESCUE.md`** - Complete 892-line user guide
  - Overview with real-world success story
  - 9 key features fully explained
  - Quick start (5 steps) + detailed workflows
  - Smart features guide (redactions, stamps, formatting)
  - Session report structure & use cases
  - Pro tips & best practices
  - Technical details & dependencies
  - 15+ FAQ entries
  - Troubleshooting guide

**README.md Updates**:
- Added PDF Rescue section to CAT Tool Integration
- Featured real-world client testimonial
- Key features highlighted
- 5-step workflow included
- Direct link to comprehensive guide

**Website Updates** (`docs/index.html`):
- **NEW**: Custom logo/icon (supervertaler_icon_colours.png)
- **NEW**: PDF Rescue feature card in features grid
- **NEW**: PDF Rescue documentation link
- Updated CAT Edition to v3.6.0-beta
- PDF Rescue highlighted in download section

**Repository Cleanup**:
- ✅ Renamed: `Supervertaler_v3.5.0-beta_CAT.py` → `Supervertaler_v3.6.0-beta_CAT.py`
- ✅ Moved to `.dev/`: `ai_ocr_tool.py`, `jpg_to_docx_converter.py`, `check_task_types.py`, `debug_prompts.py`, `test_prompt_loading.py`
- ✅ Deleted: `PDF_RESCUE_BACKUP.txt` (obsolete backup)
- ✅ Cleaner root directory - only user-facing files

### 🎨 VISUAL IMPROVEMENTS

**Custom Branding**:
- Website now uses custom Supervertaler icon instead of emoji
- Professional logo display in navigation bar
- CSS styling for logo image (40x40px)

### 🌐 WEBSITE IMPACT

**supervertaler.com** now features:
- 10 feature cards (was 9) - PDF Rescue prominently displayed
- 7 documentation cards (was 6) - PDF Rescue Guide added
- Professional custom logo/icon
- Updated download links to v3.6.0-beta
- PDF Rescue highlighted in feature highlights

---

## [3.5.0-beta] - 2025-01-16 📄 PDF RESCUE MODULE

> **🚀 New Feature**: PDF Rescue - AI-Powered OCR Tool built into Supervertaler! Transform badly-formatted PDFs into clean, translator-ready documents using GPT-4 Vision.

### ✨ NEW FEATURE: PDF Rescue Module

**Complete AI-powered OCR solution for badly formatted PDFs!**

#### Core Features
- **📄 Direct PDF Import** - One-click page extraction using PyMuPDF (fitz)
  - Extracts pages at 2x resolution for optimal OCR quality
  - Saves images in `{pdf_name}_images/` folder next to source PDF
  - Persistent storage (not temp files) - client-deliverable images
  - Automatic PNG conversion and naming

- **🧠 GPT-4 Vision OCR** - Industry-leading AI-powered text extraction
  - Support for `gpt-4o`, `gpt-4o-mini`, and `gpt-4-turbo` models
  - Smart context-aware processing
  - Works with all languages supported by GPT-4 (100+)

- **🎨 Optional Formatting Preservation** - User-controlled markdown formatting
  - Checkbox toggle: "Preserve formatting (bold/italic/underline)"
  - AI outputs markdown: `**bold**`, `*italic*`, `__underline__`
  - Markdown converted to proper Word formatting during DOCX export

- **🔍 Smart Redaction Handling** - Language-aware placeholders
  - Detects blacked-out/redacted text automatically
  - Inserts contextual placeholders in document's language
  - No manual language specification needed!

- **📝 Stamp & Signature Detection** - Non-text element descriptions
  - Identifies stamps and signatures
  - Contextual descriptions in square brackets

#### Processing Features
- **⚡ Batch Processing** - Process entire documents at once
- **📊 Comprehensive Logging** - Full integration with parent app
- **👁️ Show Prompt Viewer** - Full transparency into AI instructions
- **📊 Professional Session Reports** - Comprehensive markdown documentation

#### Export Options
- **💾 DOCX Export** - Professional Word document output
- **📋 Copy to Clipboard** - Quick text extraction
- **📄 Session Report Export** - Professional documentation

#### Standalone Mode
- **🚀 Independent Operation** - Can run outside Supervertaler
  - Command: `python modules/pdf_rescue.py`

### 🔧 TECHNICAL IMPLEMENTATION

**Module**: `modules/pdf_rescue.py` (912 lines)
- **Dependencies**: OpenAI, tkinter, PyMuPDF (fitz), python-docx, PIL, re
- **API Integration**: OpenAI GPT-4 Vision API

---

## [3.1.0-beta] - 2025-10-10 🎯 PROMPT LIBRARY UPDATE

> **📌 Version Bump**: Bumped from v3.0.0-beta to v3.1.0-beta to reflect significant new feature and architectural change in prompt management system.

### ✨ NEW FEATURES

#### Unified Prompt Library
**Comprehensive prompt management system with two distinct prompt types!**

- **NEW: Custom Instructions** - User preferences and behavioral guidelines
  - Define HOW the AI should translate (tone, style, formatting preferences)
  - Examples: "Professional Tone", "Preserve Formatting", "Prefer TM Matches"
  - Separate from System Prompts (which define WHO the AI is)
  
- **NEW: Dual Prompt Type System**:
  - **🎭 System Prompts**: Define AI role/expertise (e.g., "Legal Specialist")
  - **📝 Custom Instructions**: Define user preferences/context (e.g., "Formal Tone")
  - Can combine both types for powerful, personalized workflows

- **NEW: Type Filtering**:
  - Radio buttons: All / System Prompts / Custom Instructions
  - Quick filtering in tree view
  - Sortable Type column

- **NEW: Dedicated "Prompt Library" Menu**:
  - Menu → Prompt Library → Open Prompt Library (Ctrl+P)
  - Keyboard shortcut: **Ctrl+P** for quick access

### 🗂️ FOLDER STRUCTURE CHANGES

**BREAKING CHANGE**: Unified folder structure across v2 and v3

- **New Structure**:
  ```
  user data/
  ├── System_prompts/          (public, Git-tracked)
  ├── System_prompts_private/  (private, Git-ignored)
  ├── Custom_instructions/     (public, Git-tracked)
  └── Custom_instructions_private/ (private, Git-ignored)
  ```

### 📦 EXAMPLE FILES

**3 Example Custom Instructions included**:
1. **Professional Tone & Style** - Ensures formal business language
2. **Preserve Formatting & Layout** - Maintains document structure
3. **Prefer Translation Memory Matches** - Prioritizes TM consistency

---

## [3.0.0-beta] - 2025-10-09 🚀 MAJOR RELEASE (CAT Editor)

> **📌 Version Renumbering**: This version was previously numbered v2.5.2. The jump to v3.0 reflects a **major architectural change** - a complete rewrite from the original DOCX workflow (v2.x-CLASSIC) to a segment-based CAT editor.

### ⚡ PERFORMANCE IMPROVEMENTS

#### Grid View Pagination System
**Major performance boost for large documents!**

- **NEW: Smart pagination** - Load only 50-100 segments at a time
- **Page size options**: 25, 50, 100, 200, or "All" segments per page
- **Navigation controls**: First / Prev / Next / Last buttons
- **Performance gain**: Grid view loads in ~0.5 seconds instead of 6-7 seconds
- **Benefits**: 10x faster grid view loading

#### Enhanced Loading Protection
**Prevents UI freezing during view switches**

- Loading screen with progress spinner
- Prevents clicks during grid population
- Smooth transitions between views

### 🎨 UI/UX IMPROVEMENTS

#### Smart Paragraph Detection
**Intelligent document flow in Document View**

- Groups consecutive sentences into paragraphs
- Detects paragraph boundaries (empty segments, headers)
- Natural reading experience
- Preserves document structure

#### Three Professional View Modes

1. **Grid View** (Professional Editing)
   - Spreadsheet-like grid with columns
   - Multi-selection support
   - Inline editing
   - Pagination for performance

2. **List View** (Vertical Reading)
   - Vertical stack of segment cards
   - Full text visible
   - Easy scrolling

3. **Document View** (Natural Reading)
   - Document-like presentation with paragraphs
   - Source and target side-by-side
   - Smart paragraph detection
   - Natural reading experience

### 📝 IMPORT/EXPORT FEATURES

**Flexible Data Exchange**:
- Import: DOCX, TXT, TSV, JSON (Supervertaler project data)
- Export: DOCX, TSV, TMX, XLIFF, Excel, Session Reports (MD/HTML)
- Auto-export options for automated workflows

**CafeTran & memoQ Support**:
- Import/export bilingual DOCX files
- Formatting preservation (AI-based for CafeTran, programmatic for memoQ)
- Complete round-trip workflow

### 🎯 CAT TOOL FEATURES

**Professional Translation Editor**:
- Status tracking (✗ Untranslated / ~ In Progress / ✓ Translated / ✓✓ Reviewed / 🔒 Locked)
- Segment types (Text / Heading / Caption / etc.)
- Style preservation
- Find/Replace functionality
- Bulk operations (translate selected, lock/unlock, change status)

**Translation Memory**:
- TMX import/export
- Fuzzy matching with configurable threshold
- TM matches displayed during translation

**Figure Context**:
- Multimodal AI support (GPT-4 Vision, Claude Vision, Gemini Vision)
- Auto-detects figure references in text
- Includes images in AI prompts for technical translations

---

## Version History Summary

- **v3.6.0-beta** (2025-01-16): PDF Rescue documentation + website updates
- **v3.5.0-beta** (2025-01-16): PDF Rescue module
- **v3.1.0-beta** (2025-10-10): Unified Prompt Library
- **v3.0.0-beta** (2025-10-09): Initial CAT Editor release with pagination

---

**For detailed version history and minor updates**, see the main [CHANGELOG.md](CHANGELOG.md).
