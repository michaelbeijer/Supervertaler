# Adding & Editing Terms

Supervertaler for Trados provides several ways to add, edit, and manage terminology without leaving the Trados editor.

## Quick-add (Alt+Down)

The fastest way to add a term while translating:

1. Select the **source text** you want to add as a term
2. Select the **target text** (the translation)
3. Press **Alt+Down**

The term is added instantly to all **write-enabled** termbases. No dialog, no interruption.

{% hint style="info" %}
Quick-add writes to every termbase that has **Write** enabled in your [TermLens Settings](../settings/termlens.md). If you want to target a specific termbase, use the Add Term dialog instead.
{% endhint %}

## Quick-add to project termbase (Alt+Up)

Works the same as Alt+Down, but adds the term specifically to the **project termbase** (the termbase marked as "Project" in settings). Use this when you want to keep client-specific terminology separate and prioritised.

1. Select the **source text**
2. Select the **target text**
3. Press **Alt+Up**

## Quick-add non-translatable (Ctrl+Alt+N)

For terms that should remain identical in source and target (brand names, product codes, abbreviations):

1. Select the text in the **source** field
2. Press **Ctrl+Alt+N**

This creates a term entry where source and target are the same. Non-translatable terms appear with a distinct yellow highlight in [TermLens (Workbench)](https://supervertaler.gitbook.io/supervertaler/glossaries/termlens).

## Add Term dialog (Ctrl+Alt+T)

For more control, open the full Add Term dialog:

1. Press **Ctrl+Alt+T** (or right-click in the editor and choose **Add Term...**)
2. Fill in the fields:

| Field | Description |
|-------|-------------|
| **Source** | The source-language term |
| **Target** | The target-language translation |
| **Definition** | Optional definition or usage note |
| **Non-translatable** | Check this to mark the term as non-translatable |
| **Termbase** | Choose which termbase to add the term to |

3. Click **OK** to save

{% hint style="success" %}
**Tip:** Use the project termbase for client-specific terminology that should be prioritised over background termbases. Project termbase terms appear in pink in TermLens.
{% endhint %}

## Smart selection

You don't need to precisely select entire words when adding terms. All quick-add shortcuts (**Alt+Down**, **Alt+Up**, **Ctrl+Alt+N**, **Ctrl+Alt+T**) automatically expand your selection to the nearest word boundaries.

For example, to add **standalone version** = **zelfstandige versie** to your termbase, it's enough to select **alone ver** in the source and **andige ver** in the target. Supervertaler expands both selections to the full words automatically.

This means you can work fast and loose with your mouse or keyboard selections — no need for the precise click-and-drag that normally slows you down. Just grab roughly the right area and Supervertaler takes care of the rest.

### How it works

When you make a selection, Supervertaler scans the full segment text for every occurrence of your selected text and applies these rules, in order:

1. **Exact word match wins** — if the selection matches a complete word somewhere in the segment (i.e. it sits between spaces or punctuation), that word is used as-is. For example, if the segment contains both _hechtingsbevorderaars_ and _hechting_, selecting **hechting** returns **hechting** — the exact word — not the longer compound.

2. **Shortest word wins** — if the selection is embedded inside multiple words, the shortest enclosing word is preferred. For example, if the segment contains _hechtingsbevorderaars_ and _hechting_, selecting **echt** returns **hechting** (8 characters) rather than _hechtingsbevorderaars_ (21 characters), because the user most likely intended the simpler word.

3. **Single match expands** — if the selection appears inside only one word, it expands to that word's boundaries.

### Tips for reliable results

- **Select at least 3–4 characters** — very short selections (1–2 characters) may match common short words elsewhere in the segment (e.g., selecting **he** could match the word _the_)
- **Select the whole word when in doubt** — if a segment contains similar-looking words and you want a specific one, a complete-word selection is always matched correctly
- **Use Ctrl+Alt+T for tricky cases** — the Add Term dialog lets you review and edit the expanded term before saving, so you can catch any unexpected expansion

{% hint style="info" %}
Press **F2** to manually expand your current selection to word boundaries without adding a term. This lets you preview exactly what Supervertaler would capture before pressing a quick-add shortcut.
{% endhint %}

## Merge prompt

When you add a term and the **source** or **target** already exists in the termbase (but with a different translation), Supervertaler shows a prompt asking what you want to do:

- **Add as Synonym** — merges the new translation into the existing entry as a synonym, keeping your termbase tidy
- **Keep Both** — creates a separate entry alongside the existing one
- **Cancel** — aborts the operation

**Example:** Your termbase already has **adhesion → hechting**. You select **adhesion → aanhechting** and press Alt+Down. The merge prompt appears because the source term “adhesion” already exists. Clicking “Add as Synonym” adds _aanhechting_ as a target synonym of the existing entry, so both translations are grouped together.

{% hint style="info" %}
The merge prompt only appears when the source or target matches exactly (case-insensitive). It does **not** apply to non-translatable quick-add (**Ctrl+Alt+N**).
{% endhint %}

## Editing existing terms

To edit a term that already exists in your termbase:

1. Right-click the term in the **TermLens** panel
2. Select **Edit Term...**
3. The **Term Entry Editor** opens, where you can:
   - Modify the source or target text
   - Add or remove **synonyms** (multiple translations for one source term)
   - Update the definition
   - Toggle the non-translatable flag

Click **Save** when done.

## Deleting terms

1. Right-click the term in the **TermLens** panel
2. Select **Delete Term**
3. Confirm the deletion in the dialog

{% hint style="warning" %}
Deletion is permanent. The term is removed from the termbase database file.
{% endhint %}

## Bulk Add Non-Translatable

For adding many non-translatable terms at once (e.g., a list of brand names or product codes):

1. Open **Settings** (gear icon in the TermLens panel)
2. Find the **Bulk Add Non-Translatable** option
3. Paste your terms, **one per line**
4. Click **Add** to save them all at once

---

## See Also

- [Term Picker](term-picker.md)
- [Termbase Management](../termbase-management.md)
- [TermLens Settings](../settings/termlens.md)
