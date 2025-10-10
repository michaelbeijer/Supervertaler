# Trados Studio XML-Style Tags Support Update

**Date**: October 7, 2025  
**Type**: Enhancement to CAT Tool Tag Preservation  
**Versions**: v2.4.0, v2.5.0  
**Priority**: HIGH  
**Status**: ✅ COMPLETE

---

## Background

### Discovery
User identified that Trados Studio's "external review" files use a different tag format than the memoQ-style tags initially documented:

**Trados Studio Format**:
```
<410>De uitvoer van machines en toestellen</410> <434>stelt praktisch niets meer voor</434>
```

**Previously Documented Formats**:
- memoQ: `[1}text{2]` (asymmetric bracket-brace pairs)
- CafeTran: `|1|text|2|` (pipe-delimited)

### Assessment
The existing CAT tool tag preservation instructions (implemented on October 7, 2025) used general language like "bracketed/special characters" and mentioned "Trados" by name, but:

- ❌ **Did not explicitly show XML-style tag examples** like `<410>` and `</410>`
- ❌ **Did not clarify opening/closing tag pairs** vs asymmetric pairs
- ❌ **Could be ambiguous** for AI models encountering angle-bracket tags

**Risk**: AI models might treat `<410>text</410>` as HTML-like content rather than CAT tool tags, potentially:
- Removing them as "markup"
- Translating numeric IDs
- Treating them inconsistently

---

## Solution Implemented

### Updated Tag Formats Documentation

All 6 prompts now explicitly list the three main tag format types:

```
- Source may contain CAT tool formatting tags in various formats:
  • memoQ: [1}, {2], [3}, {4] (asymmetric bracket-brace pairs)
  • Trados Studio: <410>text</410>, <434>text</434> (XML-style opening/closing tags)
  • CafeTran: |1|, |2| (pipe-delimited)
  • Other CAT tools: various bracketed or special character sequences
```

### Added Trados-Specific Examples

Each prompt now includes explicit Trados Studio examples:

**Single Segment Prompt**:
```
- Examples:
  • memoQ: '[1}De uitvoer{2]' → '[1}The exports{2]'
  • Trados: '<410>De uitvoer van machines</410>' → '<410>Exports of machinery</410>'
  • Multiple: '[1}De uitvoer{2] [3}stelt niets voor{4]' → '[1}Exports{2] [3}mean nothing{4]'
```

**Batch DOCX Prompt**:
```
- Example: '<410>De uitvoer</410> <434>stelt niets voor</434>' → '<410>Exports</410> <434>mean nothing</434>'
```

**Batch Bilingual Prompt**:
```
- Example: '<410>De uitvoer van machines</410> <434>stelt niets voor</434>' → '<410>Exports of machinery</410> <434>mean nothing</434>'
```

**Proofread Prompt**:
```
- Example: '<410>The exports</410>' remains '<410>The exports</410>'
```

---

## Files Modified

### v2.5.0 (Experimental - CAT Editor Development)
**File**: `Supervertaler_v2.5.0 (experimental - CAT editor development).py`

**Prompts Updated** (4 total):

1. **`single_segment_prompt`** (lines ~1149-1165)
   - Added 3-format breakdown with bullet points
   - Added Trados example: `<410>De uitvoer van machines</410>`
   - Comprehensive multi-format examples

2. **`batch_docx_prompt`** (lines ~1175-1183)
   - Compact format listing (memoQ | Trados | CafeTran)
   - Trados example with multiple tags
   - Emphasis on preserving ALL tags

3. **`batch_bilingual_prompt`** (lines ~1198-1208)
   - Same compact format
   - Real-world Trados example from user's file
   - Clear preservation instructions

4. **`default_proofread_prompt`** (lines ~1221-1231)
   - Compact format for proofreading context
   - Trados example showing tag stability in edits
   - Focus on maintaining existing tags

### v2.4.0 (Stable - Production Ready)
**File**: `Supervertaler_v2.4.0 (stable - production ready).py`

**Prompts Updated** (2 total):

1. **`default_translate_prompt`** (lines ~2435-2452)
   - Full 3-format breakdown with descriptions
   - Multiple Trados examples
   - Comprehensive format coverage

2. **`default_proofread_prompt`** (lines ~2459-2468)
   - Compact format listing
   - Trados example for proofreading
   - Clear tag preservation rules

---

## Technical Details

### Tag Format Characteristics

**memoQ Tags**:
- Format: `[N}...{M]` where N and M are sequential numbers
- Asymmetric: Opening `[1}` differs from closing `{2]`
- Can wrap multiple words or sentences
- Tags reposition with content

**Trados Studio Tags**:
- Format: `<NNN>...</NNN>` where NNN is a numeric ID
- XML-style: Opening `<410>` mirrors closing `</410>`
- Numeric IDs can be 2-4 digits
- Opening and closing tags always match
- Tags represent inline formatting elements

**CafeTran Tags**:
- Format: `|N|...|M|` where N and M are numbers
- Pipe-delimited: Uses vertical bar character
- Simpler structure than memoQ or Trados

### Preservation Rules (All Formats)

1. **Count Preservation**: If source has N tags, target must have N tags
2. **Format Preservation**: Never modify tag structure (`<410>` stays `<410>`, not `<411>`)
3. **Repositioning Allowed**: Tags move with content for natural target language structure
4. **No Translation**: Tag identifiers (numbers, IDs) never get translated
5. **Pair Integrity**: Opening/closing pairs must remain matched

---

## Examples from User's File

### Original Trados Studio Text
```
<410>De uitvoer van machines en toestellen</410> <434>stelt praktisch niets meer voor : amper 0,4 % van de totale exportwaarde, een bedenkenswaardig resultaat, daar waar de Sovjetambities tijdens de bijeenkomst van de werkgroep "Machines en uitrustingsgoederen" (juni 87) in de richting gingen van een spektakulaire verruiming van het toen als bijzonder laag beschouwde aandeel van 5 % ongeveer.</434>
```

