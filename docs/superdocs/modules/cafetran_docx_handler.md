# cafetran_docx_handler

**File:** `modules/cafetran_docx_handler.py`
**Lines:** 379
**Classes:** 2
**Functions:** 1

---

## Module Description

CafeTran Bilingual DOCX Handler

This module handles the import and export of CafeTran bilingual DOCX files.
CafeTran uses a simple table-based format with pipe symbols (|) to mark formatted text.

Format Structure:
- Table with columns: ID | Source | Target | Notes | *
- Pipe symbols (|) surround formatted text in the source column
- Examples:
  - |Atalanta| = underlined text
  - Biagio Pagano| = bold text (pipe at end)
  - |text| = formatted text (underlined)
  
The pipe symbols are preserved during translation and applied to the target text.

---

## Classes

### `FormattedSegment`

**Line:** 25

Represents a text segment with formatting information using pipe symbols.

#### Methods

##### `plain_text()`

Get source text with pipe symbols removed for translation.


---

### `CafeTranDOCXHandler`

**Line:** 44

Handler for CafeTran bilingual DOCX files.

This class provides methods to:
- Load and parse CafeTran bilingual DOCX files
- Extract source segments with formatting markers (pipe symbols)
- Update target segments with translations
- Save modified files while preserving formatting

#### Methods

##### `load()`

Load a CafeTran bilingual DOCX file.

Args:
    file_path: Path to the CafeTran bilingual DOCX file
    
Returns:
    bool: True if loaded successfully, False otherwise

##### `extract_source_segments()`

Extract all source segments from the CafeTran bilingual DOCX.

Returns:
    list: List of FormattedSegment objects with pipe symbols preserved

##### `update_target_segments()`

Update target segments with translations.

This method takes plain translations and applies the pipe symbol formatting
from the source segments to create properly formatted target segments.

Args:
    translations: List of translated strings (without pipe symbols)
    
Returns:
    bool: True if update successful, False otherwise

##### `save()`

Save the CafeTran bilingual DOCX with updated target segments.

Args:
    output_path: Optional path for output file. If None, overwrites original.
    
Returns:
    bool: True if saved successfully, False otherwise

##### `is_cafetran_bilingual_docx()`

Check if a DOCX file is a CafeTran bilingual DOCX.

Args:
    file_path: Path to the DOCX file
    
Returns:
    bool: True if file appears to be CafeTran bilingual DOCX, False otherwise


---

## Functions

### `test_handler()`

**Line:** 329

Test the CafeTran DOCX handler with a sample file.

---

