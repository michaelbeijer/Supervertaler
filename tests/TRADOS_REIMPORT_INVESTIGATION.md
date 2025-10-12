# Trados Re-Import Investigation Results

## Files Analyzed

1. **Original Trados Export**: `trados-test.docx.review.docx`
   - Empty target cells (for translation)
   - 26 segments
   - UTF-8 encoding with specific XML header

2. **Supervertaler Export**: `trados_bilingual_export.review.docx`
   - Contains translations
   - 26 segments (same)
   - UTF-8 encoding (slightly different XML header)

## Key Findings

### ✅ IDENTICAL Elements:
- Table structure (1 table, 4 columns, 26 rows)
- Table style (Table Grid)
- Segment IDs (UUIDs match perfectly)
- Custom XML metadata (`customXML/item.xml` with segment hashes)
- Custom XML properties (`customXML/itemProps1.xml`)
- Comments.xml (empty in both)
- Settings.xml (trackRevisions enabled in both)
- Document properties (keywords: "sidebyside")
- Package file structure (11 files)
- "Tag" character style (italic, pink FF0066)
- Header row format

### ❌ DIFFERENCES Found:

1. **XML Declaration**:
   - Trados: `<?xml version="1.0" encoding="utf-8"?>`
   - Supervertaler: `<?xml version='1.0' encoding='UTF-8' standalone='yes'?>`

2. **File Size**:
   - Trados original: 32,730 bytes
   - Supervertaler: 32,381 bytes (-349 bytes)

3. **Target Cell Content**:
   - Trados original: Empty (pre-translation)
   - Supervertaler: Contains translations

## Potential Issues for Re-Import

### Most Likely Cause:
The XML encoding declaration difference may cause Trados to reject the file. Trados is EXTREMELY strict about file format.

### Solution Needed:
When saving the updated DOCX, we need to ensure:
1. XML declaration matches EXACTLY: `version="1.0" encoding="utf-8"`
2. NO `standalone='yes'` attribute
3. Use double quotes (") not single quotes (')

## python-docx Library Limitation

The python-docx library uses lxml which automatically adds:
- Single quotes in XML declaration
- `standalone='yes'` attribute  
- UTF-8 (uppercase) encoding name

**This is hardcoded in lxml and cannot be easily changed through python-docx API.**

## Recommended Fix

We have two options:

### Option 1: Post-process the DOCX file
After creating with python-docx, re-write the XML files with correct encoding:
1. Save with python-docx
2. Unzip the DOCX
3. Rewrite `word/document.xml` with exact Trados XML declaration
4. Re-zip the DOCX

### Option 2: Use shutil.copy approach
Instead of creating new document:
1. Make a COPY of the original Trados file
2. Open the copy with python-docx
3. Update ONLY the target cells
4. Save (preserves more of the original XML structure)

**Option 2 is simpler and safer** - it's what we're already trying to do, but we may need to preserve even the XML declaration.

## Next Steps

1. Get the EXACT error message from Trados when re-importing
2. Implement XML post-processing to fix the declaration
3. Test if this resolves the re-import issue

## Testing Checklist

When you try to re-import in Trados, check:
- [ ] Does Trados show a specific error message?
- [ ] Does it import but show warnings?
- [ ] Does it reject the file completely?
- [ ] Does it import but lose some data?

Please provide the exact error/behavior from Trados!
