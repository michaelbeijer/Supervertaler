# Adding & Editing Terms

{% hint style="info" %}
This page is about **Supervertaler for Trados** — the Trados Studio plugin.
{% endhint %}

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

This creates a term entry where source and target are the same. Non-translatable terms appear with a distinct yellow highlight in [TermLens](../../glossaries/termlens.md).

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
