# MQXLIFF Namespace Fix - Testing Guide

## What Was Fixed

The MQXLIFF handler was adding namespace prefixes (`xliff:`) to standard XLIFF elements, which memoQ couldn't recognize. Specifically, the `<tool>` element was being written as `<xliff:tool>`, causing memoQ to throw the error "Tool element is not found".

## Changes Made

**File Modified:** `modules/mqxliff_handler.py`

**New Methods:**
1. `_fix_namespace_prefixes()` - Post-processes saved MQXLIFF files to remove unwanted namespace prefixes
2. Updated `save()` method - Now calls the namespace fix after writing

**What the Fix Does:**
- Converts `<xliff:xliff>` to `<xliff>`
- Converts `xmlns:xliff="..."` to `xmlns="..."` (default namespace)
- Removes `xliff:` prefixes from all standard XLIFF elements
- Preserves `mq:` prefixes for memoQ extensions

## How to Test

### 1. Use the Test File

The handler already includes a test mode:

```powershell
cd "c:\Users\mbeijer\My Drive\Software\Python\Supervertaler"
python modules\mqxliff_handler.py "projects\test_document (memoQ bilingual).mqxliff"
```

This will:
- Load the original MQXLIFF file
- Extract segments
- Create dummy translations
- Save to `projects\test_document (memoQ bilingual)_test_output.mqxliff`

### 2. Verify the Output File Structure

Open `test_document (memoQ bilingual)_test_output.mqxliff` in a text editor.

**Check the first 5 lines:**
```xml
<?xml version='1.0' encoding='utf-8'?>
<xliff xmlns="urn:oasis:names:tc:xliff:document:1.2" ...>
<file ...>
<header>
<tool tool-id="MQ" tool-name="MemoQ" .../>
```

✅ **Success:** No `xliff:` prefixes visible  
❌ **Failed:** You see `<xliff:tool>` or `<xliff:file>`

### 3. Test Import in memoQ

1. Open your memoQ project
2. Go to **Translations** → **Import Bilingual**
3. Select the test output file: `test_document (memoQ bilingual)_test_output.mqxliff`
4. Import should complete without the "Tool element is not found" error

**Expected Result:** ✅ Import succeeds, segments show as "Confirmed"

### 4. Full Workflow Test

To test the complete workflow:

1. **Export from memoQ:**
   - Export bilingual MQXLIFF from your project

2. **Import to Supervertaler:**
   - Run Supervertaler v2.4.1
   - Click "📄 Import MQXLIFF (Recommended)"
   - Select your MQXLIFF file

3. **Translate:**
   - Configure your translation settings
   - Click "Translate"
   - Wait for completion

4. **Export from Supervertaler:**
   - Click "💾 Export to MQXLIFF"
   - Save the translated file

5. **Import back to memoQ:**
   - In memoQ: **Translations** → **Import Bilingual**
   - Select the translated MQXLIFF file
   - **Should import successfully without errors**

### 5. Verify Formatting Preservation

After import to memoQ:
- Check that bold text is still bold
- Check that italic text is still italic  
- Check that underlined text is still underlined
- Check that hyperlinks are preserved

## What to Look For

### ✅ Success Indicators
- memoQ accepts the file without errors
- All segments imported correctly
- Formatting (bold, italic, underline) preserved
- Hyperlinks maintained
- Segment status set to "Confirmed"

### ❌ Failure Indicators
- "Tool element is not found" error
- "Invalid XLIFF file" error
- Missing formatting in imported segments
- Broken hyperlinks

## Known Limitations

1. **Very different translation lengths:** If translation is much longer/shorter than source, formatting may be simplified to plain text (this is intentional to avoid breaking the XML structure)

2. **Complex nested formatting:** Some very complex nested structures might not preserve perfectly

3. **Custom memoQ tags:** Advanced memoQ-specific tags beyond basic formatting may not be fully preserved

## Rollback Plan

If you encounter issues, you can:

1. **Use DOCX workflow instead:** Click "📄 Import DOCX" (green button)
2. **Manual export:** Use traditional text file workflow
3. **Previous version:** Revert to using the original memoQ bilingual DOCX feature

## Test Results Expected

With the namespace fix:
- ✅ File loads in memoQ without "Tool element is not found" error
- ✅ All 18 segments imported
- ✅ Formatting tags preserved (bold, italic, underline)
- ✅ Status set to "Confirmed"
- ✅ File structure matches memoQ's expectations

## Questions or Issues?

If you encounter any problems:
1. Check the console output for error messages
2. Verify the MQXLIFF file structure manually
3. Try with a smaller test file first
4. Report any errors with the full error message

---

**Last Updated:** October 9, 2025  
**Status:** Ready for testing
