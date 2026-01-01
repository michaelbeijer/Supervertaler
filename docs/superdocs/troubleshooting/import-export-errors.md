# Import/Export Errors

This page covers common problems when importing or exporting files.

## “Cannot read file” / import fails

**Common causes:**

- The file is open in Word (or another app)
- The file is read-only or in a protected location
- The file format doesn’t match the workflow

**Fix:**

1. Close the file everywhere (Word, CAT tool editors, preview panes)
2. Copy it to a simple path (for example `C:\Temp\`) and try again
3. Re-export from the CAT tool using the recommended bilingual/package format

## memoQ bilingual shows no segments

**Cause:** Export format doesn’t contain the expected bilingual table.

**Fix:**

- Re-export from memoQ as **Bilingual DOCX** in a **two-column table** format.
- Open the DOCX in Word and confirm it really contains a Source/Target table.

## Trados SDLPPX fails to extract

**Common causes:**

- Corrupt/partial package
- Unsupported package structure

**Fix:**

- Ask for a fresh export from Trados Studio.
- Ensure the package includes all required files.

## Garbled characters / encoding issues

**Cause:** Text encoding problems coming from the source file or export.

**Fix:**

- Try **Tools → Encoding Repair**.
- Re-export from the source tool with a modern Unicode/UTF-8 friendly path when possible.

## Segments don’t match on reimport

**Cause:** Segment structure changed.

**Fix:**

- Don’t merge or split segments in Supervertaler
- Export using the matching CAT format
- Avoid deleting placeholder/tag-only segments

## “Source file not found” during export

**Cause:** The original source file/folder was moved after import.

**Fix:**

- Use **File → Relocate Source Folder** and point it to the new location.
- If the original source is gone, re-import the project from the correct source.

## Exported file has no translations

**Cause:** Targets are empty or the wrong export format was chosen.

**Fix:**

- Verify the Target column contains translations.
- Export the matching format for the workflow you imported.

## Formatting lost on reimport

**Cause:** Tags not preserved.

**Fix:**

- Verify tags are balanced (for example `<b>text</b>`)
- Don’t delete CAT placeholder tags
- Re-export using the correct CAT workflow

## Bilingual table reimport fails

**Cause:** Bilingual tables are great for review, but not always suitable for CAT tool reimport.

**Fix:**

- Prefer the dedicated CAT exchange formats (memoQ/Trados/Phrase/CafeTran).
- If you must use a bilingual table, don’t edit the table structure in Word.
