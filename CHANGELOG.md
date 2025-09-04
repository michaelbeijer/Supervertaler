# Changelog
All notable changes to Supervertaler are documented here.

Format: Keep a Changelog (https://keepachangelog.com)  
Versioning: Semantic Versioning (https://semver.org)

## [Unreleased]
### Added
- (placeholder)

### Changed
- (placeholder)

### Fixed
- (placeholder)

---

## [2.0.1] - 2025-09-04
### Added
- Central APP_VERSION constant (used in window title and TMX header).
- Dynamic startup banner logging the running version.

### Changed
- Translate mode ingestion now explicitly ignores any extra TAB-separated columns (only first column taken as source).
- In-app info text clarified: Translate output always 2 columns; re-translation of prior exports is safe.

### Fixed
- NameError on startup when APP_VERSION was referenced before definition.
- Duplicate/looped target column issue when re-feeding previous bilingual exports.

---

## [2.0.0] - 2025-08-31
(Consolidated baseline release including items previously listed under 2.1.0.)

### Added
- Multi‑AI provider support: Claude, Gemini, OpenAI.
- PROOFREAD mode alongside TRANSLATE mode.
- Translation Memory support (.txt and .tmx).
- Tracked changes ingestion (DOCX with revisions + TSV Original<TAB>Final) and contextual sampling per batch.
- Image / figure context: normalizes figure filenames (e.g., Figure_1-A.png → fig1a) and injects images when referenced.
- Multimodal prompt support (where provider/model supports it).
- Custom instructions panel appended to system guidance.
- Chunked batch processing for large documents.
- TMX export (Translate mode) excluding empty/error segments.
- GUI enhancements: drawings folder selector, tracked-changes status, model/provider selectors.

### Changed
- Refactored translation & proofreading pipeline for provider abstraction.
- Improved prompt structure for better patent-domain accuracy.
- More robust figure reference normalization (case/spacing/variants).
- Centralized logging with queue-driven UI updates.

### Fixed
- Pillow absence now degrades gracefully with warning.
- Better error handling for TM load (unsupported ext, malformed TMX).
- Figure reference edge cases (e.g., “Fig. 1A”, “FIG 1-A”).

---

## [1.5.0] - 2025-07-02
### Added
- Enhanced GUI layout.
- Expanded logging & error reporting.
- Improved file handling and larger document throughput.

### Changed
- Performance optimizations for large inputs.
- Updated model compatibility layer.

### Fixed
- Stability improvements and memory usage refinements.

---

## [1.0.0] - 2025-05-20
### Added
- Initial public release.
- Basic AI-powered translation (single provider).
- Text file input/output, basic chunking, simple TM support.

---
