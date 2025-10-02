# Supervertaler - Changelog

## [2.5.0-prototype-v0.3.2] - 2025-10-02 (Style Preservation Update)

### Added
- **Style Preservation on Export** (Phase B) - Complete Word style preservation
  - All paragraph styles preserved: Title, Subtitle, Heading 1-3, Normal, custom styles
  - Works for both regular paragraphs and table cells
  - Modified `_replace_paragraph_text()` to accept and apply styles
  - Modified `_replace_paragraph_with_formatting()` for style support
  - Graceful error handling when style doesn't exist in template
  - Professional output documents with correct formatting hierarchy

### Fixed
- **Missing Subtitle Bug** (Critical) - Object identity comparison fix
  - Changed table paragraph filtering from object IDs to actual objects
  - Fixed Python memory address reuse causing false positives
  - Subtitle and other paragraphs no longer skipped during import
  - Reliable object comparison prevents silent data loss
  - All document content now imported correctly

### Technical Details
- **Updated**: `docx_handler.py` (Lines 75-95, 258-316, 318-382, 197-215, 227-241)
  - Table filtering uses `table_paragraphs` set (objects) instead of IDs
  - `_replace_paragraph_text()` now applies original style parameter
  - `_replace_paragraph_with_formatting()` applies style after creating runs
  - `export_docx()` passes original styles during paragraph replacement
- **Documentation**: `PHASE_B_STYLE_PRESERVATION.md`, `BUGFIX_MISSING_SUBTITLE.md`

### Benefits
- ✅ Exported documents maintain professional appearance
- ✅ No manual reformatting needed after translation
- ✅ Document structure and hierarchy preserved
- ✅ All content imported reliably (no data loss)

---

## [2.5.0-prototype-v0.3.1] - 2025-10-02 (Style Visibility Update)

### Added
- **Style Visibility** (Phase A) - Display Word styles in grid
  - New "Style" column showing paragraph styles (Heading 1-3, Title, Normal, etc.)
  - Color-coded headings for visual hierarchy:
    - Heading 1: Dark blue (bold)
    - Heading 2: Medium blue
    - Heading 3: Light blue
    - Title: Purple (bold)
    - Subtitle: Purple (italic)
  - Helper methods: `_format_style_name()`, `_get_style_tag()`
  - Grid expanded to 6 columns: ID, Type, Style, Status, Source, Target

### Fixed
- **Column Misalignment Bug** (Critical)
  - `update_segment_in_grid()` was passing 4 values to 6-column grid
  - Now correctly passes all 6 values in proper order
  - Column widths configured with `minwidth` and `stretch` properties
  - Source and target text now appear in correct columns after save

### Technical Details
- **Updated**: `cat_editor_prototype.py`
  - Lines ~37-56: Added `style` parameter to Segment class
  - Lines ~186-203: Treeview configured for 6 columns
  - Lines ~218-223: Visual tags for heading styles
  - Lines ~508-533: Fixed `update_segment_in_grid()` value count
- **Documentation**: `PHASE_A_COMPLETE.md`, `BUGFIX_COLUMN_MISALIGNMENT.md`
- **Test Script**: `test_style_support.py` (44 segments with 7 different styles)

### Benefits
- ✅ Visual document structure in grid
- ✅ Easier to maintain document hierarchy
- ✅ Color-coded headings improve readability
- ✅ Grid updates correctly after translation

---

## [2.5.0-prototype-v0.3.0] - 2025-10-02 (Table Support Update)

### Added
- **Table Support** (Phase 0.1) - Full table cell segmentation
  - Table cells imported as individual segments
  - Each cell identified as T{table}R{row}C{col} (e.g., T1R2C3)
  - "Type" column in grid showing "Para" or "T#R#C#"
  - Table cells translatable independently
  - Export reconstructs tables with translations
  - Enhanced `ParagraphInfo` with table metadata
  - Grid expanded to 5 columns: ID, Type, Status, Source, Target

