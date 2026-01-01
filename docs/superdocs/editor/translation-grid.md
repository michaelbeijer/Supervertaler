# The Translation Grid

The translation grid is where you spend most of your time: each row is a **segment** (usually a sentence or paragraph) with source and target text.

## Columns

The grid has five columns:

| Column | What it is |
|--------|------------|
| **#** | Segment number (row index) |
| **Type** | Segment type (depends on the file format/importer) |
| **Source** | Original text (typically read-only) |
| **Target** | Your translation (editable) |
| **Status** | Segment status (dropdown) |

## Editing behavior

- The grid is optimized for speed, but edits are intentionally lightweight.
- **Double-click** a cell to edit.
- Use **Shift+Enter** for a line break inside a cell (multi-line target).

## Confirming & status

- Use the **Status** dropdown to set the segment state.
- Keyboard confirm is supported (see [Editing & Confirming](editing-confirming.md)).

Common statuses include:

- Not started
- Translated
- Confirmed
- Proofread
- Approved

{% hint style="info" %}
If you plan to reimport into a CAT tool, do not merge/split content across segments. Segment boundaries must stay compatible.
{% endhint %}

## Visual cues

- **Tags** (CAT tool placeholders and formatting markers) are highlighted to make them hard to miss.
- **Spellcheck** (if enabled) underlines misspelled target words.
- **Glossary matches** can be highlighted in the source.

## See also

- [Navigation](navigation.md)
- [Editing & Confirming](editing-confirming.md)
- [Keyboard Shortcuts](keyboard-shortcuts.md)
- [Filtering](filtering.md)
