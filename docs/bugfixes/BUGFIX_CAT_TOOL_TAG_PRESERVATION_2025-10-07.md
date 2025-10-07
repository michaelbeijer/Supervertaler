# BUGFIX: CAT Tool Segmentation Tag Preservation (October 7, 2025)

## Issue Identified

AI models were **omitting or incorrectly positioning** CAT tool segmentation markers (like `[1}`, `{2]`, `[3}`, `{4]`) when translating bilingual TXT files exported from memoQ, Trados, CafeTran, and Wordfast.

### Critical Problem Examples:

**Example 1 - Missing Opening Tag:**
```
Source:  [1}De uitvoer van de USSR naar de BLEU{2] (tabel 17 en V)
❌ INCORRECT: USSR exports to the BLEU (Tables IV and V)
✅ CORRECT:   [1}USSR exports to the BLEU{2] (Tables IV and V)
```

**Example 2 - Missing ALL Tags:**
```
Source:  [1}Daarentegen...{2][3} {4]
❌ INCORRECT: By contrast, in other sectors...
✅ CORRECT:   [1}By contrast, in other sectors...{2][3} {4]
```

**Example 3 - Tag Misplacement:**
```
Source:  [1}De uitvoer van machines{2] [3}stelt praktisch niets meer voor...{4]
❌ INCORRECT: [1}Exports of machinery and equipment{2] [3}have virtually dwindled to nothing...{4]
✅ CORRECT:   [1}Exports of machinery and equipment{2] [3}have virtually dwindled to nothing...{4]
```
*(In this case the tags were correct, but the pattern shows importance of exact positioning)*

---

## Root Cause Analysis

### What Are These Tags?

These bracketed markers are **CAT tool segmentation tags**:
- **Format**: `[N}` (opening) and `{N]` (closing) where N is a number
- **Purpose**: Mark segment boundaries for re-import into CAT tools
- **Origin**: memoQ bilingual DOCX/RTF exports, Trados bilingual files, CafeTran exports, Wordfast exports
- **Criticality**: **ESSENTIAL** - Without these tags, files cannot be re-imported into CAT tools

### Why Were They Omitted?

Previous prompts only mentioned:
1. **Formatting tags** (`<b>`, `<i>`, `<u>`) - HTML-style tags
2. **Generic "special formatting markers"** - too vague

The prompts **never explicitly mentioned** bracket/brace style segmentation markers, so AIs treated them as:
- Translatable content
- Optional elements
- Formatting that could be normalized

---

## Solution Implemented

### Updated Prompts (Both v2.4.0 and v2.5.0)

Added comprehensive **"CRITICAL: TAG AND MARKER PRESERVATION"** section to all prompts:

#### Key Instructions Added:

**1. Explicit Tag Pattern Recognition:**
```
If source contains ANY bracketed markers like [1}, {2], [3}, {4], etc.,
reproduce them EXACTLY at SAME positions (start/end of segments)
```

**2. Clear Tag Origin:**
```
These are CAT tool segmentation markers from memoQ, Trados, CafeTran, 
or Wordfast - NEVER translate, move, or omit them
```

**3. Concrete Examples:**
```
Example: '[1}De uitvoer{2]' → '[1}The exports{2]' (tags at exact start/end)
Example: '[1}Text{2][3} {4]' → '[1}Translation{2][3} {4]' (ALL tags preserved)
```

**4. Critical Importance Emphasized:**
```
NEVER translate, move, or omit these markers - they are essential 
for re-importing into CAT tools
```

**5. Distinction from Formatting Tags:**
```
- Bracketed markers [1}, {2]: CAT tool markers → exact position preservation
- Formatting tags <b>, <i>: HTML tags → relative position preservation
```

---

## Files Modified

### v2.4.0 (Stable - Production Ready)
- **File**: `Supervertaler_v2.4.0 (stable - production ready).py`
- **Prompts Updated**: 2
  1. `default_translate_prompt` (lines ~2430-2440)
  2. `default_proofread_prompt` (lines ~2445-2460)

### v2.5.0 (Experimental - CAT Editor)
- **File**: `Supervertaler_v2.5.0 (experimental - CAT editor development).py`
- **Prompts Updated**: 4
  1. `single_segment_prompt` (lines ~1137-1160)
  2. `batch_docx_prompt` (lines ~1163-1180)
  3. `batch_bilingual_prompt` (lines ~1183-1210) ⭐ **MOST CRITICAL** for TXT workflow
  4. `default_proofread_prompt` (lines ~1213-1230)

---

## Technical Details

### Tag Syntax Patterns:

**Opening Tags**: `[N}` where N is a digit
- Examples: `[1}`, `[2}`, `[3}`, `[10}`, `[123}`
- Pattern: Left square bracket + number + right brace