### Fixed
- **Table Cell Duplication Bug** (Critical)
  - python-docx `document.paragraphs` includes table cell paragraphs
  - Created filtering system to prevent duplicate processing
  - Build `table_paragraph_ids` set for filtering
  - Process regular paragraphs first, then table cells separately
  - No more duplicate segments in grid

### Technical Details
- **Updated**: `docx_handler.py` (Lines 70-140, 220-241, 247-261)
  - Enhanced import to extract table cells with position tracking
  - Export reconstructs tables by finding cells using metadata
  - Helper methods: `_get_para_info()`, `_find_table_cell_info()`
- **Updated**: `cat_editor_prototype.py` (Lines ~186-203, ~377-401)
  - Grid configured for 5 columns with Type column
  - Display type labels clearly (Para vs T#R#C#)
- **Documentation**: `PHASE_0.1_COMPLETE.md`, `BUGFIX_TABLE_DUPLICATION.md`
- **Test Script**: `test_table_support.py` (26 segments: 8 para + 18 table cells)

### Benefits
- ✅ Professional documents with tables can be translated
- ✅ Clear indication of segment origin
- ✅ Table structure preserved on export
- ✅ Each cell is independent segment

---

## [2.5.0-prototype-v0.2.0] - 2025-10-01 (Feature Update)

### Added
- **Inline Formatting Tags**: Full support for bold, italic, and underline preservation
  - Automatic extraction of run-level formatting from DOCX import
  - XML-like tags display in editor (<b>, <i>, <u>, <bi> for bold+italic)
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

## [2.5.0-prototype-v0.1.1] - 2025-10-01 (Hot Fix)

### Fixed
- **DOCX Export Issues**: Corrected paragraph matching and whitespace handling
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

## [2.5.0-prototype] - 2025-10-01

### Added
- **CAT Editor Prototype**: Standalone Computer-Aided Translation editor (experimental)
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

### Technical Details (Prototype)
- **New Modules**:
  - `cat_tool_prototype/cat_editor_prototype.py` - Main application (800+ lines)
  - `cat_tool_prototype/simple_segmenter.py` - Sentence segmentation engine
  - `cat_tool_prototype/docx_handler.py` - DOCX import/export with formatting
  - `cat_tool_prototype/README.md` - Complete documentation
  - `cat_tool_prototype/QUICK_START.md` - Quick start guide
- **Dependencies**: python-docx, lxml (installed)
- **Architecture**: Standalone prototype for testing before main integration
- **Status**: Experimental - Testing phase before v2.5.0 integration

### Planned (For Main Integration)
- SRX-based segmentation rules
- Translation memory integration with existing TMAgent
- AI translation using existing translation agents (Gemini, Claude, OpenAI)
- Custom prompts integration
- Advanced tag handling for inline formatting
- Table cell segmentation
- Quality assurance checks
- Concordance search
- Auto-propagation of repeated segments

## [2.4.1] - 2025-10-01

### Added
- **Private Projects Support**: Enhanced project management with public/private separation
  - "Save to Private Folder" checkbox for projects
  - Automatic `projects_private/` folder creation for confidential projects
  - `[Private]` prefix clearly identifies private projects in project library
  - Private projects never synced to GitHub (gitignore protection)
  - Seamless integration with existing project management interface
- **Private Custom Prompts UI Enhancement**: Improved custom prompts interface
  - "Save to Private Folder" checkbox integrated into custom prompts management
  - Automatic folder selection based on privacy preference
  - Visual indication of private prompts with `[Private]` prefix
  - Consistent privacy handling across application features

### Fixed
- **Project Loading**: Fixed project file path resolution for private projects
  - Correctly loads projects from both public and private folders
  - Proper handling of `[Private]` prefix in project names
  - Prevents "File Not Found" errors when switching between public/private projects
- **Project Deletion**: Fixed deletion functionality for private projects
  - Correctly identifies private project location for deletion
  - Properly removes files from `projects_private/` folder
  - Maintains deletion confirmation dialog for safety
- **Custom Prompts Selection**: Improved prompt selection UI behavior
  - Automatically updates privacy checkbox when selecting prompts
  - Correctly removes `[Private]` prefix from name field for editing
  - Maintains consistency between prompt name display and storage

### Changed
- **Project Library**: Enhanced project listing to show all projects from both folders
  - Combined view of public and private projects in single list
  - Alphabetically sorted project list regardless of folder
  - Clear visual distinction between public and private projects

## [2.4.0] - 2025-09-14

### Added
- **GPT-5 Support**: Full compatibility with OpenAI's GPT-5 model
  - Automatic parameter detection (`max_completion_tokens` vs `max_tokens`)
  - Temperature parameter compatibility (GPT-5 uses default temperature)
  - Reasoning effort control (`reasoning_effort="low"`) to optimize token usage
  - Dynamic token limits based on segment count (up to 50K tokens for large jobs)
  - Automatic cleanup of GPT-5's double-numbering output format
- **Switch Languages Button**: New GUI feature for quick language pair switching
  - One-click swap between source and target languages
  - Convenient placement next to language input fields
  - Clear "⇄ Switch languages" label for intuitive use
- **Enhanced Debugging**: Comprehensive GPT-5 diagnostic system
  - Detailed API response analysis (finish reason, usage statistics, content validation)
  - Token usage breakdown (reasoning tokens vs output tokens)
  - Simple test request fallback for troubleshooting
- **Session Reporting**: Comprehensive markdown reports generated alongside translation outputs
  - Captures complete AI prompts sent to providers (system prompts, custom prompts, custom instructions)
  - Records all session settings (provider, model, languages, file paths, etc.)
  - Documents processing statistics and context data
  - Saved as `[output_filename]_report.md` for transparency and reproducibility

### Fixed
- **GPT-5 Compatibility Issues**: Resolved multiple compatibility problems
  - Fixed empty response issue due to insufficient token allocation
  - Resolved "max_tokens" parameter error (now uses "max_completion_tokens")
  - Fixed temperature parameter incompatibility 
  - Corrected double-numbering in translation output format
- **API Parameter Handling**: Improved parameter detection for different OpenAI models
  - Dynamic parameter selection based on model capabilities
  - Proper error handling for unsupported parameters
- **Proofreading Output Format**: Comprehensive fixes for professional CAT tool integration
  - Fixed doubled line count issue in proofreading output (proper 1:1 line mapping)
  - Resolved GPT-5 proofreading parameter conflicts and format parsing
  - Enhanced comment formatting to remove embedded newlines that broke tab-separated format
  - Improved extraction of corrected text vs explanatory comments for proper column separation
- **Gemini Proofreading Agent**: Fixed critical API format incompatibility
  - Corrected message format from OpenAI-style to proper Gemini SDK format
  - Resolved dictionary format errors that prevented Gemini proofreading from working
- **OpenAI Proofreading Agent**: Enhanced response parsing for GPT-5
  - Added intelligent text extraction to separate corrected text from explanations
  - Improved handling of various correction patterns ("corrected X to Y", "rephrased to X", etc.)
  - Smart detection of substantial corrections vs brief explanations

### Changed
- **Token Management**: Smarter token allocation strategy for reasoning models
  - GPT-5 now gets 32K-50K tokens based on content size vs previous 2K limit
  - Reasoning token overhead properly accounted for in calculations
- **Output Formatting**: Cleaner translation output format
  - GPT-5 translations now match input format (no unwanted line numbers)
  - Automatic cleanup of redundant numbering patterns

### Fixed
- **UnboundLocalError**: Fixed variable scoping issue with `img_added` in OpenAI translation function
  - Proper initialization of `img_added` variable at start of each loop iteration
  - Prevents crashes when processing patent translations with image context
- **Session Report Generation**: Fixed `tm_f` undefined variable error in report generation
  - Added `tm_file` parameter to `run_pipeline` method signature
  - Properly pass translation memory file path through threading call
  - Ensures session reports generate successfully without variable scoping errors
- **GPT-5 API Compatibility**: Fixed "Unsupported parameter" errors for GPT-5 and newer OpenAI models
  - Automatically detects model type and uses correct token parameter (`max_completion_tokens` vs `max_tokens`)
  - Handles temperature parameter restrictions (GPT-5 only supports default temperature of 1.0)
  - Maintains backward compatibility with older OpenAI models (GPT-4, GPT-3.5, etc.)
  - Prevents both "max_tokens" and "temperature" API errors when using GPT-5
- **GPT-5 Translation Format**: Improved response parsing for GPT-5's different output format
  - Enhanced system prompt with more explicit formatting instructions for GPT-5
  - Added multiple regex patterns to handle various numbering formats (1., 1), 1:)
  - Added debug logging to diagnose GPT-5 response format issues
  - Resolves "Missing TL line" placeholder issues when using GPT-5
