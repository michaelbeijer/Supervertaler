# TermLens Settings

Configure how TermLens loads and displays terminology in Trados Studio.

## Accessing TermLens settings

Click the **gear icon** in the TermLens panel, or open the plugin **Settings** dialog and switch to the **TermLens** tab.

## Database path

The path to your Supervertaler termbase `.db` file. Click **Browse** to select a database, or **Create New** to start with an empty one.

{% hint style="info" %}
**Auto-detect:** If the standalone Supervertaler application is installed on the same machine, the plugin can automatically detect its default database location. Click **Auto-detect** to find and use it.
{% endhint %}

## Termbase toggles

Each termbase in the database has three toggles. See [Termbase Management](../termbase-management.md) for full details.

| Toggle | Purpose |
|--------|---------|
| **Read** | Load terms for matching — only termbases with Read enabled appear in TermLens |
| **Write** | Receive new terms added via the [quick-add shortcuts](../termlens/adding-terms.md) |
| **Project** | Mark as the project termbase (shown in pink, prioritised) |

## Auto-load on startup

When enabled, the plugin automatically loads the termbase database when Trados Studio opens. This means terms are available immediately when you start translating, without needing to open the settings first.

If disabled, the termbase loads the first time you open the TermLens settings or click the TermLens panel.

## Panel font size

Adjust the font size used in the TermLens display panel. Valid range: **7 pt** to **16 pt**.

Increase the font size if TermLens text is hard to read; decrease it to fit more terms on screen.

---

## See Also

- [Termbase Management](../termbase-management.md)
- [AI Settings](ai-settings.md)
- [TermLens (standalone)](../../glossaries/termlens.md)