### Expected Translation
```
<410>Exports of machinery and equipment</410> <434>mean practically nothing anymore: barely 0.4% of total export value, a noteworthy result, given that Soviet ambitions during the "Machinery and Equipment" working group meeting (June 87) were moving toward a spectacular expansion of what was then considered a particularly low share of approximately 5%.</434>
```

### Key Points
- ✅ Both `<410>` and `</410>` preserved
- ✅ Both `<434>` and `</434>` preserved  
- ✅ Total tag count: 4 → 4
- ✅ Tags wrap appropriate content
- ✅ Numeric IDs unchanged (410 stays 410, 434 stays 434)
- ✅ Natural English word order maintained

---

## Testing Recommendations

### Test Case 1: Basic Trados Tags
**Input**:
```
<410>De uitvoer</410> is laag.
```

**Expected Output**:
```
<410>Exports</410> are low.
```

**Validation**:
- [ ] Opening tag `<410>` preserved
- [ ] Closing tag `</410>` preserved
- [ ] Tags wrap correct content
- [ ] Translation is accurate

### Test Case 2: Multiple Trados Tag Pairs
**Input**:
```
<410>De uitvoer van machines</410> <434>stelt niets voor</434>.
```

**Expected Output**:
```
<410>Exports of machinery</410> <434>mean nothing</434>.
```

**Validation**:
- [ ] All 4 tags preserved (2 pairs)
- [ ] Tag IDs unchanged (410, 434)
- [ ] Pairs remain matched
- [ ] Content appropriately wrapped

### Test Case 3: Mixed Tag Formats (memoQ + Trados)
**Input**:
```
[1}De <410>uitvoer</410> van machines{2] is laag.
```

**Expected Output**:
```
[1}<410>Exports</410> of machinery{2] are low.
```

**Validation**:
- [ ] memoQ tags `[1}` and `{2]` preserved
- [ ] Trados tags `<410>` and `</410>` preserved
- [ ] All 4 tags present in output
- [ ] Natural word order achieved

### Test Case 4: Tag Repositioning
**Input**:
```
<410>machines</410> <434>uitvoer</434>
```

**Expected Output** (if natural in target language):
```
<434>exports</434> <410>machinery</410>
```

**OR** (if source order is natural):
```
<410>machinery</410> <434>exports</434>
```

**Validation**:
- [ ] All tags preserved
- [ ] Tag IDs unchanged
- [ ] Pairs remain matched
- [ ] Translation is natural

---

## Impact Assessment

### Before This Update
- ⚠️ **Ambiguous**: AI might treat `<410>` as HTML or generic markup
- ⚠️ **Risk of Omission**: Tags could be removed as "formatting"
- ⚠️ **Inconsistent Handling**: Different behavior for memoQ vs Trados tags

### After This Update
- ✅ **Explicit**: Trados Studio format clearly documented
- ✅ **Comprehensive Examples**: Real-world Trados tag examples provided
- ✅ **Consistent Treatment**: All CAT tool formats treated equally
- ✅ **Lower Risk**: AI models have clear guidance for XML-style tags

---

## Compatibility Matrix

| CAT Tool | Tag Format | Support Status | Example |
|----------|-----------|----------------|---------|
| **memoQ** | `[N}...{M]` | ✅ Fully Supported | `[1}text{2]` |
| **Trados Studio** | `<NNN>...</NNN>` | ✅ **NOW Supported** | `<410>text</410>` |
| **CafeTran** | `\|N\|...\|M\|` | ✅ Fully Supported | `\|1\|text\|2\|` |
| **Wordfast** | Various | ⚠️ Generic Support | (depends on format) |
| **OmegaT** | Various | ⚠️ Generic Support | (depends on format) |

---

## Migration Notes

### No Breaking Changes
- ✅ All existing tag handling remains functional
- ✅ Previous memoQ/CafeTran examples still work
- ✅ New Trados examples additive only
- ✅ No user action required

### Backward Compatibility
- ✅ Works with existing projects
- ✅ Compatible with v2.4.0 and v2.5.0
- ✅ No changes to tag detection logic
- ✅ Prompts only enhanced, not rewritten

---

## Documentation Updates

### Created
- ✅ This document: `TRADOS_XML_TAGS_UPDATE_2025-10-07.md`

### To Update
- [ ] `CAT_TOOL_TAG_FIX_SUMMARY.md` - Add Trados format
- [ ] `SESSION_SUMMARY_2025-10-07.md` - Add this update
- [ ] User guide - Update CAT tool compatibility section
- [ ] README - Add Trados Studio to supported CAT tools list

---

## Related Documents

- **Original Tag Fix**: `BUGFIX_CAT_TOOL_TAG_PRESERVATION_2025-10-07.md`
- **Summary**: `CAT_TOOL_TAG_FIX_SUMMARY.md`
- **Session Summary**: `SESSION_SUMMARY_2025-10-07.md`

---

## Conclusion

This update ensures comprehensive support for Trados Studio's XML-style tag format in addition to the previously documented memoQ and CafeTran formats. By explicitly listing all three major formats with concrete examples, AI models will have unambiguous guidance for preserving CAT tool tags regardless of the source tool.

**Status**: ✅ **COMPLETE**  
**Prompts Updated**: 6 (4 in v2.5.0, 2 in v2.4.0)  
**Testing**: Recommended before production use  
**User Action**: None required (automatic with updated versions)

---

*Document Version: 1.0*  
*Last Updated: October 7, 2025*  
*Author: GitHub Copilot*