- **Session Report Enhancement**: Updated report to show all output files generated
  - Now explicitly lists TXT, TMX, and markdown report files with their purposes
  - Provides complete transparency of all files created during translation sessions
- (Planned) Edge cases for very long / compound figure identifiers
- (Planned) Graceful handling of partially corrupt TMX files

## 2.3.0 — 2025-09-08
- **MAJOR UPDATE**: Revolutionary Project Management System
- **NEW: Project Library** - Complete workspace configuration management:
  - Save entire application state: languages, providers, models, file paths, prompts
  - JSON-based project storage in local `projects/` folder
  - Cross-platform project management (Windows, macOS, Linux)
  - Instant project switching and workspace restoration
  - Professional project organization with timestamps
- **NEW: Domain-Specific Custom Prompt Collections** - Professional prompt libraries:
  - Medical Translation Specialist: Patient safety, medical terminology, regulatory compliance
  - Legal Translation Specialist: Juridical precision, legal system differences, formal register
  - Financial Translation Specialist: Banking terminology, regulatory compliance, market conventions
  - Technical Translation Specialist: Engineering precision, safety warnings, technical documentation
  - Cryptocurrency & Blockchain Specialist: DeFi protocols, Web3 terminology, security considerations
  - Gaming & Entertainment Specialist: Cultural adaptation, character voice, user experience optimization
