# Supercleaner Layout Changes Explanation

## Issue #2: Why does the cleaned document have different layout/formatting?

Looking at your screenshot, the right (cleaned) document has different paragraph spacing and possibly different font sizes compared to the left (original).

### Root Cause: Font Normalization Operations

The following operations can change the visual layout:

1. **"Normalize font in each paragraph"** (`normalize_font`)
   - Takes the most common font in each paragraph and applies it to ALL runs
   - If paragraph has mixed fonts (e.g., Times New Roman and Arial), it standardizes to the majority font
   - **Side effect**: Can change the dominant font if OCR misidentified some characters

2. **"Normalize font size in each paragraph"** (`normalize_font_size`)
   - Takes the most common font size in each paragraph and applies it to all text
   - If paragraph has mixed sizes (e.g., 11pt and 12pt), it standardizes to the majority size
   - **Side effect**: Can make text larger or smaller if OCR created inconsistent sizing

3. **"Normalize font color in each paragraph"** (`normalize_font_color`)
   - Takes the most common color and applies it to all text in the paragraph
   - Usually less problematic but can affect subtle color variations

4. **"Set default text spacing"** (`set_default_spacing`)
   - Resets line spacing to 1.0 (single spacing)
   - **Side effect**: If original document had 1.15 or 1.5 line spacing, this will compress it

### Recommendations:

**For documents where you want to preserve original layout:**
- **UNCHECK** these operations:
  - ❌ Normalize font in each paragraph
  - ❌ Normalize font size in each paragraph
  - ❌ Set default text spacing
  
**Keep these checked (safe for layout):**
- ✅ Remove text shading
- ✅ Remove highlighting
- ✅ Change font color to Automatic
- ✅ Remove manual hyphens
- ✅ Replace special symbols (non-breaking spaces)
- ✅ Fix incorrect line breaks
- ✅ Remove excessive spaces

**Custom Preset Suggestion:**
We could add a "Minimal Clean" preset that only does:
- Remove shading/highlighting
- Fix line breaks
- Remove excessive spaces
- Replace non-breaking spaces

This would clean up problematic formatting without changing the visual layout.
