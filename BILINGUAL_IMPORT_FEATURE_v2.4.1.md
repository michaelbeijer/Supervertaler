# Supervertaler v2.4.1 - Bilingual Import Feature

**Date**: October 7, 2025  
**Status**: ✅ EXPERIMENTAL - READY FOR TESTING  
**Based on**: v2.4.0 (stable - production ready)

---

## 🎯 What's New in v2.4.1

### NEW FEATURE: memoQ Bilingual DOCX Import/Export

v2.4.1 adds the ability to **work directly with memoQ bilingual DOCX files**, eliminating the need for manual copy-paste workflows.

### Key Capabilities:

1. **Import** memoQ bilingual DOCX files
2. **Extract** source segments automatically
3. **Translate** using existing Supervertaler workflow
4. **Export** translations back to bilingual format
5. **Preserve** all segment IDs, metadata, and CAT tool tags

---

## 🔧 What Changed from v2.4.0

### Files Modified:
- ✅ Created `Supervertaler_v2.4.1 (bilingual import experimental).py`
- ✅ v2.4.0 remains **completely untouched**

### Code Changes:
1. **Version updated**: `APP_VERSION = "2.4.1"`
2. **New functions added** (~200 lines):
   - `import_memoq_bilingual()` - Import bilingual DOCX
   - `export_memoq_bilingual()` - Export to bilingual DOCX
3. **UI enhancements**:
   - Green "📄 Import memoQ Bilingual DOCX" button (after input file)
   - Blue "💾 Export to Bilingual DOCX" button (after process buttons)

### Safety:
- ✅ **Zero changes to existing functionality**
- ✅ **Additive only** - no modifications to existing code
- ✅ **Backward compatible** - all existing workflows unchanged
- ✅ **v2.4.0 untouched** - production version remains safe

---

## 📋 Testing Checklist

### Phase 1: Basic Functionality Test ✅
- [x] v2.4.1 starts successfully
- [x] Version shows "2.4.1" in title bar
- [x] UI loads with new buttons visible
- [x] No startup errors

### Phase 2: Bilingual Import Test
Test file: `projects/memoQ bilingual.docx`

**Steps to test:**
1. Launch v2.4.1
2. Click **"📄 Import memoQ Bilingual DOCX"** button
3. Select `projects/memoQ bilingual.docx`
4. Verify success message shows "27 segments imported"
5. Check that input file is set to `memoQ bilingual_source.txt`
6. Verify temp TXT file created in projects folder

**Expected results:**
- ✅ Import dialog appears
- ✅ Success message: "Successfully imported 27 segment(s)..."
- ✅ Input file path updated automatically
- ✅ Temp TXT file contains source segments (Dutch text)
- ✅ CAT tool tags preserved: `[1}`, `{2]`, etc.

### Phase 3: Translation Test

**Steps to test:**
1. After import, configure translation settings:
   - Source language: Dutch
   - Target language: English
   - Select API provider (Gemini/Claude/OpenAI)
   - Enter API key
   - Choose model
2. Set output file location
3. Click **"Translate"**
4. Wait for translation to complete
5. Check output TXT file

**Expected results:**
- ✅ Translation processes all 27 segments
- ✅ Output TXT contains English translations
- ✅ CAT tool tags preserved in translations
- ✅ Tag positions adjusted appropriately for English
- ✅ No segments skipped

### Phase 4: Bilingual Export Test

**Steps to test:**
1. After translation completes successfully
2. Click **"💾 Export to Bilingual DOCX"** button
3. Choose save location (e.g., `memoQ bilingual_translated.docx`)
4. Verify success message

**Expected results:**
- ✅ Export dialog appears
- ✅ File saves successfully
- ✅ Success message: "Successfully exported 27 translation(s)..."

### Phase 5: Verification Test

**Steps to verify exported file:**
1. Open `memoQ bilingual_translated.docx` in Word
2. Check table structure:
   - Row 0: Header intact
   - Row 1: Column headers intact
   - Rows 2-28: Segment data
3. Verify Column 0 (ID): **Unchanged** from original
4. Verify Column 1 (Source): **Unchanged** from original
5. Verify Column 2 (Target): **Now contains English translations**
6. Verify Column 3 (Comment): **Unchanged**
7. Verify Column 4 (Status): **Updated to "Confirmed"**
8. Check specific segments with tags:
   - Row 10: Tags like `[1}`, `{2]` preserved
   - Row 12: Multiple tags handled correctly

**Critical checks:**
- ✅ Segment IDs **completely unchanged**
- ✅ Source text **completely unchanged**
- ✅ Target contains **valid translations**
- ✅ CAT tags **preserved and properly positioned**
- ✅ Status updated to **"Confirmed"**

### Phase 6: Backward Compatibility Test

