# Trados Studio Workflow

This guide covers working with Trados Studio packages in Supervertaler.

## Recommended: SDLPPX Packages

The best way to work with Trados Studio is using **project packages** (SDLPPX files).

### Export from Trados

1. In Trados Studio, open your project
2. Go to **Project** → **Package** → **Create Project Package**
3. Configure package options (include all files)
4. Save as `.sdlppx` file

### Import to Supervertaler

1. Go to **File → Import → Trados Package (SDLPPX)...**
2. Select your `.sdlppx` file
3. Supervertaler extracts and loads all segments

{% hint style="success" %}
**Tip**: Package paths are saved in your `.svproj` file, so you can re-export to the same package later.
{% endhint %}

## Translate in Supervertaler

1. Navigate through segments
2. Use AI translation (`Ctrl+T`) or translate manually
3. Confirm each segment (`Ctrl+Enter`)
4. Tags appear as `<1>`, `</1>` - keep them in your translation

### Trados Tag Format

Trados uses numbered XML-style tags:

| Tag | Purpose |
|-----|---------|
| `<1>` | Opening tag |
| `</1>` | Closing tag |
| `<2/>` | Standalone/empty tag |

These are highlighted in the grid for visibility.

## Export as Return Package

1. Go to **File → Export → Trados Return Package (SDLRPX)...**
2. The return package is created with your translations
3. Segment status is updated to "Translated"

{% hint style="info" %}
The SDLRPX is created from your original SDLPPX with translations inserted.
{% endhint %}

## Import Back to Trados

1. In Trados Studio, go to **File** → **Open Package**
2. Select the `.sdlrpx` file from Supervertaler
3. Trados imports the return package
4. Your translations appear in the target segments

---

## Alternative: Bilingual Review DOCX

⚠️ **Use SDLPPX instead if possible.** The Bilingual Review format has limitations.

### The Problem

Trados Bilingual Review DOCX is designed for **review only**, not translation:
- Empty target segments are not exported
- You cannot translate from scratch using this format

### Workaround (if you must use it)

1. **In Trados**: Copy all source to target first
   - Edit → Task → Copy source to target (batch task)
2. **Export**: File → Export → For Bilingual Review
3. **In Word**: Delete all target text (cells remain, but empty)
4. **Import to Supervertaler**: File → Import → Trados Bilingual DOCX
5. **Translate** and export
6. **Re-import to Trados**: Merge into project

{% hint style="warning" %}
This workaround is tedious. Use SDLPPX packages whenever your client provides them.
{% endhint %}

---

## Complete SDLPPX Workflow

```
Trados: Create Project Package (.sdlppx)
         ↓
Supervertaler: Import Trados Package
         ↓
Supervertaler: Translate (AI + manual)
         ↓
Supervertaler: Export Return Package (.sdlrpx)
         ↓
Trados: Open Return Package
         ↓
Trados: QA + Delivery
```

## Troubleshooting

### "Cannot find SDLXLIFF files"

The SDLPPX might be corrupted or use an unsupported format.
- Try re-exporting from Trados Studio
- Ensure all files are included in the package

### Status shows "Draft" instead of "Translated"

Fixed in v1.9.32. Update to the latest version.

### Tags not matching

Ensure you keep all `<1>`, `</1>` tags in exactly the same positions.

### Source files not found on re-export

If you moved your project, use **File → Relocate Source Folder** to point to the new location of the SDLPPX.

---

## See Also

- [CAT Tool Overview](overview.md)
- [Import/Export Formats](../import-export/formats.md)
