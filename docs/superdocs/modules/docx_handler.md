# docx_handler

**File:** `modules/docx_handler.py`
**Lines:** 646
**Classes:** 2
**Functions:** 0

---

## Module Description

DOCX Handler
Import and export DOCX files with formatting preservation

---

## Classes

### `ParagraphInfo`

**Line:** 31

Information about a paragraph for reconstruction

---

### `DOCXHandler`

**Line:** 46

Handle DOCX import and export operations

#### Methods

##### `import_docx()`

Import DOCX file and extract paragraphs with formatting tags

Args:
    file_path: Path to DOCX file
    extract_formatting: If True, convert formatting to inline tags

Returns: List of paragraph texts (with tags if extract_formatting=True)
         Includes both regular paragraphs AND table cells

##### `export_docx()`

Export translated segments back to DOCX

Args:
    segments: List of segment dictionaries with 'paragraph_id', 'source', 'target'
    output_path: Path to save the translated document
    preserve_formatting: Whether to preserve original formatting (default True)

##### `export_bilingual_docx()`

Export as bilingual document (source | target in table)
Useful for review purposes

##### `get_document_info()`

Get information about the loaded document


---