- **NEW: Private Custom Prompts Support** - Confidential prompt management:
  - `custom_prompts_private/` folder for sensitive/proprietary prompts
  - Never synced to GitHub (gitignore protection)
  - Perfect for client-specific, confidential, or company proprietary prompts
  - Seamlessly integrated with existing prompt library interface
  - [Private] prefix clearly identifies confidential prompts in UI
- **FIXED: OpenAI Integration** - Complete OpenAI support implementation:
  - Fully implemented OpenAITranslationAgent and OpenAIProofreadingAgent
  - Fixed "Translator model init failed" error when using OpenAI provider
  - Complete feature parity with Gemini and Claude (multimodal, tracked changes, custom prompts)
  - Support for all OpenAI models including latest GPT-5 (September 2025 release)
  - Proper error handling and logging throughout OpenAI integration
- **FIXED: Custom Prompt Loading Issues** - JSON structure compatibility:
  - Resolved custom prompt loading failures for domain-specific prompts
  - Standardized JSON structure across all custom prompt files
  - Converted nested "prompts" format to flat "translate_prompt"/"proofread_prompt" format
  - All 8 domain-specific prompt collections now load correctly
- **ENHANCED: Documentation Structure** - Streamlined user guide:
  - Consolidated separate Quick Start Guide into main User Guide
  - Removed redundant "Quick Start" section while preserving valuable content
  - Renamed main navigation from "Table of Contents" to "Reading Guide" for clarity
  - Integrated practical walkthroughs into "Getting Started" section
  - Fixed table of contents references and emoji encoding issues
- **ENHANCED: Library Structure Reorganization**:
  - Renamed "Advanced System Prompts" to "Prompt Library" for clarity
  - Clear hierarchy: Prompt Library → Custom Prompt Library → Project Library
  - Consistent iconography and user experience across all library sections
- **NEW: Clickable Folder Paths** - Direct file system access:
  - Click folder paths to open directories in system file manager
  - Cross-platform support with proper error handling
  - Easy access to custom prompts and project files for backup/sharing
