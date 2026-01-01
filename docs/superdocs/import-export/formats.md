# Supported File Formats

Supervertaler can import and export several formats depending on your workflow.

## Standard documents

- **DOCX** (Microsoft Word): import a document, translate in the grid, export a translated DOCX.
- **TXT** (plain text): each line becomes a segment.

## CAT tool exchange formats

Use these formats when you need to round-trip back into a CAT tool.

- **memoQ**
  - Bilingual DOCX
  - XLIFF (memoQ export)
- **Trados Studio**
  - Packages: `.sdlppx` import → `.sdlrpx` return (recommended)
  - Bilingual Review DOCX (special workflow)
- **Phrase (Memsource)**
  - Bilingual DOCX
- **CafeTran Espresso**
  - Bilingual DOCX table

## Multi-file projects

- **Folder import (Multiple Files)**: import a folder containing DOCX/TXT files into a single multi-file project.

{% hint style="warning" %}
For CAT tool round-trips, always import and export the matching CAT format. Mixing formats can break tags/statuses on reimport.
{% endhint %}

## Related pages

- [Importing DOCX Files](docx-import.md)
- [Importing Text Files](txt-import.md)
- [Multi-File Projects](multi-file.md)
- [Exporting Translations](exporting.md)
- [Bilingual Tables](bilingual-tables.md)
