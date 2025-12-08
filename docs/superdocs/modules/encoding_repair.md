# encoding_repair

**File:** `modules/encoding_repair.py`
**Lines:** 319
**Classes:** 1
**Functions:** 0

---

## Module Description

Text Encoding Corruption Detection and Repair Module

Detects and fixes common text encoding issues (mojibake), particularly:
- UTF-8 text incorrectly decoded as Latin-1 (Windows-1252)
- Double-encoded Unicode escape sequences
- Common encoding corruption patterns

---

## Classes

### `EncodingRepair`

**Line:** 21

Detect and repair text encoding corruption.

#### Methods

##### `detect_corruption()`

Detect if text contains encoding corruption patterns.

Args:
    text: Text content to analyze
    
Returns:
    Tuple of (has_corruption, corruption_count, list_of_patterns_found)

##### `repair_text()`

Repair encoding corruption in text.

Args:
    text: Text content to repair
    
Returns:
    Repaired text

##### `repair_file()`

Detect and repair encoding corruption in a file.

Args:
    file_path: Path to the file to repair
    encoding: Encoding to use when reading the file
    
Returns:
    Tuple of (success, message, repair_info)

##### `repair_with_encoding_fallback()`

Try to repair a file by attempting different encodings.

This handles the case where the file itself might be in the wrong encoding.

Args:
    file_path: Path to the file to repair
    
Returns:
    Tuple of (success, message, repair_info)

##### `scan_directory()`

Scan a directory for files with encoding corruption.

Args:
    directory_path: Path to directory to scan
    file_extensions: List of file extensions to check (e.g., ['.txt', '.csv'])
                   If None, scans all files.
    
Returns:
    Dictionary with scan results


---