- **IMPROVED: User Interface Polish**:
  - Lightning bolt indicators (⚡) for active prompts
  - Consistent visual design across all expandable sections
  - Enhanced tooltips and status indicators
- **TECHNICAL: Enhanced Project Data Structure**:
  - Complete state serialization including custom instructions
  - Robust error handling for project save/load operations
  - Backward compatibility with existing prompt library

## 2.2.0 — 2025-09-08
- **MAJOR UPDATE**: Bumped to version 2.2.0 with comprehensive GUI improvements and new prompt management system
- **NEW: Custom Prompt Library** - Revolutionary prompt management system:
  - Save and organize custom system prompt sets in local `custom_prompts/` folder
  - Load and switch between different prompt templates instantly
  - Browse prompt library with intuitive selection interface
  - Delete unwanted prompt sets with confirmation dialogs
  - Automatic JSON file organization with timestamps and metadata
  - Seamless integration with Advanced System Prompts interface
  - Perfect for creating specialized prompts for different document types or use cases
- **Enhanced GUI Design**:
  - Complete 3-panel resizable layout matching user specifications
  - Consistent white backgrounds throughout all sections
  - Sharp, professional font rendering using Segoe UI family
  - Enhanced heading fonts with increased sizes (16pt title, 12pt section headers)
  - Optimized panel sizes: larger information panel (700px), compact log panel (200px)
  - Improved visual hierarchy and professional appearance
- **Advanced System Prompts Enhancements**:
  - Added third "📁 Prompt Library" tab for comprehensive prompt management
  - Enhanced font clarity and consistency across all tabs
  - Improved button layouts with proper background colors
  - Better user experience with selection memory and visual feedback

## 2.1.1 — 2025-09-05
- Bumped app version to 2.1.1 (APP_VERSION and header banner updated).
- **NEW: Advanced System Prompts GUI** - Added collapsible section allowing users to:
  - View and edit underlying system prompts for Translation and Proofreading modes
  - Use template variables like `{source_lang}` and `{target_lang}`
  - Preview final prompts with current language settings
  - Reset prompts to defaults with one click
  - Organize prompts in tabbed interface (Translation/Proofreading)
  - Click section header to expand/collapse for easy access
- **NEW: Custom Prompt Library** - Added comprehensive prompt management system:
  - Save custom system prompt sets to local files (`custom_prompts/` folder)
  - Load and switch between saved prompt templates
  - Browse prompt library with easy selection interface
  - Delete unwanted prompt sets with confirmation
  - Automatic file organization with JSON format and timestamps
  - Seamless integration with existing Advanced System Prompts interface
- Includes fixes and improvements:
  - OutputGenerationAgent writes TXT and TMX (Translate mode).
  - Restored required agents/factories for GUI startup (TMAgent, BilingualFileIngestionAgent, Gemini/Claude agents, factory helpers).
  - Fixed TMX parsing deprecation by using explicit None checks (TMAgent.load_tm).
  - Rewrote GeminiProofreadingAgent to correctly call Gemini and parse numbered outputs + change summaries.
  - Corrected mislabeled logs in ClaudeProofreadingAgent.
  - Added TranslationApp.enable_buttons to re-enable UI after processing.
  - Improved multimodal image handling (Gemini: PIL.Image; Claude: base64).

## 2.1.0
- Initial 2.1.x baseline with tracked-changes context, multimodal figure support, and multi‑provider (Claude/Gemini/OpenAI) scaffolding.

## [2.1.0] - 2025-09-05
- Added Document Images Folder support to Claude and OpenAI providers (previously Gemini-only).
- Implemented base64 PNG image embedding helper for multimodal requests.
- Updated Claude and OpenAI agents (Translate/Proofread) to interleave text with images when figure refs are detected.
- Aligned Gemini proofreader image handling to pass PIL images consistently.
- Minor logs and prompts improvements to show when images are added to context.
- Bumped APP_VERSION to 2.1.0.

## [2.0.1] - 2025-09-04