**Test regular TXT workflow (ensure v2.4.1 didn't break anything):**

1. Close v2.4.1 and restart
2. Click regular **"Browse..."** button (NOT bilingual button)
3. Select a regular TXT file (not bilingual DOCX)
4. Configure translation normally
5. Translate
6. Verify output

**Expected results:**
- ✅ Regular TXT import works exactly as in v2.4.0
- ✅ Translation works normally
- ✅ Output TXT + TMX generated correctly
- ✅ No errors or unexpected behavior

### Phase 7: Error Handling Test

**Test invalid inputs:**

1. **Import non-bilingual DOCX:**
   - Click import button
   - Select regular DOCX (not bilingual)
   - Verify error message shown

2. **Export without import:**
   - Don't import bilingual file
   - Click export button
   - Verify warning message: "No bilingual file was imported"

3. **Export before translation:**
   - Import bilingual file
   - Don't translate
   - Click export button
   - Verify error: "No output file found"

**Expected results:**
- ✅ Appropriate error messages shown
- ✅ No crashes or freezes
- ✅ User can recover and continue

---

## 🎯 Success Criteria

v2.4.1 is ready for production if:

- ✅ All Phase 1-7 tests pass
- ✅ No crashes or errors
- ✅ v2.4.0 functionality unaffected
- ✅ Bilingual workflow completes end-to-end
- ✅ Tags preserved correctly
- ✅ Segment IDs unchanged
- ✅ Error handling works appropriately

---

## 📊 Technical Details

### Import Process Flow:
```
1. User selects memoQ bilingual DOCX
2. python-docx reads table structure
3. Extracts source text from Column 1 (rows 2+)
4. Creates temporary TXT file: `filename_source.txt`
5. Sets input file path to temp TXT
6. Stores original DOCX path in `self.bilingual_source_file`
7. User continues with normal translation workflow
```

### Export Process Flow:
```
1. User clicks export button
2. Check if bilingual source file exists
3. Read translations from output TXT file
4. Load original bilingual DOCX
5. Write translations to Column 2 (target)
6. Update Column 4 (status) to 'Confirmed'
7. Prompt user to save updated DOCX
8. File ready for reimport to memoQ
```

### Tag Preservation:
- Tags stored as **plain text runs** in DOCX cells
- No special formatting on tags
- AI preserves tags based on system prompts
- Three formats supported:
  - memoQ: `[1}...{2]`
  - Trados: `<410>...</410>`
  - CafeTran: `|1|...|2|`

### Dependencies:
- **python-docx**: Required for DOCX reading/writing
- Already installed in your environment
- Import/export functions check for library and show friendly error if missing

---

## 🚀 Next Steps

### If Testing Succeeds:
1. ✅ Mark v2.4.1 as **stable**
2. ✅ Archive v2.4.0 to `Previous versions/`
3. ✅ Rename v2.4.1 to production filename
4. ✅ Update documentation
5. ✅ Consider porting to v2.5.0

### If Issues Found:
1. ❌ Document specific issues
2. ❌ Keep using v2.4.0 (unaffected)
3. ❌ Fix issues in v2.4.1
4. ❌ Retest before production

---

## 📝 Version Comparison

| Feature | v2.4.0 (Stable) | v2.4.1 (Experimental) |
|---------|-----------------|----------------------|
| **Status** | Production Ready | Testing Phase |
| **TXT Import** | ✅ Yes | ✅ Yes (Unchanged) |
| **Bilingual Import** | ❌ No | ✅ **NEW** |
| **Bilingual Export** | ❌ No | ✅ **NEW** |
| **Tag Preservation** | ✅ Yes | ✅ Yes (Same) |
| **All Other Features** | ✅ Working | ✅ Identical |

---

## ⚠️ Important Notes

1. **v2.4.0 is untouched** - your production version is 100% safe
2. **Test thoroughly** before replacing v2.4.0
3. **Keep both versions** until confident in v2.4.1
4. **Bilingual feature is optional** - doesn't affect existing workflows
5. **Report any issues** before moving to production

---

## 🎓 User Guide Snippet

### How to Use Bilingual Import

**For memoQ Users:**

1. **Export from memoQ:**
   - In memoQ, select your project
   - Go to `Translations` → `Export for review`
   - Choose "Bilingual DOCX" format
   - Save the file

2. **Import to Supervertaler:**
   - Launch Supervertaler v2.4.1
   - Click the green **"📄 Import memoQ Bilingual DOCX"** button
   - Select your exported DOCX file
   - Success message will confirm import

3. **Translate as usual:**
   - Configure source/target languages
   - Select API provider and model
   - Click "Translate"
   - Wait for completion

4. **Export back to memoQ:**
   - Click the blue **"💾 Export to Bilingual DOCX"** button
   - Choose where to save the translated file
   - Success message confirms export

5. **Import to memoQ:**
   - In memoQ, go to `Translations` → `Import review`
   - Select your translated DOCX file
   - Translations appear with "Confirmed" status

**Benefits:**
- ✅ No manual copy-paste
- ✅ Preserves all formatting tags
- ✅ Maintains segment IDs
- ✅ Faster workflow
- ✅ Less error-prone

---

## 📞 Support

**Questions or Issues?**
- Test file provided: `projects/memoQ bilingual.docx` (27 segments)
- Check this document for troubleshooting
- v2.4.0 remains available as fallback

**Created**: October 7, 2025  
**Last Updated**: October 7, 2025  
**Version**: 2.4.1 (Experimental)
