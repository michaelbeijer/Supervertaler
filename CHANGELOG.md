# Changelog

All notable changes to Supervertaler will be documented in this file.

## [Unreleased]

### Changed - 2025-10-31
- **Standardized all tab headers** across Universal Lookup, AutoFingers, PDF Rescue, and TMX Editor
  - All tabs now use consistent 16pt blue (#1976D2) headers with emoji icons
  - Uniform light blue (#E3F2FD) description boxes with gray text (#666)
  - Consistent 10px margins and 5px spacing throughout
  - Implemented responsive design with stretch factors for optimal display on all screen sizes
  - Headers stay compact on top, main content expands to fill available space
  - Works perfectly on both small and large monitors

### Fixed - 2025-10-31
- **PDF Rescue header sizing issues** - header no longer appears oversized on large monitors
- **TMX Editor header** - updated from banner style to match standardized pattern
- **AutoFingers header** - changed from black to blue and standardized formatting
- **Responsive layout** - all tabs now properly adapt to different screen sizes using Qt stretch factors

### Documentation - 2025-10-31
- Created `docs/MODULE_HEADER_PATTERN.md` with complete standardization guide
- Includes implementation examples, style specifications, and responsive design patterns
- Documents the use of stretch factors for adaptive layouts
- Provides migration checklist for future tab development

## Previous Versions
See `CHANGELOG_Qt.md` and `CHANGELOG_Tkinter.md` for earlier version history.
