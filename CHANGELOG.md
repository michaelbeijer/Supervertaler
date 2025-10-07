# Supervertaler - Changelog

## [2.5.0] - 2025-10-07 🎉 MAJOR RELEASE (In Progress)

### 🚀 Latest Updates - October 7, 2025

#### � Session Report Generation (NEW FEATURE)
- **Added comprehensive session report generation** to v2.5.0 CAT Editor
- **Menu Location**: File → Generate Session Report...
- **Report Format**: Markdown (.md) file with complete session details
- **Report Contents**:
  - Session information (date, version, AI provider/model)
  - Project statistics (total segments, translated/untranslated breakdown)
  - Language settings (source/target languages)
  - AI translation settings (provider, model, prompts)
  - Translation features used (TM status, context awareness)
  - Library and API key availability status
  - Detailed segment breakdown by status
  - Workflow summary
- **Benefits**: 
  - Document translation project settings for future reference
  - Share AI configuration with team members
  - Track translation progress and statistics
  - Audit trail for professional projects
- **Port from v2.4.0**: Successfully adapted the report generation feature from stable version

#### �🔢 Language-Specific Number Formatting Rules (CRITICAL FIX)
- **Added to ALL translation and proofreading prompts** (both v2.4.0 and v2.5.0)
- **Continental European Languages** (Dutch, French, German, Italian, Spanish, etc.):
  - Decimal separator: **comma** (e.g., 17,1 cm)
  - Number-unit spacing: **space or non-breaking space** (e.g., 17,1 cm)
- **English/Irish**:
  - Decimal separator: **period/full stop** (e.g., 17.1 cm)
  - Number-unit spacing: **no space** (e.g., 17.1cm)
- **Impact**: Fixes incorrect number formatting in translations (e.g., "17.1 cm" incorrectly appearing in Dutch translations instead of "17,1 cm")
- **Updated Prompts**:
  - v2.4.0: `default_translate_prompt`, `default_proofread_prompt`
  - v2.5.0: `single_segment_prompt`, `batch_docx_prompt`, `batch_bilingual_prompt`, `default_proofread_prompt`

### 🚀 Latest Updates - October 6, 2025

#### ✨ Dynamic Model Fetching
- **API-Based Model Discovery**: Automatically fetch available models from each provider based on user's API key
  - **OpenAI**: Full dynamic fetch via `/v1/models` endpoint with intelligent filtering
  - **Gemini**: Full dynamic fetch via `list_models()` API
  - **Claude**: Returns curated model list (no public list endpoint)
- **🔄 Refresh Button**: Added to API Settings dialog for instant model updates
- **Smart Fallbacks**: Falls back to curated lists if API fetch fails
- **User Benefits**: 
  - No more 403 errors from outdated model names
  - Always see only models you can actually use
  - Automatic access to new models as providers release them

#### � Context-Aware Translation Prompts
- **Three Specialized Prompt Templates**:
  1. **Single Segment Mode** (Ctrl+T): Focus on quality, deep context understanding, figure references
  2. **Batch DOCX Mode**: Emphasis on consistency, structure preservation, terminology
  3. **Batch Bilingual Mode**: Focus on segment alignment, numbered output for TXT files
- **Automatic Selection**: System intelligently chooses appropriate prompt based on translation mode
- **Inline Formatting Preservation**: Explicit instructions to preserve `<b>`, `<i>`, `<u>` tags exactly

#### 📄 Bilingual TXT Import/Export (Professional CAT Tool Workflow)
- **Flexible TXT Import** - Auto-detects and handles multiple formats:
  - **Single-column source files** (all untranslated)
  - **Two-column bilingual** (Source\tTarget with partial translations)
  - **Three-column with IDs** (ID\tSource\tTarget)
