# The Translation Grid

The translation grid is your main workspace in Supervertaler.

## Grid Structure

The grid displays your document as segments (sentences or paragraphs):

| Column | Width | Description |
|--------|-------|-------------|
| **#** | Narrow | Segment number |
| **Status** | Narrow | Translation status icon |
| **Source** | ~45% | Original text (read-only) |
| **Target** | ~45% | Your translation (editable) |

## Status Icons

| Icon | Status | Description |
|------|--------|-------------|
| ⬜ | Not Started | Segment hasn't been touched |
| 📝 | Draft | Edited but not confirmed |
| ✅ | Confirmed | Translation is complete |
| 🔒 | Locked | Cannot be edited |

## Working in the Grid

### Selecting a Segment

- Click on any cell to select that segment
- Use arrow keys to navigate (see [Navigation](navigation.md))

### Editing

- Click in the Target cell
- Type your translation
- The status automatically changes to "Draft"

### Confirming

- Press `Ctrl+Enter` to confirm the current segment
- The status changes to ✅

### Multi-Select

- **Shift+Click**: Select a range of segments
- **Ctrl+Click**: Add individual segments to selection

## Visual Indicators

### Termbase Highlighting

Terms from your glossaries are highlighted in the source text:
- Green background (default)
- Higher priority terms have darker shades

### Tag Highlighting

CAT tool formatting tags are highlighted in dark red:
- memoQ: `{1}`, `[2}`, `{MQ}`
- Trados: `<1>`, `</1>`
- HTML: `<b>`, `<i>`, `</b>`

### Spellcheck

Misspelled words in the target show a red wavy underline. Right-click for suggestions.

## Customization

### Font Settings

Go to **Settings → View Settings** to:
- Change font family
- Adjust font size
- Preview changes in real-time

### Tag Colors

Customize the tag highlight color in **Settings → View Settings → Tag Colors**.

---

## See Also

- [Navigation](navigation.md)
- [Keyboard Shortcuts](keyboard-shortcuts.md)
- [Filtering](filtering.md)
