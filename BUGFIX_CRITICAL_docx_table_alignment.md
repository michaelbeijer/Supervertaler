# Critical Fix: DOCX Export Table Paragraph Mismatch

**Date**: October 6, 2025  
**Version**: v2.5.0  
**Severity**: HIGH - Data corruption during export

---

## The Problem

### Symptoms
- DOCX export completes without errors
- Everything after a certain point (e.g., "Career") remains in source language
- Translations are present in grid and TMX export works correctly
- Debug output shows mismatched content (wrong translations replacing wrong paragraphs)

### Example from Debug Output
```
[DOCX Export] Para 2: Replacing with 1 segment(s)
[DOCX Export]   Original: About...
[DOCX Export]   New: <b>Biagio Pagano</b> (geboren op 29 januari 1983) ...

[DOCX Export] Para 3: Replacing with 1 segment(s)
[DOCX Export]   Original: Biagio Pagano (born 29 January 1983) is an Italian...
[DOCX Export]   New: Pagano had 250 optredens in de Italiaanse Serie B,...

[DOCX Export] Para 4: Replacing with 1 segment(s)
[DOCX Export]   Original: Pagano had made 250 appearances in Italian Serie B...
[DOCX Export]   New: Persoonlijke informatie...  ← WRONG! This is a table heading!
```

**All translations are shifted by one paragraph!**

---

## Root Cause Analysis

### The Misalignment

The bug occurs because `doc.paragraphs` in python-docx **includes paragraphs inside tables**, but our import/export logic treats them differently.

**During IMPORT** (docx_handler.py import_docx):
```python
# Import processes in order:
1. doc.paragraphs[0] - "Biagio Pagano" → para_id 0
2. doc.paragraphs[1] - "From Wikipedia" → para_id 1  
3. doc.paragraphs[2] - "About" → para_id 2
4. doc.paragraphs[3] - "Biagio Pagano (born...)" → para_id 3
5. doc.paragraphs[4] - "Pagano had made..." → para_id 4
6. doc.paragraphs[5] - "Date of birth" → SKIPPED (in table)
7. doc.paragraphs[6] - "29 January 1983" → SKIPPED (in table)
8. doc.paragraphs[7] - "Place of birth" → SKIPPED (in table)
9. doc.paragraphs[8] - "Naples, Italy" → SKIPPED (in table)
10. doc.paragraphs[9] - "Height" → SKIPPED (in table)
11. doc.paragraphs[10] - "1.80 m" → SKIPPED (in table)

THEN processes tables separately:
- Table[0][0][0] "Date of birth" → para_id 5
- Table[0][0][1] "29 January 1983" → para_id 6
- etc...
```

**During EXPORT** (BEFORE FIX):
```python
# Export was iterating ALL paragraphs:
non_empty_para_index = 0
for para in doc.paragraphs:  # ← Includes table paragraphs!
    if not para.text.strip():
        continue
    
    if para_info and para_info.is_table_cell:
        print("Skipping (is table cell)")
        non_empty_para_index += 1  # ← Increments counter but skips paragraph
        continue
    
    # Replace with para_segments[non_empty_para_index]
    non_empty_para_index += 1
```

**The Result**:
- Iteration 0: para "Biagio Pagano" → para_id 0 ✅
- Iteration 1: para "From Wikipedia" → para_id 1 ✅
- Iteration 2: para "About" → para_id 2 ✅
- Iteration 3: para "Biagio Pagano (born...)" → para_id 3 ✅
- Iteration 4: para "Pagano had made..." → para_id 4 ✅
- Iteration 5: para "Date of birth" → SKIP, increment to para_id 5 ❌
- Iteration 6: para "29 January 1983" → SKIP, increment to para_id 6 ❌
- ...continues skipping table cells...
- Iteration 11: para "Height" → SKIP, increment to para_id 10 ❌

**After all table cells are skipped**, the counter is at 11, but there are only 5 regular paragraphs (0-4). This causes:
1. Para 5 onwards has no translations (nothing in para_segments[11+])
2. Exports stop mid-document
3. Everything after the last regular paragraph remains in source language

---

## The Fix

### Solution: Filter Out Table Paragraphs During Export

**modules/docx_handler.py** (lines ~213-265):

```python
# Build a mapping of paragraph objects in tables
table_paras = set()
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for para in cell.paragraphs:
                table_paras.add(id(para))

print(f"[DOCX Export] Found {len(table_paras)} paragraphs inside tables")

# Process regular paragraphs (excluding those in tables)
non_empty_para_index = 0
for para_idx, para in enumerate(doc.paragraphs):
    # Skip paragraphs that are inside tables
    if id(para) in table_paras:
        print(f"[DOCX Export] Skipping doc.paragraphs[{para_idx}] - it's inside a table")
        continue  # ← Don't increment non_empty_para_index!
    
    # Only process non-empty paragraphs
    if not para.text.strip():
        print(f"[DOCX Export] Skipping doc.paragraphs[{para_idx}] - empty paragraph")
        continue
    
    # Now non_empty_para_index matches import logic
    if non_empty_para_index in para_segments:
        # ... replacement logic ...
        non_empty_para_index += 1  # ← Only increment for actual regular paragraphs
```

### Key Changes

