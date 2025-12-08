# mqxliff_handler

**File:** `modules/mqxliff_handler.py`
**Lines:** 638
**Classes:** 2
**Functions:** 1

---

## Module Description

MQXLIFF Handler Module
======================
Handles import/export of memoQ XLIFF (.mqxliff) files with proper formatting preservation.

MQXLIFF is an XLIFF 1.2 format with memoQ-specific extensions for CAT tool metadata
and formatting tags. This module provides robust parsing and generation of MQXLIFF files
while preserving inline formatting (bold, italic, underline) and complex structures like
hyperlinks.

Key Features:
- Parse XLIFF trans-units with source and target segments
- Extract and preserve inline formatting tags (bpt/ept pairs)
- Handle complex nested structures (hyperlinks with formatting)
- Generate valid MQXLIFF output with proper tag structure
- Maintain segment IDs and memoQ metadata

Formatting Tag Structure:
- <bpt id="X" ctype="bold">{}</bpt>...<ept id="X">{}</ept> - Bold text
- <bpt id="X" ctype="italic">{}</bpt>...<ept id="X">{}</ept> - Italic text
- <bpt id="X" ctype="underlined">{}</bpt>...<ept id="X">{}</ept> - Underlined text
- Nested tags for hyperlinks: <bpt><bpt><bpt>text</ept></ept></ept>

---

## Classes

### `FormattedSegment`

**Line:** 30

Represents a segment with inline formatting information.

#### Methods


---

### `MQXLIFFHandler`

**Line:** 66

Handler for parsing and generating memoQ XLIFF files.

#### Methods

##### `load()`

Load and parse an MQXLIFF file.

Args:
    file_path: Path to the .mqxliff file
    
Returns:
    True if loaded successfully, False otherwise

##### `extract_source_segments()`

Extract all source segments from the MQXLIFF file.

Returns:
    List of FormattedSegment objects containing source text and formatting

##### `update_target_segments()`

Update target segments in the MQXLIFF with translations.

This method attempts to preserve formatting from the source segment by:
1. Copying the source formatting structure
2. Replacing the text content with the translation
3. Adjusting tag IDs to avoid conflicts

Args:
    translations: List of translated strings (plain text)
    
Returns:
    Number of segments updated

##### `save()`

Save the modified MQXLIFF file with proper namespace handling.

Args:
    output_path: Path where to save the file
    
Returns:
    True if saved successfully, False otherwise

##### `get_segment_count()`

Get the number of translatable segments (excluding auxiliary segments).


---

## Functions

### `test_mqxliff_handler()`

**Line:** 583

Test function to verify MQXLIFF handler functionality.

---

