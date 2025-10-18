# Supervertaler CAT Edition - Changelog

**Version Branch**: v3.x.x-beta (Experimental CAT Editor)

This changelog tracks changes specific to the **CAT Edition** of Supervertaler - the experimental segment-based CAT editor with advanced features.

For the Classic Edition changelog, see [CHANGELOG-CLASSIC.md](CHANGELOG-CLASSIC.md).  
For the unified changelog, see [CHANGELOG.md](CHANGELOG.md).

---

## [3.6.6-beta] - 2025-10-18 🤖 PROMPT ASSISTANT: REORGANIZATION & RENAMING

### 🎯 MAJOR UX IMPROVEMENTS

**Renamed "AI Assistant" to "Prompt Assistant"** 📝:
- **Better Name**: "Prompt Assistant" accurately describes its purpose (analyzing documents and generating prompts)
- **Clearer Focus**: Distinguishes from general-purpose AI chatbots
- **Professional Branding**: More specific and professional terminology

**Moved to Prompt Library as Third Tab** 📚:
- **Old Location**: Separate panel in Assistant sidebar (cluttered)
- **New Location**: Third tab inside Prompt Library (System Prompts | Custom Instructions | **Prompt Assistant**)
- **Logical Grouping**: All prompt-related features now consolidated in one place
- **Better Workflow**: Analyze → Generate → Browse/Edit → Apply (complete prompt ecosystem)
- **Space Efficient**: Reduces sidebar clutter, saves screen real estate
- **Natural Discovery**: Users find it when working with prompts

**Smart Editor Panel Visibility** 🎨:
- **Auto-Hide**: Editor panel automatically hides when Prompt Assistant tab is active
- **Full Width**: Gives you maximum workspace for document analysis and prompt generation
- **Auto-Show**: Editor reappears when switching to System Prompts or Custom Instructions tabs
- **Context-Aware**: UI adapts based on what you're doing (generating vs editing)

**Technical Changes**:
- **Removed**: AI Assistant from sidebar panel list (lines ~1957-1966)
- **Added**: Prompt Assistant as third tab in Prompt Library notebook (line ~2529)
- **Renamed**: `create_ai_assistant_tab()` → `create_prompt_assistant_content()`
- **Added**: Dynamic editor panel visibility in `_pl_on_tab_changed()` handler
- **Updated**: All UI labels, tooltips, comments, and error messages
- **Updated**: Header text from "🤖 AI Assistant (Beta)" to "🤖 Prompt Assistant"
- **Updated**: Subtitle to "Analyze your document and generate optimized translation prompts automatically"
- **Preserved**: All functionality (document analysis, prompt generation, chat interface)

**Benefits**:
- ✨ **Better Organization**: Related features grouped logically
- ✨ **Clearer Purpose**: Name describes what it does
- ✨ **Improved Discovery**: Natural place to find when working with prompts
- ✨ **Space Efficiency**: One less sidebar panel, full-width workspace when generating
- ✨ **Intuitive Workflow**: Complete prompt workflow in one location
- ✨ **Context-Aware UI**: Interface adapts to your current task

---

## [3.6.5-beta] - 2025-10-17 🎯 AI ASSISTANT: INTELLIGENT GLOSSARY GENERATION

### 🔧 CRITICAL IMPROVEMENTS TO AI ASSISTANT

**Replaced Naive Terminology Extraction with LLM-Powered Analysis** 🧠:

**PROBLEM IDENTIFIED**: Previous regex-based terminology extraction was producing garbage results:
- Extracted common words like articles ("De", "In", "Deze", "Een") as "technical terms"
- Listed section headers ("BESCHRIJVING", "FIGUREN") as "acronyms"
- Provided useless glossaries that professional translators couldn't use
- No linguistic intelligence - just pattern matching

