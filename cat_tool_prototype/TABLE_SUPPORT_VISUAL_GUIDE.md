# Table Support - Visual Guide

## What It Looks Like

### Before (v0.2.0 - No Table Support)
```
ID | Status        | Source                    | Target
---+---------------+---------------------------+-------------------------
1  | Untranslated  | Sample Contract Document  | 
2  | Untranslated  | This is an introduction...| 
3  | Untranslated  | Party Information         | 
(Table cells were ignored - content lost!)
```

### After (v0.3.0 - With Table Support)
```
ID | Type  | Status        | Source                    | Target
---+-------+---------------+---------------------------+-------------------------
1  | Para  | Untranslated  | Sample Contract Document  | 
2  | Para  | Untranslated  | This is an introduction...| 
3  | Para  | Untranslated  | This document contains... | 
4  | Para  | Untranslated  | Party Information         | 
5  | Para  | Untranslated  | The terms and conditions..| 
6  | Para  | Untranslated  | Payment Terms             | 
7  | Para  | Untranslated  | This agreement constitutes| 
8  | Para  | Untranslated  | Signed on this date by... | 
9  | T1R1C1| Untranslated  | Party A                   | 
10 | T1R1C2| Untranslated  | XYZ Corporation, Inc.     | 
11 | T1R2C1| Untranslated  | Party B                   | 
12 | T1R2C2| Untranslated  | ABC Industries Ltd.       | 
13 | T1R3C1| Untranslated  | Effective Date            | 
14 | T1R3C2| Untranslated  | January 1, 2025           | 
15 | T2R1C1| Untranslated  | Installment               | 
16 | T2R1C2| Untranslated  | Amount                    | 
17 | T2R1C3| Untranslated  | Due Date                  | 
18 | T2R2C1| Untranslated  | First Payment             | 
19 | T2R2C2| Untranslated  | $10,000                   | 
20 | T2R2C3| Untranslated  | March 1, 2025             | 
21 | T2R3C1| Untranslated  | Second Payment            | 
22 | T2R3C2| Untranslated  | $15,000                   | 
23 | T2R3C3| Untranslated  | June 1, 2025              | 
24 | T2R4C1| Untranslated  | Final Payment             | 
25 | T2R4C2| Untranslated  | $25,000                   | 
26 | T2R4C3| Untranslated  | September 1, 2025         | 
```

**Note**: Table cells appear in **blue italic** text in the actual UI!

## Type Column Explained

### Type Labels:
- **Para** - Regular paragraph
- **T#R#C#** - Table cell with coordinates:
  - **T#** = Table number (1-based)
  - **R#** = Row number (1-based)
  - **C#** = Cell/Column number (1-based)

### Examples:
- `T1R1C1` = Table 1, Row 1, Cell 1 (first cell of first table)
- `T1R2C3` = Table 1, Row 2, Cell 3 (third cell of second row)
- `T2R4C1` = Table 2, Row 4, Cell 1 (first cell of fourth row in second table)

## Original Document Structure

### Table 1: Party Information
```
+------------------+----------------------+
| Party A          | XYZ Corporation, Inc.|
+------------------+----------------------+
| Party B          | ABC Industries Ltd.  |
+------------------+----------------------+
| Effective Date   | January 1, 2025      |
+------------------+----------------------+
```
**Segments**: 6 cells (3 rows × 2 columns)

### Table 2: Payment Terms
```
+-----------------+-----------+------------------+
| Installment     | Amount    | Due Date         |
+-----------------+-----------+------------------+
| First Payment   | $10,000   | March 1, 2025    |
+-----------------+-----------+------------------+
| Second Payment  | $15,000   | June 1, 2025     |
+-----------------+-----------+------------------+
| Final Payment   | $25,000   | September 1, 2025|
+-----------------+-----------+------------------+
```
**Segments**: 12 cells (4 rows × 3 columns)

## Translation Workflow

