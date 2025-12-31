# memoQ Workflow

This guide covers working with memoQ bilingual files in Supervertaler.

## Export from memoQ

### Bilingual DOCX (Recommended)

1. In memoQ, open your project
2. Go to **Documents** view
3. Right-click your document → **Export Bilingual...**
4. Choose **Bilingual DOC/RTF/DOCX**
5. Select **Table format** (two columns)
6. Export the file

{% hint style="info" %}
The table format with source and target columns works best with Supervertaler.
{% endhint %}

### XLIFF Export

1. In memoQ, go to **Documents** view
2. Right-click → **Export Bilingual...**
3. Choose **memoQ XLIFF bilingual**
4. Save the `.mqxliff` file

## Import to Supervertaler

1. Go to **File → Import → memoQ Bilingual DOCX...**
   - Or **File → Import → memoQ XLIFF...**
2. Select your exported file
3. The segments appear in the translation grid

### What Gets Imported

- ✅ Source text
- ✅ Target text (if any)
- ✅ Inline formatting tags (`{1}`, `[2}`, etc.)
- ✅ Segment status

### memoQ Tag Handling

memoQ uses special tag formats:

| Tag Style | Example | Purpose |
|-----------|---------|---------|
| Curly | `{1}` | Inline tag |
| Mixed | `[2}` or `{3]` | Start/end tags |
| Named | `{MQ}`, `{tspan}` | Formatting tags |

These tags are highlighted in dark red in the grid (matching memoQ's color).

## Translate in Supervertaler

1. Navigate through segments
2. Use AI translation (`Ctrl+T`) or translate manually
3. Confirm each segment (`Ctrl+Enter`)
4. Save your project regularly (`Ctrl+S`)

### Tips for memoQ Projects

- **Preserve tags**: Keep all `{1}`, `[2}` tags in your translation
- **Use Superlookup**: Press `Ctrl+K` for TM and glossary searches
- **Batch translate**: Select multiple segments and press `Ctrl+Shift+T`

## Export from Supervertaler

1. Go to **File → Export → memoQ Bilingual DOCX...**
2. Choose a filename
3. The bilingual table is recreated with your translations

## Import Back to memoQ

1. In memoQ, go to **Documents** view
2. Right-click your original document
3. Select **Import/Update Translation...**
4. Choose **From bilingual DOC/RTF/DOCX file**
5. Select the file exported from Supervertaler
6. Click **Import**

### Verify the Import

- Check that translations appear in memoQ
- Confirm status shows as "Translated" or "Edited"
- Run memoQ's QA to check for issues

## Complete Workflow

```
memoQ: Export Bilingual DOCX
         ↓
Supervertaler: Import memoQ Bilingual
         ↓
Supervertaler: Translate (AI + manual)
         ↓
Supervertaler: Export memoQ Bilingual
         ↓
memoQ: Import/Update Translation
         ↓
memoQ: QA + Delivery
```

## Troubleshooting

### Tags appear as plain text

Make sure you exported as **Bilingual DOCX** (not "Export without tags").

### Formatting lost on re-import

This can happen if:
- Tags were deleted or modified during translation
- The bilingual table structure was changed

**Solution**: Always keep tags exactly as they appear.

### Status not updating in memoQ

memoQ's import may not change segment status. You can:
- Use memoQ's filtering to find imported segments
- Manually confirm segments in memoQ if needed

---

## See Also

- [CAT Tool Overview](overview.md)
- [AutoFingers (memoQ Automation)](../tools/autofingers.md)