**NEW APPROACH**: Send actual document content to LLM for intelligent analysis:
- **Full Document Context**: Sends up to 8,000 words of actual source text to LLM
- **Professional Translator Prompt**: Uses proven successful prompt pattern from real workflow:
  - "You are a professional patent translator, working between [source] and [target]"
  - Explicit instructions to IGNORE common words, articles, pronouns, section headers
  - Focus on technical terms, specialized vocabulary, domain-specific concepts
  - For patents: extract claimed elements, technical features, components
- **Bilingual Glossary Output**: LLM provides structured markdown table:
  - Source term | Target equivalent | Context notes
  - 15-25 most important terms (quality over quantity)
  - Contextual explanations for each term
- **Smart Filtering**: LLM naturally understands:
  - What is a technical term vs common word
  - Domain-specific vocabulary (medical, legal, patent, technical)
  - Multi-word technical expressions and compound terms
  - Language-specific patterns (Dutch compounds, German separable verbs, etc.)

**Technical Changes**:
- **Modified**: `analyze_current_document()` in main application
  - Now sends full document text to configured LLM (OpenAI/Claude/Gemini)
  - Uses temperature 0.3 for focused, consistent analysis
  - max_tokens=2000 to accommodate detailed glossary
  - Respects source/target language configuration
- **Modified**: `process_assistant_query()` context building
  - Now references complete LLM analysis text instead of regex results
  - Passes bilingual glossary context to subsequent chat questions
  - AI can reference its own analysis when answering questions
- **Modified**: `get_prompt_suggestion()` 
  - Now asks LLM for Supervertaler feature recommendations
  - Suggests specific tools: system prompts, glossaries, TM, figure context
- **Removed**: Dependency on `document_analyzer.py` regex patterns (still exists for fallback)

**Real-World Validation**:
Compared with successful ChatGPT.com workflow on Belgian Dutch patent (PVET.docx):
- ✅ ChatGPT produced: "voegplaat", "verankeringsrib", "deuvel", "wegdelen" (actual technical terms)
- ❌ Old Supervertaler produced: "De", "In", "Deze", "BESCHRIJVING" (garbage)
- ✅ New Supervertaler: Uses same LLM intelligence as ChatGPT workflow

**User Benefits**:
- 🎯 **Professional-Grade Glossaries**: Actual usable terminology for translation work
- ⚡ **Matches External Tools**: Same quality as ChatGPT.com but integrated into workflow
- 🌍 **Language-Aware**: Works with any language pair (Dutch-English, German-French, etc.)
- 📋 **Ready to Use**: Copy glossary directly into translation memory or glossary files
- 🔄 **Consistent Workflow**: No need to switch to external tools for analysis

**Configuration Requirements**:
- Must have LLM API key configured (OpenAI, Claude, or Gemini)
- Document must be loaded with segments
- Source and target languages should be set correctly

---

## [3.6.4-beta] - 2025-10-17 🤖 AI ASSISTANT PHASE 2: DOCUMENT-AWARE INTELLIGENCE

### ✨ MAJOR NEW FEATURE

**AI Assistant with Document Analysis** 🤖:
- **NEW TAB**: "🤖 AI Assistant" added to main workspace (between Images and PDF Rescue)
- **Smart Document Analysis**: Automatically examines your loaded document to detect:
  - **Domain Detection**: Identifies 6 domains (medical, legal, technical, patent, marketing, financial)
  - **Terminology Extraction**: Finds capitalized terms, acronyms, technical vocabulary
  - **Tone Assessment**: Analyzes formality and style (formal, informal, technical, conversational)
  - **Structure Analysis**: Detects lists, headings, figure references, document organization
  - **Special Elements**: Identifies URLs, emails, dates, measurements, currencies, percentages
  - **Statistics**: Word counts, segment counts, unique terms with averages
- **Actionable Recommendations**: AI generates prioritized suggestions based on analysis:
  - Domain-specific prompt optimization
  - Tone preservation instructions
  - Visual context recommendations (when figures detected)
  - Formatting rules (measurements, currencies)
  - Terminology management advice
