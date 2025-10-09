# MQXLIFF Import Error Troubleshooting

## Error: "Tool element is not found"

**Error Message:**
```
⛔ General error.
⛔ TYPE: System.Exception
MESSAGE: Tool element is not found
SOURCE: MemoQ.DocConverterFramework
```

### Root Cause

This error occurs when memoQ cannot find the required `<tool>` element in the XLIFF file header. The issue was caused by ElementTree adding namespace prefixes (`<xliff:tool>` instead of `<tool>`) when saving the file, which memoQ's parser doesn't recognize.

### Solution Implemented (v2.4.1+)

The MQXLIFF handler now includes a `_fix_namespace_prefixes()` method that post-processes the saved file to ensure proper namespace structure:

**Before Fix:**
```xml
<xliff:xliff xmlns:xliff="urn:oasis:names:tc:xliff:document:1.2" ...>
  <xliff:file ...>
    <xliff:header>
      <xliff:tool tool-id="MQ" .../>  <!-- ❌ memoQ can't find this -->
    </xliff:header>
  </xliff:file>
</xliff:xliff>
```

**After Fix:**
```xml
<xliff xmlns="urn:oasis:names:tc:xliff:document:1.2" ...>
  <file ...>
    <header>
      <tool tool-id="MQ" .../>  <!-- ✅ memoQ finds this correctly -->
    </header>
  </file>
</xliff>
```

### Technical Details

The fix performs the following transformations:

1. **Root element:** `<xliff:xliff>` → `<xliff>`
2. **Namespace declaration:** `xmlns:xliff="..."` → `xmlns="..."` (default namespace)
3. **Standard XLIFF elements:** Remove `xliff:` prefix from `file`, `header`, `tool`, `body`, `trans-unit`, `source`, `target`, etc.
4. **memoQ extensions:** Keep `mq:` prefix for memoQ-specific elements
5. **Formatting tags:** Remove `xliff:` prefix from `bpt`, `ept`, `ph`, etc.

### Verification

After export, you can verify the file structure by opening it in a text editor:

**Check Line 1-5:**
```xml
<?xml version='1.0' encoding='utf-8'?>
<xliff xmlns="urn:oasis:names:tc:xliff:document:1.2" ...>
<file ...>
<header>
<tool tool-id="MQ" tool-name="MemoQ" .../>
```

✅ **Correct:** No `xliff:` prefixes on standard elements  
❌ **Incorrect:** `<xliff:tool>` or `<xliff:file>` with prefixes

### If You Still Get the Error

1. **Check file encoding:** Must be UTF-8
2. **Verify XML structure:** Ensure no manual edits broke the XML
3. **memoQ version:** Ensure you're using memoQ 9.0 or later
4. **File location:** Try saving to a local drive (not network/cloud)
5. **Re-export from Supervertaler:** Try the export process again

### Manual Fix (if needed)

If you have an MQXLIFF file with this issue, you can manually fix it:

1. Open the `.mqxliff` file in a text editor (Notepad++, VS Code, etc.)
2. Find and replace:
   - `<xliff:xliff ` → `<xliff `
   - `</xliff:xliff>` → `</xliff>`
   - `xmlns:xliff=` → `xmlns=`
   - `<xliff:file` → `<file`
   - `<xliff:header` → `<header`
   - `<xliff:tool` → `<tool`
   - `<xliff:body` → `<body`
   - `<xliff:trans-unit` → `<trans-unit`
   - `<xliff:source` → `<source`
   - `<xliff:target` → `<target`
   - etc. (for all XLIFF standard elements)
3. **Do NOT remove `mq:` prefixes** - these are required
4. Save the file and try importing again

### Prevention

- Always use Supervertaler v2.4.1 or later for MQXLIFF export
- Don't manually edit MQXLIFF files unless absolutely necessary
- Keep backups of original MQXLIFF files before translation
- Test with small files first to verify your workflow

### Related Issues

- **"Invalid XLIFF file"** - Usually a syntax error or broken XML structure
- **"Unsupported XLIFF version"** - memoQ expects XLIFF 1.2
- **"Cannot parse file"** - File encoding or XML structure issue

### Support

If the issue persists:
1. Check the error log in memoQ (View → Error Log)
2. Verify the MQXLIFF file opens in an XML validator
3. Compare the structure with a known-good MQXLIFF export from memoQ
4. Consider using the DOCX workflow as a temporary workaround

---

**Status:** ✅ Fixed in Supervertaler v2.4.1  
**Date:** October 9, 2025  
**Affected Versions:** v2.4.1 (initial release) - fixed in subsequent updates
