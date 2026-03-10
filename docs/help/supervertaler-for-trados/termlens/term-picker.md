# Term Picker

The Term Picker is a compact overlay that shows all matched terms for the current segment in a sortable, keyboard-navigable list. It is useful when TermLens shows many matches and you want a quick overview without scrolling.

## Opening the Term Picker

Press **Ctrl+Shift+G** (or **Ctrl+Alt+G**) to open the Term Picker. It appears as a floating window above the editor.

## Color-coded rows

Each row in the Term Picker is color-coded by termbase type:

| Color | Meaning |
|-------|---------|
| <mark style="background-color:#E6D7D8;">**Pink**</mark> | Project termbase term |
| <mark style="background-color:#C8E6F5;">**Blue**</mark> | Regular Supervertaler termbase term |
| <mark style="background-color:#FFF3D0;">**Yellow**</mark> | Non-translatable term |
| <mark style="background-color:#D4EDDA;">**Green**</mark> | MultiTerm termbase term (`.sdltb`) |

This lets you instantly see where each term comes from and how it should be handled.

## Expandable synonyms

Terms with multiple translations display a right-arrow indicator (**&#9656;**) next to the term. To expand and see all synonym sub-rows:

- Select the row and press the **Right arrow** key
- The sub-rows appear below the parent term, showing each available translation

Press **Left arrow** to collapse the synonyms again.

## Keyboard navigation

The Term Picker is designed for fast keyboard use:

| Key | Action |
|-----|--------|
| **0-9** | Type a number to jump directly to that term |
| **Enter** | Insert the selected term and close the picker |
| **Escape** | Close the picker without inserting |
| **Up / Down** | Navigate between terms |
| **Right** | Expand synonyms for the selected term |
| **Left** | Collapse synonyms |

## Inserting a term

You can insert a term in two ways:

- **Click** any row to insert that term at the cursor position in the target field
- **Press Enter** on the selected row to insert and close

The selected translation is placed at the current cursor position in the target segment.

{% hint style="info" %}
The Term Picker shows the same matches as TermLens, but in a flat list format that is easier to scan when there are many results.
{% endhint %}

---

## See Also

- [Adding & Editing Terms](adding-terms.md)
- [TermLens (Desktop)](https://supervertaler.gitbook.io/supervertaler/glossaries/termlens)
- [Termbase Management](../termbase-management.md)
