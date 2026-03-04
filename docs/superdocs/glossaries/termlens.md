# TermLens

TermLens is Supervertaler's inline terminology display. It shows the source text of the current segment word by word, with glossary translations directly underneath each matched term.

## How it works

When you select a segment, TermLens analyses the source text against all active glossaries and displays the result in a visual layout:

- **Matched words** appear with their glossary translation underneath
- **Unmatched words** are shown in light text so you can read the full source sentence in context
- **Project glossary** matches appear in pink; **Background glossary** matches appear in blue
- **Non-translatable** terms (if configured) are shown in a distinct style

This gives you an at-a-glance overview of every term in the segment that has a glossary entry — without having to hover or click anything.

## Where to find it

TermLens appears in two places:

1. **Below the grid** — the "TermLens" tab in the bottom panel (toggle with **View → TermLens Under Grid**)
2. **In the Match Panel** — the right-side panel that also shows TM matches

Both instances update simultaneously when you navigate to a new segment.

## Inserting terms

You can insert a glossary translation from TermLens into your target text in three ways:

### Click to insert

Click any translation shown under a source word. The translation is inserted at the cursor position in the target field.

### Keyboard shortcuts (Alt+1 through Alt+9)

Each matched term in TermLens is assigned a numbered badge. Press **Alt+1** to insert the first match, **Alt+2** for the second, and so on.

**Double-tap** for terms 10 and above: press **Alt+1, Alt+1** quickly to insert term 11, **Alt+2, Alt+2** for term 22, etc.

> **Note:** Alt+0 is reserved for the Compare Panel. TermLens numbering starts at 1.

### Right-click menu

Right-click a term in TermLens to:
- **Insert** the translation
- **Edit** the glossary entry
- **Delete** the glossary entry

## Font settings

You can customise the TermLens font independently from the grid font:

1. Go to **Settings → View Settings → TermLens Font Settings**
2. Choose font family, size (6–16 pt), and bold/normal weight
3. Changes apply immediately to both TermLens instances

## Tips

- Press **F5** to force a refresh if matches appear to be missing.
- TermLens respects glossary activation — only terms from activated glossaries are shown.
- If you have many glossaries, designate one as the **Project glossary** (shown in pink) to make its terms stand out.

## TermLens for Trados

A standalone version of TermLens is also available as a plugin for **Trados Studio 2024+**. It reads the same SQLite termbase format used by Supervertaler and displays terminology matches directly inside the Trados editor.

→ [TermLens for Trados on GitHub](https://github.com/michaelbeijer/TermLens)

---

## See Also

- [Glossary Basics](basics.md)
- [Term Highlighting](highlighting.md)
- [Keyboard Shortcuts](../editor/keyboard-shortcuts.md)