- **Conversational Chat Interface**: Ask the AI questions about your document:
  - "What type of document is this?"
  - "Should I use a glossary?"
  - "What's the best prompt for this content?"
  - "Check terminology patterns"
- **Context-Aware Responses**: AI uses document analysis data to provide relevant, specific advice
- **Chat History**: Maintains conversation flow with last 10 exchanges for coherent dialogue
- **Quick Action Buttons**: Pre-configured questions for common tasks:
  - 💡 Suggest better prompt
  - 🔍 What domain is this?
  - ✨ Check terminology
- **Multi-LLM Support**: Works with OpenAI, Anthropic Claude, and Google Gemini
- **Comprehensive Reporting**: Detailed analysis summary with confidence scores

**Technical Implementation**:
- **New Module**: `document_analyzer.py` (500 lines)
  - Domain detection algorithm with 300+ keywords
  - Pattern recognition for technical formats
  - Confidence scoring system
  - Smart suggestion generation engine
- **Integration**: Seamlessly integrated into main workspace
- **Performance**: Fast analysis (completes in seconds)
- **Privacy**: All analysis happens locally (only LLM API calls go external)

**User Benefits**:
- ⚡ **Faster Setup**: Analyze document in seconds vs manual assessment
- 🎯 **Better Quality**: AI suggests optimal settings for specific content
- 📚 **Learning Tool**: Understand document characteristics instantly
- 🔄 **Workflow Integration**: No need to switch windows or interrupt work
- 💡 **Data-Driven**: Recommendations based on actual content analysis, not guesswork

**Example Workflow**:
1. Load your document (DOCX, TSV, bilingual file)
2. Open AI Assistant tab
3. Click "🔍 Analyze Document"
4. Review comprehensive analysis (domain, tone, terminology, structure)
5. Click "📝 Get Prompt Suggestion" for actionable recommendations
6. Chat with AI for specific questions or guidance
7. Implement suggestions to optimize translation setup

---

## [3.6.3-beta] - 2025-10-17 🔧 CRITICAL FIXES & NEW FEATURES

### 🐛 CRITICAL BUG FIXES

**Fixed Custom Instructions Integration (CRITICAL)**:
- **Issue**: Custom Instructions were displayed as "active" but were **never actually used during translation**
- **Root Cause**: `get_context_aware_prompt()` stored Custom Instructions in `self.active_custom_instruction` but never checked for or appended them to the system prompt
- **Impact**: Users believed their Custom Instructions were being applied, but they were completely ignored by the AI
- **Fix**: Modified `get_context_aware_prompt()` to check for active Custom Instructions and append them with markdown heading:
  ```python
  if hasattr(self, 'active_custom_instruction') and self.active_custom_instruction:
      combined_prompt = base_prompt + "\n\n# CUSTOM INSTRUCTIONS\n\n" + self.active_custom_instruction
  ```
- **Verification**: Preview Prompt now shows the complete combined prompt that will be sent to the AI

**Fixed Preview Prompt AttributeError**:
- **Issue**: Clicking "Preview Prompt" button crashed with `AttributeError: 'Supervertaler' object has no attribute 'custom_instructions_text'`
- **Root Cause**: Old code tried to access removed widget from previous architecture
- **Fix**: Changed to call `get_context_aware_prompt()` which properly combines System Prompt + Custom Instructions
- **Bonus**: Preview now shows actual combined prompt with composition breakdown (names + character counts)

**Fixed Extract Images Auto-Load Bug**:
- **Issue**: After extracting images from DOCX, clicking "Yes" to auto-load caused `AttributeError: 'FigureContextManager' object has no attribute 'load_folder'`
- **Root Cause**: Called wrong method name `load_folder()` instead of `load_from_folder()`
- **Fix**: Changed to correct method and captured loaded count for accurate feedback

### ✨ NEW FEATURES