### Added
- DOCX tracked changes ingestion (Word revisions) + TSV (Original<TAB>Final) ingestion
- Tracked Changes Browser (search, detail pane, context copy)
- Custom Instructions free‑text field appended to system/system‑like prompt
- Automatic TMX export for Translate mode (excludes error/empty targets)
- Central `APP_VERSION` constant and startup banner
- Dynamic Gemini model listing & manual refresh
- Inline figure/image normalization + multimodal context injection (when images folder supplied)
- Exact-match Translation Memory application (TMX / TXT) pre‑LLM
- Unified multi‑provider agent factories (Claude / Gemini / OpenAI)

### Changed
- Translate mode ingestion: always reads only first TAB column (prevents accidental reuse of prior target columns)
- Unified single “Context Sources” help block (modes + images + tracked changes + TM + instructions)
- Proofread mode comment synthesis: merges original comment + AI summary only if changes or meaningful summary
- Improved logging (queue-based), clearer warnings, degraded mode if Pillow or provider libs missing
- Tracked change relevance heuristic (exact + partial word overlap) for per‑batch injection

### Fixed
- Missing `APP_VERSION` (NameError) bug
- Duplicate / stale target propagation on re‑translation of exported files
- Previous proofreader undefined-variable implementation replaced with stable parser
- Safe TM language normalization; improved missing image warnings
- Placeholder insertion when model omits numbered line output

## [2.0.0] - 2025-08-31

### Added
- PROOFREAD mode alongside TRANSLATE
- Multimodal prompt support (image-aware translations)
- Document Images Folder (fig reference resolution: Figure / Fig. / Figuur patterns)
- Support for .png .jpg .jpeg .webp image formats
- Figure reference detection & normalization (e.g., “Fig. 1A” → fig1a)

### Changed
- Major translation engine refactor & chunk orchestration
- Enhanced multimodal chunk batching
- Expanded structured logging & exception handling

### Breaking Changes
- Reworked provider abstraction layer
- Configuration expectations updated (api_keys.txt + central factories)

## [1.5.0] - 2025-07-02

### Added
- Enhanced GUI
- Improved error reporting & logging depth
- More resilient file handling / normalization

### Changed
- Performance optimizations for large documents
- Broader model compatibility

### Fixed
- Stability issues under long multi-batch runs
- Memory usage reductions in large-file scenarios

## [1.0.0] - 2025-05-20

### Added
- Initial public release
- Basic AI translation (single provider)
- Text-only ingestion & chunking
- Early Translation Memory integration
- Core GUI

---

## [Unreleased]

### Added
- (Planned v2.5.0) **Standalone Executable**: Self-contained launcher requiring no Python installation
  - PyInstaller-based single-file executable for Windows/Mac/Linux
  - One-click installer with desktop shortcut creation
  - Portable version for USB/network deployment
  - Automatic folder structure setup and example files
  - Professional deployment ready for enterprise environments
- (Planned) Fuzzy Translation Memory (TM) match application
- (Planned) Optional glossary enforcement / terminology lock
- (Planned) Batch retry & per‑provider exponential backoff tuning
- (Planned) JSON export of run metadata (segments, timings, provider stats)
- (Planned) Automatic updates check system
- (Planned) **Document importer**
  - (Planned) Import .docx files and segment text into segments (with .srx segmentation rules)   
  - (Planned) Display imported documents in Grid (like in a CAT tool)
  - (Planned) Edit imported documents in Grid (like in a CAT tool)
  - (Planned) Filter imported documents in Grid (like in a CAT tool)

### Changed
- (Planned) Token / embedding–based tracked‑change relevance scoring
- (Planned) More granular model capability detection (true multimodal flags)
- (Planned) Enhanced distribution strategy for wider user adoption

---
## Legend

Sections: Added | Changed | Deprecated | Removed | Fixed | Security

## Comparison Links (adjust if using VCS tags)

- [Unreleased] – diff against `main`
- [2.0.1] – pending tag comparison  
- [2.0.0] – previous major baseline  
- [1.5.0] – intermediate feature release  
- [1.0.0] – initial release

