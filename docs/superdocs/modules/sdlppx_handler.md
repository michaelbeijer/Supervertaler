# sdlppx_handler

**File:** `modules/sdlppx_handler.py`
**Lines:** 814
**Classes:** 5
**Functions:** 1

---

## Module Description

Trados Studio Package Handler (SDLPPX/SDLRPX)

This module handles the import and export of Trados Studio project packages.
SDLPPX = Project Package (sent to translator)
SDLRPX = Return Package (sent back to PM)

Package Structure:
- .sdlppx/.sdlrpx = ZIP archive containing:
  - *.sdlproj = XML project file with settings
  - {source-lang}/*.sdlxliff = Bilingual XLIFF files
  - {target-lang}/*.sdlxliff = Target language files (may be copies)
  - Reports/ = Analysis reports (optional)

SDLXLIFF Format:
- XLIFF 1.2 with SDL namespace extensions
- <g> tags for inline formatting
- <x> tags for standalone elements
- <mrk mtype="seg"> for segment boundaries
- sdl:conf attribute for confirmation status

Author: Supervertaler

---

## Classes

### `SDLSegment`

**Line:** 51

Represents a segment from an SDLXLIFF file

---

### `SDLXLIFFFile`

**Line:** 68

Represents an SDLXLIFF file within a package

---

### `TradosPackage`

**Line:** 82

Represents a Trados Studio project package

---

### `SDLXLIFFParser`

**Line:** 99

Parser for SDLXLIFF files (Trados bilingual XLIFF format).
Handles the SDL-specific extensions to standard XLIFF.

#### Methods

##### `parse_file()`

Parse an SDLXLIFF file and extract segments.

Args:
    file_path: Path to the SDLXLIFF file
    
Returns:
    SDLXLIFFFile object with parsed segments


---

### `TradosPackageHandler`

**Line:** 415

Handler for Trados Studio project packages (SDLPPX/SDLRPX).

This class provides methods to:
- Extract and parse SDLPPX packages
- Import segments into Supervertaler projects
- Update translations in SDLXLIFF files
- Create return packages (SDLRPX)

#### Methods

##### `load_package()`

Load and extract a Trados package.

Args:
    package_path: Path to .sdlppx or .sdlrpx file
    extract_dir: Directory to extract to (temp if not specified)
    
Returns:
    TradosPackage object with parsed content

##### `get_all_segments()`

Get all segments from all files in the package.

##### `update_segment()`

Update a segment's translation.

Args:
    segment_id: The segment ID to update
    target_text: New target text
    status: New status (translated, approved, etc.)
    
Returns:
    True if updated successfully

##### `update_translations()`

Batch update translations.

Args:
    translations: Dict mapping segment_id to target_text
    
Returns:
    Number of segments updated

##### `save_xliff_files()`

Save all modified SDLXLIFF files.

Returns:
    True if all files saved successfully

##### `create_return_package()`

Create a return package (SDLRPX) with translations.

Args:
    output_path: Path for the return package (auto-generated if not specified)
    
Returns:
    Path to the created package

##### `cleanup()`

Clean up extracted files.


---

## Functions

### `detect_trados_package_type()`

**Line:** 788

Detect if a file is a Trados package and return its type.

Returns:
    'sdlppx', 'sdlrpx', or None if not a Trados package

---

