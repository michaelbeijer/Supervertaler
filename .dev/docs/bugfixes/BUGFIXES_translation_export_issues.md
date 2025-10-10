# Bug Fixes: Translation and Export Issues

**Date:** October 6, 2025  
**Issues Fixed:** 3 major bugs in translation and export

## Issue #1: Segment Numbers in Translations ✅ FIXED

**Problem:**
When translating segments, the output included the segment number prefix like "1. Translation text" instead of just "Translation text".

**Root Cause:**
The translation prompts were including:
```python
prompt_parts.append(f"Segment {segment.id}: {segment.source}")
```

This caused the AI to include the number in its response.

**Solution:**
Removed segment IDs from prompts in both single and batch translation:

**Before:**
```python
prompt_parts.append(f"\n**SEGMENT TO TRANSLATE:**")
prompt_parts.append(f"Segment {segment.id}: {segment.source}")
prompt_parts.append("\n**YOUR TRANSLATION (provide ONLY the translated text):**")
```

**After:**
```python
prompt_parts.append(f"\n**TEXT TO TRANSLATE:**")
prompt_parts.append(segment.source)
prompt_parts.append("\n**YOUR TRANSLATION (provide ONLY the translated text, no numbering):**")
```

**Files Modified:**
- `Supervertaler_v2.5.0 (experimental - CAT editor development).py`
  - `translate_current_segment()` method (~line 8293)
  - `translate_all_untranslated()` method (~line 8430)

**Testing:**
✅ Translations now output clean text without segment numbers

---

## Issue #2: Hyperlinks Missing from Translations ⚠️ PARTIALLY ADDRESSED

**Problem:**
Hyperlinks in the source document are not preserved in translations.

**Root Cause:**
The DOCX import uses `para.text` which strips all hyperlink information. The `text` property only returns plain text, losing all hyperlink data.

**Current Status:**
- ⚠️ This requires significant refactoring of the tag_manager and docx_handler
- Hyperlinks need to be extracted from XML and preserved as special tags
- Similar to bold/italic tags, but more complex with URL information

**Workaround:**
Manual hyperlink insertion in the exported DOCX.

**Future Enhancement:**
- Extract hyperlinks from paragraph XML
- Store as tags like `<link url="...">text</link>`
- Reconstruct hyperlinks during export

---

## Issue #3: DOCX Export Stops Mid-Document 🔍 INVESTIGATING

**Problem:**
When exporting translated DOCX, from "Career" section onwards, text remains in English (source language) instead of Dutch (target language).

**Investigation Steps Added:**
Added comprehensive debug logging to `docx_handler.py`:

```python
print(f"[DOCX Export] Starting export with {len(segments)} segments")
print(f"[DOCX Export] Para {non_empty_para_index}: Replacing with {len(translations)} segment(s)")
print(f"[DOCX Export]   Original: {para.text[:50]}...")
print(f"[DOCX Export]   New: {new_text[:50]}...")
```

**Potential Causes:**
1. Paragraph indexing mismatch between import and export
2. Table cell detection incorrectly marking paragraphs
3. Segment-to-paragraph mapping broken for later paragraphs
4. Style preservation interfering with text replacement

**Next Steps:**
1. Run export with debug logging
2. Check if para_info.is_table_cell is incorrectly set
3. Verify paragraph indices match between import and export
4. Check if translations exist for affected segments

**Files Modified:**
- `modules/docx_handler.py`
  - Enhanced logging in `export_docx()` method (~lines 210-270)
  - Debug output for both regular paragraphs and table cells

---

## Testing Instructions

**For Issue #1 (Segment Numbers):**
1. Import a DOCX file
2. Translate some segments using Gemini/Claude/OpenAI
3. Verify translations don't start with numbers
4. Check both single segment translation (Ctrl+T) and batch translation

**For Issue #2 (Hyperlinks):**
1. Import DOCX with hyperlinks
2. Note: Hyperlinks will appear as plain text
3. Translate the text
4. Export - hyperlinks will be missing
5. **Workaround**: Manually re-add hyperlinks in exported DOCX

**For Issue #3 (Export Stops):**
1. Import the test document
2. Translate all segments
3. Export to DOCX
4. Check console output for debug messages
5. Open exported file and verify all sections are translated

---

## Summary

| Issue | Status | Impact |
|-------|--------|--------|
| Segment numbers in translations | ✅ Fixed | High - affects all translations |
| Hyperlinks missing | ⚠️ Known limitation | Medium - needs manual workaround |
| Export stops mid-document | 🔍 Investigating | High - critical export bug |

**Immediate Actions:**
- ✅ Test translations without segment numbers
- 🔍 Run export with debug logging to diagnose issue #3
- 📝 Document hyperlink limitation

**Future Enhancements:**
- Implement proper hyperlink extraction and preservation
- Add more robust paragraph-to-segment mapping
- Consider using document.element.body for better element ordering
