# image_extractor

**File:** `modules/image_extractor.py`
**Lines:** 188
**Classes:** 1
**Functions:** 0

---

## Module Description

═══════════════════════════════════════════════════════════════════════════════
Image Extractor Module for Supervertaler
═══════════════════════════════════════════════════════════════════════════════

Purpose:
    Extract images from DOCX files and save them as sequentially numbered PNG files.
    Integrated into the Reference Images tab under Translation Resources.

Features:
    - Extract all images from DOCX documents
    - Save as PNG files with sequential naming (Fig. 1.png, Fig. 2.png, etc.)
    - Support for various image formats embedded in DOCX
    - Progress feedback during extraction
    - Can be used as standalone tool or within Translation Resources workflow

Author: Supervertaler Development Team
Created: 2025-11-17
Last Modified: 2025-11-17

═══════════════════════════════════════════════════════════════════════════════

---

## Classes

### `ImageExtractor`

**Line:** 32

Extract images from DOCX files and save as PNG

#### Methods

##### `extract_images_from_docx()`

Extract all images from a DOCX file and save as PNG files.

Args:
    docx_path: Path to the DOCX file
    output_dir: Directory where images will be saved
    prefix: Prefix for output filenames (default: "Fig.")
    
Returns:
    Tuple of (number of images extracted, list of output file paths)

##### `extract_from_multiple_docx()`

Extract images from multiple DOCX files.

Args:
    docx_paths: List of paths to DOCX files
    output_dir: Directory where images will be saved
    prefix: Prefix for output filenames (default: "Fig.")
    
Returns:
    Tuple of (total number of images extracted, list of output file paths)


---

