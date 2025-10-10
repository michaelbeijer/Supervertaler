# Archive - Abandoned Features

This folder contains documentation for **abandoned features** that were explored but not implemented.

## Files

### MQXLIFF Support (Abandoned)
- `MQXLIFF_NAMESPACE_FIX_TESTING.md` - Testing notes for MQXLIFF format support

## Why MQXLIFF Was Abandoned

**Original Goal:** Add MQXLIFF as an import/export format for memoQ bilingual files.

**Issues Encountered:**
1. Complex nested XML structure caused segment loss
2. Namespace handling was unreliable
3. Formatting preservation was inconsistent
4. Corruption of files during round-trip testing

**Alternative Solution Implemented:**
Instead of MQXLIFF, we implemented **memoQ Bilingual DOCX** support:
- More reliable format
- Easier to parse and manipulate
- Better formatting preservation (programmatic approach with 60% threshold)
- Successfully tested with 27/27 segments

**Implemented in:** v2.4.1  
**See:** `docs/features/MEMOQ_SUPPORT.md`

## Lessons Learned

1. **Simplicity wins:** DOCX format is easier to work with than complex XML
2. **User experience matters:** Bilingual DOCX is more familiar to translators
3. **Testing is critical:** Early testing revealed fundamental issues
4. **Pivot when needed:** Don't be afraid to abandon a problematic approach

---

**Status:** Abandoned  
**Replaced By:** memoQ Bilingual DOCX Support  
**Date:** October 2025
