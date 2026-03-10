# File Format Reference

This page documents the **Supervertaler Project Data Format** (Universal Data Exchange Standard).

If you prefer the repository copy, see: https://github.com/michaelbeijer/Supervertaler/blob/main/docs/specifications/SUPERVERTALER_DATA_FORMAT.md

---

# Supervertaler Project Data Format
## Universal Data Exchange Standard

**Date:** October 14, 2025  
**Version:** 1.0  
**Status:** Implemented

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

### 2. Glossary Integration 📚

**Concept:** Export segments as glossary entries

### 3. QA Workflow 🔍

**Concept:** Export for quality assurance checks

### 4. Segment Filtering & Partial Export 🎯

**Concept:** Export subsets based on filters

### 5. Version Comparison 🔄

**Concept:** Compare two versions of same document

### 6. Collaborative Translation 👥

**Concept:** Split project among multiple translators
