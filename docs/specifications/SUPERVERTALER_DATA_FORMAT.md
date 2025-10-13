# Supervertaler Project Data Format
## Universal Data Exchange Standard

**Date:** October 14, 2025  
**Version:** 1.0  
**Status:** Implemented in v3.4.0-beta

---

## Overview

The **Supervertaler Project Data Format** is a unified, comprehensive data structure available in two file formats (DOCX and TSV). It serves as the standard for data exchange, archiving, and specialized workflows.

---

## Core Format Specification

### Column Structure (Version 1.0)

| Column | Type | Description | Required |
|--------|------|-------------|----------|
| **ID** | Integer | Segment identifier | ✅ Yes |
| **Status** | String | Translation status (untranslated, draft, translated, approved, locked) | ✅ Yes |
| **Source** | String | Source text | ✅ Yes |
| **Target** | String | Target text | ✅ Yes |
| **Paragraph** | Integer | Original paragraph ID | ✅ Yes |
| **Notes** | String | Translator/proofreader notes | ⚪ Optional |

### File Formats

#### 1. DOCX Format
- **Structure:** Word table with 6 columns
- **Style:** "Light Grid Accent 1"
- **Headers:** Bold text
- **Use case:** Review, printing, Word-based workflows

#### 2. TSV Format
- **Structure:** Tab-separated values
- **Encoding:** UTF-8
- **Header row:** Column names
- **Use case:** Excel analysis, scripting, data processing

---

## Current Implementation

### Export
**Menu:** Export > Supervertaler project data (DOCX/TSV)

**Dialog:** Custom format selection with two buttons:
- "DOCX (Word table)" - Green button
- "TSV (Spreadsheet)" - Blue button

**Methods:**
- `export_supervertaler_data()` - Main entry point with format dialog
- `export_bilingual_docx_full()` - DOCX export with all 6 columns
- `export_tsv()` - TSV export with all 6 columns

### Import
**Status:** Not yet implemented (planned feature)

**Planned functionality:**
- Import DOCX or TSV files in Supervertaler project data format
- Auto-detect format based on file extension
- Validate column structure
- Reimport with full metadata preservation

---

## Future Extensions

### 1. Proofreading Workflow 📝

**Concept:** Round-trip translation → proofreading → reimport

**Export for Proofreading:**
```
Menu: Export > For proofreading (DOCX/TSV)

Format: Same 6-column structure
Special handling:
  - Lock translated segments (status = locked)
  - Add "Proofread by: ___" field
  - Include proofreading instructions
```

**Import from Proofreading:**
```
Menu: Import > Proofread document (DOCX/TSV)

Features:
  - Compare with original segments
  - Track proofreader changes
  - Update targets with proofread versions
  - Preserve status and notes
  - Generate change report
```

**Workflow:**
1. Translator exports "For proofreading (DOCX/TSV)"
2. Proofreader opens in Word/Excel
3. Proofreader edits Target column, adds Notes
4. Translator imports "Proofread document (DOCX/TSV)"
5. Supervertaler shows diff, allows accept/reject changes

---

### 2. Glossary Integration 📚

**Concept:** Export segments as glossary entries

**Export as Glossary:**
```
Menu: Export > As glossary entries (DOCX/TSV)

Format: Extended with glossary-specific columns
| Source Term | Target Term | Context | Domain | Status | Notes |

Features:
  - Filter: Only export segments marked as "glossary entry"
  - Deduplicate: Remove duplicate terms
  - Sort: Alphabetically by source term
```

**Import Glossary:**
```
Menu: Import > Glossary (DOCX/TSV)

Features:
  - Validate term pairs
  - Add to project glossary
  - Link to existing segments
  - Support bulk glossary import
```

**Use case:**
- Build project glossary from translation
- Export glossary for client approval
- Share terminology with team
- Import client-provided glossaries

---

### 3. QA Workflow 🔍

**Concept:** Export for quality assurance checks

**Export for QA:**
```
Menu: Export > For QA review (DOCX/TSV)

Format: Extended with QA-specific columns
| ID | Status | Source | Target | Word Count | QA Status | QA Notes |

Features:
  - Highlight potential issues
  - Add QA checklist columns
  - Include quality metrics
```

**Import QA Results:**
```
Menu: Import > QA results (DOCX/TSV)

Features:
  - Update QA status
  - Import QA notes
  - Flag segments for revision
  - Generate QA report
```

---

### 4. Segment Filtering & Partial Export 🎯

**Concept:** Export subsets based on filters

**Export Filtered Segments:**
```
Menu: Export > Filtered segments (DOCX/TSV)

Options:
  - By status (untranslated, draft, etc.)
  - By paragraph range
  - By search criteria
  - By date modified
  
Use cases:
  - Send untranslated segments to MT service
  - Review only approved segments
  - Export changes since date X
```

---

### 5. Version Comparison 🔄

**Concept:** Compare two versions of same document

**Export for Comparison:**
```
Menu: Export > Version snapshot (DOCX/TSV)

Format: Add version metadata
| ID | Status | Source | Target (v1) | Paragraph | Notes | Timestamp |

Features:
  - Save snapshot at specific point
  - Include version number
  - Add export timestamp
```

**Import & Compare:**
```
Menu: Import > Compare with version (DOCX/TSV)

Features:
  - Diff view showing changes
  - Highlight modified segments
  - Accept/reject changes
  - Merge versions
```

---

### 6. Collaborative Translation 👥

**Concept:** Split project among multiple translators

**Export Segment Range:**
```
Menu: Export > Segment range (DOCX/TSV)

Dialog: "Export segments 1-100, 101-200, etc."

Features:
  - Assign ranges to translators
  - Include original project context
  - Lock assigned segments
```