1. **Build table paragraph set first**: Use `id(para)` to identify which paragraphs are in tables
2. **Skip table paragraphs early**: Use `continue` WITHOUT incrementing counter
3. **Only increment for regular paragraphs**: Counter now matches import logic exactly
4. **Enhanced debug logging**: Shows which paragraphs are being skipped and why

---

## Expected Behavior After Fix

### Export Debug Output (AFTER FIX)
```
[DOCX Export] Starting export with 16 segments
[DOCX Export] Found 6 paragraphs inside tables
[DOCX Export] Paragraph segments grouped into 11 paragraph indices
[DOCX Export] Document has 11 paragraphs and 1 tables

[DOCX Export] Para 0: Replacing with 1 segment(s)
[DOCX Export]   Original: Biagio Pagano...
[DOCX Export]   New: Biagio Pagano...

[DOCX Export] Para 1: Replacing with 1 segment(s)
[DOCX Export]   Original: From Wikipedia...
[DOCX Export]   New: Van Wikipedia...

[DOCX Export] Para 2: Replacing with 1 segment(s)
[DOCX Export]   Original: About...
[DOCX Export]   New: Over...  ← CORRECT!

[DOCX Export] Para 3: Replacing with 1 segment(s)
[DOCX Export]   Original: Biagio Pagano (born 29 January 1983)...
[DOCX Export]   New: Biagio Pagano (geboren op 29 januari 1983)...  ← CORRECT!

[DOCX Export] Para 4: Replacing with 1 segment(s)
[DOCX Export]   Original: Pagano had made 250 appearances...
[DOCX Export]   New: Pagano had 250 optredens...  ← CORRECT!

[DOCX Export] Skipping doc.paragraphs[5] - it's inside a table
[DOCX Export] Skipping doc.paragraphs[6] - it's inside a table
[DOCX Export] Skipping doc.paragraphs[7] - it's inside a table
[DOCX Export] Skipping doc.paragraphs[8] - it's inside a table
[DOCX Export] Skipping doc.paragraphs[9] - it's inside a table
[DOCX Export] Skipping doc.paragraphs[10] - it's inside a table

[DOCX Export] Processing 1 tables...
[DOCX Export] Table[0][0][0] Para 5: Replacing
[DOCX Export]   Original: Date of birth...
[DOCX Export]   New: Geboortedatum...  ← CORRECT!
```

---

## Testing

### Test Case 1: Document with Table
1. Import DOCX with paragraphs before and after a table
2. Translate all segments
3. Export to DOCX
4. ✅ All paragraphs should be translated correctly
5. ✅ No shifting or misalignment
6. ✅ Table cells should be translated

### Test Case 2: Multiple Tables
1. Import DOCX with multiple tables interspersed with paragraphs
2. Translate all
3. Export
4. ✅ All content should be in target language

### Test Case 3: Nested Tables (Edge Case)
1. Import DOCX with tables inside table cells
2. ✅ Should handle gracefully (python-docx limitation)

---

## Why This Bug Was Hard to Detect

1. **Silent data corruption**: No errors thrown, export appears successful
2. **Partial success**: First N paragraphs translate correctly
3. **Position-dependent**: Only affects documents with tables
4. **TMX export works**: Because TMX doesn't use paragraph position
5. **Grid view correct**: Translations are actually stored correctly

---

## Impact Assessment

### Documents Affected
- ❌ Any DOCX with tables
- ❌ Documents with mixed paragraphs and tables
- ✅ Plain documents without tables (unaffected)
- ✅ TMX export (unaffected)
- ✅ Grid view (unaffected)

### Data Safety
- ✅ **No data loss**: Translations are stored correctly
- ✅ **Recoverable**: Re-export with fix applied will work
- ❌ **Silent corruption**: Previously exported DOCX files may have this issue

---

## Related Issues Fixed

### Issue: Model Selection Not Persisting
**Status**: Partially fixed, needs more investigation
**Current workaround**: Added detailed logging in save confirmation
```python
messagebox.showinfo("Success", 
    f"API settings saved successfully!\n\n"
    f"Provider: {self.current_llm_provider}\n"
    f"Model: {self.current_llm_model}")
```

---

## Files Modified

### modules/docx_handler.py
- Lines ~213-265: Export logic with table paragraph filtering
- Added: `table_paras` set to track table paragraphs
- Added: Enhanced debug logging
- Changed: Loop logic to skip table paragraphs without incrementing counter

### Supervertaler_v2.5.0.py
- Lines ~7481-7487: Enhanced save confirmation with model details

---

## Conclusion

This was a **critical alignment bug** caused by a mismatch between how `doc.paragraphs` includes table paragraphs and how our import/export logic handles them.

**Before Fix**: Counter incremented for skipped table paragraphs → misalignment → wrong translations → incomplete export

**After Fix**: Table paragraphs skipped early → counter only for regular paragraphs → perfect alignment → correct export

✅ **Bug severity**: HIGH  
✅ **Impact**: Documents with tables  
✅ **Fix complexity**: Medium (required understanding document structure)  
✅ **Testing**: Required on real documents with tables  
✅ **Data safety**: No data loss, re-export will work  

---

## Next Steps

1. ✅ Test with document containing tables
2. ✅ Verify all paragraphs are translated correctly
3. ✅ Confirm table cells are translated
4. ⏳ Investigate model selection persistence issue (separate bug)
5. ⏳ Add regression test for table documents
