# Keyboard Shortcuts

{% hint style="info" %}
This page is about **Supervertaler for Trados** — the Trados Studio plugin. For keyboard shortcuts in the standalone desktop app, see [Keyboard Shortcuts (Desktop)](../editor/keyboard-shortcuts.md).
{% endhint %}

All keyboard shortcuts available in Supervertaler for Trados.

## Terminology

| Shortcut | Action |
|----------|--------|
| `Alt+Down` | Quick-add term to write termbases |
| `Alt+Up` | Quick-add term to project termbase |
| `Ctrl+Alt+T` | Add term (opens dialog with full control) |
| `Ctrl+Alt+N` | Quick-add non-translatable term |
| `Ctrl+Shift+G` | Open Term Picker |
| `Alt+1` ... `Alt+9` | Insert term by badge number |
| `Alt+0` | (Reserved) |

## AI Translation

| Shortcut | Action |
|----------|--------|
| `Ctrl+Alt+A` | AI translate the active segment |

## Navigation and Display

| Shortcut | Action |
|----------|--------|
| `F1` | Context-sensitive help |
| `F2` | Expand selection to word boundaries |
| `F5` | Force refresh TermLens display |

## Two-Digit Chord for Terms 10+

When a segment has more than 9 matched terms, use a quick two-key chord to insert terms numbered 10 and above.

Press the **tens digit** followed by the **ones digit** in rapid succession:

| Chord | Inserts Term |
|-------|-------------|
| `Alt+1`, `Alt+0` | Term 10 |
| `Alt+1`, `Alt+1` | Term 11 |
| `Alt+1`, `Alt+2` | Term 12 |
| `Alt+2`, `Alt+3` | Term 23 |

The two keys must be pressed within a short time window. If you wait too long between keys, the first press is treated as a single-digit insertion.

{% hint style="info" %}
These shortcuts are active when focus is in the Trados editor or in a Supervertaler panel. They do not interfere with Trados's built-in shortcuts.
{% endhint %}

---

## See Also

- [TermLens](termlens.md)
- [Supervertaler Assistant](ai-assistant.md)
- [Batch Translate](batch-translate.md)