**Import Translated Range:**
```
Menu: Import > Translated range (DOCX/TSV)

Features:
  - Merge back into main project
  - Validate segment IDs match
  - Update only assigned range
  - Preserve other segments
```

---

## Format Evolution Plan

### Version 1.1 (Future)
**Additional columns:**
- `Modified_Date` - Timestamp of last modification
- `Translator` - Who translated this segment
- `Word_Count_Source` - Source word count
- `Word_Count_Target` - Target word count

### Version 1.2 (Future)
**Additional columns:**
- `Character_Count_Source` - Source character count
- `Character_Count_Target` - Target character count
- `TM_Match` - Best TM match score
- `MT_Used` - Was machine translation used?

### Version 2.0 (Future - Breaking Changes)
**Potential restructuring:**
- Add `Version` column to track format version
- Add `Tags` column for categorization
- Add `Locked_By` for multi-user workflows
- Add `Review_Status` separate from translation status

---

## Technical Implementation Notes

### Backward Compatibility
- Version field in first column or as metadata
- Always include core 6 columns
- New columns optional, ignored by older versions
- File naming: `project_name_v1.0.docx`

### Import Validation
```python
def validate_supervertaler_format(file_path):
    """Validate that file matches Supervertaler format"""
    required_columns = ['ID', 'Status', 'Source', 'Target', 'Paragraph', 'Notes']
    
    # Read first row
    if file_path.endswith('.docx'):
        headers = read_docx_headers(file_path)
    else:  # TSV
        headers = read_tsv_headers(file_path)
    
    # Check required columns present
    missing = [col for col in required_columns if col not in headers]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    return True
```

### Auto-detection
```python
def detect_file_format(file_path):
    """Auto-detect DOCX vs TSV"""
    if file_path.endswith('.docx'):
        return 'docx'
    elif file_path.endswith(('.tsv', '.txt')):
        return 'tsv'
    else:
        raise ValueError("Unsupported file format")
```

---

## Design Principles

1. **Unified Structure** - Same data regardless of file format
2. **Human-Readable** - Can be edited in Word/Excel
3. **Machine-Parsable** - Easy to process programmatically
4. **Extensible** - Can add columns without breaking compatibility
5. **Self-Documenting** - Column names explain content
6. **Reimportable** - Full round-trip capability

---

## Benefits

✅ **Single Standard** - One format for all workflows  
✅ **Tool Agnostic** - Works in Word, Excel, text editors  
✅ **Version Control** - Text-based TSV works with Git  
✅ **Collaborative** - Easy to share and merge  
✅ **Flexible** - DOCX for formatting, TSV for processing  
✅ **Future-Proof** - Extensible without breaking changes  

---

## Migration Path

### Phase 1: Core Implementation ✅ (Done)
- Export DOCX/TSV with 6 columns
- Format selection dialog
- Documentation

### Phase 2: Import (Planned - v3.5.0)
- Import DOCX/TSV
- Validation
- Metadata preservation

### Phase 3: Proofreading (Planned - v3.6.0)
- Export for proofreading
- Import with diff view
- Change tracking

### Phase 4: Glossary (Planned - v3.7.0)
- Export as glossary
- Import glossary
- Glossary management

### Phase 5: Advanced Features (Planned - v3.8.0+)
- QA workflow
- Segment filtering
- Version comparison
- Collaborative features

---

## Example Files

### DOCX Structure
```
┌────┬──────────┬────────────┬────────────┬───────────┬───────┐
│ ID │ Status   │ Source     │ Target     │ Paragraph │ Notes │
├────┼──────────┼────────────┼────────────┼───────────┼───────┤
│ 1  │ approved │ Hello      │ Hallo      │ 0         │       │
│ 2  │ draft    │ Goodbye    │ Tot ziens  │ 0         │       │
└────┴──────────┴────────────┴────────────┴───────────┴───────┘
```

### TSV Structure
```
ID	Status	Source	Target	Paragraph	Notes
1	approved	Hello	Hallo	0	
2	draft	Goodbye	Tot ziens	0	
```

---

## Use Cases Summary

| Workflow | Export | Import | Status |
|----------|--------|--------|--------|
| **Project Archive** | ✅ Implemented | 🔜 Planned | Current release |
| **Proofreading** | 🔜 v3.6.0 | 🔜 v3.6.0 | Planned |
| **Glossary** | 🔜 v3.7.0 | 🔜 v3.7.0 | Planned |
| **QA Review** | 🔜 v3.8.0 | 🔜 v3.8.0 | Planned |
| **Collaboration** | 🔜 v3.9.0 | 🔜 v3.9.0 | Planned |
| **Version Compare** | 🔜 v4.0.0 | 🔜 v4.0.0 | Future |

---

## Related Documentation

- **Export Menu Update:** `EXPORT_MENU_UPDATE.md`
- **Terminology Update:** `TERMINOLOGY_UPDATE_SUMMARY.md`
- **Changelog:** `CHANGELOG-CAT.md`
- **User Guide:** `USER_GUIDE.md` (to be updated)

---

## Conclusion

The **Supervertaler Project Data Format** provides a solid foundation for:
- ✅ Complete data preservation
- ✅ Flexible workflows
- ✅ Tool interoperability
- ✅ Future extensibility

By standardizing on this format, we enable powerful workflows while maintaining simplicity and human-readability. The dual DOCX/TSV approach gives users choice while maintaining data consistency.

**Next step:** Implement import functionality to enable full round-trip workflows! 🚀