**Recent Projects Menu** 🕒:
- **Quick Access**: New "Recent Projects" submenu in Project menu
- **Last 10 Projects**: Automatically tracks and displays your most recent projects
- **Smart Filtering**: Auto-removes projects whose files no longer exist
- **Persistent Storage**: Saved in `user data/recent_projects.json`
- **Clear Option**: "Clear Recent Projects" option to reset the list
- **Location**: Project menu → Recent Projects (between Open and Close)

**Extract Images from DOCX** 📤:
- **Automated Extraction**: Extract all images from DOCX files with one click
- **Smart Naming**: Automatically detects figure references in document text
  - Multilingual support: Figure, Fig., Figuur, Abbildung, Figura, 图, etc.
  - Pattern examples: "Figure 1", "Fig. 2A", "Figuur 3", "Abbildung 4"
- **Natural Sorting**: Correctly orders Figure 1, 2, ..., 10 (not 1, 10, 2)
- **Fallback Naming**: Uses sequential numbering if no figure references found
- **Auto-Load Option**: Optionally load extracted images as Figure Context immediately
- **Dual Access**: Available in both:
  - Resources menu → "📤 Extract images from DOCX..."
  - Images tab (AI Assistant) → "📤 Extract from DOCX..." button
- **Technical**: Uses python-docx to read DOCX (ZIP format) and PIL to process images

**Active Prompts Persistence** 💾:
- **Project Memory**: Active System Prompts and Custom Instructions now saved with projects
- **Automatic Restoration**: When loading a project, all active prompts are restored:
  - Translation System Prompt
  - Proofreading System Prompt
  - Custom Instructions (both name and full content)
- **UI Updates**: Active prompt labels automatically update to show restored prompts
- **Logging**: Confirms which prompts were restored in console
- **Workflow**: Set up prompts once, reload project anytime with full context preserved

**Clear Custom Instructions Button** ✖️:
- **Deactivation**: Red "✖ Clear" button next to green "✅ Use in Current Project"
- **Clean Reset**: Clears `active_custom_instruction` and updates label to "None"
- **Use Case**: Quickly remove Custom Instructions without switching projects

### 🎨 UI ENHANCEMENTS

**Markdown Headings in Prompts**:
- **System Prompts**: All three templates now start with `# SYSTEM PROMPT\n\n`
- **Custom Instructions**: Appended with `# CUSTOM INSTRUCTIONS\n\n` heading
- **Clarity**: Makes prompt structure immediately visible in Preview and AI logs
- **Consistency**: Uniform formatting across all prompt types