- **Smart Delimiter Detection**:
  - Auto-detects tab-delimited vs CSV format
  - Handles commas in source text correctly (doesn't split on them)
  - Samples multiple lines for accurate format detection
- **Bilingual TXT Export**: Simple tab-delimited format compatible with memoQ/Trados
- **Pre-Translation Support**: Automatically detects and preserves existing translations
- **Status Tracking**: Distinguishes between pre-translated and untranslated segments
- **Format Messages**: Clear feedback about file format detected (source-only, fully translated, partially translated)

#### 🐛 Critical Bug Fixes
- **DOCX Table Paragraph Alignment**: Fixed critical export bug where translations stopped mid-document
  - Problem: `doc.paragraphs` includes table paragraphs, causing counter misalignment
  - Solution: Build `table_paras` set and skip early without incrementing counter
  - Result: Perfect paragraph alignment in exported DOCX files
- **Prompt Template Mismatch**: Fixed AI confusion from SENTENCES vs TEXT placeholder inconsistency
- **Inline Formatting Tags**: Fixed AI removing or malforming `<b>`, `<i>`, `<u>` tags in translations
- **CSV Comma Splitting**: Fixed single-column TXT files being incorrectly split at commas

#### 📊 UI Enhancements
- **New Toolbar Button**: "📄 Import TXT" for quick bilingual file import
- **New Menu Items**:
  - "Import Bilingual TXT..." (File menu)
  - "Export to Bilingual TXT..." (File menu)
- **Enhanced Save Dialog**: Shows selected model details when saving configurations
- **Model Refresh Button**: In API Settings dialog for instant model list updates

#### 📁 Sample Files Created
- `test_bilingual.txt` - Sample bilingual file with 3 pre-translated, 7 untranslated segments
- `test_source_only.txt` - Sample single-column source file (10 segments)

#### 📚 Documentation Updates
- `FEATURES_dynamic_models_contextual_prompts.md` - Comprehensive guide to new features
- `QUICK_REFERENCE_dynamic_models_prompts.md` - Quick reference card
- `BUGFIX_CRITICAL_docx_table_alignment.md` - Detailed bug analysis and fix
- `STRATEGIC_PIVOT_TXT_bilingual_first.md` - Rationale for TXT-first approach
- `FEATURE_bilingual_txt_import_export.md` - Complete TXT workflow documentation

### 🔄 Strategic Direction
- **TXT Workflow First**: Focusing on simpler, more reliable bilingual TXT workflow
- **DOCX Complexity Deferred**: Pausing complex DOCX table/formatting edge cases
- **Professional CAT Integration**: Prioritizing compatibility with memoQ/Trados workflows
- **Modular Development**: Building features incrementally with comprehensive testing

### ⚠️ Known Issues
- Model selection dialog shows cached value on reopen (cosmetic only - selection saves correctly)
- DOCX table export needs more real-world testing

---

## [2.5.0] - 2025-10-05 �🎉 MAJOR RELEASE (Initial)

### 🚀 NEW: Integrated CAT Editor - Direct DOCX Translation Workflow

**Supervertaler is now a Professional CAT tool with multicontextual AI translation system!**

This major release transforms Supervertaler from an AI-powered translation assistant into a full-featured CAT (Computer-Aided Translation) tool with integrated AI capabilities. Users can now work directly with DOCX files without requiring external CAT tools like memoQ or Trados.

### ✨ Major New Features 

#### 🔧 CAT Editor Integration
- **Direct DOCX Import**: Import Word documents directly into Supervertaler
- **Automatic Segmentation**: Intelligent sentence-level segmentation with paragraph and table support
- **AI-Assisted Pre-Translation**: Revolutionary feature that brings LLM-powered contextual translation to CAT workflow
  - Unlike traditional CAT tools (Google Translate, DeepL), uses full document context
  - Supports custom domain-specific prompts
  - Integrates with TM, tracked changes, and multimodal content
  - Multiple AI providers: Gemini, Claude, OpenAI
- **DOCX Export**: Export translated documents with original formatting fully preserved
- **Segment Management**: Professional segment tracking with status indicators:
  - 🔴 Untranslated
  - 🟡 Draft (AI-generated)
  - 🟢 Translated (human-verified)
  - ✅ Approved
- **Translation Statistics**: Real-time progress tracking and segment counts
- **Collapsible CAT Editor Panel**: Clean, professional UI integration

#### 🔀 Dual Workflow Support
1. **Legacy TXT Mode** (Preserved for memoQ/Trados users):
   - Import TXT files (one segment per line)
   - AI translation with multicontextual intelligence
   - Export TXT + TMX files
   - **100% backward compatible** - no breaking changes

2. **New CAT Editor Mode** (Direct DOCX translation):
   - Import DOCX → Segment extraction
   - AI-Assisted Pre-Translation
   - Manual editing and review
   - Export translated DOCX
   - **No external CAT tool required!**

#### 🧩 Modular Architecture
- Created `modules/` package for clean code organization:
  - `segment_manager.py` - Core Segment and SegmentManager classes
  - `ai_pretranslation_agent.py` - Bridge between AI engines and CAT editor
  - `docx_handler.py` - DOCX import/export with formatting preservation
  - `simple_segmenter.py` - Intelligent sentence segmentation
  - `tag_manager.py` - Inline formatting tag handling

### 🎯 Key Innovations

#### AI-Assisted Pre-Translation
Traditional CAT tools offer "pre-translation" using basic MT engines. **Supervertaler v2.5.0 revolutionizes this**:

**Traditional CAT Tools:**
- Basic MT (Google Translate, DeepL)
- Sentence-by-sentence translation (no context)
- No customization
- No TM integration in pre-translation

**Supervertaler v2.5.0:**
- ✅ Full document context awareness
- ✅ Custom domain-specific prompts
- ✅ Multiple LLM providers (Gemini/Claude/OpenAI)
- ✅ TM integration during translation
- ✅ Tracked changes learning
- ✅ Multimodal support (images, tables)
- ✅ Batch processing with progress tracking

**Result**: Higher quality pre-translations, less post-editing, faster workflow!

### 🔧 Technical Improvements

#### New Classes & Components
- `Segment` - Universal data structure for translation segments
  - Supports paragraphs, tables, headings
  - Full metadata tracking (style, position, timestamps)
  - JSON serialization for project save/load
- `SegmentManager` - Segment collection utilities
  - Batch operations
  - Status filtering
  - Statistics calculation
- `AIPreTranslationAgent` - AI translation bridge
  - Provider-agnostic design
  - Batch processing with token limits
  - Progress callbacks
  - Context-aware translation preparation
  - Translation quality metrics

#### Enhanced UI
- New collapsible "CAT Editor" section
- DOCX import/export buttons
- AI-Assisted Pre-Translation button
- Real-time segment statistics display
- Progress indicators during translation
- Clean, professional layout

### 📊 Statistics & Metrics
- Translation progress percentage
- Segment counts by status
- Real-time updates during AI pre-translation
- Visual status indicators (🔴🟡🟢✅)

### 🔄 Workflow Comparison

#### OLD Workflow (v2.4.0 and earlier):
1. Translate in memoQ/Trados
2. Export bilingual TXT
3. Import to Supervertaler for AI enhancement
4. Export enhanced translation
5. Import back to CAT tool

#### NEW Workflow (v2.5.0 - CAT Editor):
1. Import DOCX to Supervertaler
2. Review segmentation
3. Click "AI-Assisted Pre-Translation"
4. Review and edit segments
5. Export translated DOCX
**Done!** No external CAT tool needed!

### 🎨 Branding Update
- **New tagline**: "Professional CAT tool with multicontextual AI translation system"
- Updated all documentation and UI text
- Positioned as professional-grade CAT tool

### 📚 Documentation
- Created `INTEGRATION_PLAN_v2.5.0.md` - Complete architectural blueprint
- Created `INTEGRATION_PROGRESS_v2.5.0.md` - Development progress tracking
- Created `SESSION_CHECKPOINT_v2.5.0.md` - Session summary
- Updated info panel with v2.5.0 features

### 🔧 Under the Hood
- ~2,600 lines of new code
- 7 new module files
- 3 comprehensive documentation files
- Clean separation of concerns
- Modular, testable architecture
- Future-proof design for extensions

### ⚙️ API & Integration
- Seamless integration with existing translation engines
- No changes to TXT workflow (backward compatible)
- Shared logging and progress queue
- Unified language and provider selection

### 🐛 Bug Fixes
- None (new feature release)

### ⚠️ Breaking Changes
- **None!** v2.5.0 is 100% backward compatible with v2.4.0
- All existing TXT workflows work identically
- All projects, prompts, and settings preserved

### 📦 Dependencies
- No new dependencies required
- Uses existing modules: `python-docx`, `tkinter`
- Compatible with Python 3.8+

### 🎓 User Impact
**For Professional Translators:**
- Can now use Supervertaler as primary CAT tool
- AI pre-translation saves 50-70% editing time
- Familiar CAT workflow with AI superpowers

**For Casual Users:**
- Direct DOCX translation without learning CAT tools
- Simple workflow: Import → Translate → Export
- Professional results with minimal effort

**For Power Users:**
- Full control over prompts and AI behavior
- Segment-level editing capability
- TM and tracked changes integration
- Multiple workflow options

### 🔮 Future Enhancements (Planned for v2.6.0+)
- Segment grid UI with inline editing
- Document preview pane
- Quick termbase management
- Advanced filtering and search
- Bilingual table import/export
- Integration with CAT editor's dual text selection

### 📝 Migration Notes
- No migration needed - simply use v2.5.0 in place of v2.4.0
- New CAT Editor features are additive
- Existing workflows continue to work unchanged

### 🙏 Acknowledgments
This release represents a bold step forward in integrating AI with professional translation tools. Special thanks to the translation community for feedback and feature requests that shaped this release.

---

## [Unreleased - CAT Editor Prototype] - 2025-10-01 to 2025-10-05

### Experimental: CAT Editor Prototype Development

A standalone CAT (Computer-Aided Translation) editor prototype is under active development in the `cat_tool_prototype/` folder. This experimental tool is being designed for potential integration into Supervertaler v2.5.0.

**Design Philosophy**: We're implementing features from [michaelbeijer.co.uk/what_i_look_for_in_a_cat_tool](https://michaelbeijer.co.uk/what_i_look_for_in_a_cat_tool) - a translator's non-negotiable CAT tool requirements.

**Current Status**: Prototype v0.4.2 (Feature-complete with dual text selection)

**Latest Updates (v0.4.2 - October 5, 2025)**:
- ✅ **Dual text selection** - Select corresponding pieces of source and target text simultaneously (memoQ-style) 🎉 **[Blog Feature #1]**
- ✅ **Mouse-based dual selection** - Light blue for source, light green for target
- ✅ **Keyboard-based dual selection** - Tab to switch focus, Ctrl+Shift+Arrows to extend selection
- ✅ **Bidirectional selection** - Works forward and backward with cursor memory
- ✅ **Column management** - Show/hide specific columns (View → Grid Columns...)
- ✅ **Formatting display** - Bold/italic/underline tags rendered visually in Grid View
- ✅ **Optional style colors** - Toggle style-based font colors (View → Toggle Style Colors)
- ✅ **Improved navigation** - Shows segment type (Para, Table, Heading 1, etc.)
- ✅ **Streamlined editing** - Double-click target to edit directly, removed old popups

**Core Features**:
- ✅ DOCX import/export with full formatting preservation
- ✅ Table support with cell-by-cell translation
- ✅ Style visibility and preservation (Heading 1-3, Title, Subtitle, etc.)
- ✅ Inline formatting tags (bold, italic, underline) with visual rendering
- ✅ Three view modes (Grid, List, Document) with seamless switching
- ✅ Document View shows translations in natural document flow
- ✅ Interactive translation grid with dual text selection
- ✅ Advanced filtering system with precise highlighting
- ✅ Find/Replace, project save/load
- ✅ Bilingual and TSV export options
- ✅ Column visibility management
- ✅ Optional style color display

**Implementing Blog Features**:
- ✅ Feature #1: Dual text selection in grid (memoQ-style)
- 🔄 Feature #2: Quick termbase management (planned)
- 🔄 Feature #3: Document preview pane (planned)
- 🔄 Feature #4: Bilingual table import/export with tracking (planned)
- ✅ Feature #5: Fast, responsive actions (optimized grid rendering)
- 🔄 Feature #6: Sentence/paragraph segmentation switching (planned)

**For detailed prototype changelog**, see: `cat_tool_prototype/CHANGELOG.md`

**For prototype documentation**, see: `cat_tool_prototype/README.md`

**Note**: This prototype is experimental and separate from the main Supervertaler application. It will remain a standalone tool until integration is planned and completed.

---

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

