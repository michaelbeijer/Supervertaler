# Changelog

All notable changes to Supervertaler will be documented in this file.

## [Unreleased]

### Added - 2025-11-01
- **High-quality PDF extraction in PDF Rescue** - Upgraded from 200 DPI to 300 DPI
  - PDF pages now extracted at professional print quality (3x zoom factor)
  - Optimized colorspace (RGB, no alpha) for smaller file sizes
  - Image dimensions logged during extraction for quality verification
  - Enhanced completion messages showing DPI and optimization details

### Changed - 2025-11-01
- **PDF to image conversion quality** improved by 50% (2x → 3x zoom)
  - Better text clarity for AI vision models
  - Reduces hallucinations and character recognition errors
  - Optimal balance of quality vs. file size
  - Updated documentation with image quality guidelines

### Added - 2025-10-31
- **Multi-provider support in PDF Rescue** - Now supports OpenAI, Anthropic Claude, and Google Gemini
  - Added Claude Vision API integration (claude-3-5-sonnet, claude-3-5-haiku, claude-3-opus)
  - Added Gemini Vision API integration (gemini-2.0-flash, gemini-1.5-pro, gemini-1.5-flash)
  - Model selector dropdown organized by provider with visual separators
  - Automatic provider detection based on selected model
  - Status messages show which provider is processing
  - All three providers support multi-column layout detection
  - Created comprehensive `modules/PDF_RESCUE_README.md` documentation

### Changed - 2025-10-31
- **PDF Rescue API architecture** - Refactored to support multiple vision providers
  - Replaced single OpenAI client with multi-provider client dictionary
  - Added `_initialize_clients()` method for dynamic provider initialization
  - Added provider-specific extraction methods: `_extract_with_openai()`, `_extract_with_claude()`, `_extract_with_gemini()`
  - Enhanced error messages to indicate which provider requires API key
  - Updated module description to reflect multi-provider support
- **Standardized all tab headers** across Universal Lookup, AutoFingers, PDF Rescue, and TMX Editor
  - All tabs now use consistent 16pt blue (#1976D2) headers with emoji icons
  - Uniform light blue (#E3F2FD) description boxes with gray text (#666)
  - Consistent 10px margins and 5px spacing throughout
  - Implemented responsive design with stretch factors for optimal display on all screen sizes
  - Headers stay compact on top, main content expands to fill available space
  - Works perfectly on both small and large monitors

### Fixed - 2025-10-31
- **GPT-5 compatibility** - PDF Rescue now uses `max_completion_tokens` for GPT-5/o1 models instead of `max_tokens`
- **PDF Rescue header sizing issues** - header no longer appears oversized on large monitors
- **TMX Editor header** - updated from banner style to match standardized pattern
- **AutoFingers header** - changed from black to blue and standardized formatting
- **Responsive layout** - all tabs now properly adapt to different screen sizes using Qt stretch factors
- **AI hallucinations** - Enhanced extraction prompt with strict accuracy rules to reduce word substitutions

### Documentation - 2025-10-31
- Created `modules/PDF_RESCUE_README.md` with comprehensive multi-provider guide
  - Setup instructions for all three providers
  - Model recommendations by use case
  - Cost comparison table
  - Troubleshooting guide
  - API integration examples
- Created `docs/MODULE_HEADER_PATTERN.md` with complete standardization guide
- Includes implementation examples, style specifications, and responsive design patterns
- Documents the use of stretch factors for adaptive layouts
- Provides migration checklist for future tab development

## Previous Versions
See `CHANGELOG_Qt.md` and `CHANGELOG_Tkinter.md` for earlier version history.
