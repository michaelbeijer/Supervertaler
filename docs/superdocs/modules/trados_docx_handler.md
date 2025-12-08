# trados_docx_handler

**File:** `modules/trados_docx_handler.py`
**Lines:** 422
**Classes:** 2
**Functions:** 1

---

## Module Description

Trados Bilingual DOCX Handler (Review Files)

This module handles the import and export of Trados Studio bilingual review DOCX files.
Trados uses a table-based format with numbered inline tags.

Format Structure:
- Table with columns: Segment ID | Segment status | Source segment | Target segment
- Tags use character style "Tag" and format: <N>text</N>
- Segment IDs are GUIDs with numeric prefixes
- Statuses: "Not Translated", "Draft", "Translated", etc.

Critical for re-import:
- Tags MUST preserve the "Tag" character style
- Tag numbers must match between source and target
- Segment IDs must remain unchanged

---

## Classes

### `TradosSegment`

**Line:** 29

Represents a Trados segment with tag information.

#### Methods

##### `plain_source()`

Get source text without tags for translation.


---

### `TradosDOCXHandler`

**Line:** 59

Handler for Trados Studio bilingual review DOCX files.

This class provides methods to:
- Load and parse Trados bilingual review DOCX files
- Extract source segments with tag markers
- Update target segments with translations (preserving tag style)
- Save modified files ready for re-import to Trados

#### Methods

##### `load()`

Load a Trados bilingual review DOCX file.

Args:
    file_path: Path to the Trados bilingual DOCX file
    
Returns:
    bool: True if loaded successfully, False otherwise

##### `extract_source_segments()`

Extract all source segments from the Trados bilingual DOCX.

Returns:
    list: List of TradosSegment objects

##### `update_target_segments()`

Update target segments with translations.

Args:
    translations: Dict mapping row index to translated text
    
Returns:
    int: Number of segments updated

##### `save()`

Save the modified document.

Args:
    output_path: Path to save to (defaults to original path)
    
Returns:
    bool: True if saved successfully

##### `get_segments_for_translation()`

Get segments that need translation.

Returns:
    List of (row_index, source_text, plain_source) tuples


---

## Functions

### `detect_bilingual_docx_type()`

**Line:** 388

Detect the type of bilingual DOCX file.

Returns:
    str: "trados", "cafetran", "memoq", or "unknown"

---