### Step 1: Import
```
File → Import DOCX → Select "test_document_with_tables.docx"
```

### Step 2: Translate
```
For each segment:
1. Select segment in grid
2. Type translation in "Target" field
3. Press Ctrl+Enter or click "Save Translation"
4. Status changes to "Translated"
```

### Step 3: Export
```
File → Export Translated DOCX → Choose location
```

**Result**: Original document with:
- All paragraphs translated
- All table cells translated
- Original table structure preserved
- Original formatting maintained

## Real-World Example

### English → Spanish Translation

**Segment #9** (T1R1C1):
- Source: `Party A`
- Target: `Parte A`

**Segment #10** (T1R1C2):
- Source: `XYZ Corporation, Inc.`
- Target: `XYZ Corporation, Inc.` (proper name, unchanged)

**Segment #18** (T2R2C1):
- Source: `First Payment`
- Target: `Primer Pago`

**Segment #19** (T2R2C2):
- Source: `$10,000`
- Target: `$10,000` (numbers, unchanged)

### Exported Table Structure (Spanish):
```
+-----------------+-----------+------------------+
| Cuota           | Monto     | Fecha de Venc.   |
+-----------------+-----------+------------------+
| Primer Pago     | $10,000   | 1 de marzo 2025  |
+-----------------+-----------+------------------+
| Segundo Pago    | $15,000   | 1 de junio 2025  |
+-----------------+-----------+------------------+
| Pago Final      | $25,000   | 1 de sept. 2025  |
+-----------------+-----------+------------------+
```

## Benefits

### For Translators:
✅ **See exactly what you're translating** - No confusion about table vs paragraph
✅ **Context preserved** - Know which cell you're in
✅ **Independent editing** - Each cell is separate
✅ **Visual feedback** - Blue italic for tables

### For Project Managers:
✅ **Accurate segment counts** - Tables included in total
✅ **Progress tracking** - See table vs paragraph completion
✅ **Quality control** - Review tables separately if needed
✅ **Structure integrity** - Original layout maintained

### For Clients:
✅ **Professional output** - Tables look exactly like original
✅ **Complete translation** - Nothing skipped
✅ **Format preservation** - All styling intact
✅ **Ready to use** - No manual formatting needed

## Technical Details

### Import Statistics:
```
[DOCX Handler] Extracted 26 total items:
  - Regular paragraphs: 8
  - Table cells: 18 (from 2 tables)
```

### Document Info:
```
Document Information:
  - Regular paragraphs: 8
  - Table cells: 18
  - Tables: 2
  - Total items: 26
```

### Export Confirmation:
```
[DOCX Handler] Export complete: output.docx
[DOCX Handler] Translated 26 items (paragraphs + table cells)
```

## Color Coding

### Status Colors (Background):
- 🔴 **Red tint** - Untranslated (needs work)
- 🟡 **Yellow tint** - Draft (in progress)
- 🟢 **Green tint** - Translated (complete)
- 🔵 **Blue tint** - Approved (reviewed)

### Type Styling (Text):
- **Black regular** - Paragraph
- **Blue italic** - Table cell

### Combined Example:
- Untranslated paragraph: Red background, black text, "Para"
- Translated table cell: Green background, blue italic text, "T1R2C3"

## Keyboard Shortcuts

### Navigation:
- `↑↓` - Move between segments
- `Enter` - Edit selected segment
- `Ctrl+Enter` - Save and move to next

### Table-Specific Tips:
- Cells are listed in reading order: left→right, top→bottom
- Use Type column to track position in table
- Watch for T# changes (new table starting)

## Edge Cases

### Empty Cells:
- Empty cells are skipped (not segmented)
- Only cells with text become segments

### Merged Cells:
- Treated as single segment
- Full content in one cell

### Nested Tables:
- Each table processed independently
- Numbering may not reflect nesting

---

**Tip**: Import the sample document `test_document_with_tables.docx` to see table support in action!