**Closing Tags**: `{N]` where N is a digit
- Examples: `{1]`, `{2]`, `{3]`, `{10]`, `{123]`
- Pattern: Left brace + number + right square bracket

**Tag Positioning Rules**:
1. Opening tags appear at segment START
2. Closing tags appear at segment END
3. Multiple segments can be on same line: `[1}Text{2][3}More text{4]`
4. Spacing between tags must be preserved: `{2][3} {4]` not `{2][3}{4]`

### Why This Syntax?

CAT tools use this **bracket/brace asymmetry** because:
- Easy to distinguish from normal text content
- Unlikely to appear naturally in documents
- Visually distinct pairing: `[` with `}` and `{` with `]`
- Allows nesting if needed
- Machine-readable for re-import

---

## Testing Recommendations

### Test Cases to Verify Fix:

**1. Single Segment with Tags:**
```
Source: [1}De uitvoer van de USSR naar de BLEU{2]
Expected: [1}USSR exports to the BLEU{2]
```

**2. Multiple Segments on One Line:**
```
Source: [1}Eerste zin.{2][3}Tweede zin.{4]
Expected: [1}First sentence.{2][3}Second sentence.{4]
```

**3. Tags with Trailing Spaces:**
```
Source: [1}Tekst hier.{2][3} {4]
Expected: [1}Text here.{2][3} {4]
```

**4. Complex Segment with Both Tag Types:**
```
Source: [1}De <b>uitvoer</b> van machines{2]
Expected: [1}The <b>exports</b> of machinery{2]
```

**5. Multiple Sequential Segments:**
```
Source: [1}Zin 1{2]
        [3}Zin 2{4]
        [5}Zin 3{6]
Expected: [1}Sentence 1{2]
          [3}Sentence 2{4]
          [5}Sentence 3{6]
```

### Real-World Testing:

✅ **Test with actual files from:**
- memoQ bilingual DOCX export
- memoQ bilingual RTF export
- SDL Trados bilingual TXT export
- CafeTran bilingual export
- Wordfast bilingual export

✅ **Verify round-trip:**
1. Export bilingual file from CAT tool
2. Translate with Supervertaler
3. Re-import into CAT tool
4. Confirm segments align correctly

---

## Impact Assessment

### Benefits:

✅ **v2.4.0 (TXT Workflow)**:
- Translations can now be **successfully re-imported** into CAT tools
- No more manual tag correction needed
- Professional workflow integrity maintained

✅ **v2.5.0 (CAT Editor)**:
- Critical for TXT import/export workflow
- Ensures compatibility with memoQ, Trados, CafeTran, Wordfast
- Maintains segment alignment on re-import

### Backward Compatibility:

✅ **No Breaking Changes**:
- Only adds instructions, doesn't change existing behavior
- Files without tags work exactly as before
- HTML formatting tags (`<b>`, `<i>`, `<u>`) still work correctly

---

## User Communication

### For Users of v2.4.0:

> **Important Update**: We've fixed an issue where CAT tool segmentation markers 
> (like [1}, {2]) were sometimes omitted during translation. If you work with 
> bilingual TXT files from memoQ, Trados, CafeTran, or Wordfast, please update 
> to the latest version for proper tag preservation.

### For Users of v2.5.0:

> **Critical Fix for TXT Workflow**: CAT tool segmentation tags are now properly 
> preserved during translation. This ensures your translated bilingual files can 
> be successfully re-imported into your CAT tool without manual corrections.

---

## Related Documentation

- **v2.5.0 TXT Workflow**: See `docs/user_guides/QUICK_START_bilingual_txt_workflow.md`
- **Strategic Direction**: See `docs/planning/STRATEGIC_PIVOT_TXT_bilingual_first.md`
- **Number Formatting Fix**: See `docs/features/NUMBER_FORMATTING_FIX_2025-10-07.md`

---

## Maintenance Notes

### If Adding New Prompts:

Always include this section:
```
**CRITICAL: TAG AND MARKER PRESERVATION**:
- If source contains ANY bracketed markers like [1}, {2], [3}, {4], etc., 
  reproduce them EXACTLY at SAME positions
- These are CAT tool segmentation markers from memoQ, Trados, CafeTran, 
  or Wordfast - NEVER translate, move, or omit them
- Example: '[1}Text{2]' → '[1}Translation{2]' (tags at exact start/end)
- If source contains formatting tags like <b>, <i>, <u>, preserve at 
  relative positions
```

### Future Enhancements:

Consider adding:
- Post-translation tag validation (count source tags vs target tags)
- Warning if tag count mismatch detected
- Tag highlighting in the UI
- Automatic tag insertion shortcuts

---

**Status**: ✅ Fixed and deployed in both v2.4.0 and v2.5.0  
**Priority**: 🔴 CRITICAL (breaks CAT tool re-import workflow)  
**Verification**: Ready for real-world testing with memoQ/Trados files
