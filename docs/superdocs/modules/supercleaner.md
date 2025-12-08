# supercleaner

**File:** `modules/supercleaner.py`
**Lines:** 600
**Classes:** 1
**Functions:** 1

---

## Module Description

Supercleaner Module for Supervertaler
======================================

Cleans up DOCX documents before translation by removing formatting issues,
excessive tags, and OCR artifacts. Combines functionality similar to:
- TransTools Document Cleaner (tag/formatting cleanup)
- TransTools Unbreaker (incorrect line break removal)

Author: Michael Beijer / Supervertaler

---

## Classes

### `DocumentCleaner`

**Line:** 21

Clean DOCX documents by removing formatting issues and excessive tags.
Also includes Unbreaker functionality to fix incorrect line/paragraph breaks.

#### Methods

##### `clean_document()`

Clean a DOCX document based on selected operations

Args:
    input_path: Path to input DOCX file
    output_path: Path to save cleaned DOCX file
    operations: Dictionary of operation names and whether to perform them

Returns:
    Dictionary with statistics about operations performed


---

## Functions

### `clean_document_simple()`

**Line:** 535

Convenience function for quick document cleaning with default settings

Args:
    input_path: Path to input DOCX file
    output_path: Path to save cleaned file (if None, overwrites input)
    quick_clean: If True, applies common cleaning operations

Returns:
    Statistics dictionary

---

