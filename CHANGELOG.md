# Supervertaler - Changelog

## [Unreleased]

### Added
- (Planned v2.4.0) **Standalone Executable**: Self-contained launcher requiring no Python installation
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

### Changed
- (Planned) Token / embedding–based tracked‑change relevance scoring
- (Planned) More granular model capability detection (true multimodal flags)
- (Planned) Enhanced distribution strategy for wider user adoption

### Fixed
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

## Legend

Sections: Added | Changed | Deprecated | Removed | Fixed | Security

## Comparison Links (adjust if using VCS tags)

- [Unreleased] – diff against `main`
- [2.0.1] – pending tag comparison  
- [2.0.0] – previous major baseline  
- [1.5.0] – intermediate feature release  
- [1.0.0] – initial release