**Enhanced Tab Visual Distinction**:
- **System Prompts Tab**: Light blue background (#E3F2FD) with darker blue filter bar (#BBDEFB)
- **Custom Instructions Tab**: Light green background (#E8F5E9) with darker green bars (#C8E6C9)
- **Solid Borders**: Clear visual separation between tabs
- **Color Coding**: Matches active label colors for intuitive association

**Images Tab Button**:
- **New Button**: "📤 Extract from DOCX..." in blue (#2196F3)
- **Better Discoverability**: Feature now accessible directly from Images tab
- **Logical Placement**: Between "📁 Load figure context..." and "🗑️ Clear"

### 🔧 TECHNICAL IMPROVEMENTS

**Code Architecture**:
- Added `from docx import Document` import to extract_images_from_docx()
- Fixed emoji encoding issues in menu items and buttons
- Improved error handling in image extraction process
- Better logging for prompt restoration and image loading

**Methods Modified**:
- `get_context_aware_prompt()`: Now actually includes Custom Instructions
- `preview_combined_prompt()`: Shows real combined prompt via get_context_aware_prompt()
- `save_project()`: Saves active_translate_prompt_name, active_proofread_prompt_name, active_custom_instruction, active_custom_instruction_name
- `load_project_from_path()`: Restores all active prompts and updates UI labels
- `extract_images_from_docx()`: Fixed method call from load_folder() to load_from_folder()

**New Functions**:
- `load_recent_projects()`: Loads and filters project list from JSON
- `save_recent_projects()`: Persists recent projects to JSON
- `add_recent_project()`: Adds project to top of list, removes duplicates, keeps max 10
- `update_recent_projects_menu()`: Populates menu with numbered items
- `clear_recent_projects()`: Empties list and updates menu
- `_pl_clear_custom_instruction()`: Deactivates Custom Instructions

### 🎯 USER IMPACT

**Critical**: Custom Instructions now actually work! Previous versions displayed them as active but never used them.

**Workflow Improvements**:
- Projects fully preserve your prompt setup
- Recent Projects saves time opening frequently-used projects
- Extract Images streamlines visual context setup for technical translations
- Clear Custom Instructions provides quick reset option

**Better Visibility**:
- Preview Prompt shows exactly what the AI receives
- Markdown headings clarify prompt structure
- Tab colors help distinguish prompt types
- Images tab button makes extraction more discoverable

---

## [3.6.2-beta] - 2025-10-16 ✨ PROMPT LIBRARY UI IMPROVEMENTS

### ✨ ENHANCEMENTS

**Improved Prompt Library Active Bar Labels**:
- **Enhanced Clarity**: Updated active prompt display labels for better readability
  - **Before**: `Active: | Trans: Default | Proof: Default | Custom: xyz`
  - **After**: `Active: | Translation system prompt: Default | Proofreading system prompt: Default | Custom instructions: xyz`
- **Better User Understanding**: Full descriptive labels eliminate confusion about what each active prompt represents
- **Consistent Terminology**: Aligns with user-facing terminology throughout the application

**Simplified Custom Instructions Workflow**:
- **Activation Model**: Custom Instructions now work like System Prompts
  - Single button: "✅ Use in Current Project" (green, bold)
  - Stores content in `self.active_custom_instruction`
  - Updates active label: "Custom instructions: [name]"
- **Removed Confusion**: Eliminated misleading "Load into Settings Tab" button (that tab doesn't exist in toolbar)
- **Clear Behavior**: Custom Instructions are automatically appended to System Prompts during translation
- **Visual Feedback**: Green label shows active Custom Instruction name or "None"

### 🎯 USER IMPACT

- **Clearer UI**: Users immediately understand what each active prompt does
- **Simpler Workflow**: Custom Instructions activation matches System Prompts (no special loading required)
- **Better Discoverability**: Descriptive labels help new users understand the feature

---

## [3.6.1-beta] - 2025-10-16 🐛 CAT IMPORT BUGFIX

### 🐛 BUG FIXES

**Fixed AttributeError on CAT Import at Startup**:
- **Issue**: Importing memoQ, CafeTran, or Trados bilingual tables at application startup caused `AttributeError: 'Supervertaler' object has no attribute 'grid_inner_frame'`
- **Root Cause**: Grid layout (`grid_inner_frame`) was only created during manual layout switching, not during initial import
- **Fix**: Added automatic grid layout initialization when importing files before grid is created
  - `load_segments_to_grid()` now checks if `grid_inner_frame` exists
  - If missing, creates grid layout and clears start screen automatically
  - Ensures consistent behavior whether importing via menu or at startup
- **Impact**: All three CAT import formats (memoQ, CafeTran, Trados) now work reliably on first import
- **Files Modified**: `Supervertaler_v3.6.0-beta_CAT.py` (lines 11041-11048)

### 📝 TECHNICAL DETAILS

**Changes to `load_segments_to_grid()` method**:
```python
# Before loading segments, ensure grid layout exists
if not hasattr(self, 'grid_inner_frame'):
    # Clear content frame (remove start screen if present)
    for widget in self.content_frame.winfo_children():
        widget.destroy()
    self.create_grid_layout()
```

This fix ensures the grid UI is properly initialized before attempting to populate it with segments, preventing crashes when importing CAT files at application startup.

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
