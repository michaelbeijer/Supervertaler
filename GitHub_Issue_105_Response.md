# Response to Issue #105: TMX Import Language Pair Reversal

Thank you for reporting this bug! You've identified a critical issue in the TMX import code.

**All fixes are now available in Supervertaler v1.9.109** (released January 18, 2026).

---

## The Problem

When importing TMX files, the language pair was sometimes reversed:
- **Expected:** EN-GB → DE-DE (English to German)
- **Actual:** DE-DE → EN-GB (German to English)

This made it impossible to find matches for translated segments.

---

## Root Cause

The TMX import code was incorrectly assuming that the **first language in the TMX file** was the source language and the **second** was the target language. However, TMX files list languages in arbitrary order (often alphabetically), so this assumption was wrong.

For example:
- Your TMX file contained: `en-GB, de-DE` (in that order)
- The code correctly imported it as EN-GB → DE-DE
- But a file with: `de-DE, en-GB` (alphabetical order) was incorrectly imported as DE-DE → EN-GB

---

## The Fix

I've added a **language pair selection dialog** when importing TMX files. Now you explicitly choose which language should be source and which should be target:

1. Select **File → Import TMX File** (from TM Manager)
2. Choose your TMX file
3. **NEW:** Dialog shows all detected languages (e.g., "de-DE, en-GB")
4. **NEW:** You select: Source = en-GB, Target = de-DE
5. Import proceeds with correct language pair
6. TM matches now work correctly!

---

## How to Update

### Option 1: Pip Install (Recommended)
```bash
pip install --upgrade supervertaler
```

### Option 2: Windows EXE
Download the latest Windows release from: https://github.com/michaelbeijer/Supervertaler/releases/latest

---

## Verification

To verify the fix worked:
1. Re-import your TMX file
2. Select the correct language pair in the new dialog
3. Open a translated segment
4. Check that TM matches appear in the Translation Results panel

---

## Files Modified

- `Supervertaler.py` - Added language selection dialog in `_import_tmx_as_tm()` method (2 locations: "Create new TM" and "Add to existing TM" workflows)

---

## Related

This fix applies to both workflows:
- **Create new TM from TMX** - Now lets you select language pair
- **Add to existing TM from TMX** - Now lets you select language pair when TM has no languages

---

Does this resolve your issue? Let me know if you encounter any other problems!
