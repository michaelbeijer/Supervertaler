# Termbase Management

Supervertaler for Trados uses the same SQLite termbase format as Supervertaler Workbench. You manage your termbases through the Settings dialog.

## Accessing termbase settings

1. Click the **gear icon** in the TermLens panel, or go to **Settings** in the plugin ribbon
2. Switch to the **TermLens** tab

## Database file

The plugin stores all termbases in a single `.db` file (SQLite database).

- Click **Browse** to select an existing database file
- Click **Create New** to create a fresh, empty database

{% hint style="info" %}
The `.db` file uses the same Supervertaler SQLite format as the standalone application. You can share the same termbase file between both tools.
{% endhint %}

## MultiTerm termbases

If your Trados project has MultiTerm termbases (`.sdltb` files) attached, they appear automatically at the bottom of the termbase list with a **[MultiTerm]** label and green background. These termbases are read-only in TermLens –to manage their terms, use Trados's built-in MultiTerm interface. See [MultiTerm Support](multiterm-support.md) for full details.

## Termbase list

Once a database is loaded, the termbase list shows all Supervertaler termbases it contains, plus any detected MultiTerm termbases. Each Supervertaler termbase has three toggles:

| Toggle | Purpose |
|--------|---------|
| **Read** | Load terms from this termbase for matching in TermLens |
| **Write** | New terms added via [quick-add shortcuts](termlens/adding-terms.md) go into this termbase |
| **Project** | Designate as the project termbase (terms shown in pink, prioritised in matching) |

{% hint style="warning" %}
Only one termbase can be marked as **Project** at a time. Setting a new project termbase clears the flag from the previous one.
{% endhint %}

## Creating a new termbase

1. Click **Add Termbase**
2. Enter a **name** for the termbase
3. Select the **source language** and **target language**
4. Click **OK**

The new termbase appears in the list, ready for use.

## Import from TSV

You can import terminology from a tab-separated values file:

1. Select the target termbase in the list
2. Click **Import from TSV**
3. Select your `.tsv` file

**File format:**

- Two columns separated by a tab: `source<TAB>target`
- For terms with multiple synonyms, use pipe-delimited values: `source<TAB>translation1|translation2|translation3`
- One term per line
- UTF-8 encoding recommended

**Example:**

```
database	databank|gegevensbank
software	software
user interface	gebruikersinterface|gebruikersomgeving
```

## Export to TSV

To export all terms from a termbase:

1. Select the termbase in the list
2. Click **Export to TSV**
3. Choose a save location

The exported file uses the same tab-separated format described above.

## Termbase Editor

For full editing capabilities, double-click a termbase in the list to open the **Termbase Editor**. From here you can:

- **Search** for terms by source or target text
- **Edit** individual term entries
- **Delete** terms
- Perform **bulk operations** (e.g., bulk delete, bulk edit)

## Sharing termbases

{% hint style="success" %}
**Tip:** Keep the `.db` file on a network drive or cloud-synced folder (OneDrive, Dropbox, Google Drive) to share termbases across machines and with colleagues. Since both the Trados plugin and Supervertaler Workbench use the same format, everyone can work from the same terminology.
{% endhint %}

---

## See Also

- [MultiTerm Support](multiterm-support.md)
- [TermLens Settings](settings/termlens.md)
- [Adding & Editing Terms](termlens/adding-terms.md)
- [Glossary Basics (Workbench)](https://supervertaler.gitbook.io/supervertaler/glossaries/basics)
