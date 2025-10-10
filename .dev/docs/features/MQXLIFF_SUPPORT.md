# MQXLIFF Format Support

## Overview

Supervertaler v2.4.1+ includes robust support for memoQ XLIFF (`.mqxliff`) files as the **recommended** import/export format for CAT tool integration. MQXLIFF provides superior formatting preservation compared to bilingual DOCX files.

## Why MQXLIFF is Recommended

### Advantages over DOCX format:

1. **Reliable Formatting Preservation**
   - MQXLIFF uses standardized XML tags for formatting (bold, italic, underline)
   - No ambiguity - formatting is explicitly tagged, not inferred
   - Hyperlinks and complex structures are precisely defined

2. **Better Structure**
   - Segments are clearly delimited with unique IDs
   - Metadata is preserved (language codes, segment status, etc.)
   - CAT tool-specific information maintained

3. **Proven Standard**
   - XLIFF is an OASIS industry standard for translation exchange
   - Wide support across CAT tools
   - Better for round-trip translation workflows

4. **Issue Resolution**
   - Solves the "random underlining" problem observed in DOCX format
   - Eliminates formatting inconsistencies during import/export
   - More predictable behavior

## How to Use MQXLIFF in Supervertaler

### Exporting from memoQ

1. Open your project in memoQ
2. Go to **Translations** → **Export Bilingual**
3. Select **MQXLIFF** as the export format
4. Save the `.mqxliff` file
5. Import this file into Supervertaler

### Importing MQXLIFF into Supervertaler

1. Launch Supervertaler
2. Click the **"📄 Import MQXLIFF (Recommended)"** button (blue)
3. Select your `.mqxliff` file
4. Supervertaler will:
   - Extract all translatable source segments
   - Remove formatting tags for AI translation (plain text)
   - Create temporary working files
   - Remember the original file path

### Translating

1. Configure your translation settings as usual:
   - Select AI provider (Gemini, Claude, OpenAI)
   - Choose source and target languages
   - Add custom instructions if needed
2. Click **"Translate"**
3. The AI will translate the plain text segments
4. Formatting information is preserved in the background

### Exporting Back to MQXLIFF

1. After translation completes successfully
2. Click the **"💾 Export to MQXLIFF"** button (blue)
3. Choose where to save the translated `.mqxliff` file
4. Supervertaler will:
   - Apply translations to target segments
   - Preserve all formatting tags (bold, italic, underline)
   - Maintain hyperlinks and complex structures
   - Keep segment IDs and metadata
   - Set segment status to "Confirmed"

### Importing Back to memoQ

1. Open your memoQ project
2. Go to **Translations** → **Import Bilingual**
3. Select the translated `.mqxliff` file
4. memoQ will import the translations with all formatting intact

## Formatting Preservation Details

### Supported Formatting Types

The MQXLIFF handler preserves:

- **Bold** text (`<bpt ctype="bold">`)
- **Italic** text (`<bpt ctype="italic">`)
- **Underline** text (`<bpt ctype="underlined">`)
- **Hyperlinks** with nested formatting
- **Complex nested structures** (e.g., bold + underlined hyperlinks)

### How It Works

1. **Import Phase**:
   - Source segments are parsed with all formatting tags
   - Plain text is extracted for AI processing
   - Formatting structure is stored in memory

2. **Translation Phase**:
   - AI translates plain text only (no confusing markup)
   - Formatting information is kept separate

3. **Export Phase**:
   - Formatting structure from source is cloned to target
   - Translation text replaces source text
   - Tag structure and IDs are preserved
   - XLIFF file remains valid for CAT tool import

### Formatting Strategy

The handler uses intelligent formatting preservation:

- **Simple case**: Text without formatting → direct replacement
- **Similar length**: Translation similar to source → clone formatting structure
- **Very different length**: Translation much longer/shorter → use plain text (safer)

This ensures compatibility even when translations significantly differ in length.

## Technical Details

### File Structure

MQXLIFF files use:
- **XLIFF 1.2** standard
- **memoQ-specific extensions** (mq: namespace)
- **Unicode XML** encoding (UTF-8)

### Key Components

- **trans-unit elements**: Individual translatable segments
- **source/target elements**: Source and translated text
- **bpt/ept tags**: Begin/end paired tags for formatting
- **Segment metadata**: IDs, status, timestamps, etc.

### Module Architecture

- `modules/mqxliff_handler.py`: Core MQXLIFF parsing and generation
  - `MQXLIFFHandler`: Main handler class
  - `FormattedSegment`: Segment data structure
  - XML parsing using ElementTree
  - Namespace-aware processing

## Comparison: MQXLIFF vs DOCX

| Feature | MQXLIFF | Bilingual DOCX |
|---------|---------|----------------|
| Formatting preservation | ✓ Excellent | ⚠️ Unreliable |
| Bold/Italic/Underline | ✓ Always correct | ⚠️ Sometimes incorrect |
| Hyperlinks | ✓ Fully preserved | ✓ Mostly preserved |
| Complex structures | ✓ Handled well | ⚠️ Can be problematic |
| CAT tool compatibility | ✓ Standard format | ⚠️ CAT-specific |
| Round-trip workflow | ✓ Reliable | ⚠️ May lose data |
| File size | Smaller | Larger |
| Human readability | Low (XML) | Medium (table) |

## Best Practices

1. **Always prefer MQXLIFF** when available in your CAT tool
2. **Test with small files first** to verify your workflow
3. **Keep backups** of original MQXLIFF files
4. **Verify formatting** after import back to CAT tool
5. **Use consistent settings** between export and import

## Troubleshooting

### "No translatable segments found"

- Check that the MQXLIFF file contains `<trans-unit>` elements
- Verify the file is not empty or corrupted

### "Failed to load MQXLIFF file"

- Ensure the file is valid XML (not corrupted)
- Check that it uses XLIFF 1.2 format
- Verify the file has proper XML declaration

### "Formatting not preserved correctly"

- For very different translation lengths, formatting may be simplified
- Check that original MQXLIFF had proper formatting tags
- Verify no manual editing broke the XML structure

### "Module Error: Could not load MQXLIFF handler"

- Ensure `modules/mqxliff_handler.py` exists
- Check Python path includes the modules directory
- Verify no import errors in the module

## Future Enhancements

Potential improvements for future versions:

- Support for more complex tag types (colors, fonts, etc.)
- Better handling of very long/short translations
- Segment splitting/joining detection
- Quality assurance checks
- Batch processing of multiple MQXLIFF files

## Version History

- **v2.4.1**: Initial MQXLIFF support implementation
  - Basic import/export functionality
  - Formatting preservation (bold, italic, underline)
  - Hyperlink support
  - Integration with translation workflow

---

**Note**: MQXLIFF support is the recommended approach for professional translation workflows with CAT tools. The DOCX import/export remains available for backwards compatibility but may show formatting inconsistencies.
