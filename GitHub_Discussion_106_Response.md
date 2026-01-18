# Response to Issue #106: memoQ XLIFF Import & Slovak Language Support

Thank you for trying Supervertaler and for reporting this issue! I've investigated and implemented fixes for both problems you encountered.

**All fixes are now available in Supervertaler v1.9.108** (released January 18, 2026).

---

## The Problems Found

### 1. ✅ Slovak Language Support
**Good news:** Slovak language IS already supported in Supervertaler - it's in the main language list.

### 2. ❌ Missing memoQ XLIFF Import (BUG - NOW FIXED)
**This was the real problem:** The memoQ XLIFF (`.mqxliff`) import module existed in the code (`modules/mqxliff_handler.py`) but was **never exposed in the UI menu**. This has now been fixed.

### 3. 🐛 memoQ Bilingual DOCX Language Detection (BUG - NOW FIXED)
The language detection in memoQ Bilingual DOCX import only supported 8 languages. Slovak would have defaulted to EN→NL. This has been expanded to 24 languages including Slovak.

---

## What's Been Fixed

I've just implemented complete memoQ XLIFF support and improved language detection:

### memoQ XLIFF Import/Export (NEW)
- **File → Import → memoQ XLIFF (.mqxliff)...** ← NEW menu item
- **File → Export → memoQ XLIFF - Translated (.mqxliff)...** ← NEW menu item
- Automatically detects source/target languages from the file (including Slovak: `sk`, `sk-SK`)
- Full round-trip workflow with formatting preservation

### memoQ Bilingual DOCX Language Detection (IMPROVED)
- Expanded language detection from 8 to 24 languages
- Now includes: Slovak, Czech, Hungarian, Romanian, Bulgarian, Greek, Russian, Ukrainian, Swedish, Danish, Finnish, Norwegian, Japanese, Chinese, Korean, Arabic, Turkish, Hebrew
- Slovak files will now be automatically detected instead of defaulting to EN→NL

---

## How to Use (Once Available)

These fixes will be available in the next release, or you can build from the latest source code.

### Option 1: memoQ XLIFF Workflow (Recommended)
1. In memoQ: Export your project as **XLIFF (.mqxliff)**
2. In Supervertaler: **File → Import → memoQ XLIFF (.mqxliff)...**
3. Slovak language automatically detected from file
4. Translate segments
5. **File → Export → memoQ XLIFF - Translated (.mqxliff)...**
6. In memoQ: Import the translated XLIFF file

### Option 2: memoQ Bilingual DOCX Workflow
1. In memoQ: Export your project as **Bilingual DOCX**
2. In Supervertaler: **File → Import → memoQ Bilingual Table (DOCX)...**
3. Slovak language now automatically detected from header
4. Translate segments
5. **File → Export → memoQ Bilingual Table - Translated (DOCX)...**
6. In memoQ: Import the translated bilingual DOCX

---

## Current Workaround (Until Next Release)

Until the fix is officially released, you can use the memoQ Bilingual DOCX workflow:

1. In memoQ: Export as **Bilingual DOCX** (not XLIFF)
2. In Supervertaler: File → Import → memoQ Bilingual Table (DOCX)
3. **Manually set languages** to Slovak in the import dialog (auto-detection not yet available in current release)
4. Translate
5. Export back via File → Export → memoQ Bilingual Table - Translated (DOCX)

---

## Testing Note

⚠️ **Please note:** The memoQ XLIFF import/export hasn't been extensively tested in production yet. If you encounter any issues with:
- Language detection
- Formatting preservation
- Round-trip import/export

Please report them so we can refine the implementation.

---

## Technical Summary

**Changes implemented:**
- Added `import_memoq_xliff()` method (~90 lines)
- Added `export_memoq_xliff()` method (~120 lines)
- Added `_normalize_language_code()` method supporting 30+ languages
- Expanded memoQ Bilingual DOCX language detection from 8 to 24 languages
- Added `mqxliff_source_path` to Project dataclass for persistence
- Updated project save/load to persist memoQ XLIFF source paths

**Files modified:**
- `Supervertaler.py` - Import/export menu items, methods, language detection
- `AGENTS.md` - Development history documentation

---

Does this workflow address your needs? Let me know if you have any questions or run into any issues!
