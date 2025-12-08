# termbase_import_export

**File:** `modules/termbase_import_export.py`
**Lines:** 425
**Classes:** 3
**Functions:** 0

---

## Module Description

Termbase Import/Export Module

Handles importing and exporting termbases in TSV (Tab-Separated Values) format.
TSV is simple, universal, and works well with Excel, Google Sheets, and text editors.

Format:
- First row: header with column names
- Tab-delimited fields
- UTF-8 encoding with BOM for Excel compatibility
- Multi-line content wrapped in quotes
- Boolean values: TRUE/FALSE or 1/0

Standard columns:
- Source Term (required)
- Target Term (required)
- Priority (optional, 1-99, default: 50)
- Domain (optional)
- Notes (optional, can be multi-line)
- Project (optional)
- Client (optional)
- Forbidden (optional, TRUE/FALSE)

---

## Classes

### `ImportResult`

**Line:** 32

Result of a termbase import operation

---

### `TermbaseImporter`

**Line:** 42

Import termbases from TSV files

#### Methods

##### `import_tsv()`

Import terms from TSV file

Args:
    filepath: Path to TSV file
    termbase_id: Target termbase ID
    skip_duplicates: Skip terms that already exist (based on source term)
    update_duplicates: Update existing terms instead of skipping
    
Returns:
    ImportResult with statistics and errors


---

### `TermbaseExporter`

**Line:** 334

Export termbases to TSV files

#### Methods

##### `export_tsv()`

Export termbase to TSV file

Args:
    termbase_id: Termbase ID to export
    filepath: Output file path
    include_metadata: Include all metadata fields
    
Returns:
    Tuple of (success: bool, message: str)


---

