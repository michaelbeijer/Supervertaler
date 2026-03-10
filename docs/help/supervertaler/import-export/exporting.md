# Exporting Translations

When you’re done translating, export in a format that matches your workflow.

## Export steps

1. Go to **File → Export**
2. Choose an export type (for example DOCX, bilingual table, or a CAT return format)
3. Pick a destination and save

## CAT tool round-trips

If you started from a CAT exchange format (memoQ/Trados/Phrase/CafeTran), export the matching return format.

### Important rules for round-trips

- **Segment count must match**: don’t merge or split segments.
- **Keep tags balanced**: for example `<b>text</b>` (not `<b>text`).
- **Don’t “pretty edit” bilingual tables**: changing the table structure in Word can break reimport.
- Run your CAT tool’s QA after reimport.

{% hint style="warning" %}
Don’t merge or split segments in Supervertaler when you plan to reimport into a CAT tool.
{% endhint %}

## Choosing the right export

- For CAT tool workflows, use the matching CAT export:
	- memoQ bilingual DOCX
	- Trados return package (SDLRPX) when you imported SDLPPX
	- Phrase bilingual DOCX
	- CafeTran bilingual table DOCX
- For review-only delivery, consider [Bilingual Tables](bilingual-tables.md).

## Related pages

- [Supported File Formats](formats.md)
- [Bilingual Tables](bilingual-tables.md)
- [CAT Tool Overview](../cat-tools/overview.md)
